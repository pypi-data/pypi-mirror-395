"""
仓库生成器 - 生成完整的Repository接口实现
"""

from typing import Dict, Any, List, Optional
import os

from .config_parser import EntityConfig, RelationsConfig
from .type_inferencer import TypeInferencer


class RepositoryGenerator:
    """仓库生成器类"""

    def __init__(self, config: RelationsConfig):
        self.config = config

    def generate_complete_repository(self, entity_name: str, entity_data: List[Dict[str, Any]]) -> str:
        """
        生成完整的Repository实现

        Args:
            entity_name: 实体名称
            entity_data: 实体数据

        Returns:
            完整的Repository代码
        """
        entity_config = self.config.get_entity_config(entity_name)
        if not entity_config:
            raise ValueError(f"Entity {entity_name} not found in config")

        # 推断字段类型
        inferred_types = TypeInferencer.infer_field_types_from_data(entity_data)
        field_types = self._merge_field_types(entity_config, inferred_types)

        # 生成完整代码
        code_parts = []

        # 1. 文件头部和导入
        code_parts.append(self._generate_file_header(entity_name))
        code_parts.append(self._generate_imports())

        # 2. 类型变量和基类定义
        code_parts.append(self._generate_base_class_definition(entity_name, entity_config))

        # 3. 实体类定义
        code_parts.append(self._generate_entity_class(entity_name, entity_config, field_types))

        # 4. Repository类定义
        code_parts.append(self._generate_repository_class(entity_name, entity_config, field_types))

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
        return f'"""\n{entity_name} domain model and its repository implementation.\n"""\n'

    def _generate_imports(self) -> str:
        """生成导入语句"""
        return """from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, Any, List, Optional, Union, Generic, TypeVar

from enn_iot_oc.infrastructure.repository.single_repo_base import SingleRepoBase
from enn_iot_oc.infrastructure.repository.multi_repo_base import MultiRepoBase
from enn_iot_oc.util.string_util import parse_object, parse_array

__all__ = ["{{EntityName}}", "{{EntityName}}RepoImpl"]
"""

    def _generate_base_class_definition(self, entity_name: str, entity_config: EntityConfig) -> str:
        """生成基类定义"""
        base_class = "SingleRepoBase" if entity_config.row_type == "single" else "MultiRepoBase"
        return f"""T = TypeVar('T')

# 定义基类 - 确保使用Generic[T]
{entity_name}RepoBase = {base_class}[T]
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

    def _generate_repository_class(self, entity_name: str, entity_config: EntityConfig, field_types: Dict[str, str]) -> str:
        """生成Repository类定义"""
        lines = []

        lines.append("#------------- Repository Implementation -------------")
        base_class_name = f"{entity_name}RepoBase"
        lines.append(f"class {entity_name}RepoImpl({base_class_name}[{entity_name}]):")
        lines.append(f'    """')
        lines.append(f'    {self._get_entity_description(entity_name)}')
        lines.append(f'    """')

        # 构造函数
        lines.extend(self._generate_constructor(entity_config))

        # to_domain方法
        lines.extend(self._generate_to_domain_method(entity_name, field_types))

        # from_domain方法
        lines.extend(self._generate_from_domain_method(field_types))

        # empty_object方法
        lines.extend(self._generate_empty_object_method(entity_name, field_types))

        # 多行实体特有的方法
        if entity_config.row_type == "multiple":
            lines.extend(self._generate_extract_id_method(entity_config))

        return "\n".join(lines)

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

    def _generate_constructor(self, entity_config: EntityConfig) -> List[str]:
        """生成构造函数"""
        lines = []

        init_params = 'eo_id: str = "", instance_id: str = ""'

        lines.append("    def __init__(self, {}) -> None:".format(init_params))
        lines.append('        """')
        lines.append('        初始化方法')
        lines.append('        """')

        if entity_config.row_type == "single":
            lines.append(f'        super().__init__(model_code="{entity_config.table}", eo_id=eo_id, instance_id=instance_id)')
        else:
            id_field = self.config.get_id_field_for_table(entity_config.name)
            lines.append(f'        super().__init__(model_code="{entity_config.table}", eo_id=eo_id, instance_id=instance_id, id_field="{id_field}")')

        lines.append("")
        return lines

    def _generate_to_domain_method(self, entity_name: str, field_types: Dict[str, str]) -> List[str]:
        """生成to_domain方法"""
        lines = []

        lines.append("    def to_domain(self, row: Dict[str, Any]) -> {}:".format(entity_name))
        lines.append('        """')
        lines.append('        将数据库行转换为领域模型')
        lines.append('        """')
        lines.append(f"        return {entity_name}(")

        # 生成字段映射
        for field_name, field_type in field_types.items():
            db_field_name = self._to_db_field_name(field_name)
            normalized_type = TypeInferencer.normalize_type(field_type)
            if normalized_type.startswith("List["):
                lines.append(f'            {field_name}=parse_array(row.get("{db_field_name}"), List),')
            elif normalized_type.startswith("Optional[List"):
                lines.append(f'            {field_name}=parse_array(row.get("{db_field_name}"), List),')
            else:
                lines.append(f'            {field_name}=parse_object(row.get("{db_field_name}"), {normalized_type}),')

        lines.append("        )")
        lines.append("")
        return lines

    def _generate_from_domain_method(self, field_types: Dict[str, str]) -> List[str]:
        """生成from_domain方法"""
        lines = []

        lines.append("    def from_domain(self, entity) -> Dict[str, Any]:")
        lines.append('        """')
        lines.append('        将领域模型转换为数据库行')
        lines.append('        """')
        lines.append("        return {")

        # 生成字段映射
        for field_name, field_type in field_types.items():
            db_field_name = self._to_db_field_name(field_name)
            lines.append(f'            "{db_field_name}": getattr(entity, "{field_name}", None),')

        lines.append("        }")
        lines.append("")
        return lines

    def _generate_empty_object_method(self, entity_name: str, field_types: Dict[str, str]) -> List[str]:
        """生成empty_object方法"""
        lines = []

        lines.append("    def empty_object(self) -> {}:".format(entity_name))
        lines.append('        """')
        lines.append('        创建一个空的领域模型对象')
        lines.append('        """')
        lines.append(f"        return {entity_name}(")

        # 生成默认值
        for field_name, field_type in field_types.items():
            normalized_type = TypeInferencer.normalize_type(field_type)
            default_value = TypeInferencer.get_default_value(normalized_type)
            lines.append(f'            {field_name}={default_value},')

        lines.append("        )")
        lines.append("")
        return lines

    def _generate_extract_id_method(self, entity_config: EntityConfig) -> List[str]:
        """生成extract_id方法（多行实体用）"""
        lines = []

        if entity_config.primary_key:
            lines.append("    def extract_id(self, entity) -> str:")
            lines.append('        """')
            lines.append('        提取ID值')
            lines.append('        """')
            lines.append(f'        return getattr(entity, "{entity_config.primary_key}", "")')
            lines.append("")

        return lines

    def _to_db_field_name(self, field_name: str) -> str:
        """将Python字段名转换为数据库字段名"""
        # 驼峰转下划线
        import re
        db_field = re.sub('([A-Z])', r'_\1', field_name).lower()

        # 处理特殊情况
        special_mappings = {
            'comOneid': 'com_oneid',
            'cvcuId': 'cvcu_id',
            'cSchemeId': 'c_scheme_id',
            'schemeId': 'scheme_id',
            'algorithmId': 'algorithm_id'
        }

        return special_mappings.get(field_name, db_field)

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
        file_path = os.path.join(model_dir, f"{entity_name}.py")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)

        print(f"✓ 生成Repository文件: {file_path}")

    def generate_all_repositories(self, data_dir: str, output_dir: str):
        """
        生成所有Repository

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

            # 生成Repository代码
            repository_code = self.generate_complete_repository(entity_name, entity_data)

            # 保存到文件
            self.save_to_file(entity_name, repository_code, output_dir)