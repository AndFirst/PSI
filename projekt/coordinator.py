from typing import Dict, List
import socket
import argparse
import json
from data_structures import AvaliabilityResponse, ServerInfo, VideoDescriptor, VideoKey
import logging


class Coordinator:
    def __init__(self) -> None:
        self._servers: List[ServerInfo] = []
        self._movies: Dict[VideoKey, VideoDescriptor] = {}

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [COORDINATOR] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.init_params()

    def init_params(self) -> None:
        self._movies.update(
            {VideoKey("sample.mp4", 720): VideoDescriptor("chuj", 123)})

        self._servers.append(ServerInfo("127.0.0.1", 12346))
        self._servers.append(ServerInfo("127.0.0.1", 12347))
        self._servers.append(ServerInfo("127.0.0.1", 12348))

    def run(self, host: str, port: int) -> None:
        # Create a TCP/IP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            # Bind the socket to a specific address and port
            server_address = (host, port)
            server_socket.bind(server_address)

            # Listen for incoming connections
            server_socket.listen(1)
            logging.info(f"Listening on {host}:{port}")

            try:
                while True:
                    # Wait for a connection
                    logging.info("Waiting for a connection...")
                    client_socket, client_address = server_socket.accept()
                    logging.info(f"Accepted connection from {client_address}")

                    self.handle_client(client_socket)

            except KeyboardInterrupt:
                logging.info("Shutting down.")

    def handle_client(self, client_socket):
        # Receive data from the client
        data = client_socket.recv(1024)
        if not data:
            return

        # Deserialize the received data (assuming it's in JSON format)
        video_key_data = json.loads(data.decode('utf-8'))
        video_key = VideoKey(**video_key_data)

        # Display the received VideoKey
        logging.info(f"Received VideoKey: {video_key}")
        video_descriptor = self._movies.get(video_key)

        if video_descriptor:
            successful_servers = self.send_video_key_to_servers(
                video_descriptor)
            self.send_server_list_to_client(client_socket, successful_servers)
        else:
            logging.warning(
                "VideoKey not found in the coordinator's database.")

    def send_server_list_to_client(self, client_socket, server_list):
        # Convert the list of servers to a JSON string
        serialized_server_list = json.dumps(
            [server.__dict__ for server in server_list])

        # Send the server list to the client
        client_socket.sendall(serialized_server_list.encode('utf-8'))

    def send_video_key_to_servers(self, video_descriptor):
        serialized_data = json.dumps(video_descriptor.__dict__)

        successful_servers = []  # List to track servers that responded positively

        for server in self._servers:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_address = (server.address, server.port)

                try:
                    server_socket.connect(server_address)
                    server_socket.sendall(serialized_data.encode('utf-8'))
                    logging.info(
                        f"Sent data to server {server.address}:{server.port}")

                    # Receive response from the server
                    response_data = server_socket.recv(1024)
                    response_dict = json.loads(response_data.decode('utf-8'))

                    # Convert the response data into a CoordinatorResponse object
                    response = AvaliabilityResponse(**response_dict)

                    if response.avaliable:
                        successful_servers.append(server)

                except Exception as e:
                    logging.error(
                        f"Failed to send data to server {server.address}:{server.port}: {e}")
                finally:
                    server_socket.close()

        return successful_servers


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Your script description here.")
    parser.add_argument("--host", default="127.0.0.1",
                        help="The host address to run the coordinator on.")
    parser.add_argument("--port", type=int, default=12345,
                        help="The port number to run the coordinator on.")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    host = args.host
    port = args.port

    coordinator = Coordinator()
    coordinator.run(host, port)
