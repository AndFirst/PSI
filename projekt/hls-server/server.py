from flask import Flask, send_from_directory
from flask_cors import CORS
import subprocess
import argparse
import os


app = Flask(__name__)
CORS(app)

app.static_folder = 'static'


def should_generate_hls(mp4_path, m3u8_path):
    if not os.path.exists(m3u8_path):
        return True

    mp4_mtime = os.path.getmtime(mp4_path)
    m3u8_mtime = os.path.getmtime(m3u8_path)

    return mp4_mtime > m3u8_mtime


@app.route('/<path:filename>.m3u8')
def hls_playlist(filename):
    hls_directory = 'static'
    mp4_path = f'media/{filename}.mp4'
    m3u8_path = f'{hls_directory}/{filename}.m3u8'

    os.makedirs(hls_directory, exist_ok=True)

    if should_generate_hls(mp4_path, m3u8_path):
        subprocess.run([
            'ffmpeg', '-i', mp4_path,
            '-c:v', 'libx264',
            '-hls_time', '6',  # Decreased HLS segment duration to 6 seconds
            '-hls_list_size', '0',
            '-f', 'hls', m3u8_path
        ])

    return send_from_directory('static', f'{filename}.m3u8')


@app.route('/<path:filename>')
def hls_stream(filename):
    return send_from_directory('static', filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the Flask app with an optional port argument.')
    parser.add_argument('--port', type=int, default=5000, help='Port number for the server (default: 5000)')
    args = parser.parse_args()

    app.run(debug=True, port=args.port)
