from flask import Flask, send_from_directory, Response
from flask_cors import CORS
import subprocess
import os


app = Flask(__name__)
CORS(app)


@app.route('/hls.m3u8')
def hls_playlist():
    hls_directory = 'static'
    # Generate HLS playlist using ffmpeg
    if not os.path.exists(hls_directory):
        os.makedirs(hls_directory)
    subprocess.run([
        'ffmpeg', '-i', 'media/video2.mp4',
        '-c:v', 'libx264',
        '-hls_time', '6',  # Decreased HLS segment duration to 6 seconds
        '-hls_list_size', '0',  # This ensures all segments are referenced in the playlist
        '-f', 'hls', f'{hls_directory}/hls.m3u8'
    ])
    return send_from_directory('static', 'hls.m3u8')


@app.route('/<path:filename>')
def hls_stream(filename):
    return send_from_directory('static', filename)


if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app
