import socket
import argparse

SIZE = 1024


def send_data(message, server_address, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.sendto(message, (server_address, server_port))
        response, _ = client_socket.recvfrom(SIZE)
        print(f"Received response: {response}")


def generate_valid_data(length):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    result = ''
    for i in range(length-3):
        letter = alphabet[i % 26]
        result += letter

    return result


def prepare_message(data):
    data = data + '\0'
    data_length = len(data) + 2
    message = data_length.to_bytes(2, byteorder='big') + data.encode()
    return message


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script description')

    parser.add_argument('--server_address', type=str, default='127.0.0.1', help='Server address')
    parser.add_argument('--server_port', type=int, default=8000, help='Server port')
    parser.add_argument('--max_data_size', type=int, default=1000, help='Maximum data size to send')

    args = parser.parse_args()

    print("Python client")
    print("Server Address:", args.server_address)
    print("Server Port:", args.server_port)

    for size in range(0, args.max_data_size + 1):
        data_to_send = generate_valid_data(size)
        message = prepare_message(data_to_send)
        print("Message length:", len(message))

        send_data(message, args.server_address, args.server_port)
