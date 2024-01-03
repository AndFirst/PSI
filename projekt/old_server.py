import cv2
import socket
import struct
import pickle
import threading

# Ustawienia serwera
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345

# Inicjalizacja serwera
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(5)

print(f"Serwer nasłuchuje na {SERVER_IP}:{SERVER_PORT}")

# Otwarcie pliku wideo
video_path = 'sample.mp4'

# Funkcja do przesyłania klatek do klienta


def send_frames(conn):
    video_capture = cv2.VideoCapture(video_path)
    while True:
        success, frame = video_capture.read()
        if not success:
            break

        # Konwersja klatki na bajty
        _, frame_data = cv2.imencode('.jpeg', frame)
        frame_bytes = pickle.dumps(frame_data, protocol=4)

        # Wysłanie rozmiaru klatki do klienta
        data_size = struct.pack("L", len(frame_bytes))
        conn.sendall(data_size)

        # Wysłanie samej klatki do klienta
        conn.sendall(frame_bytes)

    # Wysyłanie sygnału końca transmisji
    conn.sendall(struct.pack("L", 0))
    conn.close()
    video_capture.release()


# Oczekiwanie na połączenie klienta
while True:
    client_conn, addr = server_socket.accept()
    print(f"Nowe połączenie od {addr}")

    # Rozpoczęcie przesyłania klatek do klienta w osobnym wątku
    frame_sender_thread = threading.Thread(
        target=send_frames, args=(client_conn,))
    frame_sender_thread.start()
