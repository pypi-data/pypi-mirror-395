"""
配置解析器 - 解析YAML配置文件
"""

import yaml
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class FieldConfig:
    """字段配置"""
    name: str
    type: str
    role: str = "normal"  # pk, fk, embed, normal
    to: Optional[str] = None  # 关联的实体名
    from_field: Optional[str] = None  # 来源字段和实体


@dataclass
class EntityConfig:
    """实体配置"""
    name: str
    table: str
    row_type: str  # single, multiple
    fields: Dict[str, FieldConfig]
    primary_key: Optional[str] = None


@dataclass
class RelationsConfig:
    """关系配置"""
    entities: Dict[str, EntityConfig]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RelationsConfig":
        """从字典创建配置对象"""
        entities = {}

        for entity_name, entity_data in data.get("entities", {}).items():
            fields = {}
            primary_key = None

            # 解析字段配置
            for field_name, field_data in entity_data.get("fields", {}).items():
                if isinstance(field_data, dict):
                    field_config = FieldConfig(
                        name=field_name,
                        type=field_data.get("type", "str"),
                        role=field_data.get("role", "normal"),
                        to=field_data.get("to"),
                        from_field=field_data.get("from")
                    )
                    fields[field_name] = field_config

                    # 记录主键
                    if field_config.role == "pk":
                        primary_key = field_name
                else:
                    # 简单格式，只有类型
                    field_config = FieldConfig(
                        name=field_name,
                        type=str(field_data),
                        role="normal"
                    )
                    fields[field_name] = field_config

            # 检查主键是否存在
            if not primary_key:
                raise ValueError(f"实体 '{entity_name}' 没有定义主键字段。请在 relations.yaml 中为该实体添加一个 role: pk 的字段。")

            entity_config = EntityConfig(
                name=entity_name,
                table=entity_data.get("table", entity_name.lower()),
                row_type=entity_data.get("row_type", "single"),
                fields=fields,
                primary_key=primary_key
            )
            entities[entity_name] = entity_config

        return cls(entities=entities)

    @classmethod
    def from_file(cls, config_path: str) -> "RelationsConfig":
        """从YAML文件创建配置对象"""
        with open(config_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return cls.from_dict(data)

    def get_entity_config(self, entity_name: str) -> Optional[EntityConfig]:
        """获取实体配置"""
        return self.entities.get(entity_name)

    def is_single_entity(self, entity_name: str) -> bool:
        """判断是否为单行实体"""
        config = self.get_entity_config(entity_name)
        return config.row_type == "single" if config else False

    def is_multiple_entity(self, entity_name: str) -> bool:
        """判断是否为多行实体"""
        config = self.get_entity_config(entity_name)
        return config.row_type == "multiple" if config else False

    def get_primary_key(self, entity_name: str) -> Optional[str]:
        """获取实体的主键字段"""
        config = self.get_entity_config(entity_name)
        return config.primary_key if config else None

    def get_id_field_for_table(self, entity_name: str) -> str:
        """获取表对应的ID字段名"""
        config = self.get_entity_config(entity_name)
        if not config:
            return "id"

        if config.primary_key:
            return config.primary_key

        # 根据表名推断ID字段
        table_name = config.table
        if "algorithm" in table_name.lower():
            return "algorithm_id"
        elif "task" in table_name.lower():
            return "id"
        else:
            return "id"

    def get_embed_fields(self, entity_name: str) -> List[FieldConfig]:
        """获取实体的所有嵌入字段"""
        config = self.get_entity_config(entity_name)
        if not config:
            return []

        embed_fields = []
        for field_config in config.fields.values():
            if field_config.role == "embed":
                embed_fields.append(field_config)
        return embed_fields

    def get_fk_fields(self, entity_name: str) -> List[FieldConfig]:
        """获取实体的所有外键字段"""
        config = self.get_entity_config(entity_name)
        if not config:
            return []

        fk_fields = []
        for field_config in config.fields.values():
            if field_config.role == "fk":
                fk_fields.append(field_config)
        return fk_fields

    def parse_relation_from_field(self, from_field: str) -> tuple:
        """
        解析关联字段的来源信息
        格式: EntityName.fieldName
        返回: (entity_name, field_name)
        """
        if '.' in from_field:
            return from_field.split('.', 1)
        return None, None

    def get_target_entity_field(self, relation_config: FieldConfig) -> tuple:
        """
        获取关联目标实体和字段
        返回: (target_entity_name, target_field_name)
        """
        if relation_config.to and relation_config.from_field:
            source_entity, source_field = self.parse_relation_from_field(relation_config.from_field)
            if source_entity and source_field:
                return relation_config.to, source_field
        return relation_config.to, None