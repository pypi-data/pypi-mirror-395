from mcp.server.fastmcp import FastMCP, Context
import ffmpeg
import os
import re
import logging
from logging.handlers import RotatingFileHandler
import tempfile
import subprocess
import threading
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

package = "video-trim-mcp"

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


def _ffmpeg_run_with_progress(stream_spec, operation_name: str = "Processing", ctx: Context = None, **kwargs):
    """Run ffmpeg with progress notifications to prevent timeout."""
    if 'overwrite_output' not in kwargs:
        kwargs['overwrite_output'] = True

    process = _ffmpeg_run_async(stream_spec, pipe_stderr=True, **kwargs)

    def monitor_progress():
        if ctx:
            progress = 0
            while process.poll() is None:
                ctx.report_progress(progress, f"{operation_name}... {progress}%")
                time.sleep(2)
                progress = min(progress + 10, 90)

            if process.returncode == 0:
                ctx.report_progress(100, f"{operation_name} completed successfully")
            else:
                ctx.report_progress(100, f"{operation_name} failed")

    if ctx:
        monitor_thread = threading.Thread(target=monitor_progress, daemon=True)
        monitor_thread.start()

    stdout, stderr = process.communicate()

    if process.returncode != 0:
        error_message = stderr.decode("utf8") if stderr else "Unknown error"
        raise ffmpeg.Error("ffmpeg", stdout, stderr)

    return process


def _prepare_path(input_path: str, output_path: str, overwrite: bool = False) -> None:
    """Prepare and validate input/output paths."""
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


mcp = FastMCP("VideoTrim")


def _generate_output_path(input_path: str, suffix: str) -> str:
    """Generate output path with timestamp to avoid conflicts.
    
    Args:
        input_path: Input file path
        suffix: Suffix to add before timestamp (e.g., '_trim')
        
    Returns:
        Generated output path with timestamp
    """
    directory = os.path.dirname(input_path)
    name, ext = os.path.splitext(os.path.basename(input_path))
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    return os.path.join(directory, f"{name}{suffix}_{timestamp}{ext}")


@mcp.tool()
def trim_video(
    video_path: str,
    start_time: str,
    end_time: str,
    output_video_path: str | None = None,
    ctx: Context = None,
) -> str:
    """Trim a video clip according to the provided time range.

    Args:
        video_path: Path to the input video file.
        start_time: Start timestamp ('HH:MM:SS' or seconds).
        end_time: End timestamp ('HH:MM:SS' or seconds).
        output_video_path: Path for the trimmed output file (optional, auto-generated with timestamp if not provided).

    Returns:
        A status message indicating success or failure.
    """
    execution_start_time = time.time()
    if output_video_path is None:
        output_video_path = _generate_output_path(video_path, "_trim")
    _prepare_path(video_path, output_video_path)

    # 简单时间格式校验
    for time_val, name in [(start_time, "start_time"), (end_time, "end_time")]:
        if not re.match(r"^\d+(\.\d+)?$|^\d{1,2}:\d{2}:\d{2}(\.\d+)?$", str(time_val)):
            raise RuntimeError(
                f"Error: Invalid {name} format '{time_val}'. Expected 'HH:MM:SS' or seconds."
            )

    try:
        if ctx:
            ctx.report_progress(0, "Starting video trimming...")

        input_stream = ffmpeg.input(video_path, ss=start_time, to=end_time)
        # Attempt to copy codecs to avoid re-encoding if possible
        output_stream = input_stream.output(output_video_path, c="copy")
        _ffmpeg_run_with_progress(output_stream, ctx=ctx, operation_name="Video trimming")

        # 计算执行时间
        execution_time = time.time() - execution_start_time
        result_message = f"Video trimmed successfully (codec copy) to {output_video_path}. Execution time: {execution_time:.2f} seconds."

        # 只有执行时间超过1秒才调用 _open_aido_link
        if execution_time > 59:
            _open_aido_link(ctx, output_video_path)

        return result_message
    except ffmpeg.Error as e:
        error_message_copy = e.stderr.decode("utf8") if e.stderr else str(e)
        try:
            # Fallback to re-encoding if codec copy fails
            input_stream_recode = ffmpeg.input(video_path, ss=start_time, to=end_time)
            output_stream_recode = input_stream_recode.output(output_video_path)
            _ffmpeg_run_with_progress(
                output_stream_recode, ctx=ctx, operation_name="Video trimming"
            )

            # 计算执行时间
            execution_time = time.time() - execution_start_time
            result_message = f"Video trimmed successfully (re-encoded) to {output_video_path}. Execution time: {execution_time:.2f} seconds."

            # 只有执行时间超过1秒才调用 _open_aido_link
            if execution_time > 59:
                _open_aido_link(ctx, output_video_path)

            return result_message
        except ffmpeg.Error as e_recode:
            error_message_recode = (
                e_recode.stderr.decode("utf8") if e_recode.stderr else str(e_recode)
            )
            raise RuntimeError(
                f"Error trimming video. Copy attempt: {error_message_copy}. Re-encode attempt: {error_message_recode}"
            )
    except FileNotFoundError:
        raise RuntimeError(f"Error: Input video file not found at {video_path}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {str(e)}")


def main():
    """Main entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
