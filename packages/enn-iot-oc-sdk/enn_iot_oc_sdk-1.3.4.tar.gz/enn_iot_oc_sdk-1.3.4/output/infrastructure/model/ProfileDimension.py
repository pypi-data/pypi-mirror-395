"""
ProfileDimension domain model and its repository implementation.
"""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, Any, List, Optional, Union, Generic, TypeVar

from enn_iot_oc.infrastructure.repository.single_repo_base import SingleRepoBase
from enn_iot_oc.infrastructure.repository.multi_repo_base import MultiRepoBase
from enn_iot_oc.util.string_util import parse_object, parse_array

__all__ = ["ProfileDimension", "ProfileDimensionRepoImpl"]

T = TypeVar('T')

# 定义基类 - 确保使用Generic[T]
ProfileDimensionRepoBase = MultiRepoBase[T]

#------------- Domain Model -------------
@dataclass
class ProfileDimension:
    """
    ProfileDimension
    """

    dimension_id: str = ""
    profile_id: str = ""
    dimension_name: str = ""
    dimension_value: str = ""
    data_source: str = ""

#------------- Repository Implementation -------------
class ProfileDimensionRepoImpl(ProfileDimensionRepoBase[ProfileDimension]):
    """
    ProfileDimension
    """
    def __init__(self, eo_id: str = "", instance_id: str = "") -> None:
        """
        初始化方法
        """
        super().__init__(model_code="profile_dimension", eo_id=eo_id, instance_id=instance_id, id_field="dimension_id")

    def to_domain(self, row: Dict[str, Any]) -> ProfileDimension:
        """
        将数据库行转换为领域模型
        """
        return ProfileDimension(
            profile_id=parse_object(row.get("profile_id"), str),
            dimension_id=parse_object(row.get("dimension_id"), str),
            dimension_name=parse_object(row.get("dimension_name"), str),
            dimension_value=parse_object(row.get("dimension_value"), str),
            data_source=parse_object(row.get("data_source"), str),
        )

    def from_domain(self, entity) -> Dict[str, Any]:
        """
        将领域模型转换为数据库行
        """
        from dataclasses import asdict, is_dataclass
        result = {
            "profile_id": getattr(entity, "profile_id", None),
            "dimension_id": getattr(entity, "dimension_id", None),
            "dimension_name": getattr(entity, "dimension_name", None),
            "dimension_value": getattr(entity, "dimension_value", None),
            "data_source": getattr(entity, "data_source", None),
        }
        return result

    def empty_object(self) -> ProfileDimension:
        """
        创建一个空的领域模型对象
        """
        return ProfileDimension(
            profile_id="",
            dimension_id="",
            dimension_name="",
            dimension_value="",
            data_source="",
        )

    def extract_id(self, entity) -> str:
        """
        提取ID值
        """
        return getattr(entity, "dimension_id", "")
