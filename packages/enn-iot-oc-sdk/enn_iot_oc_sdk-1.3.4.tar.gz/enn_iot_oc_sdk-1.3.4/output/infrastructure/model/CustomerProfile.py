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
        from dataclasses import asdict, is_dataclass
        result = {
            "profile_id": getattr(entity, "profile_id", None),
            "dimension_set": getattr(entity, "dimension_set", None),
            "associated_cust_id": getattr(entity, "associated_cust_id", None),
            "update_time": getattr(entity, "update_time", None),
            "dimensions": [asdict(item) if is_dataclass(item) else item for item in getattr(entity, "dimensions", [])] if getattr(entity, "dimensions", None) else [],
        }
        return result

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
        使用目标Repository的to_domain()方法以正确处理嵌套字段
        """
        if not embed_data:
            return None
        
        # 如果已经是对象，直接返回
        if not isinstance(embed_data, dict):
            return embed_data
        
        # 如果是字典数据，使用Repository的to_domain()转换
        try:
            # 动态导入目标实体的Repository
            import sys
            import os
            current_dir = os.path.dirname(os.path.abspath(__file__))
            if current_dir not in sys.path:
                sys.path.insert(0, current_dir)
            
            # 导入目标实体模块
            target_module = __import__(target_entity_name)
            # 获取Repository类（命名规范：{EntityName}RepoImpl）
            repo_class_name = f"{target_entity_name}RepoImpl"
            if hasattr(target_module, repo_class_name):
                repo_class = getattr(target_module, repo_class_name)
                repo_instance = repo_class()
                # 使用to_domain()方法转换，这会正确处理嵌套字段
                return repo_instance.to_domain(embed_data)
            else:
                # 如果没有Repository，直接用类构造
                target_class = getattr(target_module, target_entity_name)
                return target_class(**embed_data)
        except Exception as e:
            # 转换失败，返回None
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
        return result

    def _load_related_data(self, record_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        加载关系数据并填充嵌入字段
        """
        import json
        import os
        
        # 加载 dimensions 关系数据
        if 'dimension_set' in record_data:
            source_value = record_data['dimension_set']
            target_records = self._load_target_entity_data('profile_dimension')
            if target_records:
                matched_records = []
                if isinstance(source_value, list):
                    # source 是列表，需要 IN 查询
                    for rec in target_records:
                        if rec.get('dimension_id') in source_value:
                            matched_records.append(rec)
                else:
                    # source 是单值，匹配相同值
                    for rec in target_records:
                        if rec.get('dimension_id') == source_value:
                            matched_records.append(rec)
                record_data['dimensions'] = matched_records
        
        return record_data

    def _load_target_entity_data(self, target_table: str) -> List[Dict[str, Any]]:
        """
        加载目标实体的所有数据
        优先从缓存文件加载，以获取完整的关联数据
        """
        import json
        import os
        
        # 1. 最优先：从缓存文件加载（包含完整的关联数据）
        cache_file = f'mock_data_{target_table}.json'
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data if isinstance(data, list) else [data]
            except Exception:
                pass
        
        # 2. 从源文件加载（如果缓存不存在）
        # 尝试从多个路径加载数据
        possible_paths = [
            f'ioc_data_sdk/data/source/{target_table}.json',
            f'data/demo/source/{target_table}.json',
            f'data/source/{target_table}.json',
        ]
        
        # 也尝试从SDK包内加载
        try:
            import ioc_data_sdk
            sdk_data_dir = os.path.join(os.path.dirname(ioc_data_sdk.__file__), 'data', 'source')
            possible_paths.insert(0, os.path.join(sdk_data_dir, f'{target_table}.json'))
        except ImportError:
            pass
        
        for path in possible_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        return data if isinstance(data, list) else [data]
                except Exception:
                    continue
        
        return []
