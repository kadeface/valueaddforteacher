#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试百分比区间赋分功能
"""

import pandas as pd
import numpy as np
from calculate_scores_final_fix import calculate_scores_final_fix

def test_percentage_scoring():
    """测试百分比区间赋分功能"""
    
    print("=" * 60)
    print("测试百分比区间赋分功能")
    print("=" * 60)
    
    # 测试文件路径
    test_file = 'data/2025Mid3.xls'
    
    # 测试科目
    test_subject = '语文'
    
    print(f"测试文件: {test_file}")
    print(f"测试科目: {test_subject}")
    print()
    
    # 1. 使用固定区间赋分
    print("1. 测试固定区间赋分...")
    try:
        result_fixed = calculate_scores_final_fix(test_file, test_subject, 'fixed')
        if result_fixed is not None:
            print("✅ 固定区间赋分测试成功")
            print(f"   结果行数: {len(result_fixed)}")
            print(f"   结果列数: {len(result_fixed.columns)}")
        else:
            print("❌ 固定区间赋分测试失败")
    except Exception as e:
        print(f"❌ 固定区间赋分测试出错: {e}")
    
    print()
    
    # 2. 使用百分比区间赋分
    print("2. 测试百分比区间赋分...")
    try:
        result_percentage = calculate_scores_final_fix(test_file, test_subject, 'percentage')
        if result_percentage is not None:
            print("✅ 百分比区间赋分测试成功")
            print(f"   结果行数: {len(result_percentage)}")
            print(f"   结果列数: {len(result_percentage.columns)}")
        else:
            print("❌ 百分比区间赋分测试失败")
    except Exception as e:
        print(f"❌ 百分比区间赋分测试出错: {e}")
    
    print()
    
    # 3. 比较两种赋分方式的结果
    if result_fixed is not None and result_percentage is not None:
        print("3. 比较两种赋分方式的结果...")
        
        # 比较综合得分
        if f'{test_subject}综合得分' in result_fixed.columns and f'{test_subject}综合得分' in result_percentage.columns:
            fixed_scores = result_fixed[f'{test_subject}综合得分'].dropna()
            percentage_scores = result_percentage[f'{test_subject}综合得分'].dropna()
            
            print(f"   固定区间赋分 - 综合得分范围: {fixed_scores.min():.2f} - {fixed_scores.max():.2f}")
            print(f"   百分比区间赋分 - 综合得分范围: {percentage_scores.min():.2f} - {percentage_scores.max():.2f}")
            
            # 计算差异
            if len(fixed_scores) == len(percentage_scores):
                differences = percentage_scores - fixed_scores
                print(f"   平均差异: {differences.mean():.2f}")
                print(f"   最大差异: {differences.max():.2f}")
                print(f"   最小差异: {differences.min():.2f}")
        
        # 比较排名
        if f'{test_subject}综合排名' in result_fixed.columns and f'{test_subject}综合排名' in result_percentage.columns:
            fixed_ranks = result_fixed[f'{test_subject}综合排名'].dropna()
            percentage_ranks = result_percentage[f'{test_subject}综合排名'].dropna()
            
            print(f"   固定区间赋分 - 排名范围: {fixed_ranks.min():.0f} - {fixed_ranks.max():.0f}")
            print(f"   百分比区间赋分 - 排名范围: {percentage_ranks.min():.0f} - {percentage_ranks.max():.0f}")
    
    print()
    print("=" * 60)
    print("测试完成")
    print("=" * 60)

def show_percentage_intervals():
    """显示百分比区间的详细信息"""
    print("百分比区间赋分规则:")
    print("=" * 40)
    
    intervals = [
        (0, 0.10, 8, 8.9, "前10%"),
        (0.10, 0.24, 6, 6.9, "10%-24%"),
        (0.24, 0.40, 5, 5.9, "24%-40%"),
        (0.40, 0.60, 4, 4.9, "40%-60%"),
        (0.60, 0.76, 3, 3.9, "60%-76%"),
        (0.76, 0.90, 2, 2.9, "76%-90%"),
        (0.90, 1.00, 0, 0, "90%-100%")
    ]
    
    print(f"{'区间':<12} {'比例':<10} {'常规赋分':<10} {'金山赋分':<10} {'说明':<10}")
    print("-" * 60)
    
    for start, end, regular, jinshan, desc in intervals:
        percentage = f"{start*100:.0f}%-{end*100:.0f}%"
        ratio = f"{(end-start)*100:.0f}%"
        print(f"{percentage:<12} {ratio:<10} {regular:<10} {jinshan:<10} {desc:<10}")
    
    print()
    print("示例：如果总共有100人，排名第5的人")
    print("  百分比 = 5/100 = 5%")
    print("  属于前10%区间")
    print("  常规赋分 = 8分")
    print("  金山中学赋分 = 8.9分")

if __name__ == "__main__":
    # 显示百分比区间规则
    show_percentage_intervals()
    print()
    
    # 运行测试
    test_percentage_scoring()
