from mcp.server.fastmcp import FastMCP, Context
import ffmpeg
import os
import tempfile
import shutil
import subprocess
import logging
import urllib.parse
import platform
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path

# 配置日志输出到stderr，避免干扰MCP通信
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

package = "video-cover-mcp"

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


def _get_media_properties(media_path: str) -> dict:
    try:
        probe = _ffprobe_probe(media_path)
        video_stream_info = next(
            (s for s in probe["streams"] if s["codec_type"] == "video"), None
        )
        audio_stream_info = next(
            (s for s in probe["streams"] if s["codec_type"] == "audio"), None
        )

        props = {
            "duration": float(probe["format"].get("duration", 0.0)),
            "has_video": video_stream_info is not None,
            "has_audio": audio_stream_info is not None,
            "width": int(video_stream_info["width"])
            if video_stream_info and "width" in video_stream_info
            else 0,
            "height": int(video_stream_info["height"])
            if video_stream_info and "height" in video_stream_info
            else 0,
            "avg_fps": 0,
            "sample_rate": int(audio_stream_info["sample_rate"])
            if audio_stream_info and "sample_rate" in audio_stream_info
            else 44100,
            "channels": int(audio_stream_info["channels"])
            if audio_stream_info and "channels" in audio_stream_info
            else 2,
        }
        if (
            video_stream_info
            and "avg_frame_rate" in video_stream_info
            and video_stream_info["avg_frame_rate"] != "0/0"
        ):
            num, den = map(int, video_stream_info["avg_frame_rate"].split("/"))
            if den > 0:
                props["avg_fps"] = num / den
            else:
                props["avg_fps"] = 30
        else:
            props["avg_fps"] = 30
        return props
    except ffmpeg.Error as e:
        raise RuntimeError(
            f"Error probing file {media_path}: {e.stderr.decode('utf8') if e.stderr else str(e)}"
        )
    except Exception as e:
        raise RuntimeError(f"Unexpected error probing file {media_path}: {str(e)}")


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

mcp = FastMCP("VideoCoverServer")


def _generate_output_path(input_path: str, suffix: str) -> str:
    """Generate output path with timestamp to avoid conflicts.
    
    Args:
        input_path: Input file path
        suffix: Suffix to add before timestamp (e.g., '_cover', '_transition')
        
    Returns:
        Generated output path with timestamp
    """
    directory = os.path.dirname(input_path)
    name, ext = os.path.splitext(os.path.basename(input_path))
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    return os.path.join(directory, f"{name}{suffix}_{timestamp}{ext}")


@mcp.tool()
def add_cover_image(
    video_path: str,
    cover_image_path: str,
    output_video_path: str | None = None,
    cover_duration: float = 3.0,
    fade_duration: float = 0.5,
    ctx: Context = None,
) -> str:
    """Add a cover image to the beginning of a video (used as the opening frame).

    Args:
        video_path: Input video file path.
        cover_image_path: Cover image path (PNG, JPG, etc.).
        output_video_path: Output video path (optional, auto-generated with timestamp if not provided).
        cover_duration: Duration to display the cover image in seconds (default 3.0).
        fade_duration: Fade transition duration in seconds (default 0.5).

    Returns:
        A status message indicating success or failure.
    """
    if output_video_path is None:
        output_video_path = _generate_output_path(video_path, "_cover")
    _prepare_path(video_path, output_video_path)
    execution_start_time = time.time()

    if not os.path.exists(cover_image_path):
        raise RuntimeError(f"Error: Cover image file not found at {cover_image_path}")

    if cover_duration <= 0:
        raise RuntimeError("Error: Cover duration must be positive.")
    if fade_duration < 0:
        raise RuntimeError("Error: Fade duration cannot be negative.")
    if fade_duration > cover_duration:
        raise RuntimeError("Error: Fade duration cannot exceed cover duration.")

    temp_dir = tempfile.mkdtemp()
    try:
        # 获取视频属性
        props = _get_media_properties(video_path)
        if not props["has_video"]:
            raise RuntimeError("Error: Input file has no video stream.")

        video_width = props["width"]
        video_height = props["height"]
        video_fps = props["avg_fps"] if props["avg_fps"] > 0 else 30
        sample_rate = props["sample_rate"]
        channels = props["channels"]

        # 创建封面视频片段（从图片生成）
        cover_video_path = os.path.join(temp_dir, "cover.mp4")

        # 使用 FFmpeg 将图片转换为视频，并添加淡出效果
        fade_out_start = cover_duration - fade_duration

        try:
            # 生成封面视频：缩放图片到视频尺寸，添加淡出效果，生成静音音轨
            cmd = [
                FFMPEG_BINARY,
                "-loop", "1",
                "-i", cover_image_path,
                "-f", "lavfi",
                "-i", f"anullsrc=channel_layout=stereo:sample_rate={sample_rate}",
                "-vf", f"scale={video_width}:{video_height}:force_original_aspect_ratio=decrease,pad={video_width}:{video_height}:(ow-iw)/2:(oh-ih)/2,fade=t=out:st={fade_out_start}:d={fade_duration}",
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-c:a", "aac",
                "-t", str(cover_duration),
                "-r", str(video_fps),
                "-y",
                cover_video_path
            ]
            subprocess.run(cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Error creating cover video: {e.stderr.decode('utf8') if e.stderr else str(e)}"
            )

        # 标准化主视频（确保格式一致）
        normalized_video_path = os.path.join(temp_dir, "normalized.mp4")
        try:
            # 为主视频添加淡入效果
            cmd = [
                FFMPEG_BINARY,
                "-i", video_path,
                "-vf", f"fade=t=in:st=0:d={fade_duration}",
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-c:a", "aac",
                "-r", str(video_fps),
                "-y",
                normalized_video_path
            ]
            subprocess.run(cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Error normalizing video: {e.stderr.decode('utf8') if e.stderr else str(e)}"
            )

        # 创建 concat 文件列表
        concat_list_path = os.path.join(temp_dir, "concat_list.txt")
        with open(concat_list_path, "w") as f:
            f.write(f"file '{cover_video_path}'\n")
            f.write(f"file '{normalized_video_path}'\n")

        # 拼接封面和主视频
        try:
            cmd = [
                FFMPEG_BINARY,
                "-f", "concat",
                "-safe", "0",
                "-i", concat_list_path,
                "-c", "copy",
                "-y",
                output_video_path
            ]
            subprocess.run(cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Error concatenating videos: {e.stderr.decode('utf8') if e.stderr else str(e)}"
            )

        success_result = f"Cover image added successfully. Output saved to {output_video_path}"
        
        execution_time = time.time() - execution_start_time
        summary = f"\nProcessing finished: 1 succeeded, 0 failed\n"
        summary += f"Total execution time: {execution_time:.2f} seconds.\n"
        result_message = summary + "\n" + success_result
        if execution_time > 59:
            _open_aido_link(ctx, output_video_path)
        return result_message

    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {str(e)}")
    finally:
        shutil.rmtree(temp_dir)


@mcp.tool()
def add_basic_transitions(
    video_path: str,
    output_video_path: str | None = None,
    transition_type: str = "fade_in",
    duration_seconds: float = 1.0,
    ctx: Context = None,
) -> str:
    """Apply a fade-in or fade-out effect to the entire video.

    Args:
        video_path: Input video file path.
        output_video_path: Output video file path (optional, auto-generated with timestamp if not provided).
        transition_type: Either 'fade_in' or 'fade_out'.
        duration_seconds: Transition duration in seconds (>0).

    Returns:
        A status message indicating success or failure.
    """
    if output_video_path is None:
        output_video_path = _generate_output_path(video_path, "_transition")
    _prepare_path(video_path, output_video_path)
    execution_start_time = time.time()
    if duration_seconds <= 0:
        raise RuntimeError("Error: Transition duration must be positive.")
    try:
        props = _get_media_properties(video_path)
        video_total_duration = props["duration"]
        if duration_seconds > video_total_duration:
            raise RuntimeError(
                f"Error: Transition duration ({duration_seconds}s) cannot exceed video duration ({video_total_duration}s)."
            )
        input_stream = ffmpeg.input(video_path)
        video_stream = input_stream.video
        audio_stream = input_stream.audio
        if transition_type == "fade_in" or transition_type == "crossfade_from_black":
            processed_video = video_stream.filter(
                "fade", type="in", start_time=0, duration=duration_seconds
            )
        elif transition_type == "fade_out" or transition_type == "crossfade_to_black":
            fade_start_time = video_total_duration - duration_seconds
            processed_video = video_stream.filter(
                "fade",
                type="out",
                start_time=fade_start_time,
                duration=duration_seconds,
            )
        else:
            raise RuntimeError(
                f"Error: Unsupported transition_type '{transition_type}'. Supported: 'fade_in', 'fade_out'."
            )

        output_streams = []
        if props["has_video"]:
            output_streams.append(processed_video)
        if props["has_audio"]:
            output_streams.append(audio_stream)
        if not output_streams:
            raise RuntimeError(
                "Error: No suitable video or audio streams found to apply transition."
            )
        try:
            output_kwargs = {"vcodec": "libx264", "pix_fmt": "yuv420p"}
            if props["has_audio"]:
                output_kwargs["acodec"] = "copy"
            _ffmpeg_run(
                ffmpeg.output(*output_streams, output_video_path, **output_kwargs),
                capture_stdout=True,
                capture_stderr=True,
            )
            success_result = f"Transition '{transition_type}' applied successfully. Output: {output_video_path}"
        except ffmpeg.Error as e_acopy:
            try:
                _ffmpeg_run(
                    ffmpeg.output(
                        *output_streams,
                        output_video_path,
                        vcodec="libx264",
                        pix_fmt="yuv420p",
                    ),
                    capture_stdout=True,
                    capture_stderr=True,
                )
                success_result = f"Transition '{transition_type}' applied successfully. Output: {output_video_path}"
            except ffmpeg.Error as e_recode:
                err_acopy = (
                    e_acopy.stderr.decode("utf8") if e_acopy.stderr else str(e_acopy)
                )
                err_recode = (
                    e_recode.stderr.decode("utf8") if e_recode.stderr else str(e_recode)
                )
                raise RuntimeError(
                    f"Error applying transition. Audio copy failed: {err_acopy}. Full re-encode failed: {err_recode}."
                )
        
        execution_time = time.time() - execution_start_time
        summary = f"\nProcessing finished: 1 succeeded, 0 failed\n"
        summary += f"Total execution time: {execution_time:.2f} seconds.\n"
        result_message = summary + "\n" + success_result
        if execution_time > 59:
            _open_aido_link(ctx, output_video_path)
        return result_message
    except ffmpeg.Error as e:
        error_message = e.stderr.decode("utf8") if e.stderr else str(e)
        raise RuntimeError(f"Error applying basic transition: {error_message}")
    except ValueError as e:
        raise RuntimeError(f"Error with input values: {str(e)}")
    except RuntimeError as e:
        raise RuntimeError(f"Runtime error during transition processing: {str(e)}")
    except Exception as e:
        raise RuntimeError(
            f"An unexpected error occurred in add_basic_transitions: {str(e)}"
        )


def main():
    """Main entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
