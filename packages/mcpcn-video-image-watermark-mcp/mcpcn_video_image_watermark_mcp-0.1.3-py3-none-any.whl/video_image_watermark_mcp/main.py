from mcp.server.fastmcp import FastMCP, Context
import ffmpeg
import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import tempfile
import urllib.parse
import platform
import subprocess
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

package = "video-image-watermark-mcp"

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
    if "overwrite_output" not in kwargs:
        kwargs["overwrite_output"] = True
    return ffmpeg.run(stream_spec, cmd=FFMPEG_BINARY, **kwargs)


def _ffprobe_probe(path: str, **kwargs):
    return ffmpeg.probe(path, cmd=FFPROBE_BINARY, **kwargs)


def _parse_time_to_seconds(time_str: str) -> float:
    if isinstance(time_str, (int, float)):
        return float(time_str)
    if ":" in time_str:
        parts = time_str.split(":")
        if len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
        elif len(parts) == 2:
            return int(parts[0]) * 60 + float(parts[1])
        else:
            raise ValueError(f"Invalid time format: {time_str}")
    return float(time_str)


def _prepare_path(input_path: str, output_path: str, overwrite: bool = False) -> None:
    if not os.path.exists(input_path):
        raise RuntimeError(f"Error: Input file not found at {input_path}")
    try:
        parent_dir = os.path.dirname(output_path)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)
    except Exception as e:
        raise RuntimeError(
            f"Error creating output directory for {output_path}: {str(e)}"
        )
    if os.path.exists(output_path) and not overwrite:
        raise RuntimeError(
            f"Error: Output file already exists at {output_path}. Please choose a different path, delete the existing file, or set overwrite=True."
        )


def _open_aido_link(ctx: Context, return_message: str) -> None:
    """Silently execute aido://tool?xxx&chatSessionId=xxx on every platform."""
    try:
        if ctx is None:
            logger.debug("Context is None, skipping aido link execution")
            return

        request_context = getattr(ctx, 'request_context', None)
        chatSessionId = None
        if request_context and hasattr(request_context, 'meta'):
            context_meta = getattr(request_context, 'meta', None)
            logger.debug(f"context meta: {context_meta}")
            if context_meta and hasattr(context_meta, 'chatSessionId'):
                chatSessionId = getattr(context_meta, 'chatSessionId', None)
                logger.debug(f"chatSessionId from request_context.meta: {chatSessionId}")

        if not chatSessionId or chatSessionId == 'None':
            logger.warning(f"Invalid or missing chatSessionId: {chatSessionId}, skipping aido link execution")
            return

        encoded_message = urllib.parse.quote(return_message, safe='')
        package_name = urllib.parse.quote(package, safe='')
        aido_url = f"aido://tool?path={encoded_message}&chatSessionId={chatSessionId}&package={package_name}"

        system = platform.system().lower()
        if system == 'darwin':
            result = subprocess.run(['open', aido_url], check=False, capture_output=True, text=True)
            if result.returncode != 0 and result.stderr:
                logger.warning(f"macOS open command failed: {result.stderr}")
        elif system == 'windows':
            try:
                os.startfile(aido_url)
            except (OSError, AttributeError) as e:
                logger.debug(f"os.startfile failed, trying start command: {e}")
                result = subprocess.run(f'start "" "{aido_url}"', shell=True, check=False, capture_output=True, text=True)
                if result.returncode != 0 and result.stderr:
                    logger.warning(f"Windows start command failed: {result.stderr}")
        elif system == 'linux':
            result = subprocess.run(['xdg-open', aido_url], check=False, capture_output=True, text=True)
            if result.returncode != 0 and result.stderr:
                logger.warning(f"Linux xdg-open command failed: {result.stderr}")
        else:
            logger.warning(f"Unsupported operating system: {system}")
            return

        logger.info(f"Executed aido link on {system}: {aido_url}")
    except Exception as e:
        logger.error(f"Failed to execute aido link: {str(e)}", exc_info=True)


mcp = FastMCP("VideoImageWatermarkServer")


def _process_single_video(
    video_path: str,
    output_video_path: str,
    image_path: str,
    position: str,
    opacity: float,
    start_time: str,
    end_time: str,
    width: str,
    height: str,
    overwrite: bool = False,
) -> str:
    """Process a single video by applying an image watermark."""
    _prepare_path(video_path, output_video_path, overwrite)
    try:
        if not os.path.exists(video_path):
            raise RuntimeError(f"Error: Input video file not found at {video_path}")
        if not os.path.exists(image_path):
            raise RuntimeError(f"Error: Overlay image file not found at {image_path}")

        main_input = ffmpeg.input(video_path)
        overlay_input = ffmpeg.input(image_path)
        processed_overlay = overlay_input

        if width or height:
            w_val = width if width else "-1"
            h_val = height if height else "-1"
            processed_overlay = processed_overlay.filter("scale", w=w_val, h=h_val)

        if opacity is not None and 0.0 <= opacity <= 1.0:
            processed_overlay = processed_overlay.filter("format", "rgba")
            processed_overlay = processed_overlay.filter(
                "colorchannelmixer", aa=str(opacity)
            )

        overlay_x_pos = "0"
        overlay_y_pos = "0"
        if position == "top_left":
            overlay_x_pos, overlay_y_pos = "10", "10"
        elif position == "top_right":
            overlay_x_pos, overlay_y_pos = "main_w-overlay_w-10", "10"
        elif position == "bottom_left":
            overlay_x_pos, overlay_y_pos = "10", "main_h-overlay_h-10"
        elif position == "bottom_right":
            overlay_x_pos, overlay_y_pos = "main_w-overlay_w-10", "main_h-overlay_h-10"
        elif position == "center":
            overlay_x_pos, overlay_y_pos = (
                "(main_w-overlay_w)/2",
                "(main_h-overlay_h)/2",
            )
        elif ":" in position:
            pos_parts = position.split(":")
            for part in pos_parts:
                if part.startswith("x="):
                    overlay_x_pos = part.split("=")[1]
                if part.startswith("y="):
                    overlay_y_pos = part.split("=")[1]

        overlay_filter_kwargs = {"x": overlay_x_pos, "y": overlay_y_pos}
        if start_time is not None or end_time is not None:
            actual_start_sec = (
                _parse_time_to_seconds(start_time) if start_time is not None else 0
            )
            if end_time is not None:
                actual_end_sec = _parse_time_to_seconds(end_time)
                enable_expr = f"between(t,{actual_start_sec},{actual_end_sec})"
            else:
                enable_expr = f"gte(t,{actual_start_sec})"
            overlay_filter_kwargs["enable"] = enable_expr

        try:
            video_with_overlay = ffmpeg.filter(
                [main_input, processed_overlay], "overlay", **overlay_filter_kwargs
            )
            probe = _ffprobe_probe(video_path)
            has_audio = any(s["codec_type"] == "audio" for s in probe["streams"])
            if has_audio:
                output_node = ffmpeg.output(
                    video_with_overlay,
                    main_input.audio,
                    output_video_path,
                    vcodec="libx264",
                    pix_fmt="yuv420p",
                    acodec="copy",
                )
            else:
                output_node = ffmpeg.output(
                    video_with_overlay,
                    output_video_path,
                    vcodec="libx264",
                    pix_fmt="yuv420p",
                )
            _ffmpeg_run(output_node, capture_stdout=True, capture_stderr=True)
            return f"Image overlay added successfully to {output_video_path}"
        except ffmpeg.Error as e_acopy:
            try:
                video_with_overlay_fallback = ffmpeg.filter(
                    [main_input, processed_overlay], "overlay", **overlay_filter_kwargs
                )
                probe = _ffprobe_probe(video_path)
                has_audio = any(s["codec_type"] == "audio" for s in probe["streams"])
                if has_audio:
                    output_node_fallback = ffmpeg.output(
                        video_with_overlay_fallback,
                        main_input.audio,
                        output_video_path,
                        vcodec="libx264",
                        pix_fmt="yuv420p",
                        acodec="aac",
                    )
                else:
                    output_node_fallback = ffmpeg.output(
                        video_with_overlay_fallback,
                        output_video_path,
                        vcodec="libx264",
                        pix_fmt="yuv420p",
                    )
                _ffmpeg_run(
                    output_node_fallback, capture_stdout=True, capture_stderr=True
                )
                return f"Image overlay added successfully to {output_video_path}"
            except ffmpeg.Error as e_recode:
                err_acopy_msg = (
                    e_acopy.stderr.decode("utf8") if e_acopy.stderr else str(e_acopy)
                )
                err_recode_msg = (
                    e_recode.stderr.decode("utf8") if e_recode.stderr else str(e_recode)
                )
                raise RuntimeError(
                    f"Error adding image overlay. Audio copy attempt: {err_acopy_msg}. Full re-encode attempt: {err_recode_msg}"
                )
    except ffmpeg.Error as e:
        error_message = e.stderr.decode("utf8") if e.stderr else str(e)
        raise RuntimeError(f"Error processing image overlay: {error_message}")
    except FileNotFoundError:
        raise RuntimeError(
            f"Error: An input file was not found (video: '{video_path}', image: '{image_path}'). Please check paths."
        )
    except Exception as e:
        raise RuntimeError(
            f"An unexpected error occurred in add_image_overlay: {str(e)}"
        )


@mcp.tool()
def add_image_overlay(
    video_paths: list[str],
    output_video_paths: list[str] | None = None,
    output_dir: str | None = None,
    image_path: str = "",
    position: str = "top_right",
    opacity: float = None,
    start_time: str = None,
    end_time: str = None,
    width: str = None,
    height: str = None,
    overwrite: bool = False,
    ctx: Context = None
) -> str:
    """Batch apply an image overlay (watermark/logo) to multiple videos.

    Args:
        video_paths: List of input video paths.
        output_video_paths: Optional list of output file paths (must match video_paths length). If provided, output_dir is ignored.
        output_dir: Output directory; each output filename gets a _watermarked suffix. Ignored if output_video_paths is provided.
        image_path: Path to the overlay image (supports alpha channel).
        position: Preset location 'top_left'|'top_right'|'bottom_left'|'bottom_right'|'center', or a custom 'x=..:y=..' expression.
        opacity: Overlay opacity between 0.0 and 1.0.
        start_time: When the overlay should start (seconds or 'HH:MM:SS').
        end_time: When the overlay should stop (seconds or 'HH:MM:SS').
        width/height: Target dimensions; specify one (or both) to scale the overlay appropriately.
        overwrite: Whether to overwrite existing output files (default: False).

    Returns:
        A summary listing the files that succeeded and failed.
    """
    execution_start_time = time.time()
    
    if not video_paths:
        raise RuntimeError("Error: video_paths list is empty")

    if not os.path.exists(image_path):
        raise RuntimeError(f"Error: Overlay image file not found at {image_path}")

    # 验证 output_video_paths 参数
    if output_video_paths is not None:
        if len(output_video_paths) != len(video_paths):
            raise RuntimeError(f"Error: output_video_paths length ({len(output_video_paths)}) must match video_paths length ({len(video_paths)})")
    elif output_dir is None:
        raise RuntimeError("Error: Either output_video_paths or output_dir must be provided")

    # 创建输出目录
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    results = []
    success_results = []
    success_count = 0
    fail_count = 0

    for idx, video_path in enumerate(video_paths):
        try:
            # 优先使用 output_video_paths，否则生成输出文件路径
            if output_video_paths is not None:
                output_video_path = output_video_paths[idx]
            else:
                # 生成输出文件路径（带时间戳避免冲突）
                base_name = os.path.basename(video_path)
                name, ext = os.path.splitext(base_name)
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                output_video_path = os.path.join(output_dir, f"{name}_watermarked_{timestamp}{ext}")

            result = _process_single_video(
                video_path=video_path,
                output_video_path=output_video_path,
                image_path=image_path,
                position=position,
                opacity=opacity,
                start_time=start_time,
                end_time=end_time,
                width=width,
                height=height,
                overwrite=overwrite,
            )
            results.append(f"✓ {video_path} -> {output_video_path}")
            success_results.append(output_video_path)
            success_count += 1
        except Exception as e:
            results.append(f"✗ {video_path}: {str(e)}")
            fail_count += 1

    execution_time = time.time() - execution_start_time
    
    summary = f"\nProcessing finished: {success_count} succeeded, {fail_count} failed\n"
    summary += f"Total execution time: {execution_time:.2f} seconds.\n"
    result_message = summary + "\n".join(results)

    # 如果全部失败，抛出异常以设置 isError: true
    if success_count == 0 and fail_count > 0:
        raise RuntimeError(result_message)

    # 如果有成功的结果且执行时间超过59秒，打开第一个成功的文件
    if success_results and execution_time > 59:
        for path in success_results:
            _open_aido_link(ctx, path)

    return result_message


def main():
    """Main entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
