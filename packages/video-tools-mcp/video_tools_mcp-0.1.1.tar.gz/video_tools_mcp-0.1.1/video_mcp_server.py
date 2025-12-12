#!/usr/bin/env python3
"""
FastMCP сервер для работы с видео.
Предоставляет инструменты для извлечения кадров, метаданных, аудио и создания GIF.
"""

import subprocess
import json
import base64
import tempfile
import os
import shutil
import sys
from pathlib import Path
from typing import Optional

from mcp.server.fastmcp import FastMCP

# Определение путей к ffmpeg/ffprobe
FFMPEG_PATH: Optional[str] = None
FFPROBE_PATH: Optional[str] = None


def find_ffmpeg() -> tuple[str, str]:
    """
    Поиск ffmpeg и ffprobe в системе.
    Возвращает пути к исполняемым файлам.
    """
    global FFMPEG_PATH, FFPROBE_PATH
    
    if FFMPEG_PATH and FFPROBE_PATH:
        return FFMPEG_PATH, FFPROBE_PATH
    
    # Стандартные имена
    ffmpeg_names = ["ffmpeg", "ffmpeg.exe"]
    ffprobe_names = ["ffprobe", "ffprobe.exe"]
    
    # Дополнительные пути для Windows
    extra_paths = []
    if sys.platform == "win32":
        extra_paths = [
            os.path.expanduser("~/ffmpeg/bin"),
            os.path.expanduser("~/scoop/shims"),
            "C:/ffmpeg/bin",
            "C:/Program Files/ffmpeg/bin",
            "C:/Program Files (x86)/ffmpeg/bin",
        ]
    
    # Поиск ffmpeg
    FFMPEG_PATH = shutil.which("ffmpeg")
    if not FFMPEG_PATH:
        for path in extra_paths:
            for name in ffmpeg_names:
                full_path = os.path.join(path, name)
                if os.path.isfile(full_path):
                    FFMPEG_PATH = full_path
                    break
            if FFMPEG_PATH:
                break
    
    # Поиск ffprobe
    FFPROBE_PATH = shutil.which("ffprobe")
    if not FFPROBE_PATH:
        for path in extra_paths:
            for name in ffprobe_names:
                full_path = os.path.join(path, name)
                if os.path.isfile(full_path):
                    FFPROBE_PATH = full_path
                    break
            if FFPROBE_PATH:
                break
    
    if not FFMPEG_PATH or not FFPROBE_PATH:
        raise RuntimeError(
            "FFmpeg not found! Please install FFmpeg and add it to PATH.\n"
            "Windows: Download from https://ffmpeg.org/download.html and add bin folder to PATH\n"
            "  or install via: winget install ffmpeg\n"
            "  or install via: scoop install ffmpeg\n"
            "macOS: brew install ffmpeg\n"
            "Linux: sudo apt install ffmpeg"
        )
    
    return FFMPEG_PATH, FFPROBE_PATH


def get_subprocess_args() -> dict:
    """Получить аргументы для subprocess в зависимости от ОС."""
    kwargs = {
        "capture_output": True,
        "text": True,
    }
    # На Windows скрываем консольное окно
    if sys.platform == "win32":
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        kwargs["startupinfo"] = startupinfo
    return kwargs

# Инициализация MCP сервера
mcp = FastMCP(
    name="video-tools",
    instructions="MCP сервер для работы с видео. Позволяет извлекать кадры, метаданные, аудио и создавать GIF."
)


def run_ffprobe(video_path: str, *args) -> dict:
    """Запуск ffprobe и получение JSON результата."""
    _, ffprobe = find_ffmpeg()
    cmd = [
        ffprobe,
        "-v", "quiet",
        "-print_format", "json",
        *args,
        video_path
    ]
    result = subprocess.run(cmd, **get_subprocess_args())
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe error: {result.stderr}")
    return json.loads(result.stdout)


def run_ffmpeg(args: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Запуск ffmpeg с указанными аргументами."""
    ffmpeg, _ = find_ffmpeg()
    cmd = [ffmpeg, "-y", "-v", "quiet", *args]
    result = subprocess.run(cmd, **get_subprocess_args())
    if check and result.returncode != 0:
        raise RuntimeError(f"ffmpeg error: {result.stderr}")
    return result


@mcp.tool()
def get_video_metadata(video_path: str) -> dict:
    """
    Получить метаданные видео: длительность, разрешение, FPS, кодек, битрейт.
    
    Args:
        video_path: Путь к видеофайлу
        
    Returns:
        Словарь с метаданными видео
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Видеофайл не найден: {video_path}")
    
    # Получаем информацию о формате и потоках
    data = run_ffprobe(video_path, "-show_format", "-show_streams")
    
    format_info = data.get("format", {})
    streams = data.get("streams", [])
    
    # Находим видео и аудио потоки
    video_stream = None
    audio_stream = None
    
    for stream in streams:
        if stream.get("codec_type") == "video" and video_stream is None:
            video_stream = stream
        elif stream.get("codec_type") == "audio" and audio_stream is None:
            audio_stream = stream
    
    result = {
        "file_path": video_path,
        "file_size_bytes": int(format_info.get("size", 0)),
        "file_size_mb": round(int(format_info.get("size", 0)) / (1024 * 1024), 2),
        "duration_seconds": float(format_info.get("duration", 0)),
        "format_name": format_info.get("format_name"),
        "bit_rate": int(format_info.get("bit_rate", 0)),
    }
    
    if video_stream:
        # Вычисляем FPS
        fps_str = video_stream.get("r_frame_rate", "0/1")
        if "/" in fps_str:
            num, den = map(int, fps_str.split("/"))
            fps = round(num / den, 2) if den != 0 else 0
        else:
            fps = float(fps_str)
        
        result["video"] = {
            "codec": video_stream.get("codec_name"),
            "codec_long_name": video_stream.get("codec_long_name"),
            "width": video_stream.get("width"),
            "height": video_stream.get("height"),
            "fps": fps,
            "total_frames": int(video_stream.get("nb_frames", 0)) if video_stream.get("nb_frames") else None,
            "pix_fmt": video_stream.get("pix_fmt"),
            "bit_rate": int(video_stream.get("bit_rate", 0)) if video_stream.get("bit_rate") else None,
        }
    
    if audio_stream:
        result["audio"] = {
            "codec": audio_stream.get("codec_name"),
            "codec_long_name": audio_stream.get("codec_long_name"),
            "sample_rate": int(audio_stream.get("sample_rate", 0)),
            "channels": audio_stream.get("channels"),
            "channel_layout": audio_stream.get("channel_layout"),
            "bit_rate": int(audio_stream.get("bit_rate", 0)) if audio_stream.get("bit_rate") else None,
        }
    
    return result


@mcp.tool()
def extract_frame(
    video_path: str,
    timestamp: str,
    output_path: Optional[str] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
    return_base64: bool = False
) -> dict:
    """
    Извлечь кадр из видео по указанному времени.
    
    Args:
        video_path: Путь к видеофайлу
        timestamp: Время в формате HH:MM:SS или SS (например, "00:01:30" или "90")
        output_path: Путь для сохранения кадра (по умолчанию: временный файл)
        width: Ширина выходного изображения (опционально, сохраняет пропорции)
        height: Высота выходного изображения (опционально, сохраняет пропорции)
        return_base64: Вернуть изображение в формате base64
        
    Returns:
        Словарь с путём к сохранённому кадру и опционально base64 данными
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Видеофайл не найден: {video_path}")
    
    # Определяем путь для сохранения
    if output_path is None:
        temp_dir = tempfile.gettempdir()
        output_path = os.path.join(temp_dir, f"frame_{timestamp.replace(':', '_')}.png")
    
    # Формируем команду ffmpeg
    args = [
        "-ss", timestamp,
        "-i", video_path,
        "-vframes", "1",
    ]
    
    # Добавляем масштабирование если указано
    if width or height:
        scale_w = width if width else -1
        scale_h = height if height else -1
        args.extend(["-vf", f"scale={scale_w}:{scale_h}"])
    
    args.append(output_path)
    
    run_ffmpeg(args)
    
    result = {
        "success": True,
        "output_path": output_path,
        "timestamp": timestamp,
    }
    
    if return_base64 and os.path.exists(output_path):
        with open(output_path, "rb") as f:
            result["base64"] = base64.b64encode(f.read()).decode("utf-8")
        result["mime_type"] = "image/png"
    
    return result


@mcp.tool()
def extract_frames_interval(
    video_path: str,
    interval_seconds: float = 1.0,
    output_dir: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    max_frames: int = 100
) -> dict:
    """
    Извлечь кадры из видео с заданным интервалом.
    
    Args:
        video_path: Путь к видеофайлу
        interval_seconds: Интервал между кадрами в секундах
        output_dir: Директория для сохранения кадров
        start_time: Время начала (формат HH:MM:SS или SS)
        end_time: Время окончания (формат HH:MM:SS или SS)
        max_frames: Максимальное количество кадров
        
    Returns:
        Словарь со списком путей к извлечённым кадрам
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Видеофайл не найден: {video_path}")
    
    # Создаём директорию для сохранения
    if output_dir is None:
        output_dir = tempfile.mkdtemp(prefix="video_frames_")
    else:
        os.makedirs(output_dir, exist_ok=True)
    
    # Формируем команду
    args = []
    
    if start_time:
        args.extend(["-ss", start_time])
    
    args.extend(["-i", video_path])
    
    if end_time:
        args.extend(["-to", end_time])
    
    # Фильтр для извлечения кадров с интервалом
    fps_value = 1 / interval_seconds
    args.extend([
        "-vf", f"fps={fps_value}",
        "-vframes", str(max_frames),
        os.path.join(output_dir, "frame_%04d.png")
    ])
    
    run_ffmpeg(args)
    
    # Собираем список извлечённых файлов
    frames = sorted([
        os.path.join(output_dir, f) 
        for f in os.listdir(output_dir) 
        if f.startswith("frame_") and f.endswith(".png")
    ])
    
    return {
        "success": True,
        "output_dir": output_dir,
        "frames_count": len(frames),
        "frames": frames,
        "interval_seconds": interval_seconds,
    }


@mcp.tool()
def extract_audio(
    video_path: str,
    output_path: Optional[str] = None,
    format: str = "mp3",
    bitrate: str = "192k",
    start_time: Optional[str] = None,
    end_time: Optional[str] = None
) -> dict:
    """
    Извлечь аудиодорожку из видео.
    
    Args:
        video_path: Путь к видеофайлу
        output_path: Путь для сохранения аудио (опционально)
        format: Формат аудио (mp3, wav, aac, flac, ogg)
        bitrate: Битрейт аудио (например, "128k", "192k", "320k")
        start_time: Время начала (формат HH:MM:SS или SS)
        end_time: Время окончания (формат HH:MM:SS или SS)
        
    Returns:
        Словарь с путём к извлечённому аудио
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Видеофайл не найден: {video_path}")
    
    # Определяем путь для сохранения
    if output_path is None:
        video_name = Path(video_path).stem
        temp_dir = tempfile.gettempdir()
        output_path = os.path.join(temp_dir, f"{video_name}_audio.{format}")
    
    # Формируем команду
    args = []
    
    if start_time:
        args.extend(["-ss", start_time])
    
    args.extend(["-i", video_path])
    
    if end_time:
        args.extend(["-to", end_time])
    
    # Настройки аудио кодека
    codec_map = {
        "mp3": "libmp3lame",
        "wav": "pcm_s16le",
        "aac": "aac",
        "flac": "flac",
        "ogg": "libvorbis",
    }
    
    codec = codec_map.get(format, "libmp3lame")
    
    args.extend([
        "-vn",  # Без видео
        "-acodec", codec,
    ])
    
    if format not in ["wav", "flac"]:
        args.extend(["-b:a", bitrate])
    
    args.append(output_path)
    
    run_ffmpeg(args)
    
    # Получаем размер файла
    file_size = os.path.getsize(output_path) if os.path.exists(output_path) else 0
    
    return {
        "success": True,
        "output_path": output_path,
        "format": format,
        "bitrate": bitrate,
        "file_size_bytes": file_size,
        "file_size_mb": round(file_size / (1024 * 1024), 2),
    }


@mcp.tool()
def create_gif(
    video_path: str,
    output_path: Optional[str] = None,
    start_time: str = "0",
    duration: float = 5.0,
    fps: int = 10,
    width: int = 480,
    optimize: bool = True
) -> dict:
    """
    Создать GIF из видео.
    
    Args:
        video_path: Путь к видеофайлу
        output_path: Путь для сохранения GIF (опционально)
        start_time: Время начала (формат HH:MM:SS или SS)
        duration: Длительность GIF в секундах
        fps: Частота кадров GIF
        width: Ширина GIF (высота масштабируется автоматически)
        optimize: Оптимизировать палитру для лучшего качества
        
    Returns:
        Словарь с путём к созданному GIF
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Видеофайл не найден: {video_path}")
    
    # Определяем путь для сохранения
    if output_path is None:
        video_name = Path(video_path).stem
        temp_dir = tempfile.gettempdir()
        output_path = os.path.join(temp_dir, f"{video_name}.gif")
    
    if optimize:
        # Двухпроходное создание GIF с оптимизированной палитрой
        palette_path = os.path.join(tempfile.gettempdir(), "palette.png")
        
        # Создаём палитру
        filter_complex = f"fps={fps},scale={width}:-1:flags=lanczos,palettegen"
        palette_args = [
            "-ss", start_time,
            "-t", str(duration),
            "-i", video_path,
            "-vf", filter_complex,
            palette_path
        ]
        run_ffmpeg(palette_args)
        
        # Создаём GIF с палитрой
        filter_complex = f"fps={fps},scale={width}:-1:flags=lanczos[x];[x][1:v]paletteuse"
        gif_args = [
            "-ss", start_time,
            "-t", str(duration),
            "-i", video_path,
            "-i", palette_path,
            "-filter_complex", filter_complex,
            output_path
        ]
        run_ffmpeg(gif_args)
        
        # Удаляем временную палитру
        if os.path.exists(palette_path):
            os.remove(palette_path)
    else:
        # Простое создание GIF
        filter_str = f"fps={fps},scale={width}:-1:flags=lanczos"
        args = [
            "-ss", start_time,
            "-t", str(duration),
            "-i", video_path,
            "-vf", filter_str,
            output_path
        ]
        run_ffmpeg(args)
    
    # Получаем размер файла
    file_size = os.path.getsize(output_path) if os.path.exists(output_path) else 0
    
    return {
        "success": True,
        "output_path": output_path,
        "duration": duration,
        "fps": fps,
        "width": width,
        "file_size_bytes": file_size,
        "file_size_mb": round(file_size / (1024 * 1024), 2),
        "optimized": optimize,
    }


@mcp.tool()
def get_video_duration(video_path: str) -> dict:
    """
    Получить длительность видео в различных форматах.
    
    Args:
        video_path: Путь к видеофайлу
        
    Returns:
        Словарь с длительностью в секундах и форматированном виде
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Видеофайл не найден: {video_path}")
    
    data = run_ffprobe(video_path, "-show_format")
    duration_seconds = float(data.get("format", {}).get("duration", 0))
    
    # Форматируем в HH:MM:SS
    hours = int(duration_seconds // 3600)
    minutes = int((duration_seconds % 3600) // 60)
    seconds = duration_seconds % 60
    
    formatted = f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"
    
    return {
        "duration_seconds": duration_seconds,
        "duration_formatted": formatted,
        "hours": hours,
        "minutes": minutes,
        "seconds": round(seconds, 3),
    }


def main():
    """Точка входа для запуска MCP сервера"""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
