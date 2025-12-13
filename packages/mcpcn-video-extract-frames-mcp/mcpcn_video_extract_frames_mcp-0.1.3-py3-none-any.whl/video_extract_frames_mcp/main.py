from mcp.server.fastmcp import FastMCP, Context
import ffmpeg
import os
import re
import logging
from logging.handlers import RotatingFileHandler
import tempfile
import subprocess
import uuid
import glob
import time
from pathlib import Path
import platform
import urllib.parse


# 配置日志输出到stderr，避免干扰MCP通信
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

package = "video-extract-frames-mcp"

# 使用用户临时目录存放日志文件
log_dir = Path(tempfile.gettempdir()) / package
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "debug.log"

file_handler = RotatingFileHandler(
    str(log_file), maxBytes=5_000_000, backupCount=3, encoding="utf-8"
)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger.addHandler(file_handler)
logger.propagate = False

FFMPEG_BINARY = os.environ.get("FFMPEG_BINARY")
FFPROBE_BINARY = os.environ.get("FFPROBE_BINARY")


def _ffmpeg_run(stream_spec, **kwargs):
    """Run ffmpeg with an explicit binary path."""
    if "overwrite_output" not in kwargs:
        kwargs["overwrite_output"] = True
    return ffmpeg.run(stream_spec, cmd=FFMPEG_BINARY, **kwargs)


def _ffmpeg_run_async(stream_spec, **kwargs):
    """Run ffmpeg asynchronously with explicit binary path."""
    return ffmpeg.run_async(stream_spec, cmd=FFMPEG_BINARY, **kwargs)


def _ffprobe_probe(path: str, **kwargs):
    """Probe media with explicit ffprobe binary."""
    return ffmpeg.probe(path, cmd=FFPROBE_BINARY, **kwargs)


def _prepare_path_for_dir(input_path: str, output_dir: str) -> None:
    """Prepare paths for directory output."""
    if not os.path.exists(input_path):
        raise RuntimeError(f"Error: Input file not found at {input_path}")
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
    except Exception as e:
        raise RuntimeError(f"Error creating output directory {output_dir}: {str(e)}")


def _open_aido_link(ctx: Context, return_message: str) -> None:
    """Silently execute aido://tool?xxx&chatSessionId=xxx across platforms."""
    try:
        if ctx is None:
            logger.debug("Context is None, skipping aido link execution")
            return

        request_context = getattr(ctx, "request_context", None)
        chatSessionId = None
        if request_context and hasattr(request_context, "meta"):
            context_meta = getattr(request_context, "meta", None)
            logger.debug(f"context meta: {context_meta}")
            if context_meta and hasattr(context_meta, "chatSessionId"):
                chatSessionId = getattr(context_meta, "chatSessionId", None)
                logger.debug(
                    f"chatSessionId from request_context.meta: {chatSessionId}"
                )

        if not chatSessionId or chatSessionId == "None":
            logger.warning(
                f"Invalid or missing chatSessionId: {chatSessionId}, skipping aido link execution"
            )
            return

        encoded_message = urllib.parse.quote(return_message, safe="")
        package_name = urllib.parse.quote(package, safe="")
        aido_url = f"aido://tool?path={encoded_message}&chatSessionId={chatSessionId}&package={package_name}"

        system = platform.system().lower()
        if system == "darwin":
            result = subprocess.run(
                ["open", aido_url], check=False, capture_output=True, text=True
            )
            if result.returncode != 0 and result.stderr:
                logger.warning(f"macOS open command failed: {result.stderr}")
        elif system == "windows":
            try:
                os.startfile(aido_url)
            except (OSError, AttributeError) as e:
                logger.debug(f"os.startfile failed, trying start command: {e}")
                result = subprocess.run(
                    f'start "" "{aido_url}"',
                    shell=True,
                    check=False,
                    capture_output=True,
                    text=True,
                )
                if result.returncode != 0 and result.stderr:
                    logger.warning(f"Windows start command failed: {result.stderr}")
        elif system == "linux":
            result = subprocess.run(
                ["xdg-open", aido_url], check=False, capture_output=True, text=True
            )
            if result.returncode != 0 and result.stderr:
                logger.warning(f"Linux xdg-open command failed: {result.stderr}")
        else:
            logger.warning(f"Unsupported operating system: {system}")
            return

        logger.info(f"Executed aido link on {system}: {aido_url}")
    except Exception as e:
        logger.error(f"Failed to execute aido link: {str(e)}", exc_info=True)


mcp = FastMCP("VideoExtractFrames")


def _get_video_output_dir(video_path: str, output_dir: str, total_videos: int) -> str:
    """Generate the output subdirectory path based on the video filename.

    A single video uses output_dir directly; multiple videos create per-video subdirectories named after each file.
    """
    if total_videos == 1:
        return output_dir
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    return os.path.join(output_dir, video_name)


def _extract_single_video_frames(
    video_path: str,
    output_dir: str,
    image_format: str,
    interval_seconds: float | None,
    extract_first: bool,
    extract_last: bool,
    width: int | None,
    height: int | None,
    ctx: Context | None,
    video_index: int = 0,
    total_videos: int = 1,
) -> list[str]:
    """Internal helper that extracts frames from a single video."""
    # 多个视频时，为每个视频创建子目录
    actual_output_dir = _get_video_output_dir(video_path, output_dir, total_videos)
    _prepare_path_for_dir(video_path, actual_output_dir)

    # 使用时间戳作为前缀避免文件名冲突
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    prefix = f"frames_{timestamp}"
    created_files: list[str] = []

    # 可选获取视频时长（末帧提取需要）
    video_duration_sec = None
    if extract_last:
        try:
            probe = _ffprobe_probe(video_path)
            video_duration_sec = (
                float(probe["format"]["duration"])
                if "format" in probe and "duration" in probe["format"]
                else None
            )
        except Exception:
            video_duration_sec = None

    base_progress = int((video_index / total_videos) * 100)
    progress_range = int(100 / total_videos)

    # 1) 按固定时间间隔导出
    if interval_seconds and interval_seconds > 0:
        if ctx:
            ctx.report_progress(
                base_progress + int(progress_range * 0.1),
                f"Video {video_index + 1}/{total_videos}: starting interval frame extraction...",
            )
        fps_val = 1.0 / float(interval_seconds)
        input_stream = ffmpeg.input(video_path)
        v = input_stream.video.filter("fps", fps=fps_val)
        if width or height:
            scale_w = width if width else -1
            scale_h = height if height else -1
            v = v.filter("scale", scale_w, scale_h)
        pattern = os.path.join(actual_output_dir, f"{prefix}_%06d.{image_format}")
        _ffmpeg_run(
            ffmpeg.output(v, pattern, vsync="vfr"),
            capture_stdout=True,
            capture_stderr=True,
        )
        created_files.extend(
            sorted(
                glob.glob(os.path.join(actual_output_dir, f"{prefix}_*.{image_format}"))
            )
        )

    # 2) 首帧导出
    if extract_first:
        if ctx:
            ctx.report_progress(
                base_progress + int(progress_range * 0.5),
                f"Video {video_index + 1}/{total_videos}: extracting the first frame...",
            )
        first_path = os.path.join(actual_output_dir, f"{prefix}_first.{image_format}")
        v1 = ffmpeg.input(video_path, ss=0)
        vf = v1.video
        if width or height:
            scale_w = width if width else -1
            scale_h = height if height else -1
            vf = vf.filter("scale", scale_w, scale_h)
        _ffmpeg_run(
            ffmpeg.output(vf, first_path, vframes=1),
            capture_stdout=True,
            capture_stderr=True,
        )
        created_files.append(first_path)

    # 3) 末帧导出
    if extract_last:
        if ctx:
            ctx.report_progress(
                base_progress + int(progress_range * 0.8),
                f"Video {video_index + 1}/{total_videos}: extracting the last frame...",
            )
        if video_duration_sec is None or video_duration_sec <= 0:
            raise RuntimeError(
                f"Error: Failed to resolve video duration for last-frame extraction: {video_path}"
            )
        last_ts = max(video_duration_sec - 0.01, 0)
        last_path = os.path.join(actual_output_dir, f"{prefix}_last.{image_format}")
        v2 = ffmpeg.input(video_path, ss=last_ts)
        vf2 = v2.video
        if width or height:
            scale_w = width if width else -1
            scale_h = height if height else -1
            vf2 = vf2.filter("scale", scale_w, scale_h)
        _ffmpeg_run(
            ffmpeg.output(vf2, last_path, vframes=1),
            capture_stdout=True,
            capture_stderr=True,
        )
        created_files.append(last_path)

    return created_files


@mcp.tool()
def extract_video_frames(
    video_path: list[str],
    output_dir: str,
    image_format: str = "png",
    interval_seconds: float | None = None,
    extract_first: bool = False,
    extract_last: bool = False,
    width: int | None = None,
    height: int | None = None,
    ctx: Context = None,
) -> str:
    """Extract frames from videos at intervals or specific positions.

    Args:
        video_path: List of input video paths; multiple videos are supported.
        output_dir: Output directory (created automatically if missing).
        image_format: Output image format such as 'png', 'jpg', or 'webp'. Default is 'png'.
        interval_seconds: Interval between frames (seconds). When > 0, interval extraction is enabled.
        extract_first: Whether to additionally export the first frame.
        extract_last: Whether to additionally export the last frame.
        width: Optional width for scaling the output frames.
        height: Optional height for scaling the output frames.

    Returns:
        A status message indicating success or failure.
    """
    execution_start_time = time.time()

    # 兼容单个路径字符串输入
    if isinstance(video_path, str):
        video_path = [video_path]

    if not video_path:
        raise RuntimeError("Error: video_path list is empty.")

    # 校验图片格式
    valid_formats = {"png", "jpg", "jpeg", "webp", "bmp", "tiff"}
    if image_format not in valid_formats:
        raise RuntimeError(
            f"Error: Invalid image_format '{image_format}'. Supported: {', '.join(sorted(valid_formats))}"
        )

    # 校验间隔参数
    if interval_seconds is not None and interval_seconds <= 0:
        raise RuntimeError("Error: interval_seconds must be positive.")

    # 校验尺寸参数
    if width is not None and width <= 0:
        raise RuntimeError("Error: width must be positive.")
    if height is not None and height <= 0:
        raise RuntimeError("Error: height must be positive.")

    try:
        if (
            not (interval_seconds and interval_seconds > 0)
            and not extract_first
            and not extract_last
        ):
            raise RuntimeError(
                "Error: At least one extraction mode must be specified (interval_seconds>0 and/or extract_first/extract_last)."
            )

        all_created_files: list[str] = []
        total_videos = len(video_path)

        for idx, single_video_path in enumerate(video_path):
            files = _extract_single_video_frames(
                video_path=single_video_path,
                output_dir=output_dir,
                image_format=image_format,
                interval_seconds=interval_seconds,
                extract_first=extract_first,
                extract_last=extract_last,
                width=width,
                height=height,
                ctx=ctx,
                video_index=idx,
                total_videos=total_videos,
            )
            all_created_files.extend(files)

        if not all_created_files:
            raise RuntimeError(
                "Error: No frames were produced. Please check parameters."
            )

        if ctx:
            ctx.report_progress(100, "Frame extraction completed")

        execution_time = time.time() - execution_start_time

        if execution_time > 59 and all_created_files:
            _open_aido_link(ctx, output_dir)

        return (
            f"Frames extracted successfully. Videos={total_videos}, Count={len(all_created_files)}. "
            f"Output dir='{output_dir}'."
        )
    except ffmpeg.Error as e:
        error_message = e.stderr.decode("utf8") if e.stderr else str(e)
        raise RuntimeError(f"Error extracting frames: {error_message}")
    except Exception as e:
        raise RuntimeError(
            f"An unexpected error occurred in extract_video_frames: {str(e)}"
        )


def _extract_single_scene_change_frames(
    video_path: str,
    output_dir: str,
    image_format: str,
    scene_threshold: float,
    min_scene_gap_seconds: float | None,
    max_frames: int | None,
    width: int | None,
    height: int | None,
    ctx: Context | None,
    video_index: int = 0,
    total_videos: int = 1,
) -> list[str]:
    """Internal helper that extracts scene-change keyframes for a single video."""
    # 多个视频时，为每个视频创建子目录
    actual_output_dir = _get_video_output_dir(video_path, output_dir, total_videos)
    _prepare_path_for_dir(video_path, actual_output_dir)

    base_progress = int((video_index / total_videos) * 100)
    progress_range = int(100 / total_videos)

    # 获取视频时长
    duration = None
    try:
        probe = _ffprobe_probe(video_path)
        duration = (
            float(probe["format"].get("duration", 0.0))
            if "format" in probe
            else None
        )
    except Exception:
        duration = None

    if ctx:
        ctx.report_progress(
            base_progress + int(progress_range * 0.1),
            f"Video {video_index + 1}/{total_videos}: detecting scene changes...",
        )

    # 第一遍：用 select+showinfo 找到候选时间戳
    detect_spec = (
        ffmpeg.input(video_path)
        .video.filter("select", f"gt(scene,{scene_threshold})")
        .filter("showinfo")
        .output("-", format="null")
    )
    detect_proc = _ffmpeg_run_async(detect_spec, pipe_stderr=True)
    _, stderr_bytes = detect_proc.communicate()
    stderr_str = stderr_bytes.decode("utf8")

    times = [float(x) for x in re.findall(r"pts_time:(\d+(?:\.\d+)?)", stderr_str)]
    if not times:
        return []

    # 二次去重：最小间隔
    filtered_times: list[float] = []
    last_kept = None
    gap = (
        float(min_scene_gap_seconds)
        if (min_scene_gap_seconds and min_scene_gap_seconds > 0)
        else None
    )
    for t in sorted(times):
        if duration is not None:
            t = min(max(t, 0.0), max(duration - 0.01, 0.0))
        if last_kept is None:
            filtered_times.append(t)
            last_kept = t
            continue
        if gap is None or (t - last_kept) >= gap:
            filtered_times.append(t)
            last_kept = t

    # 限制最大数量
    if max_frames and max_frames > 0:
        filtered_times = filtered_times[:max_frames]

    if not filtered_times:
        return []

    # 使用时间戳作为前缀避免文件名冲突
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    prefix = f"scenes_{timestamp}"
    created_files: list[str] = []

    if ctx:
        ctx.report_progress(
            base_progress + int(progress_range * 0.5),
            f"Video {video_index + 1}/{total_videos}: extracting scene keyframes...",
        )

    # 第二遍：逐时间戳抽帧
    for idx, ts in enumerate(filtered_times, start=1):
        out_path = os.path.join(actual_output_dir, f"{prefix}_{idx:06d}.{image_format}")
        inp = ffmpeg.input(video_path, ss=ts)
        vf = inp.video
        if width or height:
            scale_w = width if width else -1
            scale_h = height if height else -1
            vf = vf.filter("scale", scale_w, scale_h)
        _ffmpeg_run(
            ffmpeg.output(vf, out_path, vframes=1),
            capture_stdout=True,
            capture_stderr=True,
        )
        created_files.append(out_path)

        if ctx:
            frame_progress = base_progress + int(
                progress_range * (0.5 + 0.4 * (idx / len(filtered_times)))
            )
            ctx.report_progress(
                frame_progress,
                f"Video {video_index + 1}/{total_videos}: extracted {idx}/{len(filtered_times)} frame(s)...",
            )

    return created_files


@mcp.tool()
def extract_scene_change_frames(
    video_path: list[str],
    output_dir: str,
    image_format: str = "png",
    scene_threshold: float = 0.4,
    min_scene_gap_seconds: float | None = None,
    max_frames: int | None = None,
    width: int | None = None,
    height: int | None = None,
    ctx: Context = None,
) -> str:
    """Detect scene changes and export representative keyframes.

    Args:
        video_path: List of input video paths (multiple videos supported).
        output_dir: Output directory (auto-created if needed).
        image_format: Output image format such as 'png', 'jpg', or 'webp'. Default is 'png'.
        scene_threshold: Scene-change threshold (0.0–1.0, typically 0.3–0.5).
        min_scene_gap_seconds: Minimum gap between consecutive keyframes.
        max_frames: Maximum number of keyframes to export.
        width: Optional width for scaling.
        height: Optional height for scaling.

    Returns:
        A status message indicating success or failure.
    """
    execution_start_time = time.time()

    # 兼容单个路径字符串输入
    if isinstance(video_path, str):
        video_path = [video_path]

    if not video_path:
        raise RuntimeError("Error: video_path list is empty.")

    # 校验参数
    valid_formats = {"png", "jpg", "jpeg", "webp", "bmp", "tiff"}
    if image_format not in valid_formats:
        raise RuntimeError(
            f"Error: Invalid image_format '{image_format}'. Supported: {', '.join(sorted(valid_formats))}"
        )

    if not (0.0 <= scene_threshold <= 1.0):
        raise RuntimeError(
            f"Error: scene_threshold must be between 0.0 and 1.0, got {scene_threshold}"
        )

    if min_scene_gap_seconds is not None and min_scene_gap_seconds <= 0:
        raise RuntimeError("Error: min_scene_gap_seconds must be positive.")

    if max_frames is not None and max_frames <= 0:
        raise RuntimeError("Error: max_frames must be positive.")

    if width is not None and width <= 0:
        raise RuntimeError("Error: width must be positive.")
    if height is not None and height <= 0:
        raise RuntimeError("Error: height must be positive.")

    try:
        all_created_files: list[str] = []
        total_videos = len(video_path)

        for idx, single_video_path in enumerate(video_path):
            files = _extract_single_scene_change_frames(
                video_path=single_video_path,
                output_dir=output_dir,
                image_format=image_format,
                scene_threshold=scene_threshold,
                min_scene_gap_seconds=min_scene_gap_seconds,
                max_frames=max_frames,
                width=width,
                height=height,
                ctx=ctx,
                video_index=idx,
                total_videos=total_videos,
            )
            all_created_files.extend(files)

        if ctx:
            ctx.report_progress(100, "Scene keyframe extraction completed")

        execution_time = time.time() - execution_start_time

        if execution_time > 59 and all_created_files:
            for path in all_created_files:
                _open_aido_link(ctx, path)

        if not all_created_files:
            return "No scene-change frames detected in any video."

        return (
            f"Scene-change frames extracted. Videos={total_videos}, Count={len(all_created_files)}. "
            f"Output dir='{output_dir}'."
        )
    except ffmpeg.Error as e:
        error_message = e.stderr.decode("utf8") if e.stderr else str(e)
        raise RuntimeError(f"Error extracting scene-change frames: {error_message}")
    except Exception as e:
        raise RuntimeError(
            f"An unexpected error occurred in extract_scene_change_frames: {str(e)}"
        )


def main():
    """Main entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
