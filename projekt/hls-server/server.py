from flask import Flask, send_from_directory
from flask_cors import CORS
import subprocess
import argparse
import os
import hashlib
import argparse
from re import T
import logging
from typing import Dict
from flask import Flask, jsonify, request
from flask_cors import CORS
from data_structures import VideoDescriptor, AvaliabilityResponse
import os


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [SERVER] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class Server:
    def __init__(self, coordinator_host: str, coordinator_port: int, server_id: int, config) -> None:
        self._coordinator_host: str = coordinator_host
        self._coordinator_port: int = coordinator_port
        self._server_id: int = server_id

        self._movies_location: Dict[VideoDescriptor, str] = {}
        self.config = config

        self.init_params()

        app = Flask(__name__)
        CORS(app)

        @app.route('/availability/', methods=['POST'])
        def get_file_location():
            try:
                data = request.get_json()
                received_descriptor = VideoDescriptor(**data)
                logging.info(
                    f'Received descriptior: {received_descriptor}')
                if received_descriptor in self._movies_location:
                    video_location = self._movies_location[received_descriptor]
                    logging.info(
                        f"VideoDescriptor found in the coordinator's database. Location: {video_location}")

                    # Send a response to the coordinator indicating file presence
                    response_data = {"avaliable": True,
                                     "location": video_location}
                    response = AvaliabilityResponse(**response_data)
                    logging.info(f'Response: {jsonify(response)}')
                    return jsonify(response)

            except Exception as e:
                logging.warning(str(e))
                return jsonify({'error': str(e)}), 400

        @app.route('/<string:videoname>/<string:quality>/hls.m3u8')
        def hls_playlist(videoname, quality):
            file_dir = os.path.dirname(os.path.abspath(__file__))
            logging.info(file_dir)
            return send_from_directory(f'{file_dir}/static/{videoname}/{quality}', 'hls.m3u8')

        @app.route('/<string:videoname>/<string:quality>/<path:filename>')
        def hls_stream(videoname, quality, filename):
            file_dir = os.path.dirname(os.path.abspath(__file__))
            logging.info(file_dir)
            return send_from_directory(f'{file_dir}/static/{videoname}/{quality}', filename)

        self.app = app

    def init_params(self):
        self._movies_location.update(
            {VideoDescriptor("chuj", 123): "sample.mp4"})


def should_generate_hls(mp4_path, m3u8_path):
    if not os.path.exists(m3u8_path):
        return True

    mp4_mtime = os.path.getmtime(mp4_path)
    m3u8_mtime = os.path.getmtime(m3u8_path)

    return mp4_mtime > m3u8_mtime


def generate_hls(videoname, qualities):
    file_dir = os.path.dirname(os.path.abspath(__file__))
    hls_directory = f'{file_dir}/static/{videoname}'
    mp4_path = f'{file_dir}/media/{videoname}.mp4'

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


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Your script description here.")
    parser.add_argument("--coordinator_host", default="127.0.0.1",
                        help="The host address to connect the coordinator.")
    parser.add_argument("--coordinator_port", type=int, default=12345,
                        help="The port number to connect the coordinator.")
    parser.add_argument("--server_host", default="127.0.0.1",
                        help="The host address to run the server.")
    parser.add_argument("--server_port", type=int, default=12345,
                        help="The port number to run the server.")
    parser.add_argument("--server_id", type=int, default=1,
                        help="The identifier of the server.")
    parser.add_argument('--videonames', nargs='+', type=str, default=[
                        'video', 'video2'], help='List of input video names (without extension)')
    parser.add_argument('--qualities', nargs='+', type=int,
                        default=[144, 240, 360, 720], help='List of supported qualities')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    coordinator_host = args.coordinator_host
    coordinator_port = args.coordinator_port
    server_host = args.server_host
    server_port = args.server_port
    server_id = args.server_id
    videonames = args.videonames
    qualities = args.qualities

    for videoname in videonames:
        generate_hls(videoname, qualities)

    config = {}
    config['videonames'] = videonames
    config['qualities'] = qualities

    server = Server(coordinator_host, coordinator_port, server_id, config)
    server.app.run(server_host, server_port, debug=True)
