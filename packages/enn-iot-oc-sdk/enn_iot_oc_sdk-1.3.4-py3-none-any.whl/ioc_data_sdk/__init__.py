"""
ENN IoC数据SDK

提供工业物联网数据查询和管理功能的Python SDK。

主要功能:
- 实体数据查询 (单行/多行实体)
- 关系数据管理
- 数据缓存和性能优化
- 类型安全的数据访问

基本使用:
    from ioc_data_sdk import BiogasProjectInformation, BiogasProjectInformationRepoImpl

    # 创建Repository实例
    repo = BiogasProjectInformationRepoImpl()

    # 查询数据
    project = repo.find()
    if project:
        print(f"客户名称: {project.customerName}")
"""

__version__ = "1.3.4"
__author__ = "ENN Energy"
__email__ = "developer@enn.com"

# 导入核心模块
from .core import BizContext, set_token, set_biz

# 导入实体和Repository（可能动态生成）
from .entities import *
from .repositories import *

__all__ = [
    # 版本信息
    "__version__",

    # 核心功能
    "BizContext",
    "set_token",
    "set_biz",

    # 实体类
    "Customer",
    "CustomerProfile",
    "CustomerCategory",
    "ProfileDimension",
    "CategoryRequirement",

    # Repository类
    "CustomerRepoImpl",
    "CustomerProfileRepoImpl",
    "CustomerCategoryRepoImpl",
    "ProfileDimensionRepoImpl",
    "CategoryRequirementRepoImpl",

    # 便捷函数
    "get_customers",
    "get_customer_profiles",
    "get_customer_categories",
    "initialize",
]

# 添加便捷函数
def get_customers():
    """获取客户列表的便捷函数"""
    repo = CustomerRepoImpl()
    return repo.list()

def get_customer_profiles():
    """获取客户档案列表的便捷函数"""
    repo = CustomerProfileRepoImpl()
    return repo.list()

def get_customer_categories():
    """获取客户分类列表的便捷函数"""
    repo = CustomerCategoryRepoImpl()
    return repo.list()

# SDK初始化时自动设置认证信息
def initialize(auth_token: str = None, csrf_token: str = None, eo_id: str = None, instance_id: str = None):
    """
    初始化SDK，设置认证和业务上下文

    Args:
        auth_token: 认证令牌
        csrf_token: CSRF令牌
        eo_id: 企业ID
        instance_id: 实例ID
    """
    if auth_token and csrf_token:
        set_token(auth_token, csrf_token)

    if eo_id and instance_id:
        from .core import BizContext
        biz_context = BizContext(
            eo_id=eo_id,
            instance_id=instance_id,
            task_id="",
            job_id=""
        )
        set_biz(biz_context)