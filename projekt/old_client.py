import threading
from queue import Queue
import pickle
import struct
import socket
import cv2

# Ustawienia klienta
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345


def receive_frames(frame_queue):
    while True:
        # Odbierz rozmiar klatki
        data_size = client_socket.recv(8)
        if not data_size:
            break

        frame_size = struct.unpack("L", data_size)[0]

        # Zakończ transmisję, jeśli rozmiar klatki wynosi 0
        if frame_size == 0:
            frame_queue.put("END")
            break

        # Odbierz klatkę
        frame_data = b""
        while len(frame_data) < frame_size:
            remaining_size = frame_size - len(frame_data)
            frame_chunk = client_socket.recv(
                4096 if remaining_size > 4096 else remaining_size)
            if not frame_chunk:
                break
            frame_data += frame_chunk

        # Zdekoduj klatkę i dodaj do kolejki
        frame = pickle.loads(frame_data, fix_imports=False, encoding="bytes")
        frame_queue.put(frame)

    # Zamknij połączenie po zakończeniu transmisji
    print("Zakończono buforowanie")
    client_socket.close()


# Funkcja do wyświetlania klatek


def display_frames(frame_queue):
    while True:
        if not frame_queue.empty():
            frame = frame_queue.get()

            if type(frame) == str and frame == "END":
                break

            # Wyświetl klatkę za pomocą OpenCV
            cv2.imshow('Received Frame', cv2.imdecode(frame, cv2.IMREAD_COLOR))

            # Ustaw opóźnienie na 40 ms (25 fps)
            if cv2.waitKey(1000//25) & 0xFF == ord('q'):
                break


if __name__ == '__main__':

    # Inicjalizacja klienta
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))

    # Kolejka do przechowywania klatek
    frame_queue = Queue()

    # Rozpocznij wątek odbierający klatki
    receive_thread = threading.Thread(
        target=receive_frames, args=[frame_queue,])
    receive_thread.start()

    # Rozpocznij wątek wyświetlający klatki
    display_thread = threading.Thread(
        target=display_frames, args=[frame_queue,])
    display_thread.start()

    # Czekaj na zakończenie wątków
    receive_thread.join()
    display_thread.join()

    # Zakończ działanie klienta po zamknięciu okna
    print("Zamykanie klienta.")
    client_socket.close()
