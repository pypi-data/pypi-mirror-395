from mcp.server.fastmcp import FastMCP, Context
import ffmpeg
import os
import logging
import tempfile
import shutil
import subprocess
import urllib.parse
import platform
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

package = "video-concatenate-mcp"

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

FFMPEG_BINARY = os.environ.get("FFMPEG_BINARY") or "ffmpeg"
FFPROBE_BINARY = os.environ.get("FFPROBE_BINARY") or "ffprobe"


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


def _get_media_properties(media_path: str) -> dict:
    """Retrieve media stream properties for a given file."""
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
            "channel_layout": audio_stream_info.get("channel_layout", "stereo")
            if audio_stream_info
            else "stereo",
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


# 支持的转场效果列表
VALID_TRANSITIONS = {
    "dissolve",
    "fade",
    "fadeblack",
    "fadewhite",
    "fadegrays",
    "distance",
    "wipeleft",
    "wiperight",
    "wipeup",
    "wipedown",
    "slideleft",
    "slideright",
    "slideup",
    "slidedown",
    "smoothleft",
    "smoothright",
    "smoothup",
    "smoothdown",
    "circlecrop",
    "rectcrop",
    "circleopen",
    "circleclose",
    "vertopen",
    "vertclose",
    "horzopen",
    "horzclose",
    "diagtl",
    "diagtr",
    "diagbl",
    "diagbr",
    "hlslice",
    "hrslice",
    "vuslice",
    "vdslice",
    "pixelize",
    "radial",
    "hblur",
}

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

mcp = FastMCP("VideoConcatenateServer")


def _generate_output_path(input_paths: list[str], suffix: str) -> str:
    """Generate output path with timestamp to avoid conflicts.
    
    Args:
        input_paths: List of input file paths (uses first one for directory and extension)
        suffix: Suffix to add before timestamp (e.g., '_concat')
        
    Returns:
        Generated output path with timestamp
    """
    first_path = input_paths[0]
    directory = os.path.dirname(first_path)
    _, ext = os.path.splitext(os.path.basename(first_path))
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    return os.path.join(directory, f"concat{suffix}_{timestamp}{ext}")


@mcp.tool()
def concatenate_videos(
    video_paths: list[str],
    output_video_path: str | None = None,
    transition_effect: str = None,
    transition_duration: float = None,
    ctx: Context = None,
) -> str:
    """Concatenate a series of videos with optional transitions between clips.

    Args:
        video_paths: List of input video paths (at least one).
        output_video_path: Output video path (optional, auto-generated with timestamp if not provided).
        transition_effect: Optional transition effect. Supported categories include:
            - Fade family: 'dissolve', 'fade', 'fadeblack', 'fadewhite', 'fadegrays'
            - Wipe family: 'wipeleft', 'wiperight', 'wipeup', 'wipedown'
            - Slide family: 'slideleft', 'slideright', 'slideup', 'slidedown'
            - Smooth family: 'smoothleft', 'smoothright', 'smoothup', 'smoothdown'
            - Circular transitions: 'circlecrop', 'circleopen', 'circleclose'
            - Rectangular transitions: 'rectcrop', 'vertopen', 'vertclose', 'horzopen', 'horzclose'
            - Diagonal transitions: 'diagtl', 'diagtr', 'diagbl', 'diagbr'
            - Slice transitions: 'hlslice', 'hrslice', 'vuslice', 'vdslice'
            - Other effects: 'distance', 'pixelize', 'radial', 'hblur'
        transition_duration: Transition length in seconds (>0). Only valid when a transition is specified and there are two videos.

    Returns:
        A status message indicating success or failure.

    Examples:
        # Simple concatenation (no transitions)
        concatenate_videos(["/path/video1.mp4", "/path/video2.mp4"], "/path/output.mp4")

        # Concatenation with a dissolve transition
        concatenate_videos(
            ["/path/video1.mp4", "/path/video2.mp4"],
            "/path/output.mp4",
            transition_effect="dissolve",
            transition_duration=1.0
        )
    """
    if not video_paths:
        raise RuntimeError("Error: No video paths provided for concatenation.")
    if len(video_paths) < 1:
        raise RuntimeError("Error: At least one video is required.")

    execution_start_time = time.time()

    # 验证所有输入文件存在
    for video_path in video_paths:
        if not os.path.exists(video_path):
            raise RuntimeError(f"Error: Input file not found at {video_path}")

    # Auto-generate output path if not provided
    if output_video_path is None:
        output_video_path = _generate_output_path(video_paths, "")

    # 验证输出路径
    try:
        parent_dir = os.path.dirname(output_video_path)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)
    except Exception as e:
        raise RuntimeError(
            f"Error creating output directory for {output_video_path}: {str(e)}"
        )
    if os.path.exists(output_video_path):
        raise RuntimeError(
            f"Error: Output file already exists at {output_video_path}. Please choose a different path or delete the existing file."
        )

    # 验证转场参数
    if transition_effect and transition_duration is None:
        raise RuntimeError(
            "Error: transition_duration is required when transition_effect is specified."
        )
    if transition_effect and transition_duration <= 0:
        raise RuntimeError("Error: transition_duration must be positive.")
    if transition_effect and transition_effect not in VALID_TRANSITIONS:
        raise RuntimeError(
            f"Error: Invalid transition_effect '{transition_effect}'. Valid options: {', '.join(sorted(VALID_TRANSITIONS))}"
        )

    # 单个视频直接处理
    if len(video_paths) == 1:
        try:
            _ffmpeg_run(
                ffmpeg.input(video_paths[0]).output(
                    output_video_path, vcodec="libx264", acodec="aac"
                ),
                capture_stdout=True,
                capture_stderr=True,
            )
            result_message = f"Single video processed and saved to {output_video_path}"
        except ffmpeg.Error as e:
            raise RuntimeError(
                f"Error processing single video: {e.stderr.decode('utf8') if e.stderr else str(e)}"
            )

    # 两个视频带转场效果
    elif transition_effect and len(video_paths) == 2:
        result_message = _concatenate_with_transition(
            video_paths[0], video_paths[1], output_video_path,
            transition_effect, transition_duration
        )

    # 多个视频简单拼接
    else:
        result_message = _concatenate_simple(video_paths, output_video_path)

    execution_time = time.time() - execution_start_time
    summary_line = f"\nTotal execution time: {execution_time:.2f} seconds."
    result_message += summary_line

    if execution_time > 59:
        _open_aido_link(ctx, output_video_path)

    return result_message


def _concatenate_with_transition(
    video1_path: str,
    video2_path: str,
    output_video_path: str,
    transition_effect: str,
    transition_duration: float,
) -> str:
    """Concatenate two videos using FFmpeg's xfade transition."""
    temp_dir = tempfile.mkdtemp()
    try:
        props1 = _get_media_properties(video1_path)
        props2 = _get_media_properties(video2_path)

        if not props1["has_video"] or not props2["has_video"]:
            raise RuntimeError(
                "Error: xfade transition requires both inputs to be videos."
            )
        if transition_duration >= props1["duration"]:
            raise RuntimeError(
                f"Error: Transition duration ({transition_duration}s) cannot be equal or longer than the first video's duration ({props1['duration']})."
            )

        has_audio = props1["has_audio"] and props2["has_audio"]
        target_w = max(props1["width"], props2["width"], 640)
        target_h = max(props1["height"], props2["height"], 360)
        target_fps = max(props1["avg_fps"], props2["avg_fps"], 30)
        if target_fps <= 0:
            target_fps = 30

        # 标准化第一个视频
        norm_video1_path = os.path.join(temp_dir, "norm_video1.mp4")
        try:
            subprocess.run(
                [
                    FFMPEG_BINARY,
                    "-i", video1_path,
                    "-vf", f"scale={target_w}:{target_h}",
                    "-r", str(target_fps),
                    "-c:v", "libx264",
                    "-pix_fmt", "yuv420p",
                    "-c:a", "aac",
                    "-y", norm_video1_path,
                ],
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Error normalizing first video: {e.stderr.decode('utf8') if e.stderr else str(e)}"
            )

        # 标准化第二个视频
        norm_video2_path = os.path.join(temp_dir, "norm_video2.mp4")
        try:
            subprocess.run(
                [
                    FFMPEG_BINARY,
                    "-i", video2_path,
                    "-vf", f"scale={target_w}:{target_h}",
                    "-r", str(target_fps),
                    "-c:v", "libx264",
                    "-pix_fmt", "yuv420p",
                    "-c:a", "aac",
                    "-y", norm_video2_path,
                ],
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Error normalizing second video: {e.stderr.decode('utf8') if e.stderr else str(e)}"
            )

        # 获取标准化后的视频时长
        norm_props1 = _get_media_properties(norm_video1_path)
        norm_video1_duration = norm_props1["duration"]
        if transition_duration >= norm_video1_duration:
            raise RuntimeError(
                f"Error: Transition duration ({transition_duration}s) is too long for the normalized first video ({norm_video1_duration}s)."
            )

        # 计算转场开始时间
        offset = norm_video1_duration - transition_duration

        # 构建 filter_complex
        filter_complex = f"[0:v][1:v]xfade=transition={transition_effect}:duration={transition_duration}:offset={offset}[v]"
        cmd = [
            FFMPEG_BINARY,
            "-i", norm_video1_path,
            "-i", norm_video2_path,
            "-filter_complex",
        ]

        if has_audio:
            filter_complex += f";[0:a][1:a]acrossfade=d={transition_duration}:c1=tri:c2=tri[a]"
            cmd.extend([filter_complex, "-map", "[v]", "-map", "[a]"])
        else:
            cmd.extend([filter_complex, "-map", "[v]"])

        cmd.extend(["-c:v", "libx264", "-c:a", "aac", "-y", output_video_path])

        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return f"Videos concatenated successfully with '{transition_effect}' transition to {output_video_path}"
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Error during xfade process: {e.stderr.decode('utf8') if e.stderr else str(e)}"
            )
    finally:
        shutil.rmtree(temp_dir)


def _concatenate_simple(video_paths: list[str], output_video_path: str) -> str:
    """Concatenate multiple videos sequentially without transitions."""
    temp_dir = tempfile.mkdtemp()
    try:
        # 获取第一个视频的属性作为目标参数
        first_props = _get_media_properties(video_paths[0])
        target_w = first_props["width"] if first_props["width"] > 0 else 1280
        target_h = first_props["height"] if first_props["height"] > 0 else 720
        target_fps = first_props["avg_fps"] if first_props["avg_fps"] > 0 else 30
        if target_fps <= 0:
            target_fps = 30

        # 标准化所有视频
        normalized_paths = []
        for i, video_path in enumerate(video_paths):
            norm_path = os.path.join(temp_dir, f"norm_{i}.mp4")
            try:
                subprocess.run(
                    [
                        FFMPEG_BINARY,
                        "-i", video_path,
                        "-vf", f"scale={target_w}:{target_h}",
                        "-r", str(target_fps),
                        "-c:v", "libx264",
                        "-pix_fmt", "yuv420p",
                        "-c:a", "aac",
                        "-y", norm_path,
                    ],
                    check=True,
                    capture_output=True,
                )
                normalized_paths.append(norm_path)
            except subprocess.CalledProcessError as e:
                raise RuntimeError(
                    f"Error normalizing video {i}: {e.stderr.decode('utf8') if e.stderr else str(e)}"
                )

        # 创建拼接列表文件
        concat_list_path = os.path.join(temp_dir, "concat_list.txt")
        with open(concat_list_path, "w") as f:
            for path in normalized_paths:
                f.write(f"file '{path}'\n")

        # 执行拼接
        try:
            subprocess.run(
                [
                    FFMPEG_BINARY,
                    "-f", "concat",
                    "-safe", "0",
                    "-i", concat_list_path,
                    "-c", "copy",
                    "-y", output_video_path,
                ],
                check=True,
                capture_output=True,
            )
            return f"Videos concatenated successfully to {output_video_path}"
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Error during concatenation: {e.stderr.decode('utf8') if e.stderr else str(e)}"
            )
    finally:
        shutil.rmtree(temp_dir)


@mcp.tool()
def list_transition_effects() -> str:
    """List every supported transition effect.

    Returns:
        A textual description of all available transitions.
    """
    effects_info = """
Supported transition effects:

[Fade family]
- dissolve: Dissolve transition (recommended)
- fade: Basic fade
- fadeblack: Fade to black
- fadewhite: Fade to white
- fadegrays: Fade to grayscale

[Wipe family]
- wipeleft: Wipe from right to left
- wiperight: Wipe from left to right
- wipeup: Wipe from bottom to top
- wipedown: Wipe from top to bottom

[Slide family]
- slideleft: Slide to the left
- slideright: Slide to the right
- slideup: Slide upward
- slidedown: Slide downward

[Smooth family]
- smoothleft: Smooth slide left
- smoothright: Smooth slide right
- smoothup: Smooth slide up
- smoothdown: Smooth slide down

[Circular]
- circlecrop: Circular crop
- circleopen: Circular open
- circleclose: Circular close

[Rectangular]
- rectcrop: Rectangular crop
- vertopen: Vertical open
- vertclose: Vertical close
- horzopen: Horizontal open
- horzclose: Horizontal close

[Diagonal]
- diagtl: Diagonal from top-left
- diagtr: Diagonal from top-right
- diagbl: Diagonal from bottom-left
- diagbr: Diagonal from bottom-right

[Slice]
- hlslice: Horizontal-left slice
- hrslice: Horizontal-right slice
- vuslice: Vertical-upper slice
- vdslice: Vertical-lower slice

[Other]
- distance: Distance-based transition
- pixelize: Pixelated transition
- radial: Radial transition
- hblur: Horizontal blur transition
"""
    return effects_info


def main():
    """Main entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
