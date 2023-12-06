import struct
from dataclasses import dataclass


@dataclass
class MyData:
    int_value: int
    fixed_string: str
    variable_string: str

    def pack(self) -> bytes:
        fixed_string_padded = self.fixed_string.ljust(16)[:16]
        variable_string_bytes = self.variable_string.encode('utf-8')
        packed_data = struct.pack(f"!i16sI{len(variable_string_bytes)}s",
                                  self.int_value,
                                  fixed_string_padded.encode('utf-8'),
                                  len(variable_string_bytes),
                                  variable_string_bytes)
        return packed_data

    @classmethod
    def unpack(cls, packed_data: bytes):
        unpacked_data = struct.unpack("!i16sI", packed_data[:struct.calcsize("!i16sI")])
        int_value, fixed_string_padded, variable_string_length = unpacked_data
        fixed_string = fixed_string_padded.decode('utf-8').rstrip('\x00')
        variable_string = struct.unpack(f"{variable_string_length}s",
                                        packed_data[struct.calcsize("!i16sI"):])[0].decode('utf-8')
        return cls(int_value, fixed_string, variable_string)


class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def display(self):
        current = self.head
        while current:
            print(current.data)
            current = current.next

    def to_bytes(self):
        bytes_list = b""
        current = self.head
        while current:
            bytes_list += current.data.pack()
            current = current.next
        return bytes_list

    @staticmethod
    def from_bytes(data):
        ll = LinkedList()
        while data:
            node_header_size = struct.calcsize("!i16sI")

            node_data = data[:node_header_size]
            _, _, variable_length = struct.unpack("!i16sI", node_data)
            total_node_size = node_header_size + variable_length

            node_data = data[:total_node_size]
            ll.append(MyData.unpack(node_data))
            data = data[total_node_size:]
        return ll
