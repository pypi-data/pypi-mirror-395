"""TOON格式编码工具模块

TOON (Tabular Object Notation) 是一种紧凑的数据格式，专门用于表示结构化数据。
它使用表格形式来表示对象数组，使数据更加紧凑和易读。
"""

def toon_encode(data, indent=2, delimiter=',') -> str:
    """将Python数据转换为TOON格式

    Args:
        data: 要编码的数据（字典、列表或原始类型）
        indent: 缩进空格数（默认2）
        delimiter: 数组和表格行的分隔符（默认','）

    Returns:
        TOON格式字符串
    """
    if data is None:
        return 'null'
    elif isinstance(data, bool):
        return 'true' if data else 'false'
    elif isinstance(data, (int, float)):
        # 处理NaN和无穷大
        import math
        if isinstance(data, float):
            if math.isnan(data):
                return 'null'
            elif math.isinf(data):
                return 'null'
        return str(data)
    elif isinstance(data, str):
        # 如果字符串包含特殊字符或空格，需要引号包围
        if any(c in data for c in ':,[]{}'):
            return f'"{data}"'
        return data
    elif isinstance(data, dict):
        items = []
        for key, value in data.items():
            key_str = toon_encode(key, indent, delimiter)
            val_str = toon_encode(value, indent, delimiter)
            # 嵌套字典需要增加缩进
            if '\n' in val_str:
                items.append(f'{key_str}:\n  {val_str.replace(chr(10), chr(10) + "  ")}')
            else:
                items.append(f'{key_str}: {val_str}')
        return '\n'.join(items)
    elif isinstance(data, list):
        # 处理空数组
        if len(data) == 0:
            return '[]'

        # 检查是否是对象数组且具有相同键
        if data and all(isinstance(item, dict) for item in data):
            keys = set()
            for item in data:
                if isinstance(item, dict):
                    keys.update(item.keys())
            keys = sorted(keys)

            # 如果所有对象都有相同的键，使用表格格式
            if len(keys) > 0:
                header = f'[{len(data)}]{{{",".join(str(k) for k in keys)}}}'
                rows = []
                for item in data:
                    row_values = []
                    for key in keys:
                        val = item.get(key, '')
                        val_str = toon_encode(val, indent, delimiter)
                        row_values.append(str(val_str))
                    rows.append(' ' * indent + delimiter.join(row_values))
                return header + '\n' + '\n'.join(rows)

        # 简单数组
        values = [str(toon_encode(item, indent, delimiter)) for item in data]
        if any('\n' in v for v in values):
            # 如果有嵌套值，需要特殊处理
            return f'[{len(data)}]:\n' + '\n'.join('  ' + v for v in values)
        return f'[{len(data)}]: {",".join(values)}'
    else:
        # 其他类型（如日期等）转换为字符串
        return str(data)


def format_toon_output(data, indent=2, delimiter=',') -> str:
    """格式化TOON输出，确保没有尾随空格

    Args:
        data: 要编码的数据
        indent: 缩进空格数
        delimiter: 分隔符

    Returns:
        格式化的TOON字符串
    """
    return toon_encode(data, indent, delimiter)
