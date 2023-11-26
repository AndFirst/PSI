import socket
import argparse 

SIZE = 1000

def process_data(data):
    correct = True
    if not len(data) >= 2:
        correct = False
        
    data_length = int.from_bytes(data[:2], byteorder='big')

    if not len(data) == data_length + 2:
        correct = False
    
    payload = data[2:]
    if not all(65 <= char <= 90 for char in payload):  
        correct = False
        
    for i, char in enumerate(payload[:-1]):
        if not ((payload[i + 1] - payload[i]) == 1 or (payload[i] == ord('Z') and payload[i+1] == ord('A'))):
            correct = False
            break
    
    return "Data correct" if correct else "Invalid data"
    
    
       
def serve(server_address, server_port):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
            server_socket.bind((server_address, server_port))
            while True:
                    data, client_address = server_socket.recvfrom(SIZE)
                    processed_data = process_data(data)
                    server_socket.sendto(processed_data.encode(), client_address)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script description')

    parser.add_argument('--server_address', type=str, default='0.0.0.0', help='Server address')
    parser.add_argument('--server_port', type=int, default=12345, help='Server port')
    
    args = parser.parse_args()

    serve(args.server_address, args.server_port)
    
