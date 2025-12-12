"""
类型推断器 - 自动推断JSON字段的Python类型
"""

import json
from typing import Any, Dict, List, Type, Union, Optional
from typing_inspect import get_origin, get_args


class TypeInferencer:
    """类型推断器类"""

    @staticmethod
    def infer_type(value: Any, field_name: str = "") -> str:
        """
        推断值的Python类型

        Args:
            value: 要推断类型的值
            field_name: 字段名（用于特殊判断）

        Returns:
            Python类型字符串
        """
        if value is None:
            return "str"

        # 检查布尔类型
        if isinstance(value, bool):
            return "bool"

        # 检查整数类型
        if isinstance(value, int) and not isinstance(value, bool):
            return "int"

        # 检查浮点数类型
        if isinstance(value, float):
            return "float"

        # 检查字符串类型
        if isinstance(value, str):
            return "str"

        # 检查列表类型
        if isinstance(value, list):
            if not value:
                return "List[str]"

            # 推断列表元素类型
            element_type = TypeInferencer.infer_type(value[0])
            return f"List[{element_type}]"

        # 检查字典类型
        if isinstance(value, dict):
            return "Dict[str, Any]"

        # 默认返回字符串类型
        return "str"

    @staticmethod
    def get_default_value(type_str: str) -> str:
        """
        根据类型获取默认值

        Args:
            type_str: 类型字符串

        Returns:
            默认值的字符串表示
        """
        type_mapping = {
            "str": '""',
            "int": "0",
            "float": "0.0",
            "bool": "False",
            "List[str]": "field(default_factory=list)",
            "List[int]": "field(default_factory=list)",
            "List[float]": "field(default_factory=list)",
            "List[bool]": "field(default_factory=list)",
            "Dict[str, Any]": "field(default_factory=dict)",
        }

        return type_mapping.get(type_str, '""')

    @staticmethod
    def infer_field_types_from_data(data_list: List[Dict[str, Any]]) -> Dict[str, str]:
        """
        从数据列表中推断所有字段类型

        Args:
            data_list: 数据列表

        Returns:
            字段名到类型字符串的映射
        """
        if not data_list:
            return {}

        field_types = {}

        # 遍历所有数据，推断每个字段的类型
        for item in data_list:
            for field_name, field_value in item.items():
                if field_name not in field_types:
                    field_types[field_name] = TypeInferencer.infer_type(field_value, field_name)
                else:
                    # 如果已经有类型，检查是否需要升级为更通用的类型
                    current_type = field_types[field_name]
                    new_type = TypeInferencer.infer_type(field_value, field_name)
                    field_types[field_name] = TypeInferencer._get_more_general_type(current_type, new_type)

        return field_types

    @staticmethod
    def _get_more_general_type(type1: str, type2: str) -> str:
        """
        获取两个类型中更通用的类型

        Args:
            type1: 类型1
            type2: 类型2

        Returns:
            更通用的类型
        """
        # 类型优先级：bool < int < float < str < Any
        type_priority = {
            "bool": 1,
            "int": 2,
            "float": 3,
            "str": 4,
            "Dict[str, Any]": 5
        }

        # 处理列表类型
        if "List[" in type1 or "List[" in type2:
            return "List[str]"  # 列表类型统一为List[str]

        # 获取优先级，返回优先级更高的类型
        priority1 = type_priority.get(type1.split("[")[0], 6)
        priority2 = type_priority.get(type2.split("[")[0], 6)

        if priority1 >= priority2:
            return type1
        else:
            return type2

    @staticmethod
    def normalize_type(type_str: str) -> str:
        """
        规范化类型字符串

        Args:
            type_str: 原始类型字符串

        Returns:
            规范化后的类型字符串
        """
        # 统一字符串类型
        if type_str in ["string", "String"]:
            return "str"

        # 统一列表类型
        if "List[" in type_str:
            return "List[str]"

        # 规范化字典类型
        if type_str in ["dict", "Dict"]:
            return "Dict[str, Any]"

        return type_str