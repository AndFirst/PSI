import socket
import argparse
from linked_list import LinkedList, MyData
import datetime
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
    with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((server_address, server_port))
        server_socket.listen(5)
        print("Server listening on port", server_port)
        while True:
            client_socket, client_address = server_socket.accept()
            
            received_data = b''  # Accumulator for received data

            while True:
                data_chunk = client_socket.recv(SIZE)
                if not data_chunk:
                    break  # No more data, exit the loop
                
                received_data += data_chunk

                while True:
                    start = 0
                    str_len = int.from_bytes(received_data[20:24], byteorder='big')
                    # print(start, str_len)
                    node = received_data[start: 24 + str_len]
                    # print(len(node))
                    if len(node) == 24 + str_len:
                        # print("full_node")
                        received_data = received_data[24+str_len:]
                        data = MyData.unpack(node)
                        print(datetime.datetime.now())
                        print(data)
                    if len(node) < 24 + str_len:
                        break

                # Check if the complete message has been received
                # if len(received_data) >= 4:
                #     message_length = int.from_bytes(received_data[:4], byteorder='big')
                #     if len(received_data) >= message_length:
                #         break  # Complete message received, exit the loop
            
            # log_message_received(received_data, client_address)

            # response = 'Data correct\0' if is_data_correct(received_data) else 'Invalid data\0'
            # client_socket.sendall(response.encode())
            
            # client_socket.close()




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script description')
    parser.add_argument('--server_address', type=str, default='::1', help='Server address (IPv6)')
    parser.add_argument('--server_port', type=int, default=8000, help='Server port')

    args = parser.parse_args()

    serve(args.server_address, args.server_port)
