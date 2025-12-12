"""
CustomerProfile domain model and its repository implementation.
"""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, Any, List, Optional, Union, Generic, TypeVar

from enn_iot_oc.infrastructure.repository.single_repo_base import SingleRepoBase
from enn_iot_oc.infrastructure.repository.multi_repo_base import MultiRepoBase
from enn_iot_oc.util.string_util import parse_object, parse_array

__all__ = ["CustomerProfile", "CustomerProfileRepoImpl"]

T = TypeVar('T')

# 定义基类 - 确保使用Generic[T]
CustomerProfileRepoBase = MultiRepoBase[T]

#------------- Domain Model -------------
@dataclass
class CustomerProfile:
    """
    CustomerProfile
    """

    profile_id: str = ""
    dimension_set: list = ""
    associated_cust_id: str = ""
    update_time: str = ""
    dimensions: Optional[List['ProfileDimension.dimension_id']] = field(default_factory=list)

#------------- Repository Implementation -------------
class CustomerProfileRepoImpl(CustomerProfileRepoBase[CustomerProfile]):
    """
    CustomerProfile
    """
    def __init__(self, eo_id: str = "", instance_id: str = "") -> None:
        """
        初始化方法
        """
        super().__init__(model_code="customer_profile", eo_id=eo_id, instance_id=instance_id, id_field="profile_id")

    def to_domain(self, row: Dict[str, Any]) -> CustomerProfile:
        """
        将数据库行转换为领域模型
        """
        return CustomerProfile(
            profile_id=parse_object(row.get("profile_id"), str),
            dimension_set=parse_object(row.get("dimension_set"), list),
            associated_cust_id=parse_object(row.get("associated_cust_id"), str),
            update_time=parse_object(row.get("update_time"), str),
            dimensions=self._convert_embed_list(row.get("dimensions"), "ProfileDimension"),
        )

    def from_domain(self, entity) -> Dict[str, Any]:
        """
        将领域模型转换为数据库行
        """
        return {
            "profile_id": getattr(entity, "profile_id", None),
            "dimension_set": getattr(entity, "dimension_set", None),
            "associated_cust_id": getattr(entity, "associated_cust_id", None),
            "update_time": getattr(entity, "update_time", None),
            "dimensions": getattr(entity, "dimensions", None),
        }

    def empty_object(self) -> CustomerProfile:
        """
        创建一个空的领域模型对象
        """
        return CustomerProfile(
            profile_id="",
            dimension_set="",
            associated_cust_id="",
            update_time="",
            dimensions="",
        )

    def extract_id(self, entity) -> str:
        """
        提取ID值
        """
        return getattr(entity, "profile_id", "")


    def _convert_embed_object(self, embed_data, target_entity_name: str):
        """
        转换嵌入对象
        """
        if not embed_data:
            return None
        
        # 如果是字典数据，直接转换为对象
        if isinstance(embed_data, dict):
            try:
                # 使用生成器中的实体配置来创建对象实例
                target_module = __import__(f"infrastructure.model.{target_entity_name}", fromlist=[target_entity_name])
                target_class = getattr(target_module, target_entity_name)
                # 直接调用构造函数创建实例
                target_obj = target_class()
                # 设置对象属性
                for key, value in embed_data.items():
                    setattr(target_obj, key, value)
                return target_obj
            except Exception as e:
                # 转换失败，返回None而不是原始字典数据
                return None
        
        # 如果是字符串，可能是之前缓存的对象字符串表示
        if isinstance(embed_data, str):
            # 可以在这里尝试解析字符串，但通常返回None
            return None
        
        return None

    def _convert_embed_list(self, embed_list, target_entity_name: str):
        """
        转换嵌入对象列表
        """
        if not embed_list:
            return []
        
        result = []
        for item in embed_list:
            converted = self._convert_embed_object(item, target_entity_name)
            if converted is not None:
                result.append(converted)
            # 转换失败时不再保留原始字典数据，只添加成功转换的对象
        return result
