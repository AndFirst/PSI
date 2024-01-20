from flask import Flask, send_from_directory
from flask_cors import CORS
import subprocess
import argparse
import os
import hashlib


app = Flask(__name__)
CORS(app)


def should_generate_hls(mp4_path, m3u8_path):
    if not os.path.exists(m3u8_path):
        return True

    mp4_mtime = os.path.getmtime(mp4_path)
    m3u8_mtime = os.path.getmtime(m3u8_path)

    return mp4_mtime > m3u8_mtime


def generate_hls(videoname, qualities):
    hls_directory = f'static/{videoname}'
    mp4_path = f'media/{videoname}.mp4'

    for quality in qualities:
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


@app.route('/<string:videoname>/<string:quality>/hls.m3u8')
def hls_playlist(videoname, quality):
    return send_from_directory(f'static/{videoname}/{quality}', 'hls.m3u8')


@app.route('/<string:videoname>/<string:quality>/<path:filename>')
def hls_stream(videoname, quality, filename):
    return send_from_directory(f'static/{videoname}/{quality}', filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the Flask app with an optional port argument.')
    parser.add_argument('--port', type=int, default=5000, help='Port number for the server (default: 5000)')
    parser.add_argument('--videonames', nargs='+', type=str, default=['video', 'video2'], help='List of input video names (without extension)')
    parser.add_argument('--qualities', nargs='+', type=int, default=[144, 240, 360, 720], help='List of supported qualities')
    args = parser.parse_args()

    videonames = args.videonames
    qualities = args.qualities

    for videoname in videonames:
        generate_hls(videoname, qualities)

    app.config['videonames'] = videonames
    app.config['qualities'] = qualities
    app.run(debug=True, port=args.port)
