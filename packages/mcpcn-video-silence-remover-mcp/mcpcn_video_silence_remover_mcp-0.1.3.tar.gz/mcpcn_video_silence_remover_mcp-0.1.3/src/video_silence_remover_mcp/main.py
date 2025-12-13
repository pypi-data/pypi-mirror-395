from mcp.server.fastmcp import FastMCP, Context
import ffmpeg
import os
import re
import tempfile
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import urllib.parse
import platform
import subprocess
import time

# 配置日志输出到stderr，避免干扰MCP通信
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

package = "video-silence-remover-mcp"

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

# 支持自定义 FFmpeg 路径
FFMPEG_BINARY = os.environ.get("FFMPEG_BINARY", "ffmpeg")
FFPROBE_BINARY = os.environ.get("FFPROBE_BINARY", "ffprobe")


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


mcp = FastMCP("VideoSilenceRemoverServer")


def _process_single_file(
    media_path: str,
    output_media_path: str,
    silence_threshold_db: int,
    min_silence_duration_ms: int,
    padding_seconds: float,
    overwrite: bool = False,
) -> str:
    """Remove silence from a single media file."""
    _prepare_path(media_path, output_media_path, overwrite)
    if min_silence_duration_ms <= 0:
        raise RuntimeError("Error: Minimum silence duration must be positive.")

    min_silence_duration_s = min_silence_duration_ms / 1000.0

    try:
        # 获取媒体信息
        probe = _ffprobe_probe(media_path)
        has_video = any(s["codec_type"] == "video" for s in probe["streams"])
        has_audio = any(s["codec_type"] == "audio" for s in probe["streams"])

        if not has_audio:
            # 如果没有音频流，直接复制
            _ffmpeg_run(
                ffmpeg.input(media_path).output(output_media_path, c="copy"),
                capture_stdout=True,
                capture_stderr=True,
            )
            return (
                f"No audio stream found. Original media copied to {output_media_path}."
            )

        # 使用 silenceremove 滤镜直接移除静音，这比手动切割更可靠
        input_stream = ffmpeg.input(media_path)

        # 构建滤镜链
        if has_video and has_audio:
            # 对音频应用 silenceremove 滤镜
            audio_filtered = input_stream.audio.filter(
                "silenceremove",
                start_periods=1,
                start_duration=min_silence_duration_s,
                start_threshold=f"{silence_threshold_db}dB",
                detection="peak",
                stop_periods=-1,
                stop_duration=min_silence_duration_s,
                stop_threshold=f"{silence_threshold_db}dB",
            )

            # 视频需要与音频同步，使用 aselect 和 select 滤镜
            # 先检测静音片段
            silence_detection_process = (
                ffmpeg.input(media_path)
                .filter(
                    "silencedetect",
                    n=f"{silence_threshold_db}dB",
                    d=min_silence_duration_s,
                )
                .output("-", format="null")
                .run_async(pipe_stderr=True, cmd=FFMPEG_BINARY)
            )
            _, stderr_bytes = silence_detection_process.communicate()
            stderr_str = stderr_bytes.decode("utf8")

            # 解析静音时间点
            silence_starts = [
                float(x) for x in re.findall(r"silence_start: (\d+\.?\d*)", stderr_str)
            ]
            silence_ends = [
                float(x) for x in re.findall(r"silence_end: (\d+\.?\d*)", stderr_str)
            ]

            if not silence_starts:
                # 没有检测到静音，直接复制
                _ffmpeg_run(
                    ffmpeg.input(media_path).output(output_media_path, c="copy"),
                    capture_stdout=True,
                    capture_stderr=True,
                )
                return f"No significant silences detected. Original media copied to {output_media_path}."

            # 计算需要保留的时间段
            total_duration = float(probe["format"]["duration"])
            keep_segments = []
            current_pos = 0.0

            # 确保 silence_ends 和 silence_starts 数量匹配
            for i in range(len(silence_starts)):
                silence_start = silence_starts[i]
                silence_end = (
                    silence_ends[i] if i < len(silence_ends) else total_duration
                )

                # 添加静音前的片段，并在前后添加缓冲时间
                if silence_start > current_pos:
                    # 计算带缓冲的片段边界
                    segment_start = max(0.0, current_pos - padding_seconds)
                    segment_end = min(total_duration, silence_start + padding_seconds)

                    # 确保片段有效且不与之前的片段重叠
                    if segment_end > segment_start and (
                        not keep_segments or segment_start >= keep_segments[-1][1]
                    ):
                        keep_segments.append((segment_start, segment_end))
                    elif keep_segments and segment_start < keep_segments[-1][1]:
                        # 如果有重叠，扩展上一个片段的结束时间
                        keep_segments[-1] = (keep_segments[-1][0], segment_end)

                current_pos = silence_end

            # 添加最后一个片段，并添加缓冲时间
            if current_pos < total_duration:
                segment_start = max(0.0, current_pos - padding_seconds)
                segment_end = total_duration

                # 确保片段有效且不与之前的片段重叠
                if segment_end > segment_start and (
                    not keep_segments or segment_start >= keep_segments[-1][1]
                ):
                    keep_segments.append((segment_start, segment_end))
                elif keep_segments and segment_start < keep_segments[-1][1]:
                    # 如果有重叠，扩展上一个片段的结束时间
                    keep_segments[-1] = (keep_segments[-1][0], segment_end)

            if not keep_segments:
                raise RuntimeError(
                    "Error: No audio segments to keep. The media might be entirely silent."
                )

            # 使用 concat 滤镜来连接片段，这样可以确保时长一致
            video_inputs = []
            audio_inputs = []

            for start, end in keep_segments:
                duration = end - start
                if duration > 0.1:  # 只保留大于0.1秒的片段
                    segment_input = ffmpeg.input(media_path, ss=start, t=duration)
                    video_inputs.append(segment_input["v"])
                    audio_inputs.append(segment_input["a"])

            if not video_inputs:
                raise RuntimeError("Error: No valid segments to concatenate.")

            # 连接所有片段
            if len(video_inputs) == 1:
                # 只有一个片段，直接输出
                video_output = video_inputs[0]
                audio_output = audio_inputs[0]
            else:
                # 多个片段，使用 concat 滤镜
                video_output = ffmpeg.filter(
                    video_inputs, "concat", n=len(video_inputs), v=1, a=0
                )
                audio_output = ffmpeg.filter(
                    audio_inputs, "concat", n=len(audio_inputs), v=0, a=1
                )

            # 输出设置
            output_kwargs = {
                "vcodec": "libx264",
                "acodec": "aac",
                "preset": "medium",
                "crf": "23",
            }

            _ffmpeg_run(
                ffmpeg.output(
                    video_output, audio_output, output_media_path, **output_kwargs
                ),
                capture_stdout=True,
                capture_stderr=True,
            )

        elif has_audio:
            # 只有音频的情况
            audio_filtered = input_stream.filter(
                "silenceremove",
                start_periods=1,
                start_duration=min_silence_duration_s,
                start_threshold=f"{silence_threshold_db}dB",
                detection="peak",
                stop_periods=-1,
                stop_duration=min_silence_duration_s,
                stop_threshold=f"{silence_threshold_db}dB",
            )

            _ffmpeg_run(
                ffmpeg.output(audio_filtered, output_media_path, acodec="aac"),
                capture_stdout=True,
                capture_stderr=True,
            )
        else:
            raise RuntimeError(
                "Error: No audio or video streams found in the input file."
            )

        return f"Silent segments removed. Output saved to {output_media_path}"

    except ffmpeg.Error as e:
        error_message = e.stderr.decode("utf8") if e.stderr else str(e)
        raise RuntimeError(f"Error removing silence: {error_message}")
    except Exception as e:
        raise RuntimeError(
            f"An unexpected error occurred while removing silence: {str(e)}"
        )


def _generate_output_path(input_path: str, output_dir: str | None = None) -> str:
    """Generate an output path derived from the input file name."""
    input_file = Path(input_path)
    base_name = input_file.stem
    extension = input_file.suffix

    if output_dir:
        output_directory = Path(output_dir)
    else:
        output_directory = input_file.parent

    # 使用时间戳避免文件名冲突
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_directory / f"{base_name}_no_silence_{timestamp}{extension}"

    return str(output_path)


@mcp.tool()
def remove_silence(
    media_paths: list[str],
    output_media_paths: list[str] | None = None,
    output_dir: str | None = None,
    silence_threshold_db: int = -30,
    min_silence_duration_ms: int = 500,
    padding_seconds: float = 0.2,
    overwrite: bool = False,
    ctx: Context = None
) -> str:
    """Remove silent segments from audio or video files.

    Args:
        media_paths: List of media file paths (audio or video).
        output_media_paths: Optional list of output file paths (must match media_paths length). If provided, output_dir is ignored.
        output_dir: Optional destination directory; defaults to the source directory. Ignored if output_media_paths is provided.
        silence_threshold_db: Silence threshold in dBFS (default -30).
        min_silence_duration_ms: Minimum silence duration in milliseconds to remove (default 500).
        padding_seconds: Extra seconds to keep before and after each retained segment (default 0.2).
        overwrite: Whether to overwrite existing output files (default: False).

    Returns:
        A summary of the processing results.
    """
    execution_start_time = time.time()
    # 兼容整数或字符串形式的参数，统一转换为数值类型
    try:
        silence_threshold_db = int(silence_threshold_db)
    except (TypeError, ValueError):
        raise RuntimeError("Error: silence_threshold_db must be an integer value.")
    try:
        min_silence_duration_ms = int(min_silence_duration_ms)
    except (TypeError, ValueError):
        raise RuntimeError("Error: min_silence_duration_ms must be an integer value.")

    if not media_paths:
        raise RuntimeError("Error: media_paths cannot be empty.")

    # 验证 output_media_paths 参数
    if output_media_paths is not None:
        if len(output_media_paths) != len(media_paths):
            raise RuntimeError(f"Error: output_media_paths length ({len(output_media_paths)}) must match media_paths length ({len(media_paths)})")

    # 确保输出目录存在
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    results = []
    success_results = []
    success_count = 0
    fail_count = 0

    for idx, media_path in enumerate(media_paths):
        try:
            if output_media_paths is not None:
                output_path = output_media_paths[idx]
            else:
                output_path = _generate_output_path(media_path, output_dir)
            result = _process_single_file(
                media_path,
                output_path,
                silence_threshold_db,
                min_silence_duration_ms,
                padding_seconds,
                overwrite,
            )
            results.append(f"✓ {media_path} -> {output_path}")
            success_results.append(output_path)
            success_count += 1
        except Exception as e:
            results.append(f"✗ {media_path}: {str(e)}")
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
