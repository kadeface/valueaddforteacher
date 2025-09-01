#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试统一的百分比赋分规则
验证不同总人数下的赋分结果
"""

import pandas as pd
import numpy as np
from calculate_scores_final_fix import calculate_scores_final_fix

def test_unified_scoring():
    """测试统一百分比赋分规则"""
    
    print("=" * 80)
    print("统一百分比赋分规则测试")
    print("=" * 80)
    
    # 测试文件路径
    test_file = 'data/2025Mid3.xls'
    
    print(f"测试文件: {test_file}")
    print()
    
    # 测试处理
    print("1. 测试统一百分比赋分...")
    try:
        result = calculate_scores_final_fix(test_file, '语文')
        if result is not None:
            print("✅ 统一百分比赋分测试成功")
            print(f"   结果行数: {len(result)}")
            print(f"   结果列数: {len(result.columns)}")
            
            # 分析赋分分布
            if '语文综合得分' in result.columns:
                scores = result['语文综合得分'].dropna()
                print(f"   综合得分范围: {scores.min():.2f} - {scores.max():.2f}")
                print(f"   平均得分: {scores.mean():.2f}")
                
                # 统计各分数段人数
                print("   分数分布:")
                score_ranges = [(0, 2), (2, 4), (4, 6), (6, 8), (8, 10)]
                for low, high in score_ranges:
                    count = len(scores[(scores >= low) & (scores < high)])
                    percentage = count / len(scores) * 100
                    print(f"     {low}-{high}分: {count}人 ({percentage:.1f}%)")
        else:
            print("❌ 统一百分比赋分测试失败")
    except Exception as e:
        print(f"❌ 统一百分比赋分测试出错: {e}")
    
    print()

def test_different_sizes():
    """测试不同规模下的赋分区间"""
    
    print("2. 测试不同规模下的赋分区间...")
    print("-" * 60)
    
    # 定义百分比区间
    percentage_intervals = [
        (0, 0.10, 8, 8.9),      # 前10%
        (0.10, 0.24, 6, 6.9),   # 10%-24%
        (0.24, 0.40, 5, 5.9),   # 24%-40%
        (0.40, 0.60, 4, 4.9),   # 40%-60%
        (0.60, 0.76, 3, 3.9),   # 60%-76%
        (0.76, 0.90, 2, 2.9),   # 76%-90%
        (0.90, 1.00, 0, 0)      # 90%-100%
    ]
    
    def generate_intervals(total_count):
        """生成指定总人数的赋分区间"""
        intervals = []
        for start_pct, end_pct, regular_score, jinshan_score in percentage_intervals:
            start_rank = round(start_pct * total_count)
            end_rank = round(end_pct * total_count)
            
            if start_rank == 0:
                start_rank = 1
            
            intervals.append((start_rank, end_rank, regular_score, jinshan_score))
        
        return intervals
    
    # 测试不同规模
    test_sizes = [20, 50, 100, 176, 200, 500]
    
    for size in test_sizes:
        print(f"\n总人数: {size}")
        intervals = generate_intervals(size)
        
        print(f"{'排名区间':<15} {'人数':<8} {'比例':<10} {'赋分':<8}")
        print("-" * 50)
        
        for start, end, regular, jinshan in intervals:
            count = end - start + 1
            percentage = count / size * 100
            print(f"{start}-{end:<10} {count:<8} {percentage:>6.1f}% {regular:<8}")

def demonstrate_unified_advantage():
    """演示统一赋分规则的优势"""
    
    print("\n" + "=" * 80)
    print("统一赋分规则的优势演示")
    print("=" * 80)
    
    print("🎯 优势1: 适用于任意规模")
    print("   - 不再需要根据总人数选择不同的赋分规则")
    print("   - 自动适应不同规模的学校")
    print("   - 相对排名更加公平")
    
    print("\n🎯 优势2: 四舍五入确保精确性")
    print("   - 使用round()函数进行四舍五入")
    print("   - 误差控制在±0.5以内")
    print("   - 保持赋分结果的稳定性")
    
    print("\n🎯 优势3: 代码简化")
    print("   - 统一的assign_score函数")
    print("   - 不再需要scoring_method参数")
    print("   - 减少代码复杂度和维护成本")
    
    print("\n🎯 优势4: 用户体验提升")
    print("   - 界面更简洁")
    print("   - 无需选择赋分方式")
    print("   - 自动获得最佳赋分结果")

if __name__ == "__main__":
    # 测试统一赋分规则
    test_unified_scoring()
    
    # 测试不同规模
    test_different_sizes()
    
    # 演示优势
    demonstrate_unified_advantage()
