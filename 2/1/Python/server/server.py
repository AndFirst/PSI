import socket
import argparse
from linked_list import LinkedList, MyData

SIZE = 1000


def is_data_correct(data):
    data_length = int.from_bytes(data[:4], byteorder='big')

    if not len(data) == data_length:
        print('not correct length')
        return False

    return True


def log_message_received(message, address):
    message_length = int.from_bytes(message[:4], byteorder='big')
    message_content = message[4:]
    print(message)
    linked_list = LinkedList.from_bytes(message_content)
    print('-------------------------------------')
    print(f'Received message from: {address[0]}')
    print(f'Message length: {message_length}')
    print(f'Message: {message_content}\n')
    print("Received List:\n")
    linked_list.display()
    print('-------------------------------------')


def serve(server_address, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((server_address, server_port))
        server_socket.listen(5)
        print("Server listening on port", server_port)
        while True:
            client_socket, client_address = server_socket.accept()
            data = client_socket.recv(SIZE)
            if data:
                log_message_received(data, client_address)
                response = 'Data correct\0' if is_data_correct(data) else 'Invalid data\0'
                client_socket.sendall(response.encode())
            client_socket.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script description')
    parser.add_argument('--server_address', type=str, default='z35_python_server_2_1', help='Server address')
    parser.add_argument('--server_port', type=int, default=8000, help='Server port')

    args = parser.parse_args()

    serve(args.server_address, args.server_port)
