import hashlib
import os
import subprocess


def calculate_file_hash(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as file:
        while chunk := file.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()


def get_video_length(video_path):
    return 1000


def should_generate_hls(mp4_path, m3u8_path):
    if not os.path.exists(m3u8_path):
        return True

    mp4_mtime = os.path.getmtime(mp4_path)
    m3u8_mtime = os.path.getmtime(m3u8_path)

    return mp4_mtime > m3u8_mtime


def generate_hls(videoname, quality):
    videoname = videoname.split('/')[-1]
    file_dir = os.path.dirname(os.path.abspath(__file__))
    hls_directory = f'{file_dir}/static/{videoname}'
    mp4_path = f'media/{videoname}'

    width = quality * 16.0 / 9.0
    height = quality

    quality_dir = f"{hls_directory}/{quality}p"
    quality_m3u8 = f"{quality_dir}/hls.m3u8"

    os.makedirs(quality_dir, exist_ok=True)

    if should_generate_hls(mp4_path, quality_m3u8):
        video_bitrate = max(int(quality / 480 * 2000), 500)
        audio_bitrate = max(int(quality / 480 * 128), 64)

        subprocess.run([
            'ffmpeg', '-i', mp4_path,
            '-vf', f"scale={width}:{height}",
            '-c:a', 'aac',
            '-b:a', f'{audio_bitrate}k',
            '-c:v', 'h264',
            '-b:v', f'{video_bitrate}k',
            '-hls_time', '6',
            '-hls_playlist_type', 'vod',
            '-hls_list_size', '0',
            '-hls_segment_filename', f"{quality_dir}/hls-%03d.ts",
            '-f', 'hls', quality_m3u8
        ])
