"""
Repository实现模块

此模块包含所有预定义的Repository类，用户可以直接使用这些类进行数据查询。
"""

# 动态导入Repository类
try:
    # 尝试从生成的模块导入Repository类
    import sys
    import os
    output_path = os.path.join(os.path.dirname(__file__), '..', 'output', 'infrastructure', 'model')
    if output_path not in sys.path:
        sys.path.insert(0, output_path)

    # 直接导入模块
    import BiogasProjectInformation
    import MechanismCloudAlgorithm
    import MechanismTaskPlanning

    # 获取Repository类
    BiogasProjectInformationRepoImplClass = getattr(BiogasProjectInformation, 'BiogasProjectInformationRepoImpl')
    MechanismCloudAlgorithmRepoImplClass = getattr(MechanismCloudAlgorithm, 'MechanismCloudAlgorithmRepoImpl')
    MechanismTaskPlanningRepoImplClass = getattr(MechanismTaskPlanning, 'MechanismTaskPlanningRepoImpl')

    # 导入当前命名空间
    globals()['BiogasProjectInformationRepoImpl'] = BiogasProjectInformationRepoImplClass
    globals()['MechanismCloudAlgorithmRepoImpl'] = MechanismCloudAlgorithmRepoImplClass
    globals()['MechanismTaskPlanningRepoImpl'] = MechanismTaskPlanningRepoImplClass

    __all__ = [
        "BiogasProjectInformationRepoImpl",
        "MechanismCloudAlgorithmRepoImpl",
        "MechanismTaskPlanningRepoImpl"
    ]

except ImportError as e:
    # 如果导入失败，提供空的Repository类定义
    print(f"警告: 无法导入Repository类，请先运行 main.py 生成Repository: {e}")

    class BiogasProjectInformationRepoImpl:
        def __init__(self, **kwargs):
            pass
        def find(self):
            return None

    class MechanismCloudAlgorithmRepoImpl:
        def __init__(self, **kwargs):
            pass
        def list(self):
            return []
        def find_by_id(self, id):
            return None

    class MechanismTaskPlanningRepoImpl:
        def __init__(self, **kwargs):
            pass
        def list(self):
            return []
        def find_by_id(self, id):
            return None

    __all__ = [
        "BiogasProjectInformationRepoImpl",
        "MechanismCloudAlgorithmRepoImpl",
        "MechanismTaskPlanningRepoImpl"
    ]