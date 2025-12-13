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

package = "video-text-watermark-mcp"

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


def _prepare_path(input_path: str, output_path: str) -> None:
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
    if os.path.exists(output_path):
        raise RuntimeError(
            f"Error: Output file already exists at {output_path}. Please choose a different path or delete the existing file."
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


mcp = FastMCP("VideoTextWatermarkServer")


def _generate_output_path(input_path: str, suffix: str) -> str:
    """Generate output path with timestamp to avoid conflicts.
    
    Args:
        input_path: Input file path
        suffix: Suffix to add before timestamp (e.g., '_text_watermark')
        
    Returns:
        Generated output path with timestamp
    """
    directory = os.path.dirname(input_path)
    name, ext = os.path.splitext(os.path.basename(input_path))
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    return os.path.join(directory, f"{name}{suffix}_{timestamp}{ext}")


def _process_single_text_watermark(
    video_path: str,
    output_video_path: str,
    watermark_text: str,
    font_size: int,
    font_color: str,
    position: str,
    opacity: float,
    font_file: str,
    outline_color: str,
    outline_width: int,
    box: bool,
    box_color: str,
    box_padding: int,
) -> str:
    """Handle text watermarking for a single video."""
    _prepare_path(video_path, output_video_path)
    try:
        if not os.path.exists(video_path):
            raise RuntimeError(f"Error: Input video file not found at {video_path}")

        safe_text = (
            watermark_text.replace("\\", "\\\\")
            .replace("'", "\\'")
            .replace(":", "\\:")
            .replace(",", "\\,")
        )

        position_map = {
            "top_left": ("10", "10"),
            "top_center": ("(w-text_w)/2", "10"),
            "top_right": ("w-text_w-10", "10"),
            "center_left": ("10", "(h-text_h)/2"),
            "center": ("(w-text_w)/2", "(h-text_h)/2"),
            "center_right": ("w-text_w-10", "(h-text_h)/2"),
            "bottom_left": ("10", "h-text_h-10"),
            "bottom_center": ("(w-text_w)/2", "h-text_h-10"),
            "bottom_right": ("w-text_w-10", "h-text_h-10"),
        }

        if position in position_map:
            x_pos, y_pos = position_map[position]
        elif ":" in position:
            parts = position.split(":")
            x_pos = "w-text_w-10"
            y_pos = "h-text_h-10"
            for part in parts:
                if part.startswith("x="):
                    x_pos = part.split("=")[1]
                elif part.startswith("y="):
                    y_pos = part.split("=")[1]
        else:
            raise RuntimeError(f"Error: Invalid position '{position}'")

        filter_params = [
            f"text='{safe_text}'",
            f"fontsize={font_size}",
            f"fontcolor={font_color}@{opacity}",
            f"x={x_pos}",
            f"y={y_pos}",
        ]

        if font_file and os.path.exists(font_file):
            safe_font_path = (
                font_file.replace("\\", "\\\\").replace("'", "\\'").replace(":", "\\:")
            )
            filter_params.append(f"fontfile='{safe_font_path}'")
        else:
            if any("\u4e00" <= char <= "\u9fff" for char in watermark_text):
                default_cn_fonts = [
                    "/System/Library/Fonts/PingFang.ttc",
                    "/System/Library/Fonts/STHeiti Medium.ttc",
                    "/Library/Fonts/Arial Unicode.ttf",
                ]
                for font in default_cn_fonts:
                    if os.path.exists(font):
                        safe_font_path = (
                            font.replace("\\", "\\\\")
                            .replace("'", "\\'")
                            .replace(":", "\\:")
                        )
                        filter_params.append(f"fontfile='{safe_font_path}'")
                        logger.info(f"Using fallback Chinese font: {font}")
                        break

        if outline_color and outline_width > 0:
            filter_params.append(f"bordercolor={outline_color}")
            filter_params.append(f"borderw={outline_width}")

        if box:
            filter_params.append("box=1")
            filter_params.append(f"boxcolor={box_color}")
            filter_params.append(f"boxborderw={box_padding}")

        drawtext_filter = f"drawtext={':'.join(filter_params)}"

        input_stream = ffmpeg.input(video_path)

        try:
            stream = input_stream.output(
                output_video_path,
                vf=drawtext_filter,
                vcodec="libx264",
                pix_fmt="yuv420p",
                acodec="copy",
            )
            _ffmpeg_run(stream, capture_stdout=True, capture_stderr=True)
            return f"Text watermark added successfully to {output_video_path}"
        except ffmpeg.Error as e_acopy:
            try:
                stream_recode = input_stream.output(
                    output_video_path,
                    vf=drawtext_filter,
                    vcodec="libx264",
                    pix_fmt="yuv420p",
                    acodec="aac",
                )
                _ffmpeg_run(stream_recode, capture_stdout=True, capture_stderr=True)
                return f"Text watermark added successfully (audio re-encoded) to {output_video_path}"
            except ffmpeg.Error as e_recode_all:
                err_acopy_msg = (
                    e_acopy.stderr.decode("utf8") if e_acopy.stderr else str(e_acopy)
                )
                err_recode_msg = (
                    e_recode_all.stderr.decode("utf8")
                    if e_recode_all.stderr
                    else str(e_recode_all)
                )
                raise RuntimeError(
                    f"Error adding text watermark. Audio copy attempt: {err_acopy_msg}. Full re-encode attempt: {err_recode_msg}"
                )
    except ffmpeg.Error as e:
        error_message = e.stderr.decode("utf8") if e.stderr else str(e)
        raise RuntimeError(f"Error processing text watermark: {error_message}")
    except FileNotFoundError:
        raise RuntimeError(f"Error: Input video file not found.")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {str(e)}")


@mcp.tool()
def add_text_watermark(
    video_paths: list[str],
    watermark_text: str,
    output_video_paths: list[str] | None = None,
    font_size: int = 24,
    font_color: str = "white",
    position: str = "bottom_right",
    opacity: float = 0.7,
    font_file: str = None,
    outline_color: str = None,
    outline_width: int = 0,
    box: bool = False,
    box_color: str = "black@0.5",
    box_padding: int = 5,
    ctx: Context = None
) -> str:
    """Add persistent text watermarks to videos, supporting batch processing.

    Args:
        video_paths: Input video paths.
        watermark_text: Text to render as the watermark.
        output_video_paths: Output paths (optional, auto-generated with timestamp if not provided).
        font_size: Font size (default 24).
        font_color: Font color (default 'white'; accepts names or hex '#FFFFFF').
        position: Watermark location:
            - 'top_left': top-left corner
            - 'top_center': top edge, centered
            - 'top_right': top-right corner
            - 'center_left': middle left
            - 'center': center of the frame
            - 'center_right': middle right
            - 'bottom_left': bottom-left corner
            - 'bottom_center': bottom edge, centered
            - 'bottom_right': bottom-right corner (default)
            - or custom expressions like 'x=100:y=100'
        opacity: Opacity between 0.0 and 1.0 (default 0.7).
        font_file: Optional font file path (useful for CJK or special fonts).
        outline_color: Optional outline color.
        outline_width: Outline width (default 0).
        box: Whether to draw a background box (default False).
        box_color: Background color (default 'black@0.5' for semi-transparent black).
        box_padding: Inner padding for the background box (default 5).

    Returns:
        A status message indicating success or failure.
    """
    execution_start_time = time.time()
    
    # Auto-generate output paths if not provided
    if output_video_paths is None:
        output_video_paths = [_generate_output_path(vp, "_text_watermark") for vp in video_paths]
    elif len(video_paths) != len(output_video_paths):
        raise RuntimeError(
            f"Error: video_paths count ({len(video_paths)}) must match output_video_paths count ({len(output_video_paths)})"
        )

    results = []
    success_results = []
    for video_path, output_video_path in zip(video_paths, output_video_paths):
        try:
            result = _process_single_text_watermark(
                video_path=video_path,
                output_video_path=output_video_path,
                watermark_text=watermark_text,
                font_size=font_size,
                font_color=font_color,
                position=position,
                opacity=opacity,
                font_file=font_file,
                outline_color=outline_color,
                outline_width=outline_width,
                box=box,
                box_color=box_color,
                box_padding=box_padding,
            )
            results.append(result)
            success_results.append(output_video_path)
        except Exception as e:
            results.append(f"Failed to process {video_path}: {str(e)}")

    execution_time = time.time() - execution_start_time
    
    # 统计成功和失败数量
    success_count = sum(1 for r in results if not r.startswith("Failed"))
    fail_count = len(results) - success_count
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


def _process_single_text_overlay(
    video_path: str, output_video_path: str, text_elements: list[dict]
) -> str:
    """Apply time-based text overlays to a single video."""
    _prepare_path(video_path, output_video_path)
    try:
        if not os.path.exists(video_path):
            raise RuntimeError(f"Error: Input video file not found at {video_path}")
        if not text_elements:
            raise RuntimeError("Error: No text elements provided for overlay.")

        input_stream = ffmpeg.input(video_path)
        drawtext_filters = []

        for element in text_elements:
            text = element.get("text")
            start_time = element.get("start_time")
            end_time = element.get("end_time")
            if text is None or start_time is None or end_time is None:
                raise RuntimeError(
                    f"Error: Text element is missing required keys (text, start_time, end_time)."
                )
            safe_text = (
                text.replace("\\", "\\\\")
                .replace("'", "\\'")
                .replace(":", "\\:")
                .replace(",", "\\,")
            )
            start_sec = _parse_time_to_seconds(start_time)
            end_sec = _parse_time_to_seconds(end_time)

            font_size = element.get("font_size", 48)
            font_color = element.get("font_color", "white")
            x_pos = element.get("x_pos", "(w-text_w)/2")
            y_pos = element.get("y_pos", "h-text_h-50")
            box_padding = element.get("box_padding", 10)

            filter_params = [
                f"text='{safe_text}'",
                f"fontsize={font_size}",
                f"fontcolor={font_color}",
                f"x={x_pos}",
                f"y={y_pos}",
                f"enable=between(t\\,{start_sec}\\,{end_sec})",
            ]

            if element.get("box", False):
                filter_params.append("box=1")
                box_color = element.get("box_color", "black@0.7")
                filter_params.append(f"boxcolor={box_color}")
                box_border_width = element.get("box_border_width", box_padding)
                filter_params.append(f"boxborderw={box_border_width}")
                if "black" in box_color.lower() and font_color.lower() == "black":
                    filter_params[2] = "fontcolor=white"
                    logger.info(
                        "Automatically switched text color to white for better contrast with a black background"
                    )

            if "font_file" in element:
                font_path = (
                    element["font_file"]
                    .replace("\\", "\\\\")
                    .replace("'", "\\'")
                    .replace(":", "\\:")
                )
                filter_params.append(f"fontfile='{font_path}'")
            else:
                if any("\u4e00" <= char <= "\u9fff" for char in text):
                    default_cn_fonts = [
                        "/System/Library/Fonts/PingFang.ttc",
                        "/System/Library/Fonts/STHeiti Medium.ttc",
                        "/Library/Fonts/Arial Unicode.ttf",
                        "/System/Library/Fonts/Helvetica.ttc",
                    ]
                    for font in default_cn_fonts:
                        if os.path.exists(font):
                            safe_font_path = (
                                font.replace("\\", "\\\\")
                                .replace("'", "\\'")
                                .replace(":", "\\:")
                            )
                            filter_params.append(f"fontfile='{safe_font_path}'")
                            logger.info(f"Using fallback Chinese font: {font}")
                            break
            drawtext_filter = f"drawtext={':'.join(filter_params)}"
            drawtext_filters.append(drawtext_filter)

        final_vf_filter = ",".join(drawtext_filters)

        try:
            stream = input_stream.output(
                output_video_path,
                vf=final_vf_filter,
                vcodec="libx264",
                pix_fmt="yuv420p",
                acodec="copy",
            )
            _ffmpeg_run(stream, capture_stdout=True, capture_stderr=True)
            return f"Text overlays added successfully to {output_video_path}"
        except ffmpeg.Error as e_acopy:
            try:
                stream_recode = input_stream.output(
                    output_video_path,
                    vf=final_vf_filter,
                    vcodec="libx264",
                    pix_fmt="yuv420p",
                    acodec="aac",
                )
                _ffmpeg_run(stream_recode, capture_stdout=True, capture_stderr=True)
                return f"Text overlays added successfully to {output_video_path}"
            except ffmpeg.Error as e_recode_all:
                err_acopy_msg = (
                    e_acopy.stderr.decode("utf8") if e_acopy.stderr else str(e_acopy)
                )
                err_recode_msg = (
                    e_recode_all.stderr.decode("utf8")
                    if e_recode_all.stderr
                    else str(e_recode_all)
                )
                raise RuntimeError(
                    f"Error adding text overlays. Audio copy attempt: {err_acopy_msg}. Full re-encode attempt: {err_recode_msg}"
                )
    except ffmpeg.Error as e:
        error_message = e.stderr.decode("utf8") if e.stderr else str(e)
        raise RuntimeError(f"Error processing text overlays: {error_message}")
    except FileNotFoundError:
        raise RuntimeError(f"Error: Input video file not found.")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {str(e)}")


@mcp.tool()
def add_text_overlay(
    video_paths: list[str], 
    text_elements: list[dict],
    output_video_paths: list[str] | None = None,
    ctx: Context = None
) -> str:
    """Apply time-bound text overlays to videos, supporting batch operations.

    Args:
        video_paths: Input video file paths.
        text_elements: List of dictionaries describing each overlay:
            - text: Text content (required).
            - start_time/end_time: Time range in seconds or 'HH:MM:SS'.
            - font_size: Font size (integer, default 24).
            - font_color: Font color (default 'white').
            - x_pos/y_pos: Position expressions or absolute pixels (default center/bottom).
            - box: Whether to display a background box (bool).
            - box_color/box_border_width: Background color and border width.
            - font_file: Optional font file path.
            - box_padding: Inner padding for the background box (integer, default 5).
        output_video_paths: Output file paths (optional, auto-generated with timestamp if not provided).

    Returns:
        A status message indicating success or failure.
    """
    execution_start_time = time.time()
    
    # Auto-generate output paths if not provided
    if output_video_paths is None:
        output_video_paths = [_generate_output_path(vp, "_text_overlay") for vp in video_paths]
    elif len(video_paths) != len(output_video_paths):
        raise RuntimeError(
            f"Error: video_paths count ({len(video_paths)}) must match output_video_paths count ({len(output_video_paths)})"
        )

    results = []
    success_results = []
    for video_path, output_video_path in zip(video_paths, output_video_paths):
        try:
            result = _process_single_text_overlay(
                video_path=video_path,
                output_video_path=output_video_path,
                text_elements=text_elements,
            )
            results.append(result)
            success_results.append(output_video_path)
        except Exception as e:
            results.append(f"Failed to process {video_path}: {str(e)}")

    execution_time = time.time() - execution_start_time
    
    # 统计成功和失败数量
    success_count = sum(1 for r in results if not r.startswith("Failed"))
    fail_count = len(results) - success_count
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
