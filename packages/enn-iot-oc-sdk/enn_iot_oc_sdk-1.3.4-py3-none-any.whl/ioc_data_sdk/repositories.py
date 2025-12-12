"""
Repository实现模块

此模块包含所有预定义的Repository类，用户可以直接使用这些类进行数据查询。
"""

# 动态导入Repository类
try:
    # 尝试从生成的模块导入Repository类
    import sys
    import os

    # 优先从包内路径导入，否则尝试外部路径
    try:
        # 方法1: 直接从包内的模块导入（推荐，适用于已发布的SDK）
        from output.infrastructure.model.Customer import CustomerRepoImpl
        from output.infrastructure.model.CustomerProfile import CustomerProfileRepoImpl
        from output.infrastructure.model.CustomerCategory import CustomerCategoryRepoImpl
        from output.infrastructure.model.ProfileDimension import ProfileDimensionRepoImpl
        from output.infrastructure.model.CategoryRequirement import CategoryRequirementRepoImpl

        # 已经是类对象，直接使用
        CustomerRepoImplClass = CustomerRepoImpl
        CustomerProfileRepoImplClass = CustomerProfileRepoImpl
        CustomerCategoryRepoImplClass = CustomerCategoryRepoImpl
        ProfileDimensionRepoImplClass = ProfileDimensionRepoImpl
        CategoryRequirementRepoImplClass = CategoryRequirementRepoImpl

    except ImportError:
        # 方法2: 从外部output目录导入（用于开发环境）
        output_path = os.path.join(os.path.dirname(__file__), '..', 'output', 'infrastructure', 'model')
        if output_path not in sys.path:
            sys.path.insert(0, output_path)

        # 直接导入模块
        import Customer
        import CustomerProfile
        import CustomerCategory
        import ProfileDimension
        import CategoryRequirement

        # 获取Repository类
        CustomerRepoImplClass = getattr(Customer, 'CustomerRepoImpl')
        CustomerProfileRepoImplClass = getattr(CustomerProfile, 'CustomerProfileRepoImpl')
        CustomerCategoryRepoImplClass = getattr(CustomerCategory, 'CustomerCategoryRepoImpl')
        ProfileDimensionRepoImplClass = getattr(ProfileDimension, 'ProfileDimensionRepoImpl')
        CategoryRequirementRepoImplClass = getattr(CategoryRequirement, 'CategoryRequirementRepoImpl')

    # 导入当前命名空间
    globals()['CustomerRepoImpl'] = CustomerRepoImplClass
    globals()['CustomerProfileRepoImpl'] = CustomerProfileRepoImplClass
    globals()['CustomerCategoryRepoImpl'] = CustomerCategoryRepoImplClass
    globals()['ProfileDimensionRepoImpl'] = ProfileDimensionRepoImplClass
    globals()['CategoryRequirementRepoImpl'] = CategoryRequirementRepoImplClass

    __all__ = [
        "CustomerRepoImpl",
        "CustomerProfileRepoImpl",
        "CustomerCategoryRepoImpl",
        "ProfileDimensionRepoImpl",
        "CategoryRequirementRepoImpl"
    ]

except ImportError as e:
    # 如果导入失败，提供空的Repository类定义
    print(f"警告: 无法导入Repository类，请先运行 main.py 生成Repository: {e}")

    class CustomerRepoImpl:
        def __init__(self, **kwargs):
            pass
        def list(self):
            return []
        def find_by_id(self, id):
            return None

    class CustomerProfileRepoImpl:
        def __init__(self, **kwargs):
            pass
        def list(self):
            return []
        def find_by_id(self, id):
            return None

    class CustomerCategoryRepoImpl:
        def __init__(self, **kwargs):
            pass
        def list(self):
            return []
        def find_by_id(self, id):
            return None

    class ProfileDimensionRepoImpl:
        def __init__(self, **kwargs):
            pass
        def list(self):
            return []
        def find_by_id(self, id):
            return None

    class CategoryRequirementRepoImpl:
        def __init__(self, **kwargs):
            pass
        def list(self):
            return []
        def find_by_id(self, id):
            return None

    __all__ = [
        "CustomerRepoImpl",
        "CustomerProfileRepoImpl",
        "CustomerCategoryRepoImpl",
        "ProfileDimensionRepoImpl",
        "CategoryRequirementRepoImpl"
    ]