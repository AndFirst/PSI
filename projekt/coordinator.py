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

        @app.route('/servers/', methods=['POST'])
        def get_servers():
            try:
                data = request.get_json()
                logging.info(data)
                video_key = VideoKey(**data)
                video_descriptor = self._movies.get(video_key)
                serialized_data = json.dumps(video_descriptor.__dict__)
                if video_descriptor is None:
                    return jsonify({'error': 'File not found.'}), 404

                avaliable_servers = []
                for server in self._servers:
                    url = f"http://{server.address}:{server.port}/"
                    headers = {'Content-Type': 'application/json'}
                    response = requests.post(
                        url, data=serialized_data, headers=headers)
                    response = AvaliabilityResponse(**response.json())
                    logging.info(f"Received response: {response}")
                    if response.avaliable:
                        avaliable_servers.append(server)
                serialized_servers = [
                    server.__dict__ for server in avaliable_servers]

                return jsonify(serialized_servers)

            except Exception as e:
                return jsonify({'error': str(e)}), 400

        self.app = app

    def init_params(self) -> None:
        self._movies.update(
            {VideoKey("sample.mp4", 720): VideoDescriptor("chuj", 123)})

        self._servers.append(ServerInfo("127.0.0.1", 5001))
        self._servers.append(ServerInfo("127.0.0.1", 5002))
        self._servers.append(ServerInfo("127.0.0.1", 5003))


if __name__ == "__main__":
    coordinator = Coordinator()
    coordinator.app.run(debug=True)
