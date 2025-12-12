"""
Mock版本的Repository生成器 - 使用模拟数据而不是真实SDK
"""

from typing import Dict, Any, List, Optional
import os
import json

from .type_inferencer import TypeInferencer
from .config_parser import EntityConfig, RelationsConfig


class MockRepositoryGenerator:
    """Mock Repository生成器类"""

    def __init__(self, config: RelationsConfig, data_dir: str):
        self.config = config
        self.data_dir = data_dir
        self.mock_data = self._load_mock_data()

    def _load_mock_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """加载模拟数据"""
        mock_data = {}

        for entity_name, entity_config in self.config.entities.items():
            data_file = os.path.join(self.data_dir, "source", f"{entity_config.table}.json")

            if os.path.exists(data_file):
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    mock_data[entity_name] = data
            else:
                mock_data[entity_name] = []

        return mock_data

    def generate_mock_repository(self, entity_name: str, entity_data: List[Dict[str, Any]]) -> str:
        """
        生成使用模拟数据的Repository

        Args:
            entity_name: 实体名称
            entity_data: 实体数据

        Returns:
            Mock Repository代码字符串
        """
        entity_config = self.config.get_entity_config(entity_name)
        if not entity_config:
            raise ValueError(f"Entity {entity_name} not found in config")

        # 推断字段类型
        inferred_types = TypeInferencer.infer_field_types_from_data(entity_data)
        field_types = self._merge_field_types(entity_config, inferred_types)

        # 生成完整代码
        code_parts = []

        # 1. 文件头部
        code_parts.append(self._generate_file_header(entity_name))
        code_parts.append(self._generate_mock_imports())

        # 2. 实体类定义（与真实版本相同）
        code_parts.append(self._generate_entity_class(entity_name, entity_config, field_types))

        # 3. Mock Repository类定义
        code_parts.append(self._generate_mock_repository_class(entity_name, entity_config, field_types))

        return "\n".join(code_parts)

    def _merge_field_types(self, entity_config: EntityConfig, inferred_types: Dict[str, str]) -> Dict[str, str]:
        """合并配置文件类型和推断类型"""
        merged_types = {}

        # 首先使用推断的类型
        for field_name, field_type in inferred_types.items():
            merged_types[field_name] = field_type

        # 然后用配置文件中的类型覆盖
        for field_name, field_config in entity_config.fields.items():
            if field_config.type:
                merged_types[field_name] = field_config.type

        return merged_types

    def _generate_file_header(self, entity_name: str) -> str:
        """生成文件头部"""
        return f'"""\n{entity_name} domain model and mock repository implementation.\n"""\n'

    def _generate_mock_imports(self) -> str:
        """生成导入语句"""
        return """from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, Any, List, Optional, Union, Generic, TypeVar

__all__ = ["{{EntityName}}", "{{EntityName}}RepoImpl"]
"""

    def _generate_entity_class(self, entity_name: str, entity_config: EntityConfig, field_types: Dict[str, str]) -> str:
        """生成实体类定义"""
        lines = []

        lines.append("#------------- Domain Model -------------")
        lines.append("@dataclass")
        lines.append(f"class {entity_name}:")
        lines.append(f'    """')
        lines.append(f'    {self._get_entity_description(entity_name)}')
        lines.append(f'    """')
        lines.append("")

        # 生成字段
        sorted_fields = self._sort_fields_by_importance(field_types, entity_config)

        for field_name, field_type in sorted_fields.items():
            field_config = entity_config.fields.get(field_name)

            # 处理特殊字段
            if field_config and field_config.role == "embed":
                embed_type = f"Optional[List['{field_config.to}']]"
                default_value = "field(default_factory=list)"
                lines.append(f'    {field_name}: {embed_type} = {default_value}')
            else:
                normalized_type = TypeInferencer.normalize_type(field_type)
                default_value = TypeInferencer.get_default_value(normalized_type)
                lines.append(f'    {field_name}: {normalized_type} = {default_value}')

        lines.append("")
        return "\n".join(lines)

    def _generate_mock_repository_class(self, entity_name: str, entity_config: EntityConfig, field_types: Dict[str, str]) -> str:
        """生成Mock Repository类定义"""
        lines = []

        lines.append("#------------- Mock Repository Implementation -------------")
        lines.append(f"class {entity_name}RepoImpl:")
        lines.append(f'    """')
        lines.append(f'    {self._get_entity_description(entity_name)} Mock Repository')
        lines.append(f'    """')

        # 生成构造函数
        lines.extend(self._generate_mock_constructor(entity_name, entity_config))

        # 生成查询方法
        if entity_config.row_type == "single":
            lines.extend(self._generate_mock_find_method(entity_name, entity_config))
        else:
            lines.extend(self._generate_mock_list_method(entity_name, entity_config))
            lines.extend(self._generate_mock_find_by_id_method(entity_name, entity_config))

        # 生成辅助方法
        lines.extend(self._generate_mock_helper_methods(entity_name, field_types))

        return "\n".join(lines)

    def _generate_mock_constructor(self, entity_name: str, entity_config: EntityConfig) -> List[str]:
        """生成Mock构造函数"""
        lines = []

        lines.append("    def __init__(self, eo_id: str = \"\", instance_id: str = \"\") -> None:")
        lines.append('        """')
        lines.append('        初始化Mock Repository')
        lines.append('        """')
        lines.append("        self.eo_id = eo_id")
        lines.append("        self.instance_id = instance_id")
        lines.append("        self._data = self._load_mock_data()")
        lines.append("")

        return lines

    def _generate_mock_find_method(self, entity_name: str, entity_config: EntityConfig) -> List[str]:
        """生成Mock find方法（单行实体）"""
        lines = []

        lines.append(f"    def find(self) -> {entity_name}:")
        lines.append('        """')
        lines.append('        Mock查询单行实体')
        lines.append('        """')
        lines.append(f"        if self._data:")
        lines.append(f"            return self._dict_to_{entity_name.lower()}(self._data[0])")
        lines.append("        else:")
        lines.append(f"            return {entity_name}()")
        lines.append("")

        return lines

    def _generate_mock_list_method(self, entity_name: str, entity_config: EntityConfig) -> List[str]:
        """生成Mock list方法（多行实体）"""
        lines = []

        lines.append(f"    def list(self) -> List[{entity_name}]:")
        lines.append('        """')
        lines.append('        Mock查询所有实体')
        lines.append('        """')
        lines.append(f"        return [self._dict_to_{entity_name.lower()}(item) for item in self._data]")
        lines.append("")

        return lines

    def _generate_mock_find_by_id_method(self, entity_name: str, entity_config: EntityConfig) -> List[str]:
        """生成Mock find_by_id方法（多行实体）"""
        lines = []

        id_field = entity_config.primary_key or "id"

        lines.append(f"    def find_by_id(self, entity_id: str) -> {entity_name}:")
        lines.append('        """')
        lines.append('        Mock根据ID查询实体')
        lines.append('        """')
        lines.append(f"        for item in self._data:")
        lines.append(f"            if item.get('{id_field}') == entity_id:")
        lines.append(f"                return self._dict_to_{entity_name.lower()}(item)")
        lines.append(f"        return {entity_name}()")
        lines.append("")

        return lines

    def _generate_mock_helper_methods(self, entity_name: str, field_types: Dict[str, str]) -> List[str]:
        """生成Mock辅助方法"""
        lines = []

        # 数据加载方法
        lines.append(f"    def _load_mock_data(self) -> List[Dict[str, Any]]:")
        lines.append('        """')
        lines.append('        加载Mock数据')
        lines.append('        """')
        # 生成真实的数据加载代码
        lines.append(f"        # 加载真实数据")
        mock_data_list = self.mock_data.get(entity_name, [])
        if mock_data_list:
            lines.append(f"        return {repr(mock_data_list)}")
        else:
            lines.append(f"        return []")
        lines.append("")

        # 字典转实体方法
        lines.append(f"    def _dict_to_{entity_name.lower()}(self, data: Dict[str, Any]) -> {entity_name}:")
        lines.append('        """')
        lines.append('        将字典转换为实体对象')
        lines.append('        """')
        lines.append(f"        return {entity_name}(")

        for field_name, field_type in field_types.items():
            normalized_type = TypeInferencer.normalize_type(field_type)
            lines.append(f"            {field_name}=data.get('{field_name}', {TypeInferencer.get_default_value(normalized_type)}),")

        lines.append("        )")
        lines.append("")

        return lines

    def _sort_fields_by_importance(self, field_types: Dict[str, str], entity_config: EntityConfig) -> Dict[str, str]:
        """按重要性排序字段"""
        sorted_fields = {}

        # 首先添加主键字段
        if entity_config.primary_key and entity_config.primary_key in field_types:
            sorted_fields[entity_config.primary_key] = field_types[entity_config.primary_key]

        # 然后添加外键字段
        for field_name, field_config in entity_config.fields.items():
            if field_config.role == "fk" and field_name in field_types:
                sorted_fields[field_name] = field_types[field_name]

        # 最后添加其他字段
        for field_name, field_type in field_types.items():
            if field_name not in sorted_fields:
                sorted_fields[field_name] = field_type

        return sorted_fields

    def _get_entity_description(self, entity_name: str) -> str:
        """获取实体描述"""
        descriptions = {
            "BiogasProjectInformation": "沼气项目信息",
            "MechanismCloudAlgorithm": "机理云端算法",
            "MechanismTaskPlanning": "机理规划子任务",
            "TypeTemplate": "机理类沉淀模版"
        }
        return descriptions.get(entity_name, entity_name)

    def save_to_file(self, entity_name: str, code: str, output_dir: str):
        """
        保存生成的代码到文件

        Args:
            entity_name: 实体名称
            code: 生成的代码
            output_dir: 输出目录
        """
        # 创建目录
        model_dir = os.path.join(output_dir, "infrastructure", "model")
        os.makedirs(model_dir, exist_ok=True)

        # 替换模板变量
        code = code.replace("{{EntityName}}", entity_name)

        # 保存文件
        file_path = os.path.join(model_dir, f"{entity_name}Mock.py")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)

        print(f"✓ 生成Mock Repository文件: {file_path}")

    def generate_all_mock_repositories(self, output_dir: str):
        """
        生成所有Mock Repository

        Args:
            output_dir: 输出目录
        """
        # 遍历配置中的所有实体
        for entity_name, entity_config in self.config.entities.items():
            entity_data = self.mock_data.get(entity_name, [])

            # 生成Mock Repository代码
            mock_code = self.generate_mock_repository(entity_name, entity_data)

            # 保存到文件
            self.save_to_file(entity_name, mock_code, output_dir)

        # 生成Mock主文件
        self._generate_mock_main_file(output_dir)

    def _generate_mock_main_file(self, output_dir: str):
        """生成Mock主入口文件"""
        main_code = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mock版本的IoC数据SDK接口
使用模拟数据，无需真实认证
"""

from .infrastructure.model import *

# 也可以直接导入Mock版本
from .infrastructure.model.BiogasProjectInformationMock import BiogasProjectInformation as MockBiogasProjectInformation
from .infrastructure.model.BiogasProjectInformationMock import BiogasProjectInformationRepoImpl as MockBiogasProjectInformationRepoImpl
'''

        main_file = os.path.join(output_dir, "mock_main.py")
        with open(main_file, 'w', encoding='utf-8') as f:
            f.write(main_code)

        print(f"✓ 生成Mock主文件: {main_file}")