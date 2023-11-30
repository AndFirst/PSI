import socket
import argparse

SIZE = 65535


def is_data_correct(data):
    if not len(data) >= 3:
        print('too short')
        return False

    if not data[-1] == 0:
        print('no zero')
        return False        

    data_length = int.from_bytes(data[:2], byteorder='big')

    if not len(data) == data_length:
        print('not correct length')
        return False    
    payload = data[2:]
    if not all(65 <= char <= 90 for char in payload[:-1]):  
        print('not A-Z')
        return False

    for i, char in enumerate(payload[:-2]):
        if not ((payload[i + 1] - payload[i]) == 1 or (payload[i] == ord('Z') and payload[i+1] == ord('A'))):
            print('wrong order')
            return False
    return True


def log_message_recived(message, address):
    length = message[0] * 256 + message[1]
    # message_content = message[2:]
    print('-------------------------------------')
    print(f'Received message from: {address[0]}')
    print(f'Message length: {length}')
    # print(f'Message: {message_content.decode()}')
    print('-------------------------------------')


def serve(server_address, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((server_address, server_port))
        while True:
            data, client_address = server_socket.recvfrom(SIZE)
            log_message_recived(data, client_address)
            response = 'Data correct.' if is_data_correct(data) else 'Invalid data.'
            server_socket.sendto(response.encode(), client_address)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script description')
    parser.add_argument('--server_address', type=str, default='z35_python_server_1_2', help='Server address')
    parser.add_argument('--server_port', type=int, default=8000, help='Server port')

    args = parser.parse_args()

    serve(args.server_address, args.server_port)

