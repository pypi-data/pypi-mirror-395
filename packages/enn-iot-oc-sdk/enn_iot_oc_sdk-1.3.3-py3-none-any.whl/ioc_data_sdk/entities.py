"""
实体类定义模块

此模块包含所有预定义的实体类，用户可以直接使用这些类进行数据访问。
"""

# 动态导入实体类
try:
    # 尝试从生成的模块导入实体类
    import sys
    import os

    # 优先从包内路径导入，否则尝试外部路径
    try:
        # 方法1: 直接从包内的模块导入（推荐，适用于已发布的SDK）
        from output.infrastructure.model.Customer import Customer
        from output.infrastructure.model.CustomerProfile import CustomerProfile
        from output.infrastructure.model.CustomerCategory import CustomerCategory
        from output.infrastructure.model.ProfileDimension import ProfileDimension
        from output.infrastructure.model.CategoryRequirement import CategoryRequirement

        # 已经是类对象，直接使用
        CustomerClass = Customer
        CustomerProfileClass = CustomerProfile
        CustomerCategoryClass = CustomerCategory
        ProfileDimensionClass = ProfileDimension
        CategoryRequirementClass = CategoryRequirement

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

        # 获取实体类
        CustomerClass = getattr(Customer, 'Customer')
        CustomerProfileClass = getattr(CustomerProfile, 'CustomerProfile')
        CustomerCategoryClass = getattr(CustomerCategory, 'CustomerCategory')
        ProfileDimensionClass = getattr(ProfileDimension, 'ProfileDimension')
        CategoryRequirementClass = getattr(CategoryRequirement, 'CategoryRequirement')

    # 导入当前命名空间
    globals()['Customer'] = CustomerClass
    globals()['CustomerProfile'] = CustomerProfileClass
    globals()['CustomerCategory'] = CustomerCategoryClass
    globals()['ProfileDimension'] = ProfileDimensionClass
    globals()['CategoryRequirement'] = CategoryRequirementClass

    __all__ = [
        "Customer",
        "CustomerProfile",
        "CustomerCategory",
        "ProfileDimension",
        "CategoryRequirement"
    ]

except ImportError as e:
    # 如果导入失败，提供空的实体类定义
    print(f"警告: 无法导入实体类，请先运行 main.py 生成实体: {e}")

    class Customer:
        def __init__(self):
            self.cust_id = None
            self.enterprise_tag = None

    class CustomerProfile:
        def __init__(self):
            self.profile_id = None
            self.dimension_set = []

    class CustomerCategory:
        def __init__(self):
            self.category_id = None
            self.category_name = None

    class ProfileDimension:
        def __init__(self):
            self.dimension_id = None
            self.dimension_name = None

    class CategoryRequirement:
        def __init__(self):
            self.dimension_id = None
            self.industry_tag = None

    __all__ = [
        "Customer",
        "CustomerProfile",
        "CustomerCategory",
        "ProfileDimension",
        "CategoryRequirement"
    ]