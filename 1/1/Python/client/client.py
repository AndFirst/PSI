import socket
import sys
import argparse

SIZE = 1000

def send_data(message, server_address, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.sendto(message, (server_address, server_port))
        response, _ = client_socket.recvfrom(SIZE)
        print(f"Received response: {response.decode()}")

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

    parser.add_argument('--server_address', type=str, default='z35_python_server_1_1', help='Server address')
    parser.add_argument('--server_port', type=int, default=8000, help='Server port')
    parser.add_argument('--data_to_send', type=str, default=generate_valid_data(5), help='Data to send')
    
    args = parser.parse_args()
    
    message = prepare_message(args.data_to_send)
    print("Python client")
    print("Server Address:", args.server_address)
    print("Server Port:", args.server_port)
    print("Message length:", len(message))
    print("Content:", args.data_to_send)
    
    send_data(message, args.server_address, args.server_port)
