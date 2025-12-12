from pydantic import ConfigDict, BaseModel

from wmain.common.utils.string import normalize_field_name
from wmain.common.utils.mutree import MuTree, NodeType

DEFAULT_ALIAS_CONFIG = ConfigDict(
    validate_by_name=True,
    validate_by_alias=True,
    extra="ignore",
    str_strip_whitespace=True,
    alias_generator=normalize_field_name
)


class LooseModel(BaseModel):
    model_config = DEFAULT_ALIAS_CONFIG

    @classmethod
    def from_any_dict(cls, data: dict) -> "LooseModel":
        if not isinstance(data, dict):
            raise TypeError(f"Expected dict, got {type(data)}")

        tree = MuTree(data)
        for node in tree.walk():
            if (
                node.parent is not None and
                node.parent.node_type == NodeType.KEY and
                node.data_type is str
            ):
                node.data = normalize_field_name(node.data)
        return cls(**tree.get())
