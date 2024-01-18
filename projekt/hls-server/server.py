from flask import Flask, send_from_directory
from flask_cors import CORS
import subprocess
import argparse
import os


app = Flask(__name__)
CORS(app)


def should_generate_hls(mp4_path, m3u8_path):
    if not os.path.exists(m3u8_path):
        return True

    mp4_mtime = os.path.getmtime(mp4_path)
    m3u8_mtime = os.path.getmtime(m3u8_path)

    return mp4_mtime > m3u8_mtime


@app.route('/<path:videoname>/hls.m3u8')
def hls_playlist(videoname):
    hls_directory = f'static/{videoname}'
    mp4_path = f'media/{videoname}.mp4'
    m3u8_path = f'{hls_directory}/hls.m3u8'

    os.makedirs(hls_directory, exist_ok=True)

    if should_generate_hls(mp4_path, m3u8_path):
        subprocess.run([
            'ffmpeg', '-i', mp4_path,
            '-c:v', 'libx264',
            '-hls_time', '6',  # Decreased HLS segment duration to 6 seconds
            '-hls_list_size', '0',
            '-f', 'hls', m3u8_path
        ])

    return send_from_directory(f'static/{videoname}', 'hls.m3u8')


@app.route('/<path:videoname>/<path:filename>')
def hls_stream(videoname, filename):
    return send_from_directory(f'static/{videoname}', filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the Flask app with an optional port argument.')
    parser.add_argument('--port', type=int, default=5000, help='Port number for the server (default: 5000)')
    args = parser.parse_args()

    app.run(debug=True, port=args.port)
