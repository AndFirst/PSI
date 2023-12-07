import socket
import argparse
from linked_list import LinkedList, MyData

SIZE = 1000


def send_data(message, server_address, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_address, server_port))
        client_socket.sendall(message)
        response = client_socket.recv(SIZE)
        print(f"Received response: {response.decode()}")


def generate_valid_data():
    linked_list = LinkedList()
    data1 = MyData(123, "FixedString1-123", "Sample String 1")
    data2 = MyData(456, "FixedString2-456", "Another Sample String")
    data3 = MyData(321, "FixedString3-321", "3rd sample string")
    data4 = MyData(654, "FixedString4-654", "And yet another Sample String")
    linked_list.append(data1)
    linked_list.append(data2)
    linked_list.append(data3)
    linked_list.append(data4)
    return linked_list


def prepare_message(data):
    data_length = len(data) + 4
    message = data_length.to_bytes(4, byteorder='big') + data
    return message


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script description')

    parser.add_argument('--server_address', type=str, default='localhost', help='Server address')
    parser.add_argument('--server_port', type=int, default=8000, help='Server port')

    args = parser.parse_args()

    linked_list = generate_valid_data()
    data_to_send = linked_list.to_bytes()

    print("Generated List:\n")
    linked_list.display()
    print('-------------------------------------')

    message = prepare_message(data_to_send)
    print("Python client")
    print("Server Address:", args.server_address)
    print("Server Port:", args.server_port)
    print("Message length:", len(message))
    print("Content:", data_to_send)

    send_data(message, args.server_address, args.server_port)
