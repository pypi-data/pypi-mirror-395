"""
实体生成器 - 自动生成符合规范的实体类
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import os

from .type_inferencer import TypeInferencer
from .config_parser import EntityConfig, RelationsConfig


class EntityGenerator:
    """实体生成器类"""

    def __init__(self, config: RelationsConfig):
        self.config = config

    def generate_entity_class(self, entity_name: str, entity_data: List[Dict[str, Any]]) -> str:
        """
        生成实体类代码

        Args:
            entity_name: 实体名称
            entity_data: 实体数据

        Returns:
            实体类代码字符串
        """
        entity_config = self.config.get_entity_config(entity_name)
        if not entity_config:
            raise ValueError(f"Entity {entity_name} not found in config")

        # 推断字段类型
        inferred_types = TypeInferencer.infer_field_types_from_data(entity_data)

        # 合并配置文件中的类型和数据推断的类型
        field_types = self._merge_field_types(entity_config, inferred_types)

        # 生成类代码
        class_code = self._generate_class_definition(entity_name, entity_config, field_types)

        return class_code

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

    def _generate_class_definition(self, entity_name: str, entity_config: EntityConfig, field_types: Dict[str, str]) -> str:
        """生成类定义代码"""
        lines = []

        # 添加文档字符串
        class_comment = f'"""\n{entity_name} domain model and its repository implementation.\n"""\n'
        lines.append(class_comment)

        # 添加导入语句
        imports = self._generate_imports(field_types)
        lines.extend(imports)
        lines.append("")

        # 添加基础类定义
        base_class = "SingleRepoBase" if entity_config.row_type == "single" else "MultiRepoBase"
        base_class_def = f"T = TypeVar('T')\n\n# 定义基类 - 确保使用Generic[T]\n{entity_name}RepoBase = {base_class}[T]\n"
        lines.append(base_class_def)

        # 添加dataclass定义
        lines.append("#------------- Domain Model -------------")
        lines.append("@dataclass")
        lines.append(f"class {entity_name}:")
        lines.append(f'    """')
        lines.append(f'    {self._get_entity_description(entity_name)}')
        lines.append(f'    """')
        lines.append("")

        # 生成字段
        for field_name, field_type in field_types.items():
            default_value = TypeInferencer.get_default_value(field_type)
            field_config = entity_config.fields.get(field_name)

            # 处理特殊字段
            if field_config and field_config.role == "embed":
                # 嵌套对象类型
                embed_type = f"Optional[List['{field_config.to}']]"
                default_value = "field(default_factory=list)"
                lines.append(f'    {field_name}: {embed_type} = {default_value}')
            else:
                # 普通字段
                normalized_type = TypeInferencer.normalize_type(field_type)
                lines.append(f'    {field_name}: {normalized_type} = {default_value}')

        lines.append("")

        return "\n".join(lines)

    def _generate_imports(self, field_types: Dict[str, str]) -> List[str]:
        """生成导入语句"""
        imports = [
            "from dataclasses import dataclass, field",
            "from decimal import Decimal",
            "from typing import Dict, Any, List, Optional, Union, Generic, TypeVar",
            "",
            "from enn_iot_oc.infrastructure.repository.single_repo_base import SingleRepoBase",
            "from enn_iot_oc.infrastructure.repository.multi_repo_base import MultiRepoBase",
            "from enn_iot_oc.util.string_util import parse_object, parse_array",
            "",
            f'__all__ = ["{self._extract_entity_name_from_field_types(field_types)}", "{self._extract_entity_name_from_field_types(field_types)}RepoImpl"]'
        ]

        return imports

    def _extract_entity_name_from_field_types(self, field_types: Dict[str, str]) -> str:
        """从字段类型中提取实体名称（这里简化处理）"""
        return "EntityName"  # 实际应该从调用上下文获取

    def _get_entity_description(self, entity_name: str) -> str:
        """获取实体描述"""
        descriptions = {
            "BiogasProjectInformation": "沼气项目信息",
            "MechanismCloudAlgorithm": "机理云端算法",
            "MechanismTaskPlanning": "机理规划子任务",
            "TypeTemplate": "机理类沉淀模版"
        }
        return descriptions.get(entity_name, entity_name)

    def generate_repository_class(self, entity_name: str) -> str:
        """
        生成仓库类代码

        Args:
            entity_name: 实体名称

        Returns:
            仓库类代码字符串
        """
        entity_config = self.config.get_entity_config(entity_name)
        if not entity_config:
            raise ValueError(f"Entity {entity_name} not found in config")

        lines = []

        # 添加仓库类定义
        lines.append("#------------- Repository Implementation -------------")
        base_class = "SingleRepoBase" if entity_config.row_type == "single" else "MultiRepoBase"
        lines.append(f"class {entity_name}RepoImpl({entity_name}RepoBase[{entity_name}]):")
        lines.append(f'    """')
        lines.append(f'    {self._get_entity_description(entity_name)}')
        lines.append(f'    """')

        # 生成构造函数
        id_field = self.config.get_id_field_for_table(entity_name)
        init_params = 'eo_id: str = "", instance_id: str = ""'
        if entity_config.row_type == "multiple":
            init_params = f'eo_id: str = "", instance_id: str = ""'

        lines.append(f"    def __init__(self, {init_params}) -> None:")
        lines.append('        """')
        lines.append('        初始化方法')
        lines.append('        """')

        # 生成super()调用
        if entity_config.row_type == "single":
            lines.append(f'        super().__init__(model_code="{entity_config.table}", eo_id=eo_id, instance_id=instance_id)')
        else:
            lines.append(f'        super().__init__(model_code="{entity_config.table}", eo_id=eo_id, instance_id=instance_id, id_field="{id_field}")')

        lines.append("")
        lines.append("    #---- Conversion ----")

        # 生成to_domain和from_domain方法的框架
        lines.append("    def to_domain(self, row: Dict[str, Any]) -> {entity_name}:")
        lines.append('        """')
        lines.append('        将数据库行转换为领域模型')
        lines.append('        """')
        lines.append(f"        return {entity_name}(")
        lines.append("            # TODO: 实现字段映射")
        lines.append("        )")
        lines.append("")

        lines.append("    def from_domain(self, entity: {entity_name}) -> Dict[str, Any]:")
        lines.append('        """')
        lines.append('        将领域模型转换为数据库行')
        lines.append('        """')
        lines.append("        return {")
        lines.append("            # TODO: 实现字段映射")
        lines.append("        }")
        lines.append("")

        return "\n".join(lines)

    def save_to_file(self, entity_name: str, entity_code: str, repository_code: str, output_dir: str):
        """
        保存生成的代码到文件

        Args:
            entity_name: 实体名称
            entity_code: 实体类代码
            repository_code: 仓库类代码
            output_dir: 输出目录
        """
        # 创建目录
        model_dir = os.path.join(output_dir, "infrastructure", "model")
        os.makedirs(model_dir, exist_ok=True)

        # 保存实体类文件
        file_path = os.path.join(model_dir, f"{entity_name}.py")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(entity_code)

        print(f"✓ 生成实体文件: {file_path}")

    def generate_all_entities(self, data_dir: str, output_dir: str):
        """
        生成所有实体类

        Args:
            data_dir: 数据目录
            output_dir: 输出目录
        """
        import json

        # 遍历配置中的所有实体
        for entity_name, entity_config in self.config.entities.items():
            # 读取对应的数据文件
            data_file = os.path.join(data_dir, "source", f"{entity_config.table}.json")

            if not os.path.exists(data_file):
                print(f"⚠ 数据文件不存在: {data_file}")
                continue

            with open(data_file, 'r', encoding='utf-8') as f:
                entity_data = json.load(f)

            # 生成实体类代码
            entity_code = self.generate_entity_class(entity_name, entity_data)

            # 生成仓库类代码
            repository_code = self.generate_repository_class(entity_name)

            # 合并代码
            full_code = entity_code + "\n" + repository_code

            # 保存到文件
            self.save_to_file(entity_name, full_code, repository_code, output_dir)