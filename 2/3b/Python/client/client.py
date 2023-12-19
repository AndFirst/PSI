import socket
import argparse
import time  # Import the time module for introducing delays
import random
from linked_list import LinkedList, MyData

SIZE = 1000

def send_data_chunk(chunk, client_socket):
    client_socket.sendall(chunk)
    time.sleep(1)  # Introduce a 1-second delay (you can adjust the delay as needed)

def send_data(linked_list, server_address, server_port):
    with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_address, server_port))
        
        data_to_send = linked_list.to_bytes()
        data_length = len(data_to_send) + 4
        message = data_length.to_bytes(4, byteorder='big') + data_to_send
        # message = data_to_send


        chunk_size = 10  # Set the desired chunk size
        for i in range(0, len(message), chunk_size):
            chunk = message[i:i + chunk_size]
            send_data_chunk(chunk, client_socket)

        response = client_socket.recv(SIZE)
        print(f"Received response: {response.decode()}")

def generate_valid_data(n):
    linked_list = LinkedList()
    data1 = MyData(123, "FixedString1-123", "Sample String 1")
    data2 = MyData(456, "FixedString2-456", "Another Sample String")
    data3 = MyData(321, "FixedString3-321", "3rd sample string")
    data4 = MyData(654, "FixedString4-654", "And yet another Sample String")
    data = [data1, data2, data3, data4]
    for d in data[:n]:
        linked_list.append(d)
    return linked_list

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script description')

    parser.add_argument('--server_address', type=str, default='z35_c_server_2_3', help='Server address (IPv6)')
    parser.add_argument('--server_port', type=int, default=8000, help='Server port')

    args = parser.parse_args()


    
    print("Python client")
    print("Server Address:", args.server_address)
    print("Server Port:", args.server_port)
    while 1:
        ll_size = random.randint(1, 4)   
        linked_list = generate_valid_data(ll_size)
        print("Generated List:\n")
        linked_list.display()
        print('-------------------------------------')
        send_data(linked_list, args.server_address, args.server_port)
