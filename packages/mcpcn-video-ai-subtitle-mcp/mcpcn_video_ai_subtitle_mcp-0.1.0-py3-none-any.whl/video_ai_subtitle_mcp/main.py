#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频AI字幕生成 MCP 服务
工具：
1. generate_subtitle - 从视频生成 SRT 字幕
2. merge_subtitle - 将字幕合并到视频
"""
import os
import subprocess
import time
import logging
from logging.handlers import RotatingFileHandler
import tempfile
import threading
from pathlib import Path
from urllib.request import urlretrieve
import platform
import urllib.parse

import ffmpeg
import requests
from mcp.server.fastmcp import FastMCP, Context

# 配置日志输出到stderr，避免干扰MCP通信
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

package = "video-ai-subtitle-mcp"

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


mcp = FastMCP("视频-AI加字幕")

# 火山引擎配置
BASE_URL = 'https://openspeech.bytedance.com/api/v1/vc'
APPID = os.environ.get("VOLCANO_APPID", "")
ACCESS_TOKEN = os.environ.get("VOLCANO_ACCESS_TOKEN", "")


def extract_audio(video_path: Path, wav_path: Path, ctx: Context = None):
    """使用 ffmpeg-python 提取音频"""
    input_stream = ffmpeg.input(str(video_path))
    output_stream = input_stream.output(
        str(wav_path),
        vn=None,  # 无视频
        ac=1,     # 单声道
        ar=16000, # 采样率 16000
        f="wav"   # 输出格式
    )
    _ffmpeg_run_with_progress(output_stream, operation_name="Extracting audio", ctx=ctx)


def upload_to_mcpcn(file_path: Path) -> str:
    with open(file_path, 'rb') as f:
        resp = requests.post(
            'https://www.mcpcn.cc/api/fileUploadAndDownload/uploadMcpFile',
            files={'file': f}
        )
    if resp.status_code == 200 and resp.json().get('code') == 0:
        return resp.json()['data']['url']
    raise RuntimeError(f"上传失败: {resp.text}")


def submit_task(file_url: str) -> str:
    resp = requests.post(
        f'{BASE_URL}/submit',
        params={
            'appid': APPID, 'language': 'zh-CN',
            'use_itn': 'True', 'use_capitalize': 'True',
            'max_lines': 1, 'words_per_line': 15,
        },
        json={'url': file_url},
        headers={'content-type': 'application/json', 'Authorization': f'Bearer; {ACCESS_TOKEN}'}
    )
    if resp.status_code != 200 or resp.json().get('message') != 'Success':
        raise RuntimeError(f"提交失败: {resp.text}")
    return resp.json()['id']


def poll_result(job_id: str) -> dict:
    while True:
        resp = requests.get(
            f'{BASE_URL}/query',
            params={'appid': APPID, 'id': job_id},
            headers={'Authorization': f'Bearer; {ACCESS_TOKEN}'}
        )
        data = resp.json()
        if data.get('message') == 'Success':
            return data
        elif data.get('message') in ['Running', 'Pending']:
            time.sleep(3)
        else:
            raise RuntimeError(f"任务失败: {data}")


def ms_to_timestamp(ms: int) -> str:
    s, ms = divmod(ms, 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def result_to_srt(data: dict, srt_path: Path):
    with open(srt_path, 'w', encoding='utf-8') as f:
        for i, u in enumerate(data.get('utterances', []), 1):
            f.write(f"{i}\n{ms_to_timestamp(u['start_time'])} --> {ms_to_timestamp(u['end_time'])}\n{u['text'].strip()}\n\n")


def _color_to_ass(color: str) -> str:
    """
    将颜色转换为 ASS 格式 (&HAABBGGRR)
    支持格式: 
    - 十六进制: #RRGGBB 或 RRGGBB
    - 颜色名称: white, black, red, green, blue, yellow, cyan, magenta, orange, pink
    """
    color_map = {
        "white": "FFFFFF",
        "black": "000000",
        "red": "FF0000",
        "green": "00FF00",
        "blue": "0000FF",
        "yellow": "FFFF00",
        "cyan": "00FFFF",
        "magenta": "FF00FF",
        "orange": "FFA500",
        "pink": "FFC0CB",
    }
    
    color_lower = color.lower().strip()
    if color_lower in color_map:
        hex_color = color_map[color_lower]
    else:
        # 去掉 # 前缀
        hex_color = color.lstrip('#').upper()
        if len(hex_color) != 6:
            hex_color = "FFFFFF"  # 默认白色
    
    # RGB -> BGR (ASS 格式是 &HAABBGGRR，AA是透明度，我们用00表示不透明)
    r, g, b = hex_color[0:2], hex_color[2:4], hex_color[4:6]
    return f"&H00{b}{g}{r}"


def burn_subtitle(
    video_path: Path,
    srt_path: Path,
    output_path: Path,
    font_color: str = "white",
    outline_color: str = "black",
    font_size: int = 24,
    position: str = "bottom",
    margin_v: int = 50,
    ctx: Context = None
):
    """
    使用 ffmpeg-python 烧录字幕
    
    Args:
        video_path: 输入视频路径
        srt_path: 字幕文件路径
        output_path: 输出视频路径
        font_color: 字幕颜色 (支持颜色名称如 white/red/yellow 或十六进制 #RRGGBB)
        outline_color: 描边颜色
        font_size: 字体大小
        position: 字幕位置 (top/center/bottom)
        margin_v: 垂直边距
        ctx: MCP Context
    """
    font_name, font_file = "Arial", None
    for name, path in [
        ("Arial Unicode MS", "/Library/Fonts/Arial Unicode.ttf"),
        ("STHeiti", "/System/Library/Fonts/STHeiti Medium.ttc"),
        ("PingFang SC", "/System/Library/Fonts/PingFang.ttc"),
    ]:
        if os.path.exists(path):
            font_name, font_file = name, path
            break
    
    # 转换颜色为 ASS 格式
    primary_colour = _color_to_ass(font_color)
    outline_colour = _color_to_ass(outline_color)
    
    # 根据位置设置对齐方式 (ASS Alignment: 1-3底部, 4-6中间, 7-9顶部, 2/5/8是居中)
    alignment_map = {
        "top": 8,      # 顶部居中
        "center": 5,   # 中间居中
        "bottom": 2,   # 底部居中
    }
    alignment = alignment_map.get(position.lower(), 2)
    
    safe_srt = str(srt_path.absolute()).replace("'", "\\'").replace(":", "\\:")
    style = f"FontName={font_name},FontSize={font_size},PrimaryColour={primary_colour},OutlineColour={outline_colour},Outline=2,Alignment={alignment},MarginV={margin_v}"
    vf = f"subtitles='{safe_srt}':force_style='{style}'"
    if font_file:
        vf += f":fontsdir='{str(Path(font_file).parent).replace(':', '\\:')}'"
    
    input_stream = ffmpeg.input(str(video_path))
    output_stream = input_stream.output(
        str(output_path),
        vf=vf,
        **{'c:v': 'libx264', 'c:a': 'copy'}
    )
    _ffmpeg_run_with_progress(output_stream, operation_name="Burning subtitle", ctx=ctx)


@mcp.tool()
def generate_subtitle(
    video_url: str,
    output_dir: str = "outputs",
    output_name: str = "output",
    ctx: Context = None
) -> str:
    """
    从视频 URL 生成 SRT 字幕文件（使用火山引擎语音识别）
    
    Args:
        video_url: 视频的公网 URL
        output_dir: 输出目录，默认 outputs
        output_name: 输出文件名前缀，默认 output
    
    Returns:
        生成结果，包含字幕文件路径
    """
    execution_start_time = time.time()
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    video_path = out_dir / f"{output_name}_original.mp4"
    wav_path = out_dir / f"{output_name}.wav"
    srt_path = out_dir / f"{output_name}.srt"
    
    if ctx:
        ctx.report_progress(0, "Downloading video...")
    
    # 下载视频
    urlretrieve(video_url, str(video_path))
    
    if ctx:
        ctx.report_progress(20, "Extracting audio...")
    
    # 提取音频
    extract_audio(video_path, wav_path, ctx)
    
    if ctx:
        ctx.report_progress(40, "Uploading audio...")
    
    # 上传音频
    audio_url = upload_to_mcpcn(wav_path)
    
    if ctx:
        ctx.report_progress(50, "Recognizing speech...")
    
    # 识别
    job_id = submit_task(audio_url)
    result = poll_result(job_id)
    
    if ctx:
        ctx.report_progress(90, "Generating subtitle file...")
    
    # 生成字幕
    result_to_srt(result, srt_path)
    
    # 计算执行时间
    execution_time = time.time() - execution_start_time
    result_message = f"✓ 字幕生成完成\n字幕文件: {srt_path.absolute()}\n视频文件: {video_path.absolute()}\n识别句数: {len(result.get('utterances', []))}\n执行时间: {execution_time:.2f} 秒"
    
    # 只有执行时间超过59秒才调用 _open_aido_link
    if execution_time > 59:
        _open_aido_link(ctx, str(srt_path.absolute()))
    
    return result_message


@mcp.tool()
def merge_subtitle(
    video_path: str,
    srt_path: str,
    output_path: str = "",
    font_color: str = "white",
    outline_color: str = "black",
    font_size: int = 24,
    position: str = "bottom",
    margin_v: int = 50,
    ctx: Context = None
) -> str:
    """
    将 SRT 字幕文件合并（烧录）到视频中
    
    Args:
        video_path: 视频文件路径
        srt_path: SRT 字幕文件路径
        output_path: 输出视频路径，默认在原视频目录生成
        font_color: 字幕颜色，支持颜色名称(white/red/yellow/green/blue/cyan/magenta/orange/pink/black)或十六进制(#RRGGBB)，默认 white
        outline_color: 描边颜色，格式同上，默认 black
        font_size: 字体大小，默认 24
        position: 字幕位置，可选 top(顶部)/center(中间)/bottom(底部)，默认 bottom
        margin_v: 垂直边距(像素)，默认 50
    
    Returns:
        合并结果，包含输出文件路径
    """
    execution_start_time = time.time()
    video = Path(video_path)
    srt = Path(srt_path)
    output = Path(output_path) if output_path else video.parent / f"{video.stem}_with_sub.mp4"
    
    _prepare_path(str(video), str(output), overwrite=True)
    
    if ctx:
        ctx.report_progress(0, "Starting subtitle merge...")
    
    burn_subtitle(
        video, srt, output,
        font_color=font_color,
        outline_color=outline_color,
        font_size=font_size,
        position=position,
        margin_v=margin_v,
        ctx=ctx
    )
    
    # 计算执行时间
    execution_time = time.time() - execution_start_time
    result_message = f"✓ 字幕合并完成\n输出文件: {output.absolute()}\n执行时间: {execution_time:.2f} 秒"
    
    # 只有执行时间超过59秒才调用 _open_aido_link
    if execution_time > 59:
        _open_aido_link(ctx, str(output.absolute()))
    
    return result_message


def main():
    """Main entry point for the MCP server."""
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
