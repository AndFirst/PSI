import argparse
from data_structures import ServerInfo, VideoKey
import json
import socket
import logging
from datetime import datetime


class Client:
    def __init__(self, coordinator_host: str, coordinator_port: int, client_id: int) -> None:
        self._coordinator_host: str = coordinator_host
        self._coordinator_port: int = coordinator_port
        self._client_id: int = client_id

        # Create a logger with a custom format
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s [Client %(client_id)s] %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.logger = logging.getLogger(__name__)
        self.logger = logging.LoggerAdapter(
            self.logger, {'client_id': self._client_id})

    def run(self, video_name: str, video_quality: int) -> None:
        video_key: VideoKey = VideoKey(video_name, video_quality)
        serialized_data: str = json.dumps(video_key.__dict__)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            coordinator_address = (
                self._coordinator_host, self._coordinator_port)

            # Connect to the coordinator
            client_socket.connect(coordinator_address)

            self.logger.info(
                f"Connected to the coordinator at {coordinator_address}")

            # Send the serialized data to the coordinator
            client_socket.sendall(serialized_data.encode('utf-8'))

            server_list_data = client_socket.recv(1024)
            if not server_list_data:
                self.logger.warning(
                    "No server list received from the coordinator.")
                return

            # Deserialize the received server list
            server_list = [ServerInfo(**server_data)
                           for server_data in json.loads(server_list_data.decode('utf-8'))]

            # Display the received server list using logger
            self.logger.info("Received server list:")
            for server in server_list:
                self.logger.info(f"Server {server.address}:{server.port}")

            # Close the client socket
            client_socket.close()


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Your script description here.")
    parser.add_argument("--coordinator_host", default="127.0.0.1",
                        help="The host address to connect the coordinator.")
    parser.add_argument("--coordinator_port", type=int, default=12345,
                        help="The port number to connect the coordinator.")
    parser.add_argument('--video_name', type=str, default='sample.mp4',
                        help="The name of video you want to see.")
    parser.add_argument('--video_quality', type=int, default=720,
                        help="The quality of video you want to see.")
    parser.add_argument('--client_id', type=int, default=1,
                        help="The identifier of the client.")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    coordinator_host = args.coordinator_host
    coordinator_port = args.coordinator_port
    video_name = args.video_name
    video_quality = args.video_quality
    client_id = args.client_id

    client = Client(coordinator_host, coordinator_port, client_id)
    client.run(video_name, video_quality)
