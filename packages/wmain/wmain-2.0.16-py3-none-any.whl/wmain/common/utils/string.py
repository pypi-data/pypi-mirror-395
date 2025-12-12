def normalize_field_name(name: str) -> str:
    """
    规范化字段名：
    - 转为小写
    - 去除非字母数字字符（包含下划线、空格、破折号）
    - 用于实现字段名称大小写无关 / 下划线无关匹配
    """
    if not isinstance(name, str):
        return name

    return ''.join(ch.lower() for ch in name if ch.isalnum())
