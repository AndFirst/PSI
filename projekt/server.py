import argparse
from re import T
import logging
from typing import Dict
from flask import Flask, jsonify, request
from flask_cors import CORS
from data_structures import VideoDescriptor, AvaliabilityResponse

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [SERVER] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class Server:
    def __init__(self, coordinator_host: str, coordinator_port: int, server_id: int) -> None:
        self._coordinator_host: str = coordinator_host
        self._coordinator_port: int = coordinator_port
        self._server_id: int = server_id

        self._movies_location: Dict[VideoDescriptor, str] = {}

        self.init_params()

        app = Flask(__name__)
        CORS(app)

        @app.route('/', methods=['POST'])
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

        self.app = app

    def init_params(self):
        self._movies_location.update(
            {VideoDescriptor("chuj", 123): "sample.mp4"})


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
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    coordinator_host = args.coordinator_host
    coordinator_port = args.coordinator_port
    server_host = args.server_host
    server_port = args.server_port
    server_id = args.server_id

    server = Server(coordinator_host, coordinator_port, server_id)
    server.app.run(server_host, server_port, debug=True)
