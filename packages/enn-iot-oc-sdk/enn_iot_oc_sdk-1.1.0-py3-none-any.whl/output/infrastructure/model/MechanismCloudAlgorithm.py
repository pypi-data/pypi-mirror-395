"""
MechanismCloudAlgorithm domain model and its repository implementation.
"""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, Any, List, Optional, Union, Generic, TypeVar

from enn_iot_oc.infrastructure.repository.single_repo_base import SingleRepoBase
from enn_iot_oc.infrastructure.repository.multi_repo_base import MultiRepoBase
from enn_iot_oc.util.string_util import parse_object, parse_array

__all__ = ["MechanismCloudAlgorithm", "MechanismCloudAlgorithmRepoImpl"]

T = TypeVar('T')

# 定义基类 - 确保使用Generic[T]
MechanismCloudAlgorithmRepoBase = MultiRepoBase[T]

#------------- Domain Model -------------
@dataclass
class MechanismCloudAlgorithm:
    """
    机理云端算法
    """

    algorithmId: str = ""
    cSchemeId: str = ""
    comOneid: str = ""
    cvcuId: str = ""
    schemeId: str = ""
    mechanismSubtaskObject: Optional[List['MechanismTaskPlanning']] = field(default_factory=list)

#------------- Repository Implementation -------------
class MechanismCloudAlgorithmRepoImpl(MechanismCloudAlgorithmRepoBase[MechanismCloudAlgorithm]):
    """
    机理云端算法
    """
    def __init__(self, eo_id: str = "", instance_id: str = "") -> None:
        """
        初始化方法
        """
        super().__init__(model_code="mechanism_cloud_algorithm", eo_id=eo_id, instance_id=instance_id, id_field="algorithmId")

    def to_domain(self, row: Dict[str, Any]) -> MechanismCloudAlgorithm:
        """
        将数据库行转换为领域模型
        """
        return MechanismCloudAlgorithm(
            algorithmId=parse_object(row.get("algorithm_id"), str),
            cSchemeId=parse_object(row.get("c_scheme_id"), str),
            comOneid=parse_object(row.get("com_oneid"), str),
            cvcuId=parse_object(row.get("cvcu_id"), str),
            schemeId=parse_object(row.get("scheme_id"), str),
            mechanismSubtaskObject=parse_object(row.get("mechanism_subtask_object"), object),
        )

    def from_domain(self, entity) -> Dict[str, Any]:
        """
        将领域模型转换为数据库行
        """
        return {
            "algorithm_id": getattr(entity, "algorithmId", None),
            "c_scheme_id": getattr(entity, "cSchemeId", None),
            "com_oneid": getattr(entity, "comOneid", None),
            "cvcu_id": getattr(entity, "cvcuId", None),
            "scheme_id": getattr(entity, "schemeId", None),
            "mechanism_subtask_object": getattr(entity, "mechanismSubtaskObject", None),
        }

    def empty_object(self) -> MechanismCloudAlgorithm:
        """
        创建一个空的领域模型对象
        """
        return MechanismCloudAlgorithm(
            algorithmId="",
            cSchemeId="",
            comOneid="",
            cvcuId="",
            schemeId="",
            mechanismSubtaskObject="",
        )

    def extract_id(self, entity) -> str:
        """
        提取ID值
        """
        return getattr(entity, "algorithmId", "")
