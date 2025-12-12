#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
关联数据测试脚本

此脚本测试实体间的外键关联是否正确处理
"""

import sys
import os

# 添加output目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from infrastructure.model import (
    MechanismCloudAlgorithmRepoImpl,
    MechanismTaskPlanningRepoImpl,
    ddRepoImpl
)

def test_relations():
    """测试数据关联"""
    print("🔗 测试数据关联关系")
    print("=" * 50)

    try:
        # 1. 创建Repository实例
        algo_repo = MechanismCloudAlgorithmRepoImpl()
        task_repo = MechanismTaskPlanningRepoImpl()
        dd_repo = ddRepoImpl()

        # 2. 查询算法数据
        print("\n1. 查询算法数据（包含关联关系）:")
        print("-" * 40)
        algorithms = algo_repo.list()

        for algo in algorithms:
            print(f"\n算法ID: {algo.algorithmId}")
            print(f"方案ID: {algo.schemeId}")
            print(f"子任务ID: {algo.cSchemeId}")

            # 检查关联的子任务对象
            if algo.mechanismSubtaskObject:
                print(f"✓ 关联子任务: {algo.mechanismSubtaskObject.name}")
                print(f"  目标: {algo.mechanismSubtaskObject.target}")
            else:
                print("⚠ 未关联子任务对象")

            # 检查关联的DD对象列表
            if algo.ddObject and len(algo.ddObject) > 0:
                print(f"✓ 关联DD对象数量: {len(algo.ddObject)}")
                for dd in algo.ddObject:
                    print(f"  - DD ID: {dd.id}, 数值: {dd.num}")
            else:
                print("⚠ 未关联DD对象列表")

        # 3. 单独查询任务数据
        print("\n\n2. 单独查询任务数据:")
        print("-" * 40)
        tasks = task_repo.list()
        for task in tasks[:2]:  # 只显示前两个
            print(f"任务ID: {task.id}")
            print(f"任务名: {task.name}")

        # 4. 单独查询DD数据
        print("\n\n3. 单独查询DD数据:")
        print("-" * 40)
        dd_data = dd_repo.list()
        for dd in dd_data[:3]:  # 只显示前三个
            print(f"DD ID: {dd.id}, 数值: {dd.num}")

        print("\n\n🎉 关联数据测试完成！")

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_relations()
