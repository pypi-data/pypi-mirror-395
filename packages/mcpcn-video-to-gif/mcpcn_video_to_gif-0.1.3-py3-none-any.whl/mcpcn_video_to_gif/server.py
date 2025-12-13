"""
Video to GIF Converter MCP Server

Core server implementation for video to GIF conversion.
"""

from mcp.server.fastmcp import FastMCP, Context
import ffmpeg
import os
import subprocess
import platform
import urllib.parse
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import tempfile
import shutil
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

PACKAGE_NAME = "mcpcn-video-to-gif"

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


def _parse_time_to_seconds(time_input) -> float:
    """Parse time input to seconds (float)."""
    if isinstance(time_input, (int, float)):
        return float(time_input)
    if isinstance(time_input, str):
        # HH:MM:SS[.mmm] format
        if ':' in time_input:
            parts = time_input.split(':')
            if len(parts) == 3:
                h, m, s = parts
                return float(h) * 3600 + float(m) * 60 + float(s)
            elif len(parts) == 2:
                m, s = parts
                return float(m) * 60 + float(s)
        else:
            return float(time_input)
    raise ValueError(f"Invalid time format: {time_input}")


def _prepare_path(input_path: str, output_path: str, overwrite: bool = False) -> None:
    """Validate the input path and prepare the output directory."""
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


# 创建 MCP 服务器实例
mcp = FastMCP("VideoToGIF")


def _generate_output_path(video_path: str, output_dir: str | None = None) -> str:
    """Generate the GIF output path based on the source video."""
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    if output_dir:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        return os.path.join(output_dir, f"{video_name}_{timestamp}.gif")
    else:
        video_dir = os.path.dirname(video_path) or "."
        return os.path.join(video_dir, f"{video_name}_{timestamp}.gif")


def _convert_single_video(
    video_path: str,
    output_gif_path: str,
    fps: int,
    width: int | None,
    height: int | None,
    keep_aspect: bool,
    start_time: str | float | None,
    dither: str,
    max_colors: int,
    loop: int,
    crop: dict | None,
    scale_flags: str,
    bayer_scale: int | None,
    palette_stats_mode: str,
    use_reserve_transparent: bool,
    alpha_threshold: int,
    overwrite: bool,
) -> str:
    """Convert a single video into a GIF."""
    _prepare_path(video_path, output_gif_path, overwrite)

    # 参数校验
    if not output_gif_path.lower().endswith(".gif"):
        raise RuntimeError("Error: output_gif_path must end with .gif")
    if fps <= 0:
        raise RuntimeError("Error: fps must be positive")
    if not (2 <= int(max_colors) <= 256):
        raise RuntimeError("Error: max_colors must be in [2, 256]")
    if loop < 0:
        raise RuntimeError("Error: loop must be >= 0")

    valid_dither = {"none", "bayer", "floyd_steinberg", "sierra2_4a", "burkes"}
    if dither not in valid_dither:
        raise RuntimeError(f"Error: Unsupported dither '{dither}'. Supported: {', '.join(sorted(valid_dither))}")
    if dither == "bayer" and bayer_scale is not None and not (0 <= int(bayer_scale) <= 5):
        raise RuntimeError("Error: bayer_scale must be in [0, 5]")

    valid_stats_modes = {"single", "diff", "full"}
    if palette_stats_mode not in valid_stats_modes:
        raise RuntimeError(f"Error: Unsupported palette_stats_mode '{palette_stats_mode}'. Supported: {', '.join(sorted(valid_stats_modes))}")

    if not (0 <= alpha_threshold <= 255):
        raise RuntimeError("Error: alpha_threshold must be in [0, 255]")

    if keep_aspect and (width and height):
        raise RuntimeError("Error: When keep_aspect=True, provide only width or height, not both")

    # 输入裁剪参数校验
    crop_params = None
    if crop is not None:
        required_keys = {"x", "y", "w", "h"}
        if not isinstance(crop, dict) or not required_keys.issubset(crop.keys()):
            raise RuntimeError("Error: crop must be a dict with keys {'x','y','w','h'}")
        crop_params = {
            "x": int(crop["x"]),
            "y": int(crop["y"]),
            "w": int(crop["w"]),
            "h": int(crop["h"]),
        }

    # 解析时间
    ss_arg = None
    if start_time is not None:
        ss_arg = _parse_time_to_seconds(start_time)

    # 构建公共滤镜链（两遍都要）
    def apply_common_filters(stream):
        filtered = stream
        filtered = filtered.filter("fps", fps)
        if crop_params:
            filtered = filtered.filter("crop", w=crop_params["w"], h=crop_params["h"], x=crop_params["x"],
                                       y=crop_params["y"])

        # 处理缩放逻辑
        if width or height:
            if keep_aspect:
                if width and height:
                    filtered = filtered.filter("scale", width, height,
                                               force_original_aspect_ratio="decrease",
                                               flags=scale_flags)
                elif width:
                    filtered = filtered.filter("scale", f"{width}", f"{width}*ih/iw", flags=scale_flags)
                elif height:
                    filtered = filtered.filter("scale", f"{height}*iw/ih", f"{height}", flags=scale_flags)
            else:
                if width and height:
                    filtered = filtered.filter("scale", width, height, flags=scale_flags)
                elif width:
                    filtered = filtered.filter("scale", width, -1, flags=scale_flags)
                elif height:
                    filtered = filtered.filter("scale", -1, height, flags=scale_flags)

        # 颜色空间处理
        filtered = filtered.filter("format", "yuv420p")
        filtered = filtered.filter("format", "rgb24")
        return filtered

    # 临时调色板文件
    temp_dir = tempfile.mkdtemp()
    palette_path = os.path.join(temp_dir, "palette.png")

    try:
        # 第一遍：生成调色板
        in1_kwargs = {}
        if ss_arg is not None:
            in1_kwargs["ss"] = ss_arg

        in1 = ffmpeg.input(video_path, **in1_kwargs) if in1_kwargs else ffmpeg.input(video_path)
        palette_gen_params = {
            "stats_mode": palette_stats_mode,
            "max_colors": max_colors
        }
        if use_reserve_transparent:
            palette_gen_params["reserve_transparent"] = 1

        v1 = apply_common_filters(in1.video).filter("palettegen", **palette_gen_params)
        _ffmpeg_run(ffmpeg.output(v1, palette_path, update=1), capture_stdout=True, capture_stderr=True)

        # 第二遍：应用调色板生成 GIF
        in2_kwargs = {}
        if ss_arg is not None:
            in2_kwargs["ss"] = ss_arg

        in2 = ffmpeg.input(video_path, **in2_kwargs) if in2_kwargs else ffmpeg.input(video_path)
        v2 = apply_common_filters(in2.video)
        pal = ffmpeg.input(palette_path)

        paletteuse_params = {"dither": dither}
        if dither == "bayer" and bayer_scale is not None:
            paletteuse_params["bayer_scale"] = bayer_scale
        if use_reserve_transparent:
            paletteuse_params["alpha_threshold"] = alpha_threshold

        gif_v = ffmpeg.filter([v2, pal], "paletteuse", **paletteuse_params)
        _ffmpeg_run(
            ffmpeg.output(gif_v, output_gif_path, format="gif", loop=loop),
            capture_stdout=True,
            capture_stderr=True,
        )

        return output_gif_path
    finally:
        try:
            shutil.rmtree(temp_dir)
        except Exception:
            pass


@mcp.tool()
def convert_video_to_gif(
    video_paths: list[str],
    output_paths: list[str] | None = None,
    output_dir: str | None = None,
    fps: int = 8,
    width: int | None = None,
    height: int | None = None,
    keep_aspect: bool = True,
    start_time: str | float | None = None,
    dither: str = "floyd_steinberg",
    max_colors: int = 256,
    loop: int = 0,
    crop: dict | None = None,
    scale_flags: str = "lanczos",
    bayer_scale: int | None = 3,
    palette_stats_mode: str = "diff",
    use_reserve_transparent: bool = False,
    alpha_threshold: int = 128,
    overwrite: bool = False,
    ctx: Context = None
) -> str:
    """Export video clips to high-quality GIFs (optimized palettegen/paletteuse two-pass workflow).

    Args:
        video_paths: List of input videos; batch conversion is supported.
        output_paths: Optional list of output file paths (must match video_paths length). If provided, output_dir is ignored.
        output_dir: Optional destination directory. Defaults to the source directory per video. Ignored if output_paths is provided.
        fps: GIF frame rate (8–20 is common).
        width: Target width (leave height unset when keep_aspect is True).
        height: Target height (leave width unset when keep_aspect is True).
        keep_aspect: Whether to preserve the aspect ratio.
        start_time: Starting time (seconds or 'HH:MM:SS(.ms)').
        dither: Dithering algorithm ('none'|'bayer'|'floyd_steinberg'|'sierra2_4a'|'burkes').
        max_colors: Palette size between 2 and 256.
        loop: Number of loops (0 for infinite).
        crop: Optional crop dict such as {"x":0,"y":0,"w":320,"h":240}.
        scale_flags: Scaling algorithm, e.g., 'lanczos' or 'bicubic'.
        bayer_scale: Scale factor for Bayer dithering (0–5).
        palette_stats_mode: Palette stats mode ('single'|'diff'|'full').
        use_reserve_transparent: Whether to reserve a palette slot for transparency.
        alpha_threshold: Alpha threshold (0–255).
        overwrite: Whether to overwrite existing output files (default: False).

    Returns:
        A status message indicating success or failure for all videos.
    """
    execution_start_time = time.time()

    if not video_paths:
        raise RuntimeError("Error: video_paths cannot be empty")

    # 验证 output_paths 参数
    if output_paths is not None:
        if len(output_paths) != len(video_paths):
            raise RuntimeError(f"Error: output_paths length ({len(output_paths)}) must match video_paths length ({len(video_paths)})")

    success_results = []
    failed_results = []

    for idx, video_path in enumerate(video_paths):
        # 优先使用 output_paths，否则使用 _generate_output_path
        if output_paths is not None:
            output_gif_path = output_paths[idx]
        else:
            output_gif_path = _generate_output_path(video_path, output_dir)
        try:
            result_path = _convert_single_video(
                video_path=video_path,
                output_gif_path=output_gif_path,
                fps=fps,
                width=width,
                height=height,
                keep_aspect=keep_aspect,
                start_time=start_time,
                dither=dither,
                max_colors=max_colors,
                loop=loop,
                crop=crop,
                scale_flags=scale_flags,
                bayer_scale=bayer_scale,
                palette_stats_mode=palette_stats_mode,
                use_reserve_transparent=use_reserve_transparent,
                alpha_threshold=alpha_threshold,
                overwrite=overwrite,
            )
            success_results.append(result_path)
            logger.info(f"Successfully converted: {video_path} -> {result_path}")
        except Exception as e:
            error_msg = str(e)
            failed_results.append({"video": video_path, "error": error_msg})
            logger.error(f"Failed to convert {video_path}: {error_msg}")

    execution_time = time.time() - execution_start_time

    # 构建返回消息
    result_parts = []
    if success_results:
        result_parts.append(f"Successfully converted {len(success_results)} video(s):")
        for path in success_results:
            result_parts.append(f"  - {path}")

    if failed_results:
        result_parts.append(f"Failed to convert {len(failed_results)} video(s):")
        for item in failed_results:
            result_parts.append(f"  - {item['video']}: {item['error']}")

    result_parts.append(f"Total execution time: {execution_time:.2f} seconds.")

    result_message = "\n".join(result_parts)

    # 如果全部失败，抛出异常以设置 isError: true
    if not success_results and failed_results:
        raise RuntimeError(result_message)

    # 如果有成功的结果且执行时间超过1秒，打开第一个成功的文件
    if success_results and execution_time > 59:
        for path in success_results:
            _open_aido_link(ctx, path)

    return result_message


def main():
    """Main entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
