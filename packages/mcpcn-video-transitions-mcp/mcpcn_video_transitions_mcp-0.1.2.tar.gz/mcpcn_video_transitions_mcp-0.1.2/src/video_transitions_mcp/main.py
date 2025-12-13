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

# 常量定义
DEFAULT_FPS = 30
MAX_LOG_SIZE = 5_000_000
LOG_BACKUP_COUNT = 3

# 配置日志输出到stderr，避免干扰MCP通信
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

package = "video-transitions-mcp"

# 使用用户临时目录存放日志文件
log_dir = Path(tempfile.gettempdir()) / package
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "debug.log"

file_handler = RotatingFileHandler(
    str(log_file), maxBytes=MAX_LOG_SIZE, backupCount=LOG_BACKUP_COUNT, encoding="utf-8"
)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger.addHandler(file_handler)
logger.propagate = False

# 测试代码使用的
FFMPEG_BINARY = os.environ.get("FFMPEG_BINARY")
FFPROBE_BINARY = os.environ.get("FFPROBE_BINARY")


def _ffmpeg_run(stream_spec, **kwargs):
    """执行 ffmpeg 命令"""
    if "overwrite_output" not in kwargs:
        kwargs["overwrite_output"] = True
    return ffmpeg.run(stream_spec, cmd=FFMPEG_BINARY, **kwargs)


def _ffprobe_probe(path: str, **kwargs):
    """探测媒体文件属性"""
    return ffmpeg.probe(path, cmd=FFPROBE_BINARY, **kwargs)


def _get_media_properties(media_path: str) -> dict:
    """获取媒体文件的属性信息
    
    Args:
        media_path: 媒体文件路径
        
    Returns:
        包含媒体属性的字典，包括时长、是否有视频/音频流等信息
        
    Raises:
        RuntimeError: 当探测文件失败时
    """
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
                props["avg_fps"] = DEFAULT_FPS
        else:
            props["avg_fps"] = DEFAULT_FPS
            
        return props
    except ffmpeg.Error as e:
        raise RuntimeError(
            f"Error probing file {media_path}: {e.stderr.decode('utf8') if e.stderr else str(e)}"
        )
    except Exception as e:
        raise RuntimeError(f"Unexpected error probing file {media_path}: {str(e)}")


def _prepare_path(input_path: str, output_path: str) -> None:
    """准备和验证输入输出路径
    
    Args:
        input_path: 输入文件路径
        output_path: 输出文件路径
        
    Raises:
        RuntimeError: 当输入文件不存在或输出文件已存在时
    """
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


# 支持的过渡效果类型
SUPPORTED_TRANSITIONS = {
    "fade_in": "淡入效果",
    "fade_out": "淡出效果",
    "slide_in_left": "从左侧滑入",
    "slide_in_right": "从右侧滑入",
    "slide_in_top": "从顶部滑入",
    "slide_in_bottom": "从底部滑入",
    "slide_out_left": "向左侧滑出",
    "slide_out_right": "向右侧滑出",
    "slide_out_top": "向顶部滑出",
    "slide_out_bottom": "向底部滑出",
    "zoom_in": "缩放进入（从小到大）",
    "zoom_out": "缩放退出（从大到小）",
    "wipe_left": "从左向右擦除进入",
    "wipe_right": "从右向左擦除进入",
    "circle_open": "圆形展开",
    "circle_close": "圆形收缩",
}


def _decode_ffmpeg_error(e: ffmpeg.Error) -> str:
    """解码 FFmpeg 错误信息"""
    return e.stderr.decode("utf8") if e.stderr else str(e)


def _apply_transition_filter(
    video_stream,
    transition_type: str,
    duration: float,
    start_time: float,
    width: int,
    height: int,
    fps: float,
) -> any:
    """应用指定的过渡滤镜
    
    Args:
        video_stream: FFmpeg 视频流
        transition_type: 过渡类型
        duration: 过渡时长（秒）
        start_time: 开始时间（秒）
        width: 视频宽度
        height: 视频高度
        fps: 帧率
        
    Returns:
        应用滤镜后的视频流
    """
    if transition_type in ["fade_in", "crossfade_from_black"]:
        return video_stream.filter("fade", type="in", start_time=start_time, duration=duration)
    
    elif transition_type in ["fade_out", "crossfade_to_black"]:
        return video_stream.filter("fade", type="out", start_time=start_time, duration=duration)
    
    # 滑动效果
    elif transition_type == "slide_in_left":
        # 从左侧滑入：x 从 -width 到 0
        expr = f"if(lt(t,{start_time}),-w,if(lt(t,{start_time + duration}),-w+(w*(t-{start_time})/{duration}),0))"
        return video_stream.filter("pad", w=f"{width}*2", h=height, x=width, y=0, color="black").filter(
            "crop", w=width, h=height, x=expr, y=0
        )
    
    elif transition_type == "slide_in_right":
        # 从右侧滑入：x 从 width 到 0
        expr = f"if(lt(t,{start_time}),w,if(lt(t,{start_time + duration}),w-(w*(t-{start_time})/{duration}),0))"
        return video_stream.filter("pad", w=f"{width}*2", h=height, x=0, y=0, color="black").filter(
            "crop", w=width, h=height, x=expr, y=0
        )
    
    elif transition_type == "slide_in_top":
        # 从顶部滑入：y 从 -height 到 0
        expr = f"if(lt(t,{start_time}),-h,if(lt(t,{start_time + duration}),-h+(h*(t-{start_time})/{duration}),0))"
        return video_stream.filter("pad", w=width, h=f"{height}*2", x=0, y=height, color="black").filter(
            "crop", w=width, h=height, x=0, y=expr
        )
    
    elif transition_type == "slide_in_bottom":
        # 从底部滑入：y 从 height 到 0
        expr = f"if(lt(t,{start_time}),h,if(lt(t,{start_time + duration}),h-(h*(t-{start_time})/{duration}),0))"
        return video_stream.filter("pad", w=width, h=f"{height}*2", x=0, y=0, color="black").filter(
            "crop", w=width, h=height, x=0, y=expr
        )
    
    elif transition_type == "slide_out_left":
        # 向左滑出：x 从 0 到 -width
        expr = f"if(lt(t,{start_time}),0,if(lt(t,{start_time + duration}),-(w*(t-{start_time})/{duration}),-w))"
        return video_stream.filter("pad", w=f"{width}*2", h=height, x=width, y=0, color="black").filter(
            "crop", w=width, h=height, x=expr, y=0
        )
    
    elif transition_type == "slide_out_right":
        # 向右滑出：x 从 0 到 width
        expr = f"if(lt(t,{start_time}),0,if(lt(t,{start_time + duration}),(w*(t-{start_time})/{duration}),w))"
        return video_stream.filter("pad", w=f"{width}*2", h=height, x=0, y=0, color="black").filter(
            "crop", w=width, h=height, x=expr, y=0
        )
    
    elif transition_type == "slide_out_top":
        # 向顶部滑出：y 从 0 到 -height
        expr = f"if(lt(t,{start_time}),0,if(lt(t,{start_time + duration}),-(h*(t-{start_time})/{duration}),-h))"
        return video_stream.filter("pad", w=width, h=f"{height}*2", x=0, y=height, color="black").filter(
            "crop", w=width, h=height, x=0, y=expr
        )
    
    elif transition_type == "slide_out_bottom":
        # 向底部滑出：y 从 0 到 height
        expr = f"if(lt(t,{start_time}),0,if(lt(t,{start_time + duration}),(h*(t-{start_time})/{duration}),h))"
        return video_stream.filter("pad", w=width, h=f"{height}*2", x=0, y=0, color="black").filter(
            "crop", w=width, h=height, x=0, y=expr
        )
    
    # 缩放效果
    elif transition_type == "zoom_in":
        # 从小到大缩放：scale 从 0.1 到 1.0
        scale_expr = f"if(lt(t,{start_time}),0.1,if(lt(t,{start_time + duration}),0.1+(0.9*(t-{start_time})/{duration}),1.0))"
        return video_stream.filter(
            "scale",
            w=f"iw*{scale_expr}",
            h=f"ih*{scale_expr}",
        ).filter(
            "pad",
            w=width,
            h=height,
            x=f"({width}-iw)/2",
            y=f"({height}-ih)/2",
            color="black"
        )
    
    elif transition_type == "zoom_out":
        # 从大到小缩放：scale 从 1.0 到 0.1
        scale_expr = f"if(lt(t,{start_time}),1.0,if(lt(t,{start_time + duration}),1.0-(0.9*(t-{start_time})/{duration}),0.1))"
        return video_stream.filter(
            "scale",
            w=f"iw*{scale_expr}",
            h=f"ih*{scale_expr}",
        ).filter(
            "pad",
            w=width,
            h=height,
            x=f"({width}-iw)/2",
            y=f"({height}-ih)/2",
            color="black"
        )
    
    # 擦除效果
    elif transition_type == "wipe_left":
        # 从左向右擦除
        w_expr = f"if(lt(t,{start_time}),0,if(lt(t,{start_time + duration}),w*(t-{start_time})/{duration},w))"
        return video_stream.filter("crop", w=w_expr, h=height, x=0, y=0).filter(
            "pad", w=width, h=height, x=0, y=0, color="black"
        )
    
    elif transition_type == "wipe_right":
        # 从右向左擦除
        w_expr = f"if(lt(t,{start_time}),0,if(lt(t,{start_time + duration}),w*(t-{start_time})/{duration},w))"
        x_expr = f"if(lt(t,{start_time}),w,if(lt(t,{start_time + duration}),w-(w*(t-{start_time})/{duration}),0))"
        return video_stream.filter("crop", w=w_expr, h=height, x=x_expr, y=0).filter(
            "pad", w=width, h=height, x=f"{width}-iw", y=0, color="black"
        )
    
    # 圆形效果（使用 geq 滤镜）
    elif transition_type == "circle_open":
        # 圆形展开
        max_radius = f"sqrt(({width}/2)^2+({height}/2)^2)"
        radius_expr = f"if(lt(t,{start_time}),0,if(lt(t,{start_time + duration}),{max_radius}*(t-{start_time})/{duration},{max_radius}))"
        return video_stream.filter(
            "geq",
            r=f"if(lt(sqrt((X-{width}/2)^2+(Y-{height}/2)^2),{radius_expr}),r(X,Y),0)",
            g=f"if(lt(sqrt((X-{width}/2)^2+(Y-{height}/2)^2),{radius_expr}),g(X,Y),0)",
            b=f"if(lt(sqrt((X-{width}/2)^2+(Y-{height}/2)^2),{radius_expr}),b(X,Y),0)",
        )
    
    elif transition_type == "circle_close":
        # 圆形收缩
        max_radius = f"sqrt(({width}/2)^2+({height}/2)^2)"
        radius_expr = f"if(lt(t,{start_time}),{max_radius},if(lt(t,{start_time + duration}),{max_radius}-({max_radius}*(t-{start_time})/{duration}),0))"
        return video_stream.filter(
            "geq",
            r=f"if(lt(sqrt((X-{width}/2)^2+(Y-{height}/2)^2),{radius_expr}),r(X,Y),0)",
            g=f"if(lt(sqrt((X-{width}/2)^2+(Y-{height}/2)^2),{radius_expr}),g(X,Y),0)",
            b=f"if(lt(sqrt((X-{width}/2)^2+(Y-{height}/2)^2),{radius_expr}),b(X,Y),0)",
        )
    
    else:
        raise RuntimeError(f"Unsupported transition type: {transition_type}")


# 创建 FastMCP 实例
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

mcp = FastMCP("VideoTransitionsServer")


def _generate_output_path(input_path: str, suffix: str) -> str:
    """Generate output path with timestamp to avoid conflicts.
    
    Args:
        input_path: Input file path
        suffix: Suffix to add before timestamp (e.g., '_transition')
        
    Returns:
        Generated output path with timestamp
    """
    directory = os.path.dirname(input_path)
    name, ext = os.path.splitext(os.path.basename(input_path))
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    return os.path.join(directory, f"{name}{suffix}_{timestamp}{ext}")


@mcp.tool()
def list_available_transitions() -> str:
    """列出所有可用的过渡效果类型。

    Returns:
        包含所有支持的过渡效果及其描述的格式化字符串。
        
    Examples:
        transitions = list_available_transitions()
        print(transitions)
    """
    result = "可用的过渡效果：\n\n"
    for effect_type, description in SUPPORTED_TRANSITIONS.items():
        result += f"- {effect_type}: {description}\n"
    return result


@mcp.tool()
def add_transition(
    video_path: str,
    transition_type: str,
    duration_seconds: float,
    output_video_path: str | None = None,
    quality_preset: str = "medium",
    ctx: Context = None,
) -> str:
    """为视频添加进入或退出过渡效果。

    Args:
        video_path: 输入视频文件路径。
        transition_type: 过渡类型，支持以下效果：
            - fade_in/crossfade_from_black: 淡入效果
            - fade_out/crossfade_to_black: 淡出效果
            - slide_in_left/right/top/bottom: 滑入效果
            - slide_out_left/right/top/bottom: 滑出效果
            - zoom_in: 缩放进入（从小到大）
            - zoom_out: 缩放退出（从大到小）
            - wipe_left/right: 擦除效果
            - circle_open: 圆形展开
            - circle_close: 圆形收缩
        duration_seconds: 过渡时长（秒，必须大于 0）。
        output_video_path: 输出视频文件路径（可选，不提供时自动生成带时间戳的文件名）。
        quality_preset: 编码质量预设，可选 'ultrafast', 'fast', 'medium', 'slow', 'veryslow'，默认 'medium'。

    Returns:
        成功或失败的状态消息。
        
    Raises:
        RuntimeError: 当参数无效或处理失败时
        
    Examples:
        # 添加 2 秒的淡入效果
        add_transition(
            video_path="/path/to/input.mp4",
            transition_type="fade_in",
            duration_seconds=2.0
        )
        
        # 添加从左侧滑入效果
        add_transition(
            video_path="/path/to/input.mp4",
            transition_type="slide_in_left",
            duration_seconds=1.5
        )
        
        # 添加圆形展开效果，使用快速编码
        add_transition(
            video_path="/path/to/input.mp4",
            transition_type="circle_open",
            duration_seconds=2.0,
            quality_preset="fast"
        )
    """
    # 验证路径
    execution_start_time = time.time()
    if output_video_path is None:
        output_video_path = _generate_output_path(video_path, "_transition")
    _prepare_path(video_path, output_video_path)
    
    # 验证过渡时长
    if duration_seconds <= 0:
        raise RuntimeError("Error: Transition duration must be positive.")
    
    # 验证过渡类型
    if transition_type not in SUPPORTED_TRANSITIONS and transition_type not in ["crossfade_from_black", "crossfade_to_black"]:
        available = ", ".join(SUPPORTED_TRANSITIONS.keys())
        raise RuntimeError(
            f"Error: Unsupported transition_type '{transition_type}'. Available: {available}"
        )
    
    # 验证质量预设
    valid_presets = ["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow"]
    if quality_preset not in valid_presets:
        raise RuntimeError(
            f"Error: Invalid quality_preset '{quality_preset}'. Valid options: {', '.join(valid_presets)}"
        )
    
    try:
        # 获取视频属性
        props = _get_media_properties(video_path)
        video_total_duration = props["duration"]
        width = props["width"]
        height = props["height"]
        fps = props["avg_fps"]
        
        # 验证过渡时长不超过视频总时长
        if duration_seconds > video_total_duration:
            raise RuntimeError(
                f"Error: Transition duration ({duration_seconds}s) cannot exceed video duration ({video_total_duration}s)."
            )
        
        # 创建输入流
        input_stream = ffmpeg.input(video_path)
        video_stream = input_stream.video
        audio_stream = input_stream.audio
        
        # 确定开始时间
        if transition_type.endswith("_out") or transition_type == "crossfade_to_black" or transition_type == "circle_close" or transition_type == "zoom_out":
            # 退出效果：在视频结束前应用
            start_time = video_total_duration - duration_seconds
            logger.info(f"Applying exit transition '{transition_type}' starting at {start_time}s")
        else:
            # 进入效果：从视频开始应用
            start_time = 0
            logger.info(f"Applying entrance transition '{transition_type}' with duration {duration_seconds}s")
        
        # 应用过渡滤镜
        processed_video = _apply_transition_filter(
            video_stream,
            transition_type,
            duration_seconds,
            start_time,
            width,
            height,
            fps,
        )

        # 构建输出流列表
        output_streams = []
        if props["has_video"]:
            output_streams.append(processed_video)
        if props["has_audio"]:
            output_streams.append(audio_stream)
        if not output_streams:
            raise RuntimeError(
                "Error: No suitable video or audio streams found to apply transition."
            )
        
        # 尝试使用音频复制进行编码
        try:
            output_kwargs = {
                "vcodec": "libx264",
                "pix_fmt": "yuv420p",
                "preset": quality_preset,
            }
            if props["has_audio"]:
                output_kwargs["acodec"] = "copy"
            _ffmpeg_run(
                ffmpeg.output(*output_streams, output_video_path, **output_kwargs),
                capture_stdout=True,
                capture_stderr=True,
            )
            logger.info(f"Successfully applied transition with audio copy")
            success_result = f"Transition '{transition_type}' applied successfully. Output: {output_video_path}"
        except ffmpeg.Error as e_acopy:
            # Record failure but continue to attempt full re-encode
            # 如果音频复制失败，尝试完全重新编码
            logger.warning(f"Audio copy failed, trying full re-encode: {_decode_ffmpeg_error(e_acopy)}")
            try:
                _ffmpeg_run(
                    ffmpeg.output(
                        *output_streams,
                        output_video_path,
                        vcodec="libx264",
                        pix_fmt="yuv420p",
                        preset=quality_preset,
                    ),
                    capture_stdout=True,
                    capture_stderr=True,
                )
                logger.info(f"Successfully applied transition with full re-encode")
                success_result = f"Transition '{transition_type}' applied successfully (audio re-encoded). Output: {output_video_path}"
            except ffmpeg.Error as e_recode:
                raise RuntimeError(
                    f"Error applying transition. Audio copy failed: {_decode_ffmpeg_error(e_acopy)}. "
                    f"Full re-encode failed: {_decode_ffmpeg_error(e_recode)}."
                )
    except ffmpeg.Error as e:
        raise RuntimeError(f"Error applying transition: {_decode_ffmpeg_error(e)}")
    except ValueError as e:
        raise RuntimeError(f"Error with input values: {str(e)}")
    except RuntimeError as e:
        # 重新抛出已经格式化的 RuntimeError
        raise e
    except Exception as e:
        raise RuntimeError(
            f"An unexpected error occurred in add_transition: {str(e)}"
        )

    # Build summary with execution time
    execution_time = time.time() - execution_start_time
    summary = f"\nProcessing finished: 1 succeeded, 0 failed\n"
    summary += f"Total execution time: {execution_time:.2f} seconds.\n"
    result_message = summary + "\n" + (success_result if 'success_result' in locals() else "")
    # Notify external app if execution > 59 seconds and we have a successful result
    if execution_time > 59 and success_result:
        _open_aido_link(ctx, output_video_path)
    return result_message

@mcp.tool()
def add_combined_transitions(
    video_path: str,
    entrance_type: str,
    entrance_duration: float,
    exit_type: str,
    exit_duration: float,
    output_video_path: str | None = None,
    quality_preset: str = "medium",
    ctx: Context = None,
) -> str:
    """为视频同时添加进入和退出过渡效果。

    Args:
        video_path: 输入视频文件路径。
        entrance_type: 进入过渡类型（如 'fade_in', 'slide_in_left', 'zoom_in' 等）。
        entrance_duration: 进入过渡时长（秒）。
        exit_type: 退出过渡类型（如 'fade_out', 'slide_out_right', 'zoom_out' 等）。
        exit_duration: 退出过渡时长（秒）。
        output_video_path: 输出视频文件路径（可选，不提供时自动生成带时间戳的文件名）。
        quality_preset: 编码质量预设，默认 'medium'。

    Returns:
        成功或失败的状态消息。
        
    Raises:
        RuntimeError: 当参数无效或处理失败时
        
    Examples:
        # 添加淡入和淡出效果
        add_combined_transitions(
            video_path="/path/to/input.mp4",
            entrance_type="fade_in",
            entrance_duration=2.0,
            exit_type="fade_out",
            exit_duration=2.0
        )
        
        # 添加滑入和缩放退出效果
        add_combined_transitions(
            video_path="/path/to/input.mp4",
            entrance_type="slide_in_left",
            entrance_duration=1.5,
            exit_type="zoom_out",
            exit_duration=2.0
        )
    """
    # 验证路径
    execution_start_time = time.time()
    if output_video_path is None:
        output_video_path = _generate_output_path(video_path, "_combined_transition")
    _prepare_path(video_path, output_video_path)
    
    # 验证时长
    if entrance_duration <= 0 or exit_duration <= 0:
        raise RuntimeError("Error: Transition durations must be positive.")
    
    # 验证过渡类型
    for trans_type in [entrance_type, exit_type]:
        if trans_type not in SUPPORTED_TRANSITIONS and trans_type not in ["crossfade_from_black", "crossfade_to_black"]:
            available = ", ".join(SUPPORTED_TRANSITIONS.keys())
            raise RuntimeError(
                f"Error: Unsupported transition_type '{trans_type}'. Available: {available}"
            )
    
    # 验证质量预设
    valid_presets = ["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow"]
    if quality_preset not in valid_presets:
        raise RuntimeError(
            f"Error: Invalid quality_preset '{quality_preset}'. Valid options: {', '.join(valid_presets)}"
        )
    
    try:
        # 获取视频属性
        props = _get_media_properties(video_path)
        video_total_duration = props["duration"]
        width = props["width"]
        height = props["height"]
        fps = props["avg_fps"]
        
        # 验证过渡时长
        if entrance_duration + exit_duration > video_total_duration:
            raise RuntimeError(
                f"Error: Combined transition duration ({entrance_duration + exit_duration}s) "
                f"cannot exceed video duration ({video_total_duration}s)."
            )
        
        # 创建输入流
        input_stream = ffmpeg.input(video_path)
        video_stream = input_stream.video
        audio_stream = input_stream.audio
        
        # 应用进入效果
        logger.info(f"Applying entrance transition '{entrance_type}' with duration {entrance_duration}s")
        video_with_entrance = _apply_transition_filter(
            video_stream,
            entrance_type,
            entrance_duration,
            0,  # 进入效果从开始
            width,
            height,
            fps,
        )
        
        # 应用退出效果
        exit_start_time = video_total_duration - exit_duration
        logger.info(f"Applying exit transition '{exit_type}' starting at {exit_start_time}s")
        video_with_both = _apply_transition_filter(
            video_with_entrance,
            exit_type,
            exit_duration,
            exit_start_time,
            width,
            height,
            fps,
        )
        
        # 构建输出流
        output_streams = []
        if props["has_video"]:
            output_streams.append(video_with_both)
        if props["has_audio"]:
            output_streams.append(audio_stream)
        if not output_streams:
            raise RuntimeError(
                "Error: No suitable video or audio streams found to apply transitions."
            )
        
        # 尝试编码
        try:
            output_kwargs = {
                "vcodec": "libx264",
                "pix_fmt": "yuv420p",
                "preset": quality_preset,
            }
            if props["has_audio"]:
                output_kwargs["acodec"] = "copy"
            _ffmpeg_run(
                ffmpeg.output(*output_streams, output_video_path, **output_kwargs),
                capture_stdout=True,
                capture_stderr=True,
            )
            logger.info(f"Successfully applied combined transitions")
            success_result = f"Combined transitions '{entrance_type}' + '{exit_type}' applied successfully. Output: {output_video_path}"
        except ffmpeg.Error as e_acopy:
            logger.warning(f"Audio copy failed, trying full re-encode: {_decode_ffmpeg_error(e_acopy)}")
            try:
                _ffmpeg_run(
                    ffmpeg.output(
                        *output_streams,
                        output_video_path,
                        vcodec="libx264",
                        pix_fmt="yuv420p",
                        preset=quality_preset,
                    ),
                    capture_stdout=True,
                    capture_stderr=True,
                )
                logger.info(f"Successfully applied combined transitions with full re-encode")
                success_result = f"Combined transitions '{entrance_type}' + '{exit_type}' applied successfully (audio re-encoded). Output: {output_video_path}"
            except ffmpeg.Error as e_recode:
                raise RuntimeError(
                    f"Error applying combined transitions. Audio copy failed: {_decode_ffmpeg_error(e_acopy)}. "
                    f"Full re-encode failed: {_decode_ffmpeg_error(e_recode)}."
                )
    except ffmpeg.Error as e:
        raise RuntimeError(f"Error applying combined transitions: {_decode_ffmpeg_error(e)}")
    except ValueError as e:
        raise RuntimeError(f"Error with input values: {str(e)}")
    except RuntimeError as e:
        raise e
    except Exception as e:
        raise RuntimeError(
            f"An unexpected error occurred in add_combined_transitions: {str(e)}"
        )

    # Build summary with execution time
    execution_time = time.time() - execution_start_time
    summary = f"\nProcessing finished: 1 succeeded, 0 failed\n"
    summary += f"Total execution time: {execution_time:.2f} seconds.\n"
    result_message = summary + "\n" + (success_result if 'success_result' in locals() else "")
    # Notify external app if execution > 59 seconds and we have a successful result
    if execution_time > 59 and success_result:
        _open_aido_link(ctx, output_video_path)
    return result_message

def main():
    """Main entry point for the MCP server."""
    logger.info(f"Starting {package} server...")
    mcp.run()


if __name__ == "__main__":
    main()
