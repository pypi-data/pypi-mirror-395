#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成的IoC数据SDK使用示例

此示例展示了如何使用自动生成的Repository接口进行数据查询
"""

# 导入生成的实体和Repository
from infrastructure.model import (
    BiogasProjectInformation, BiogasProjectInformationRepoImpl,
    MechanismCloudAlgorithm, MechanismCloudAlgorithmRepoImpl,
    MechanismTaskPlanning, MechanismTaskPlanningRepoImpl
)

# 导入SDK核心模块
from enn_iot_oc.core import BizContext, set_token, set_biz

def example_usage():
    """使用示例"""
    print("🔍 IoC数据SDK查询示例")
    print("=" * 50)

    # 1. 设置认证（需要替换为实际的token）
    # set_token("your_auth_token", "your_csrf_token")

    # 2. 设置业务上下文
    # set_biz(BizContext(
    #     eo_id="your_eo_id",
    #     instance_id="your_instance_id",
    #     task_id="your_task_id",
    #     job_id="your_job_id"
    # ))

    print("注意: 请先设置正确的认证信息和业务上下文")
    print()

    # 3. 沼气项目信息查询（单行实体）
    print("1. 查询沼气项目信息")
    print("-" * 30)

    try:
        project_repo = BiogasProjectInformationRepoImpl()
        project_info = project_repo.find()

        if project_info:
            print(f"✓ 客户名称: {project_info.customerName}")
            print(f"✓ 总投资: {project_info.totalInvestment}")
            print(f"✓ 年收入: {project_info.totalRevenue}")
        else:
            print("⚠ 未找到沼气项目信息")
    except Exception as e:
        print(f"❌ 查询失败: {e}")

    print()

    # 4. 机理云端算法查询（多行实体）
    print("2. 查询机理云端算法")
    print("-" * 30)

    try:
        algo_repo = MechanismCloudAlgorithmRepoImpl()
        algorithms = algo_repo.list()

        print(f"✓ 共找到 {len(algorithms)} 个算法")
        for i, algo in enumerate(algorithms, 1):
            print(f"  {i}. {algo.algorithmId} - {algo.schemeId}")
    except Exception as e:
        print(f"❌ 查询失败: {e}")

    print()

    # 5. 机理规划子任务查询（多行实体）
    print("3. 查询机理规划子任务")
    print("-" * 30)

    try:
        task_repo = MechanismTaskPlanningRepoImpl()
        tasks = task_repo.list()

        print(f"✓ 共找到 {len(tasks)} 个任务")
        for i, task in enumerate(tasks, 1):
            print(f"  {i}. {task.name} - {task.target}")
    except Exception as e:
        print(f"❌ 查询失败: {e}")

if __name__ == "__main__":
    example_usage()
