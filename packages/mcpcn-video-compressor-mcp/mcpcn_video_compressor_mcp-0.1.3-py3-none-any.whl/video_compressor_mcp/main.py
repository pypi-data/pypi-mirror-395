from mcp.server.fastmcp import FastMCP, Context
import ffmpeg
import os
import re
import shutil
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import tempfile
import platform
import urllib.parse
import subprocess
import time
from typing import List

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

package = "video-compressor-mcp"

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
    if "overwrite_output" not in kwargs:
        kwargs["overwrite_output"] = True
    return ffmpeg.run(stream_spec, cmd=FFMPEG_BINARY, **kwargs)


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


def _generate_output_path(input_path: str, output_dir: str, suffix: str = "_processed") -> str:
    """Create an output path based on the input file and output directory."""
    basename = os.path.basename(input_path)
    name, ext = os.path.splitext(basename)
    output_filename = f"{name}{suffix}{ext}"
    return os.path.join(output_dir, output_filename)


def _open_aido_link(ctx: Context, return_message: str) -> None:
    """Silently execute aido://tool?xxx&chatSessionId=xxx on all supported platforms."""
    try:
        # 检查 ctx 是否为 None
        if ctx is None:
            logger.debug("Context is None, skipping aido link execution")
            return

        # 尝试从 request_context 获取
        request_context = getattr(ctx, "request_context", None)
        # 尝试从 request_context.meta 获取 chatSessionId
        chatSessionId = None
        if request_context and hasattr(request_context, "meta"):
            context_meta = getattr(request_context, "meta", None)
            logger.debug(f"context meta: {context_meta}")
            if context_meta and hasattr(context_meta, "chatSessionId"):
                chatSessionId = getattr(context_meta, "chatSessionId", None)
                logger.debug(
                    f"chatSessionId from request_context.meta: {chatSessionId}"
                )

        # 验证 chatSessionId 是否有效
        if not chatSessionId or chatSessionId == "None":
            logger.warning(
                f"Invalid or missing chatSessionId: {chatSessionId}, skipping aido link execution"
            )
            return

        encoded_message = urllib.parse.quote(return_message, safe="")
        package_name = urllib.parse.quote(package, safe="")
        aido_url = f"aido://tool?path={encoded_message}&chatSessionId={chatSessionId}&package={package_name}"

        # 根据操作系统选择合适的命令
        system = platform.system().lower()
        if system == "darwin":  # macOS
            result = subprocess.run(
                ["open", aido_url], check=False, capture_output=True, text=True
            )
            if result.returncode != 0 and result.stderr:
                logger.warning(f"macOS open command failed: {result.stderr}")
        elif system == "windows":  # Windows
            # 使用 os.startfile (推荐方式) 或修正 start 命令语法
            try:
                os.startfile(aido_url)
            except (OSError, AttributeError) as e:
                # 如果 os.startfile 不可用,回退到 start 命令
                logger.debug(f"os.startfile failed, trying start command: {e}")
                # 修正 start 命令语法: start "窗口标题" "URL"
                result = subprocess.run(
                    f'start "" "{aido_url}"',
                    shell=True,
                    check=False,
                    capture_output=True,
                    text=True,
                )
                if result.returncode != 0 and result.stderr:
                    logger.warning(f"Windows start command failed: {result.stderr}")
        elif system == "linux":  # Linux
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


mcp = FastMCP("VideoCompressServer")


def _run_ffmpeg_with_fallback(
    input_path: str,
    output_path: str,
    primary_kwargs: dict,
    fallback_kwargs: dict,
    ctx: Context = None,
    execution_start_time: float = None,
) -> str:
    try:
        _ffmpeg_run(
            ffmpeg.input(input_path).output(output_path, **primary_kwargs),
            capture_stdout=True,
            capture_stderr=True,
        )
        method = "primary method"
    except ffmpeg.Error as e_primary:
        try:
            _ffmpeg_run(
                ffmpeg.input(input_path).output(output_path, **fallback_kwargs),
                capture_stdout=True,
                capture_stderr=True,
            )
            method = "fallback method"
        except ffmpeg.Error as e_fallback:
            err_primary_msg = (
                e_primary.stderr.decode("utf8") if e_primary.stderr else str(e_primary)
            )
            err_fallback_msg = (
                e_fallback.stderr.decode("utf8")
                if e_fallback.stderr
                else str(e_fallback)
            )
            raise RuntimeError(
                f"Error. Primary method failed: {err_primary_msg}. Fallback method also failed: {err_fallback_msg}"
            )
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {str(e)}")

    # 计算执行时间
    if execution_start_time:
        execution_time = time.time() - execution_start_time
        result_message = f"Operation successful ({method}) and saved to {output_path}. Execution time: {execution_time:.2f} seconds."

        # 只有执行时间超过1秒才调用 _open_aido_link
        if execution_time > 59:
            _open_aido_link(ctx, output_path)

        return result_message
    else:
        return f"Operation successful ({method}) and saved to {output_path}"


@mcp.tool()
def set_video_bitrate(
    input_video_paths: List[str],
    output_dir: str,
    video_bitrate: str,
    ctx: Context = None,
) -> str:
    """Set the video bitrate for one or more files.

    Args:
        input_video_paths: List of input video paths.
        output_dir: Output directory.
        video_bitrate: Target bitrate (e.g., '2500k', '1M').

    Returns:
        A status message indicating success or failure.
    """
    execution_start_time = time.time()

    # 校验码率格式
    if not re.match(r"^\d+[kKmM]?$", video_bitrate):
        raise RuntimeError(
            f"Error: Invalid video_bitrate format '{video_bitrate}'. Expected format like '2500k', '1M', or '1000'."
        )

    results = []
    output_paths = []

    for input_video_path in input_video_paths:
        output_video_path = _generate_output_path(input_video_path, output_dir, "_bitrate")
        _prepare_path(input_video_path, output_video_path)

        primary_kwargs = {"video_bitrate": video_bitrate, "acodec": "copy"}
        fallback_kwargs = {"video_bitrate": video_bitrate}

        result = _run_ffmpeg_with_fallback(
            input_video_path,
            output_video_path,
            primary_kwargs,
            fallback_kwargs,
        )
        results.append(result)
        output_paths.append(output_video_path)

    # 计算总执行时间
    execution_time = time.time() - execution_start_time

    # 只有执行时间超过1秒才调用 _open_aido_link（使用第一个输出路径）
    if execution_time > 59 and output_paths:
        _open_aido_link(ctx, output_paths[0])

    return f"Processed {len(input_video_paths)} video(s). Total execution time: {execution_time:.2f} seconds. Output files: {', '.join(output_paths)}"


@mcp.tool()
def set_video_resolution(
    input_video_paths: List[str], output_dir: str, resolution: str, ctx: Context = None
) -> str:
    """Change the resolution of one or more videos.

    Args:
        input_video_paths: List of input video paths.
        output_dir: Output directory.
        resolution: Target resolution such as '1920x1080' or a height like '720'.

    Returns:
        A status message indicating success or failure.
    """
    execution_start_time = time.time()

    # 校验分辨率格式
    if "x" in resolution:
        if not re.match(r"^\d{2,5}x\d{2,5}$", resolution):
            raise RuntimeError(
                f"Error: Invalid resolution format '{resolution}'. Expected format like '1920x1080'."
            )
    else:
        if not re.match(r"^\d{2,5}$", resolution):
            raise RuntimeError(
                f"Error: Invalid resolution format '{resolution}'. Expected height like '720'."
            )

    vf_filters = []
    if "x" in resolution:
        vf_filters.append(f"scale={resolution}")
    else:
        vf_filters.append(f"scale=-2:{resolution}")
    vf_filter_str = ",".join(vf_filters)

    results = []
    output_paths = []

    for input_video_path in input_video_paths:
        output_video_path = _generate_output_path(input_video_path, output_dir, "_resolution")
        _prepare_path(input_video_path, output_video_path)

        primary_kwargs = {"vf": vf_filter_str, "acodec": "copy"}
        fallback_kwargs = {"vf": vf_filter_str}

        result = _run_ffmpeg_with_fallback(
            input_video_path,
            output_video_path,
            primary_kwargs,
            fallback_kwargs,
        )
        results.append(result)
        output_paths.append(output_video_path)

    # 计算总执行时间
    execution_time = time.time() - execution_start_time

    # 只有执行时间超过1秒才调用 _open_aido_link（使用第一个输出路径）
    if execution_time > 59 and output_paths:
        _open_aido_link(ctx, output_paths[0])

    return f"Processed {len(input_video_paths)} video(s). Total execution time: {execution_time:.2f} seconds. Output files: {', '.join(output_paths)}"


@mcp.tool()
def set_video_frame_rate(
    input_video_paths: List[str], output_dir: str, frame_rate: int, ctx: Context = None
) -> str:
    """Adjust the frame rate for one or more videos.

    Args:
        input_video_paths: List of input video paths.
        output_dir: Output directory.
        frame_rate: Target frames per second (e.g., 24, 30, 60).

    Returns:
        A status message indicating success or failure.
    """
    execution_start_time = time.time()

    # 校验帧率范围
    if frame_rate <= 0 or frame_rate > 240:
        raise RuntimeError(
            f"Error: Invalid frame_rate '{frame_rate}'. Expected range: 1-240 fps."
        )

    results = []
    output_paths = []

    for input_video_path in input_video_paths:
        output_video_path = _generate_output_path(input_video_path, output_dir, "_framerate")
        _prepare_path(input_video_path, output_video_path)

        primary_kwargs = {"r": frame_rate, "acodec": "copy"}
        fallback_kwargs = {"r": frame_rate}

        result = _run_ffmpeg_with_fallback(
            input_video_path,
            output_video_path,
            primary_kwargs,
            fallback_kwargs,
        )
        results.append(result)
        output_paths.append(output_video_path)

    # 计算总执行时间
    execution_time = time.time() - execution_start_time

    # 只有执行时间超过1秒才调用 _open_aido_link（使用第一个输出路径）
    if execution_time > 59 and output_paths:
        for  path in output_paths:
            _open_aido_link(ctx, path)

    return f"Processed {len(input_video_paths)} video(s). Total execution time: {execution_time:.2f} seconds. Output files: {', '.join(output_paths)}"


def main():
    """Main entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
