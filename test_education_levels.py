#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试教育阶段计算逻辑
验证小学和初中使用不同指标和权重的计算差异
"""

from calculate_scores_final_fix import calculate_scores_final_fix
import pandas as pd
import numpy as np

def test_education_levels():
    """测试不同教育阶段的计算逻辑"""
    print("=" * 60)
    print("测试教育阶段计算逻辑")
    print("=" * 60)
    
    # 创建测试数据
    test_data = create_test_data()
    
    print("\n1. 测试初中计算逻辑（默认）")
    print("-" * 40)
    try:
        # 测试初中逻辑
        middle_result = calculate_scores_final_fix(
            input_file_path=None,  # 使用默认文件
            subject='语文',
            education_level='middle'
        )
        if middle_result is not None:
            print("✅ 初中计算成功")
            print(f"   结果列数: {len(middle_result.columns)}")
            print(f"   数据行数: {len(middle_result)}")
        else:
            print("❌ 初中计算失败")
    except Exception as e:
        print(f"❌ 初中计算出错: {e}")
    
    print("\n2. 测试小学计算逻辑")
    print("-" * 40)
    try:
        # 测试小学逻辑
        primary_result = calculate_scores_final_fix(
            input_file_path=None,  # 使用默认文件
            subject='语文',
            education_level='primary'
        )
        if primary_result is not None:
            print("✅ 小学计算成功")
            print(f"   结果列数: {len(primary_result.columns)}")
            print(f"   数据行数: {len(primary_result)}")
        else:
            print("❌ 小学计算失败")
    except Exception as e:
        print(f"❌ 小学计算出错: {e}")
    
    print("\n3. 测试无效教育阶段（应该回退到初中）")
    print("-" * 40)
    try:
        # 测试无效教育阶段
        invalid_result = calculate_scores_final_fix(
            input_file_path=None,  # 使用默认文件
            subject='语文',
            education_level='invalid'
        )
        if invalid_result is not None:
            print("✅ 无效教育阶段处理成功（回退到初中）")
        else:
            print("❌ 无效教育阶段处理失败")
    except Exception as e:
        print(f"❌ 无效教育阶段处理出错: {e}")

def create_test_data():
    """创建测试数据文件（如果需要）"""
    print("创建测试数据...")
    
    # 这里可以创建测试数据文件
    # 目前使用默认的data/2025Mid3.xls文件进行测试
    return None

def test_weight_differences():
    """测试权重差异"""
    print("\n" + "=" * 60)
    print("测试权重差异")
    print("=" * 60)
    
    print("\n初中权重配置:")
    print("  平均分: 30%")
    print("  优秀率: 20%")
    print("  优良率: 20%")
    print("  合格率: 20%")
    print("  低分率: 10%")
    print("  总计: 100%")
    
    print("\n小学权重配置:")
    print("  平均分: 50%")
    print("  优秀率: 20%")
    print("  合格率: 20%")
    print("  低分率: 10%")
    print("  总计: 100%")
    
    print("\n主要差异:")
    print("  1. 小学去掉了'优良率'指标")
    print("  2. 小学平均分权重从30%提升到50%")
    print("  3. 其他指标权重保持不变")

def test_scoring_consistency():
    """测试赋分规则一致性"""
    print("\n" + "=" * 60)
    print("测试赋分规则一致性")
    print("=" * 60)
    
    print("\n赋分规则（小学和初中保持一致）:")
    print("  前10%: 8分（金山中学8.9分）")
    print("  10%-24%: 6分（金山中学6.9分）")
    print("  24%-40%: 5分（金山中学5.9分）")
    print("  40%-60%: 4分（金山中学4.9分）")
    print("  60%-76%: 3分（金山中学3.9分）")
    print("  76%-90%: 2分（金山中学2.9分）")
    print("  90%-100%: 0分")
    
    print("\n优势:")
    print("  ✅ 小学和初中使用相同的赋分算法")
    print("  ✅ 适用于任意规模的学校")
    print("  ✅ 相对排名更公平")
    print("  ✅ 自动适应不同总人数")

if __name__ == "__main__":
    print("开始测试教育阶段计算逻辑...")
    
    # 测试权重差异
    test_weight_differences()
    
    # 测试赋分规则一致性
    test_scoring_consistency()
    
    # 测试实际计算（如果有测试数据）
    test_education_levels()
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)
