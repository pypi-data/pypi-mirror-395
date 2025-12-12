"""
CategoryRequirement domain model and its repository implementation.
"""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, Any, List, Optional, Union, Generic, TypeVar

from enn_iot_oc.infrastructure.repository.single_repo_base import SingleRepoBase
from enn_iot_oc.infrastructure.repository.multi_repo_base import MultiRepoBase
from enn_iot_oc.util.string_util import parse_object, parse_array

__all__ = ["CategoryRequirement", "CategoryRequirementRepoImpl"]

T = TypeVar('T')

# 定义基类 - 确保使用Generic[T]
CategoryRequirementRepoBase = MultiRepoBase[T]

#------------- Domain Model -------------
@dataclass
class CategoryRequirement:
    """
    CategoryRequirement
    """

    dimension_id: str = ""
    category_name: str = ""
    rule_id: list = ""
    industry_tag: str = ""
    creator_type: str = ""

#------------- Repository Implementation -------------
class CategoryRequirementRepoImpl(CategoryRequirementRepoBase[CategoryRequirement]):
    """
    CategoryRequirement
    """
    def __init__(self, eo_id: str = "", instance_id: str = "") -> None:
        """
        初始化方法
        """
        super().__init__(model_code="category_requirement", eo_id=eo_id, instance_id=instance_id, id_field="dimension_id")

    def to_domain(self, row: Dict[str, Any]) -> CategoryRequirement:
        """
        将数据库行转换为领域模型
        """
        return CategoryRequirement(
            dimension_id=parse_object(row.get("dimension_id"), str),
            category_name=parse_object(row.get("category_name"), str),
            rule_id=parse_object(row.get("rule_id"), list),
            industry_tag=parse_object(row.get("industry_tag"), str),
            creator_type=parse_object(row.get("creator_type"), str),
        )

    def from_domain(self, entity) -> Dict[str, Any]:
        """
        将领域模型转换为数据库行
        """
        from dataclasses import asdict, is_dataclass
        result = {
            "dimension_id": getattr(entity, "dimension_id", None),
            "category_name": getattr(entity, "category_name", None),
            "rule_id": getattr(entity, "rule_id", None),
            "industry_tag": getattr(entity, "industry_tag", None),
            "creator_type": getattr(entity, "creator_type", None),
        }
        return result

    def empty_object(self) -> CategoryRequirement:
        """
        创建一个空的领域模型对象
        """
        return CategoryRequirement(
            dimension_id="",
            category_name="",
            rule_id="",
            industry_tag="",
            creator_type="",
        )

    def extract_id(self, entity) -> str:
        """
        提取ID值
        """
        return getattr(entity, "dimension_id", "")
