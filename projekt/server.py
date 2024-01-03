import argparse
import socket
import json
import logging
from typing import Dict

from data_structures import VideoDescriptor, AvaliabilityResponse


class Server:
    def __init__(self, coordinator_host: str, coordinator_port: int, server_id: int) -> None:
        self._coordinator_host: str = coordinator_host
        self._coordinator_port: int = coordinator_port
        self._server_id: int = server_id

        self._movies_location: Dict[VideoDescriptor, str] = {}

        # Create a logger with a custom format
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s [SERVER %(server_id)s] %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.logger = logging.getLogger(__name__)
        self.logger = logging.LoggerAdapter(
            self.logger, {'server_id': self._server_id})
        self.init_params()

    def init_params(self):
        self._movies_location.update(
            {VideoDescriptor("chuj", 123): "sample.mp4"})

    def run(self, host: str, port: int) -> None:
        # Create a TCP/IP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            # Bind the socket to a specific address and port
            server_address = (host, port)
            server_socket.bind(server_address)

            # Listen for incoming connections
            server_socket.listen(1)
            self.logger.info(f"Listening on {host}:{port}")
            try:
                while True:
                    # Wait for a connection
                    self.logger.info("Waiting for a connection...")
                    client_socket, client_address = server_socket.accept()
                    self.logger.info(
                        f"Accepted connection from {client_address}")

                    # Handle the client connection
                    self.handle_client(client_socket)

            except KeyboardInterrupt:
                self.logger.info("Shutting down.")

    def handle_client(self, client_socket: socket.socket):
        # Receive data from the coordinator
        data = client_socket.recv(1024)
        if not data:
            return

        # Deserialize the received data (assuming it's in JSON format)
        video_descriptor_data = json.loads(data.decode('utf-8'))

        # Display the received VideoDescriptor
        self.logger.info(f"Received VideoDescriptor: {video_descriptor_data}")

        # Check if the received video descriptor is in self._movies_location
        received_descriptor = VideoDescriptor(**video_descriptor_data)
        if received_descriptor in self._movies_location:
            video_location = self._movies_location[received_descriptor]
            self.logger.info(
                f"VideoDescriptor found in the coordinator's database. Location: {video_location}")

            # Send a response to the coordinator indicating file presence
            response_data = {"avaliable": True, "location": video_location}
            response = AvaliabilityResponse(**response_data)
            response_message = json.dumps(response.__dict__)
            client_socket.sendall(response_message.encode('utf-8'))
        else:
            self.logger.warning(
                "VideoDescriptor not found in the coordinator's database.")

            # Send a response to the coordinator indicating file absence
            response_data = {"avaliable": False, "location": None}
            response = AvaliabilityResponse(**response_data)
            response_message = json.dumps(response.__dict__)
            client_socket.sendall(response_message.encode('utf-8'))


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
    server.run(server_host, server_port)
