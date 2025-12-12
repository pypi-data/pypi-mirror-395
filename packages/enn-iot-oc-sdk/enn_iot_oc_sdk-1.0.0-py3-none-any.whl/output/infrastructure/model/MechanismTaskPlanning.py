"""
MechanismTaskPlanning domain model and its repository implementation.
"""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, Any, List, Optional, Union, Generic, TypeVar

from enn_iot_oc.infrastructure.repository.single_repo_base import SingleRepoBase
from enn_iot_oc.infrastructure.repository.multi_repo_base import MultiRepoBase
from enn_iot_oc.util.string_util import parse_object, parse_array

__all__ = ["MechanismTaskPlanning", "MechanismTaskPlanningRepoImpl"]

T = TypeVar('T')

# 定义基类 - 确保使用Generic[T]
MechanismTaskPlanningRepoBase = MultiRepoBase[T]

#------------- Domain Model -------------
@dataclass
class MechanismTaskPlanning:
    """
    机理规划子任务
    """

    id: str = ""
    desc: str = ""
    name: str = ""
    target: str = ""
    taskList: List[str] = field(default_factory=list)

#------------- Repository Implementation -------------
class MechanismTaskPlanningRepoImpl(MechanismTaskPlanningRepoBase[MechanismTaskPlanning]):
    """
    机理规划子任务
    """
    def __init__(self, eo_id: str = "", instance_id: str = "") -> None:
        """
        初始化方法
        """
        super().__init__(model_code="mechanism_task_planning", eo_id=eo_id, instance_id=instance_id, id_field="id")

    def to_domain(self, row: Dict[str, Any]) -> MechanismTaskPlanning:
        """
        将数据库行转换为领域模型
        """
        return MechanismTaskPlanning(
            desc=parse_object(row.get("desc"), str),
            id=parse_object(row.get("id"), str),
            name=parse_object(row.get("name"), str),
            target=parse_object(row.get("target"), str),
            taskList=parse_array(row.get("task_list"), List),
        )

    def from_domain(self, entity) -> Dict[str, Any]:
        """
        将领域模型转换为数据库行
        """
        return {
            "desc": getattr(entity, "desc", None),
            "id": getattr(entity, "id", None),
            "name": getattr(entity, "name", None),
            "target": getattr(entity, "target", None),
            "task_list": getattr(entity, "taskList", None),
        }

    def empty_object(self) -> MechanismTaskPlanning:
        """
        创建一个空的领域模型对象
        """
        return MechanismTaskPlanning(
            desc="",
            id="",
            name="",
            target="",
            taskList=field(default_factory=list),
        )

    def extract_id(self, entity) -> str:
        """
        提取ID值
        """
        return getattr(entity, "id", "")
