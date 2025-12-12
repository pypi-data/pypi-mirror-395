"""
实体类定义模块

此模块包含所有预定义的实体类，用户可以直接使用这些类进行数据访问。
"""

# 动态导入实体类
try:
    # 尝试从生成的模块导入实体类
    import sys
    import os
    output_path = os.path.join(os.path.dirname(__file__), '..', 'output', 'infrastructure', 'model')
    if output_path not in sys.path:
        sys.path.insert(0, output_path)

    # 直接导入模块
    import BiogasProjectInformation
    import MechanismCloudAlgorithm
    import MechanismTaskPlanning

    # 获取实体类
    BiogasProjectInformationClass = getattr(BiogasProjectInformation, 'BiogasProjectInformation')
    MechanismCloudAlgorithmClass = getattr(MechanismCloudAlgorithm, 'MechanismCloudAlgorithm')
    MechanismTaskPlanningClass = getattr(MechanismTaskPlanning, 'MechanismTaskPlanning')

    # 导入当前命名空间
    globals()['BiogasProjectInformation'] = BiogasProjectInformationClass
    globals()['MechanismCloudAlgorithm'] = MechanismCloudAlgorithmClass
    globals()['MechanismTaskPlanning'] = MechanismTaskPlanningClass

    __all__ = [
        "BiogasProjectInformation",
        "MechanismCloudAlgorithm",
        "MechanismTaskPlanning"
    ]

except ImportError as e:
    # 如果导入失败，提供空的实体类定义
    print(f"警告: 无法导入实体类，请先运行 main.py 生成实体: {e}")

    class BiogasProjectInformation:
        def __init__(self):
            self.customerName = None
            self.totalInvestment = None

    class MechanismCloudAlgorithm:
        def __init__(self):
            self.algorithmId = None
            self.schemeId = None

    class MechanismTaskPlanning:
        def __init__(self):
            self.id = None
            self.name = None

    __all__ = [
        "BiogasProjectInformation",
        "MechanismCloudAlgorithm",
        "MechanismTaskPlanning"
    ]