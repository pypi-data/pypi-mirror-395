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

package = "video-aspect-ratio-mcp"

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


def _generate_output_path(input_path: str, output_dir: str) -> str:
    """Generate an output path based on the input file and target directory."""
    filename = os.path.basename(input_path)
    name, ext = os.path.splitext(filename)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_filename = f"{name}_aspect_{timestamp}{ext}"
    return os.path.join(output_dir, output_filename)


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

mcp = FastMCP("VideoAspectRatioServer")


def _process_single_video(
    video_path: str,
    output_video_path: str,
    target_aspect_ratio: str,
    resize_mode: str,
    padding_color: str,
    overwrite: bool = False,
) -> str:
    """Adjust the aspect ratio for a single video."""
    _prepare_path(video_path, output_video_path, overwrite)
    try:
        probe = _ffprobe_probe(video_path)
        video_stream_info = next(
            (stream for stream in probe["streams"] if stream["codec_type"] == "video"),
            None,
        )
        if not video_stream_info:
            raise RuntimeError("Error: No video stream found in the input file.")

        original_width = int(video_stream_info["width"])
        original_height = int(video_stream_info["height"])

        num, den = map(int, target_aspect_ratio.split(":"))
        target_ar_val = num / den
        original_ar_val = original_width / original_height

        vf_filter = ""

        if resize_mode == "pad":
            if abs(original_ar_val - target_ar_val) < 1e-4:
                try:
                    _ffmpeg_run(
                        ffmpeg.input(video_path).output(output_video_path, c="copy"),
                        capture_stdout=True,
                        capture_stderr=True,
                    )
                    return f"Video aspect ratio already matches. Copied to {output_video_path}."
                except ffmpeg.Error:
                    _ffmpeg_run(
                        ffmpeg.input(video_path).output(output_video_path),
                        capture_stdout=True,
                        capture_stderr=True,
                    )
                    return f"Video aspect ratio already matches. Re-encoded to {output_video_path}."

            option1_w = int(original_height * target_ar_val)
            option1_h = original_height
            option2_w = original_width
            option2_h = int(original_width / target_ar_val)

            if option1_w >= original_width and option1_h >= original_height:
                final_w = option1_w
                final_h = option1_h
            elif option2_w >= original_width and option2_h >= original_height:
                final_w = option2_w
                final_h = option2_h
            else:
                if option1_w * option1_h > option2_w * option2_h:
                    final_w = max(option1_w, original_width)
                    final_h = max(option1_h, original_height)
                else:
                    final_w = max(option2_w, original_width)
                    final_h = max(option2_h, original_height)

            vf_filter = f"scale={final_w}:{final_h}:force_original_aspect_ratio=decrease,pad={final_w}:{final_h}:(ow-iw)/2:(oh-ih)/2:{padding_color}"

        elif resize_mode == "crop":
            if abs(original_ar_val - target_ar_val) < 1e-4:
                try:
                    _ffmpeg_run(
                        ffmpeg.input(video_path).output(output_video_path, c="copy"),
                        capture_stdout=True,
                        capture_stderr=True,
                    )
                    return f"Video aspect ratio already matches. Copied to {output_video_path}."
                except ffmpeg.Error:
                    _ffmpeg_run(
                        ffmpeg.input(video_path).output(output_video_path),
                        capture_stdout=True,
                        capture_stderr=True,
                    )
                    return f"Video aspect ratio already matches. Re-encoded to {output_video_path}."

            if original_ar_val > target_ar_val:
                new_width = int(original_height * target_ar_val)
                vf_filter = f"crop={new_width}:{original_height}:(iw-{new_width})/2:0"
            else:
                new_height = int(original_width / target_ar_val)
                vf_filter = f"crop={original_width}:{new_height}:0:(ih-{new_height})/2"
        else:
            raise RuntimeError(
                f"Error: Invalid resize_mode '{resize_mode}'. Must be 'pad' or 'crop'."
            )

        try:
            _ffmpeg_run(
                ffmpeg.input(video_path).output(
                    output_video_path,
                    vf=vf_filter,
                    vcodec="libx264",
                    pix_fmt="yuv420p",
                    acodec="copy",
                ),
                capture_stdout=True,
                capture_stderr=True,
            )
            return f"Video aspect ratio changed (audio copy) to {target_aspect_ratio} using {resize_mode}. Saved to {output_video_path}"
        except ffmpeg.Error as e_acopy:
            try:
                _ffmpeg_run(
                    ffmpeg.input(video_path).output(
                        output_video_path,
                        vf=vf_filter,
                        vcodec="libx264",
                        pix_fmt="yuv420p",
                    ),
                    capture_stdout=True,
                    capture_stderr=True,
                )
                return f"Video aspect ratio changed (audio re-encoded) to {target_aspect_ratio} using {resize_mode}. Saved to {output_video_path}"
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
                    f"Error changing aspect ratio. Audio copy attempt failed: {err_acopy_msg}. Full re-encode attempt also failed: {err_recode_msg}."
                )
    except ffmpeg.Error as e:
        error_message = e.stderr.decode("utf8") if e.stderr else str(e)
        raise RuntimeError(f"Error changing aspect ratio: {error_message}")
    except FileNotFoundError:
        raise RuntimeError(f"Error: Input video file not found at {video_path}")
    except ValueError:
        raise RuntimeError(
            f"Error: Invalid target_aspect_ratio format. Expected 'num:den' (e.g., '16:9')."
        )
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {str(e)}")


@mcp.tool()
def change_aspect_ratio(
    video_paths: list[str],
    output_video_paths: list[str] | None = None,
    output_dir: str | None = None,
    target_aspect_ratio: str = "16:9",
    resize_mode: str = "pad",
    padding_color: str = "black",
    overwrite: bool = False,
    ctx: Context = None,
) -> str:
    """Batch-adjust the aspect ratio for multiple videos.

    Args:
        video_paths: List of input video paths.
        output_video_paths: Optional list of output file paths (must match video_paths length). If provided, output_dir is ignored.
        output_dir: Directory where processed videos are saved. Ignored if output_video_paths is provided.
        target_aspect_ratio: Ratio string like '16:9', '4:3', or '1:1'.
        resize_mode: 'pad' for letterboxing, 'crop' for center-cropping.
        padding_color: Padding color when using 'pad' (e.g., 'black', 'white', '#RRGGBB').
        overwrite: Whether to overwrite existing output files (default: False).

    Returns:
        A summary describing the processing outcome.
    """
    if not video_paths:
        raise RuntimeError("Error: No video paths provided.")

    # 验证 output_video_paths 参数
    if output_video_paths is not None:
        if len(output_video_paths) != len(video_paths):
            raise RuntimeError(f"Error: output_video_paths length ({len(output_video_paths)}) must match video_paths length ({len(video_paths)})")
    elif output_dir is None:
        raise RuntimeError("Error: Either output_video_paths or output_dir must be provided")

    execution_start_time = time.time()

    # 确保输出目录存在
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    results = []
    success_results = []
    success_count = 0
    fail_count = 0

    for idx, video_path in enumerate(video_paths):
        if output_video_paths is not None:
            output_video_path = output_video_paths[idx]
        else:
            output_video_path = _generate_output_path(video_path, output_dir)
        try:
            result = _process_single_video(
                video_path,
                output_video_path,
                target_aspect_ratio,
                resize_mode,
                padding_color,
                overwrite,
            )
            results.append(f"✓ {os.path.basename(video_path)}: {result}")
            success_results.append(output_video_path)
            success_count += 1
        except Exception as e:
            results.append(f"✗ {os.path.basename(video_path)}: {str(e)}")
            fail_count += 1

    execution_time = time.time() - execution_start_time
    summary = f"\nProcessing finished: {success_count} succeeded, {fail_count} failed\n"
    summary += f"Total execution time: {execution_time:.2f} seconds.\n"
    result_message = summary + "\n".join(results)

    # 如果全部失败，抛出异常以设置 isError: true
    if success_count == 0 and fail_count > 0:
        raise RuntimeError(result_message)

    if success_results and execution_time > 59:
        for path in success_results:
            _open_aido_link(ctx, path)

    return result_message


def main():
    """Main entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
