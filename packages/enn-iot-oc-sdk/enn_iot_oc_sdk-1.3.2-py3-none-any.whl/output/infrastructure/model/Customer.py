"""
Customer domain model and its repository implementation.
"""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, Any, List, Optional, Union, Generic, TypeVar

from enn_iot_oc.infrastructure.repository.single_repo_base import SingleRepoBase
from enn_iot_oc.infrastructure.repository.multi_repo_base import MultiRepoBase
from enn_iot_oc.util.string_util import parse_object, parse_array

__all__ = ["Customer", "CustomerRepoImpl"]

T = TypeVar('T')

# 定义基类 - 确保使用Generic[T]
CustomerRepoBase = MultiRepoBase[T]

#------------- Domain Model -------------
@dataclass
class Customer:
    """
    Customer
    """

    cust_id: str = ""
    profile_id: str = ""
    category_id: str = ""
    enterprise_tag: str = ""
    business_unit: str = ""
    industry: str = ""
    profile: Optional['CustomerProfile'] = None
    category: Optional['CustomerCategory'] = None

#------------- Repository Implementation -------------
class CustomerRepoImpl(CustomerRepoBase[Customer]):
    """
    Customer
    """
    def __init__(self, eo_id: str = "", instance_id: str = "") -> None:
        """
        初始化方法
        """
        super().__init__(model_code="customer", eo_id=eo_id, instance_id=instance_id, id_field="cust_id")

    def to_domain(self, row: Dict[str, Any]) -> Customer:
        """
        将数据库行转换为领域模型
        """
        return Customer(
            cust_id=parse_object(row.get("cust_id"), str),
            enterprise_tag=parse_object(row.get("enterprise_tag"), str),
            profile_id=parse_object(row.get("profile_id"), str),
            category_id=parse_object(row.get("category_id"), str),
            business_unit=parse_object(row.get("business_unit"), str),
            industry=parse_object(row.get("industry"), str),
            profile=self._convert_embed_object(row.get("profile"), "CustomerProfile"),
            category=self._convert_embed_object(row.get("category"), "CustomerCategory"),
        )

    def from_domain(self, entity) -> Dict[str, Any]:
        """
        将领域模型转换为数据库行
        """
        return {
            "cust_id": getattr(entity, "cust_id", None),
            "enterprise_tag": getattr(entity, "enterprise_tag", None),
            "profile_id": getattr(entity, "profile_id", None),
            "category_id": getattr(entity, "category_id", None),
            "business_unit": getattr(entity, "business_unit", None),
            "industry": getattr(entity, "industry", None),
            "profile": getattr(entity, "profile", None),
            "category": getattr(entity, "category", None),
        }

    def empty_object(self) -> Customer:
        """
        创建一个空的领域模型对象
        """
        return Customer(
            cust_id="",
            enterprise_tag="",
            profile_id="",
            category_id="",
            business_unit="",
            industry="",
            profile="",
            category="",
        )

    def extract_id(self, entity) -> str:
        """
        提取ID值
        """
        return getattr(entity, "cust_id", "")


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
