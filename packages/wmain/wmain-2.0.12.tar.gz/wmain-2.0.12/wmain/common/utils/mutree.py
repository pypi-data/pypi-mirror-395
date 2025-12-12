from enum import Enum
from typing import Optional, List, Any


class Key:

    def __init__(self, key):
        self.key = key


class Value:

    def __init__(self, value):
        self.value = value


class Kv:

    def __init__(self, key: Key, value: Value):
        self.key = key
        self.value = value


CONTAINER_TYPES = (list, dict, tuple, set, Kv, Key, Value)


class NodeType(Enum):
    LIST = list
    DICT = dict
    TUPLE = tuple
    SET = set
    KV = Kv
    KEY = Key
    VALUE = Value

    @classmethod
    def from_value(cls, value) -> Optional["NodeType"]:
        """安全地根据 value 取 Enum，不存在返回 None"""
        try:
            return cls(value)
        except ValueError:
            return None


class Node:

    def __init__(self, parent: Optional["Node"], data):
        self.parent = parent
        self.children: List["Node"] = []
        self.type = NodeType.from_value(type(data))
        if isinstance(self, LeafNode):
            return

        if self.type == NodeType.DICT:
            for k, v in data.items():
                self.add_child_node(Kv(Key(k), Value(v)))
        elif (
                self.type == NodeType.LIST or
                self.type == NodeType.TUPLE or
                self.type == NodeType.SET
        ):
            for v in data:
                self.add_child_node(v)
        elif self.type == NodeType.KV:
            self.add_child_node(data.key)
            self.add_child_node(data.value)
        elif self.type == NodeType.KEY:
            self.add_child_node(data.key)
        elif self.type == NodeType.VALUE:
            self.add_child_node(data.value)
        else:
            self.add_child_node(data)

    def __repr__(self):
        if isinstance(self, LeafNode):
            return f"<{self.__class__.__name__} {self.data}>"
        return f"<{self.__class__.__name__} {self.type}>"

    def add_child_node(self, data):
        if isinstance(data, CONTAINER_TYPES):
            self.children.append(Node(self, data))
        else:
            self.children.append(LeafNode(self, data))
        return self.children[-1]

    def delete(self):
        self.parent.children.remove(self)
        if (
                self.parent.type == NodeType.KEY or
                self.parent.type == NodeType.VALUE or
                self.parent.type == NodeType.KV
        ):
            self.parent.delete()

    def walk(self):
        yield self
        for child in self.children.copy():
            yield from child.walk()

    def get(self) -> Any:
        if self.type == NodeType.DICT:
            return {
                child.children[0].get(): child.children[1].get()
                for child in self.children
            }
        if self.type == NodeType.KEY or self.type == NodeType.VALUE:
            if isinstance(self, LeafNode):
                return self.data
            return self.children[0].get()
        if (
                self.type == NodeType.LIST or
                self.type == NodeType.TUPLE or
                self.type == NodeType.SET
        ):
            data = [child.get() for child in self.children]
            return self.type.value(data)

        if isinstance(self, LeafNode):
            return self.data


class LeafNode(Node):

    def __init__(self, parent: Optional["Node"], data):
        super().__init__(parent, data)
        self.data = data


class MuTree:

    def __init__(self, data):
        self.root = Node(None, None).add_child_node(data)

    def walk(self):
        yield from self.root.walk()

    def get(self):
        return self.root.get()
