from typing import get_origin

from pydantic import ConfigDict, BaseModel

from wmain.common.utils.string import normalize_field_name

DEFAULT_ALIAS_CONFIG = ConfigDict(
    validate_by_name=True,
    validate_by_alias=True,
    extra="ignore",
    str_strip_whitespace=True,
    alias_generator=normalize_field_name
)


class BaseAliasModel(BaseModel):
    model_config = DEFAULT_ALIAS_CONFIG

    @classmethod
    def from_any_dict(cls, data: dict) -> "BaseAliasModel":
        if not isinstance(data, dict):
            raise TypeError(f"Expected dict, got {type(data)}")

        normalized_data: dict = {}

        # 遍历当前 Model 的所有字段
        for field_name, field_info in cls.model_fields.items():
            raw_key = field_name
            alias_key = normalize_field_name(field_name)  # 用来匹配 JSON 中的 key

            # 从原始 dict 中找匹配的 key（支持任意大小写/下划线/连字符）
            value = None
            for k, v in data.items():
                if normalize_field_name(k) == alias_key:
                    value = v
                    break
            if value is None:
                continue  # 没找到就跳过（有默认值或 Optional 的会自己处理）

            # === 关键：根据字段类型决定怎么解析 value ===
            field_type = field_info.annotation

            # List[SubModel] 情况
            if get_origin(field_type) is list:
                print(field_type)
                if not isinstance(value, list):
                    raise TypeError(f"Expected list, got {type(value)}")
                if isinstance(value, list) and issubclass(item_type, BaseAliasModel):
                    normalized_data[field_name] = [
                        item_type.from_any_dict(item) for item in value
                    ]
                    continue

            # 单个嵌套 Model 情况
            elif issubclass(field_type, BaseAliasModel):
                if isinstance(value, dict):
                    normalized_data[field_name] = field_type.from_any_dict(value)
                    continue

            # 普通类型（int/str/bool/datetime 等）
            else:
                normalized_data[field_name] = value

        return cls(**normalized_data)

