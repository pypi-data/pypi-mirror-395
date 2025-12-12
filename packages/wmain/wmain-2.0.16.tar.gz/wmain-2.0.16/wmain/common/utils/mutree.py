from enum import Enum
from dataclasses import dataclass
from typing import Optional, List, Any, Set, Generator
from collections.abc import Mapping, Sequence, Set


class MuTreeException(Exception):
    """所有错误的父类"""
    pass


class CircularReferenceException(MuTreeException):
    pass


class UnhashableException(MuTreeException):
    pass


class NodeStructureException(MuTreeException):
    pass


@dataclass
class Key:
    key: Any


@dataclass
class Value:
    value: Any


@dataclass
class Kv:
    key: Key
    value: Value


class NodeType(Enum):
    # 仅判断节点的类型, 不考虑容器具体类型
    SEQUENCE = Sequence
    MAPPING = Mapping
    SET = Set
    KV = Kv
    KEY = Key
    VALUE = Value
    LEAF = "leaf"

    @classmethod
    def from_value(cls, value: Any) -> "NodeType":
        """根据对象类型获取 NodeType，非容器类型归为 LEAF"""
        if isinstance(value, (str, bytes)):
            return cls.LEAF

        if isinstance(value, Sequence):
            return cls.SEQUENCE
        elif isinstance(value, Mapping):
            return cls.MAPPING
        elif isinstance(value, Set):
            return cls.SET
        else:
            return cls.LEAF


class Node:
    def __init__(self,
                 parent: Optional["Node"],
                 node_type: NodeType,
                 data_type: type,
                 data: Any = None):
        self.parent = parent
        self.children: List["Node"] = []
        self.node_type = node_type
        self.data_type = data_type
        self.data = data

    @property
    def is_leaf(self) -> bool:
        return self.node_type == NodeType.LEAF

    def add_child(self, node: "Node") -> "Node":
        node.parent = self
        self.children.append(node)
        return node

    def delete(self):
        if self.parent:
            if self in self.parent.children:
                self.parent.children.remove(self)

            if self.parent.node_type in (NodeType.KEY, NodeType.VALUE, NodeType.KV):
                self.parent.delete()

    def walk(self) -> Generator["Node", None, None]:
        yield self
        for child in list(self.children):
            yield from child.walk()

    def get(self) -> Any:
        """将当前节点及其子节点还原为 Python 原生对象"""
        if self.is_leaf:
            return self.data

        # 处理字典：期望子节点是 KV 类型
        if self.node_type == NodeType.MAPPING:
            if not all(child.node_type == NodeType.KV for child in self.children):
                raise NodeStructureException(
                    "Node structure error, expect KV type"
                )
            result = {}
            for child in self.children:
                if len(child.children) != 2:
                    raise NodeStructureException(
                        "Node structure error, expect 2 children"
                    )
                k = child.children[0].get()
                v = child.children[1].get()
                if not hash(k):
                    raise UnhashableException(
                        f"Unhashable key: {k}"
                    )
                result[k] = v

            return result

        # 处理 Key/Value/Kv 包装器：透传内容
        if self.node_type in (NodeType.KEY, NodeType.VALUE):
            return self.children[0].get() if self.children else None

        if self.node_type == NodeType.KV:
            if len(self.children) == 2:
                return self.children[0].get(), self.children[1].get()
            return None

        # 处理列表/元组/集合 (依赖 data 的具体类型，保持不变)
        if self.node_type in (NodeType.SEQUENCE, NodeType.SET):
            data_list = [child.get() for child in self.children]
            return self.data_type(data_list)

        return None

    def __repr__(self):
        content = f" data={self.data} data-type={self.data_type}" if self.is_leaf else f" children_num={len(self.children)}"
        return f"<{self.__class__.__name__} type={self.node_type.name}{content}>"


class TreeBuilder:
    """负责将 Python 对象递归转换为 Node 树，处理循环引用"""

    def __init__(self):
        self._memo: Set[int] = set()

    def build(self, data: Any, parent: Optional[Node] = None) -> Node:
        # 使用 isinstance 检查是否为容器，但不再依赖 CONTAINER_TYPES 元组
        # 只要类型不是原生类型且不在 NodeType 中，就可能被识别为容器，需要 ID 检查
        is_container = (
                isinstance(data, (Mapping, Sequence, Set, Kv, Key, Value)) and
                not isinstance(data, (str, bytes))
        )
        data_id = id(data)
        data_type = type(data)

        if is_container:
            if data_id in self._memo:
                raise CircularReferenceException(
                    f"Circular reference detected, id = {data_id}"
                )
            self._memo.add(data_id)

        try:
            # 优化点 3: NodeType.from_value 已经处理了 LEAF 和 str 的判断
            node_type = NodeType.from_value(data)

            # 2. 创建当前节点
            if node_type == NodeType.LEAF:
                return Node(parent, node_type, data_type, data)

            current_node = Node(
                parent,
                node_type,
                data_type,
                data if not is_container else None
            )

            # 3. 递归构建子节点 (这里需要根据 NodeType 精确区分 MAPPING/SEQUENCE/SET 的处理方式)
            if node_type == NodeType.MAPPING:
                # MAPPING 的处理逻辑不变，因为需要 KV 包装
                for k, v in data.items():
                    kv_node = Node(current_node, NodeType.KV, data_type)
                    current_node.add_child(kv_node)

                    key_node = Node(kv_node, NodeType.KEY, data_type)
                    kv_node.add_child(key_node)
                    key_node.add_child(self.build(k, key_node))

                    val_node = Node(kv_node, NodeType.VALUE, data_type)
                    kv_node.add_child(val_node)
                    val_node.add_child(self.build(v, val_node))

            elif node_type in (NodeType.SEQUENCE, NodeType.SET):
                # SEQUENCE/SET 的处理逻辑合并：都按迭代器处理
                for item in data:
                    child = self.build(item, current_node)
                    current_node.add_child(child)

            elif node_type in (NodeType.KEY, NodeType.VALUE):
                inner_data = data.key if node_type == NodeType.KEY else data.value
                current_node.add_child(self.build(inner_data, current_node))

            return current_node

        finally:
            if is_container:
                self._memo.remove(data_id)


class MuTree:
    def __init__(self, data: Any):
        builder = TreeBuilder()
        self.root = builder.build(data)

    def walk(self):
        """
        遍历树节点
        :return: Node 类型
        """
        yield from self.root.walk()

    def get(self):
        """
        获取构造后的 python 结构
        :return:
        """
        return self.root.get()
