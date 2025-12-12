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

package = "video-speed-mcp"

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

mcp = FastMCP("VideoSpeedServer")


def _process_single_video(
    video_path: str, output_video_path: str, speed_factor: float, overwrite: bool = False
) -> str:
    """Adjust the playback speed for a single video."""
    _prepare_path(video_path, output_video_path, overwrite)

    atempo_value = speed_factor
    atempo_filters = []
    if speed_factor < 0.5:
        while atempo_value < 0.5:
            atempo_filters.append("atempo=0.5")
            atempo_value *= 2
        if atempo_value < 0.99:
            atempo_filters.append(f"atempo={atempo_value}")
    elif speed_factor > 2.0:
        while atempo_value > 2.0:
            atempo_filters.append("atempo=2.0")
            atempo_value /= 2
        if atempo_value > 1.01:
            atempo_filters.append(f"atempo={atempo_value}")
    else:
        atempo_filters.append(f"atempo={speed_factor}")

    probe = _ffprobe_probe(video_path)
    has_audio = any(s["codec_type"] == "audio" for s in probe["streams"])

    input_stream = ffmpeg.input(video_path)

    pts_factor = 1.0 / speed_factor
    video = input_stream.video.filter("setpts", f"{pts_factor}*PTS")

    if has_audio:
        audio = input_stream.audio
        for filter_str in atempo_filters:
            if filter_str == "atempo=0.5":
                tempo_val = 0.5
            elif filter_str == "atempo=2.0":
                tempo_val = 2.0
            elif filter_str.startswith("atempo="):
                tempo_val = float(filter_str.replace("atempo=", ""))
            else:
                tempo_val = speed_factor
            audio = audio.filter("atempo", tempo_val)

        output = ffmpeg.output(
            video, audio, output_video_path, vcodec="libx264", acodec="aac"
        )
    else:
        output = ffmpeg.output(video, output_video_path, vcodec="libx264")

    _ffmpeg_run(output, capture_stdout=True, capture_stderr=True)
    return output_video_path


@mcp.tool()
def change_video_speed(
    video_paths: list[str],
    output_video_paths: list[str] | None = None,
    output_dir: str | None = None,
    speed_factor: float = 1.0,
    overwrite: bool = False,
    ctx: Context = None
) -> str:
    """Change the playback speed of one or more videos while keeping audio in sync.

    Args:
        video_paths: List of input video file paths.
        output_video_paths: Optional list of output file paths (must match video_paths length). If provided, output_dir is ignored.
        output_dir: Directory where the processed videos are stored. Ignored if output_video_paths is provided.
        speed_factor: Playback multiplier (>0; e.g., 2.0 for double speed, 0.5 for half speed).
        overwrite: Whether to overwrite existing output files (default: False).

    Returns:
        A status message indicating success or failure.
    """
    if speed_factor <= 0:
        raise RuntimeError("Error: Speed factor must be positive.")

    if not video_paths:
        raise RuntimeError("Error: No video files provided.")

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
    errors = []

    for idx, video_path in enumerate(video_paths):
        try:
            # 优先使用 output_video_paths，否则生成输出文件路径
            if output_video_paths is not None:
                output_video_path = output_video_paths[idx]
            else:
                # 生成输出文件路径（带时间戳避免冲突）
                filename = os.path.basename(video_path)
                name, ext = os.path.splitext(filename)
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                output_filename = f"{name}_speed_{speed_factor}x_{timestamp}{ext}"
                output_video_path = os.path.join(output_dir, output_filename)

            output_path = _process_single_video(video_path, output_video_path, speed_factor, overwrite)
            results.append(output_path)
            logger.info(f"Successfully processed: {video_path} -> {output_path}")
        except ffmpeg.Error as e:
            error_message = e.stderr.decode("utf8") if e.stderr else str(e)
            errors.append(f"{video_path}: {error_message}")
            logger.error(f"Error processing {video_path}: {error_message}")
        except Exception as e:
            errors.append(f"{video_path}: {str(e)}")
            logger.error(f"Error processing {video_path}: {str(e)}")

    # 构建返回消息
    message_parts = []
    if results:
        message_parts.append(f"Successfully processed {len(results)} video(s) with speed factor {speed_factor}x:")
        for path in results:
            message_parts.append(f"  - {path}")

    if errors:
        message_parts.append(f"\nFailed to process {len(errors)} video(s):")
        for error in errors:
            message_parts.append(f"  - {error}")

    execution_time = time.time() - execution_start_time
    summary_line = f"\nTotal execution time: {execution_time:.2f} seconds."
    result_message = "\n".join(message_parts) + summary_line

    # 如果全部失败，抛出异常以设置 isError: true
    if not results and errors:
        raise RuntimeError(result_message)

    if results and execution_time > 59:
        for path in results:
            _open_aido_link(ctx, path)

    return result_message


def main():
    """Main entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
