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
    for i in range(length):
        letter = alphabet[i % 26]
        result += letter

    return result

def prepare_message(data):
    data_length = len(data)  
    message = data_length.to_bytes(2, byteorder='big') + data.encode()    
    return message


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script description')

    parser.add_argument('--server_address', type=str, default='192.168.1.192', help='Server address')
    parser.add_argument('--server_port', type=int, default=12345, help='Server port')
    parser.add_argument('--data_to_send', type=str, default=generate_valid_data(998), help='Data to send')
    
    args = parser.parse_args()
    
    message = prepare_message(args.data_to_send)
    
    print("Server Address:", args.server_address)
    print("Server Port:", args.server_port)
    print("Data to Send:", args.data_to_send)
    print("Encoded data:", message)
    
    send_data(message, args.server_address, args.server_port)
