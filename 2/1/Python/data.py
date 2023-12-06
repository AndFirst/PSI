import json
from dataclasses import dataclass


@dataclass
class MyData:
    int_value: int
    variable_string: str
    fixed_string: str


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

    def to_dict(self):
        data = []
        current = self.head
        while current:
            data.append({
                "int_value": current.data.int_value,
                "variable_string": current.data.variable_string,
                "fixed_string": current.data.fixed_string
            })
            current = current.next
        return data

    def from_dict(self, data):
        for item in data:
            data_obj = MyData(item['int_value'], item['variable_string'], item['fixed_string'])
            self.append(data_obj)

    def to_json(self):
        return json.dumps(self.to_dict())

    def from_json(self, serialized_data):
        deserialized_data = json.loads(serialized_data)
        self.from_dict(deserialized_data)
