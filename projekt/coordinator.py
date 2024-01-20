from re import S, T
from typing import Dict, List
import socket
import argparse
import json
from data_structures import AvaliabilityResponse, ServerInfo, VideoDescriptor, VideoKey
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests


class Coordinator:
    def __init__(self) -> None:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [COORDINATOR] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
        self._servers: List[ServerInfo] = []
        self._movies: Dict[VideoKey, VideoDescriptor] = {}

        self.init_params()

        app = Flask(__name__)
        CORS(app)

        @app.route('/add_video/', methods=['POST'])
        def add_video():
            try:
                data = request.get_json()
                video_descriptor = VideoDescriptor(**data)
                video_key = VideoKey(**data)
                self._movies[video_key] = video_descriptor
                return jsonify(data)
            except Exception as e:
                logging.info(e)
                return jsonify({'error': str(e)}), 400

        @app.route('/servers/', methods=['POST'])
        def get_servers():
            try:
                data = request.get_json()
                logging.info(data)

                video_key, video_descriptor = self.extract_video_info(data)

                if video_descriptor is None:
                    return jsonify({'error': 'File not found.'}), 404

                available_servers = self.find_available_servers(
                    video_descriptor)
                serialized_servers = [server.__dict__
                                      for server in available_servers]
                logging.info(serialized_servers)

                return jsonify(serialized_servers)

            except Exception as e:
                logging.info(e)
                return jsonify({'error': str(e)}), 400
        self.app = app

    def extract_video_info(self, data):
        video_key = VideoKey(**data)
        video_descriptor = self._movies.get(video_key)
        return video_key, video_descriptor

    def find_available_servers(self, video_descriptor):
        serialized_data = json.dumps(video_descriptor.__dict__)
        available_servers = []

        for server in self._servers:
            url = f"http://{server.address}:{server.port}/availability/"
            headers = {'Content-Type': 'application/json'}
            try:
                response = self.check_server_availability(
                    url, serialized_data, headers)
                response = AvaliabilityResponse(**response.json())
                logging.info(f"Received response: {response}")

                if response.avaliable:
                    available_servers.append(server)
            except Exception as e:
                logging.info(e)

        return available_servers

    def check_server_availability(self, url, data, headers):
        return requests.post(url, data=data, headers=headers)

    def init_params(self) -> None:
        self._movies.update(
            {VideoKey("video", 720): VideoDescriptor(hash='7a61d0db03466273ba38ea8663dcc25ae7298621135622a653bf2b9b39fee559', length=1000)})

        self._servers.append(ServerInfo("127.0.0.1", 5001))
        self._servers.append(ServerInfo("127.0.0.1", 5002))
        # self._servers.append(ServerInfo("127.0.0.1", 5003))


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Your script description here.")
    parser.add_argument("--coordinator_host", default="127.0.0.1",
                        help="The host address to connect the coordinator.")
    parser.add_argument("--coordinator_port", type=int, default=12345,
                        help="The port number to connect the coordinator.")

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    coordinator_host = args.coordinator_host
    coordinator_port = args.coordinator_port
    coordinator = Coordinator()
    coordinator.app.run(coordinator_host, coordinator_port, debug=True)
