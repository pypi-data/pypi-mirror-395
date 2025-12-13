"""
Video Format Converter MCP Server

Core server implementation for video format conversion.
"""

from mcp.server.fastmcp import FastMCP, Context
import ffmpeg
import os
import re
import subprocess
import platform
import urllib.parse
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import tempfile
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

PACKAGE_NAME = "mcpcn-video-format-converter"

# 使用用户临时目录存放日志文件
log_dir = Path(tempfile.gettempdir()) / PACKAGE_NAME
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "debug.log"

file_handler = RotatingFileHandler(str(log_file), maxBytes=5_000_000, backupCount=3, encoding="utf-8")
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)
logger.propagate = False

# FFmpeg 二进制路径配置
FFMPEG_BINARY = os.environ.get('FFMPEG_BINARY')
FFPROBE_BINARY = os.environ.get('FFPROBE_BINARY')


def _ffmpeg_run(stream_spec, **kwargs):
    """Run ffmpeg with an explicit binary path to avoid env propagation issues."""
    if FFMPEG_BINARY:
        return ffmpeg.run(stream_spec, cmd=FFMPEG_BINARY, **kwargs)
    else:
        return ffmpeg.run(stream_spec, **kwargs)


def _ffprobe_probe(path: str, **kwargs):
    """Probe media with explicit ffprobe binary."""
    if FFPROBE_BINARY:
        return ffmpeg.probe(path, cmd=FFPROBE_BINARY, **kwargs)
    else:
        return ffmpeg.probe(path, **kwargs)


def _prepare_path(input_path: str, output_path: str, overwrite: bool = False) -> None:
    """Validate the input path and prepare the destination directory."""
    if not os.path.exists(input_path):
        raise RuntimeError(f"Error: Input file not found at {input_path}")
    try:
        parent_dir = os.path.dirname(output_path)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)
    except Exception as e:
        raise RuntimeError(f"Error creating output directory for {output_path}: {str(e)}")
    if os.path.exists(output_path) and not overwrite:
        raise RuntimeError(
            f"Error: Output file already exists at {output_path}. Please choose a different path, delete the existing file, or set overwrite=True.")


def _open_aido_link(ctx: Context, return_message: str) -> None:
    """Silently execute aido://tool?xxx&chatSessionId=xxx across platforms."""
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
        package_name = urllib.parse.quote(PACKAGE_NAME, safe='')
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


def _get_container_defaults(fmt: str) -> tuple[str | None, str | None, dict]:
    """Return default codec settings for a given container format."""
    fmt_l = (fmt or '').lower()
    extra: dict = {}
    v, a = None, None

    if fmt_l in {'mp4', 'm4v'}:
        v, a = 'libx264', 'aac'
        extra.update({'pix_fmt': 'yuv420p', 'movflags': '+faststart'})
    elif fmt_l in {'mov'}:
        v, a = 'libx264', 'aac'
        extra.update({'pix_fmt': 'yuv420p'})
    elif fmt_l in {'webm'}:
        v, a = 'libvpx-vp9', 'libopus'
        extra.update({'pix_fmt': 'yuv420p'})
    elif fmt_l in {'mkv'}:
        v, a = 'libx264', 'aac'
        extra.update({'pix_fmt': 'yuv420p'})
    elif fmt_l in {'avi'}:
        v, a = 'mpeg4', 'mp3'
    elif fmt_l in {'wmv'}:
        v, a = 'wmv2', 'wmav2'

    return v, a, extra


# 创建 MCP 服务器实例
mcp = FastMCP("VideoFormatConverter")


def _convert_single_video(
    input_video_path: str,
    output_video_path: str,
    target_format: str,
    resolution: str,
    video_codec: str,
    video_bitrate: str,
    frame_rate: int,
    audio_codec: str,
    audio_bitrate: str,
    audio_sample_rate: int,
    audio_channels: int,
    overwrite: bool,
    ctx: Context
) -> str:
    """Internal helper that converts a single video file."""
    start_time = time.time()

    _prepare_path(input_video_path, output_video_path, overwrite)

    try:
        # 后缀与目标容器不一致时给出提示
        out_ext = os.path.splitext(output_video_path)[1].lstrip('.').lower() if os.path.splitext(output_video_path)[1] else ''
        if out_ext and out_ext != target_format.lower():
            logger.warning(
                f"Output file extension '.{out_ext}' does not match target_format '{target_format}'. This may be confusing.")

        # 分辨率参数校验
        if resolution and resolution.lower() != 'preserve':
            if 'x' in resolution:
                if not re.match(r'^\d{2,5}x\d{2,5}$', resolution):
                    raise RuntimeError(f"Error: Invalid resolution '{resolution}'. Expected like '1920x1080'.")
            else:
                if not re.match(r'^\d{2,5}$', str(resolution)):
                    raise RuntimeError(f"Error: Invalid resolution '{resolution}'. Expected height like '720'.")

        # 纯换容器（remux）快速路径
        pure_remux = (
            (not resolution or str(resolution).lower() == 'preserve') and
            video_codec is None and video_bitrate is None and frame_rate is None and
            audio_codec is None and audio_bitrate is None and audio_sample_rate is None and audio_channels is None
        )

        stream = ffmpeg.input(input_video_path)

        if pure_remux:
            try:
                output_stream = stream.output(output_video_path, format=target_format, c='copy')
                _ffmpeg_run(output_stream, capture_stdout=True, capture_stderr=True)

                execution_time = time.time() - start_time
                return f"Remux completed: {output_video_path} ({execution_time:.2f}s)"
            except ffmpeg.Error as e_copy:
                logger.info(
                    f"Remux failed, falling back to re-encode: {e_copy.stderr.decode('utf8') if e_copy.stderr else str(e_copy)}")

        # 获取容器默认编解码器
        def_v, def_a, def_extra = _get_container_defaults(target_format)

        kwargs: dict = {}
        vf_filters = []

        # 分辨率处理
        if resolution and str(resolution).lower() != 'preserve':
            if 'x' in resolution:
                vf_filters.append(f"scale={resolution}")
            else:
                vf_filters.append(f"scale=-2:{resolution}")
        if vf_filters:
            kwargs['vf'] = ",".join(vf_filters)

        # 选择编码器
        vcodec_to_use = video_codec or def_v
        acodec_to_use = audio_codec or def_a
        if vcodec_to_use:
            kwargs['vcodec'] = vcodec_to_use
        if acodec_to_use:
            kwargs['acodec'] = acodec_to_use

        # H.264/H.265 默认 yuv420p
        if vcodec_to_use and any(x in vcodec_to_use for x in ['libx264', 'libx265', 'h264', 'hevc']):
            kwargs.setdefault('pix_fmt', 'yuv420p')

        # 按容器附加参数
        for k, v in def_extra.items():
            kwargs.setdefault(k, v)

        # 码率/帧率/音频参数
        if video_bitrate:
            kwargs['video_bitrate'] = video_bitrate
        if frame_rate:
            kwargs['r'] = frame_rate
        if audio_bitrate:
            kwargs['audio_bitrate'] = audio_bitrate
        if audio_sample_rate:
            kwargs['ar'] = audio_sample_rate
        if audio_channels:
            kwargs['ac'] = audio_channels

        kwargs['format'] = target_format

        output_stream = stream.output(output_video_path, **kwargs)
        _ffmpeg_run(output_stream, capture_stdout=True, capture_stderr=True)

        execution_time = time.time() - start_time
        return f"Converted: {output_video_path} ({execution_time:.2f}s)"

    except ffmpeg.Error as e:
        error_message = e.stderr.decode('utf8') if e.stderr else str(e)
        raise RuntimeError(f"Error converting {input_video_path}: {error_message}")
    except FileNotFoundError:
        raise RuntimeError(f"Error: Input video file not found at {input_video_path}")
    except Exception as e:
        raise RuntimeError(f"Error converting {input_video_path}: {str(e)}")


@mcp.tool()
def convert_video_format(
    input_video_paths: list[str],
    output_video_paths: list[str] | None = None,
    output_dir: str | None = None,
    target_format: str = "mp4",
    resolution: str = None,
    video_codec: str = None,
    video_bitrate: str = None,
    frame_rate: int = None,
    audio_codec: str = None,
    audio_bitrate: str = None,
    audio_sample_rate: int = None,
    audio_channels: int = None,
    overwrite: bool = False,
    ctx: Context = None
) -> str:
    """Batch-convert videos to new containers and optionally adjust encoding parameters.

    Args:
        input_video_paths: List of input video paths (batch conversion supported).
        output_video_paths: Optional list of output file paths (must match input_video_paths length). If provided, output_dir and target_format are ignored.
        output_dir: Destination directory; outputs keep the original filename but use the target format extension. Ignored if output_video_paths is provided.
        target_format: Target container (e.g., 'mp4', 'mov', 'mkv', 'webm', 'm4v', 'avi'). Ignored if output_video_paths is provided.
        resolution: Desired resolution, e.g., '1920x1080', or a height such as '720'. Use 'preserve'/None to keep the original.
        video_codec: Video codec (e.g., 'libx264', 'libx265', 'vp9', 'libvpx-vp9', 'wmv2'). Defaults to container preference/original.
        video_bitrate: Video bitrate (e.g., '2500k', '1M'). Defaults to encoder settings.
        frame_rate: Target frame rate (integer such as 24/30/60). Defaults to the original.
        audio_codec: Audio codec (e.g., 'aac', 'libopus', 'libvorbis', 'mp3', 'wmav2'). Defaults to container/original.
        audio_bitrate: Audio bitrate (e.g., '128k', '192k'). Defaults to encoder settings.
        audio_sample_rate: Audio sample rate in Hz (e.g., 44100/48000). Defaults to the original.
        audio_channels: Number of audio channels (1=mono, 2=stereo). Defaults to the original.
        overwrite: Whether to overwrite existing output files (default: False).

    Returns:
        A status message indicating success or failure for each video.
    """
    total_start_time = time.time()

    if not input_video_paths:
        raise RuntimeError("Error: input_video_paths cannot be empty")

    # 验证 output_video_paths 参数
    if output_video_paths is not None:
        if len(output_video_paths) != len(input_video_paths):
            raise RuntimeError(f"Error: output_video_paths length ({len(output_video_paths)}) must match input_video_paths length ({len(input_video_paths)})")
    elif output_dir is None:
        raise RuntimeError("Error: Either output_video_paths or output_dir must be provided")

    # 确保输出目录存在
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    results = []
    success_count = 0
    fail_count = 0
    output_paths = []

    for idx, input_path in enumerate(input_video_paths):
        # 优先使用 output_video_paths，否则生成输出文件路径
        if output_video_paths is not None:
            output_path = output_video_paths[idx]
        else:
            # 生成输出文件路径（带时间戳避免冲突）
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(output_dir, f"{base_name}_{timestamp}.{target_format}")

        try:
            result = _convert_single_video(
                input_video_path=input_path,
                output_video_path=output_path,
                target_format=target_format,
                resolution=resolution,
                video_codec=video_codec,
                video_bitrate=video_bitrate,
                frame_rate=frame_rate,
                audio_codec=audio_codec,
                audio_bitrate=audio_bitrate,
                audio_sample_rate=audio_sample_rate,
                audio_channels=audio_channels,
                overwrite=overwrite,
                ctx=ctx
            )
            results.append(f"✓ {result}")
            success_count += 1
            output_paths.append(output_path)
        except Exception as e:
            results.append(f"✗ Failed: {os.path.basename(input_path)} - {str(e)}")
            fail_count += 1

    total_time = time.time() - total_start_time

    # 构建结果消息
    summary = f"\n\nBatch conversion completed: {success_count} succeeded, {fail_count} failed. Total time: {total_time:.2f}s"
    result_message = "\n".join(results) + summary

    # 如果全部失败，抛出异常以设置 isError: true
    if success_count == 0 and fail_count > 0:
        raise RuntimeError(result_message)

    # 如果有成功转换的文件，调用 aido link（使用输出目录）
    if success_count > 0 and total_time > 59:
        for path in output_paths:
            _open_aido_link(ctx, path)

    return result_message


def main():
    """Main entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
