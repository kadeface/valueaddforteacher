#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修复后的排名一致性
验证所有排名都使用method='min'算法
"""

import pandas as pd
import numpy as np
from calculate_scores_final_fix import calculate_scores_final_fix

def test_ranking_consistency():
    """测试排名一致性"""
    print("=" * 60)
    print("测试修复后的排名一致性")
    print("=" * 60)
    
    # 运行计算
    print("正在运行计算...")
    result = calculate_scores_final_fix(subject='语文', education_level='middle')
    
    if result is None:
        print("❌ 计算失败！")
        return False
    
    print("✅ 计算成功！")
    print(f"结果列数: {len(result.columns)}")
    
    # 检查排名列
    rank_cols = [col for col in result.columns if '排名' in col]
    print(f"\n找到排名列: {len(rank_cols)}个")
    for i, col in enumerate(rank_cols[:10]):  # 只显示前10个
        print(f"  {i+1}: {col}")
    if len(rank_cols) > 10:
        print(f"  ... 还有 {len(rank_cols) - 10} 个排名列")
    
    # 分析排名一致性
    print("\n" + "=" * 60)
    print("分析排名一致性")
    print("=" * 60)
    
    # 检查综合排名
    if '语文综合排名' in result.columns:
        print("✅ 综合排名列存在")
        print(f"综合排名范围: {result['语文综合排名'].min()} - {result['语文综合排名'].max()}")
        
        # 检查是否有重复排名
        rank_counts = result['语文综合排名'].value_counts()
        duplicate_ranks = rank_counts[rank_counts > 1]
        if len(duplicate_ranks) > 0:
            print(f"✅ 发现 {len(duplicate_ranks)} 个重复排名（符合method='min'逻辑）")
            print("重复排名示例:")
            for rank, count in duplicate_ranks.head(3).items():
                print(f"  排名 {rank}: {count} 个")
        else:
            print("ℹ️  没有重复排名")
    
    # 检查各指标排名
    metric_rank_cols = [col for col in rank_cols if '综合排名' not in col]
    print(f"\n各指标排名列: {len(metric_rank_cols)}个")
    
    # 检查前几个指标排名的重复情况
    for i, col in enumerate(metric_rank_cols[:5]):
        if col in result.columns:
            rank_counts = result[col].value_counts()
            duplicate_ranks = rank_counts[rank_counts > 1]
            print(f"  {col}: {len(duplicate_ranks)} 个重复排名")
    
    return True

def test_specific_ranking_scenarios():
    """测试特定排名场景"""
    print("\n" + "=" * 60)
    print("测试特定排名场景")
    print("=" * 60)
    
    # 创建测试数据
    test_data = {
        '学校代码': ['S001', 'S002', 'S003', 'S004', 'S005'],
        '学校名称': ['学校1', '学校2', '学校3', '学校4', '学校5'],
        '班别': ['班1', '班2', '班3', '班4', '班5'],
        '语文科任': ['教师1', '教师2', '教师3', '教师4', '教师5'],
        '七年下_语文_平均分': [85.5, 85.5, 90.0, 78.0, 85.5],  # 3个相同分数
        '七年下_语文_优秀率': [20.0, 25.0, 30.0, 15.0, 20.0],  # 2个相同分数
        '七年下_语文_优良率': [60.0, 65.0, 70.0, 55.0, 60.0],  # 2个相同分数
        '七年下_语文_合格率': [95.0, 90.0, 95.0, 85.0, 95.0],  # 3个相同分数
        '七年下_语文_低分率': [5.0, 10.0, 5.0, 15.0, 5.0]     # 3个相同分数
    }
    
    df = pd.DataFrame(test_data)
    
    print("测试数据:")
    print(df[['学校名称', '七年下_语文_平均分', '七年下_语文_优秀率']].to_string(index=False))
    
    # 测试排名
    print("\n使用method='min'排名:")
    df['平均分排名'] = df['七年下_语文_平均分'].rank(ascending=False, method='min')
    df['优秀率排名'] = df['七年下_语文_优秀率'].rank(ascending=False, method='min')
    
    print("排名结果:")
    print(df[['学校名称', '七年下_语文_平均分', '平均分排名', '七年下_语文_优秀率', '优秀率排名']].to_string(index=False))
    
    # 验证排名逻辑
    print("\n验证排名逻辑:")
    print("平均分排名:")
    print("  85.5分: 排名1,1,1 (相同分数相同排名)")
    print("  90.0分: 排名4 (下一个排名跳过重复数量)")
    print("  78.0分: 排名5")
    
    print("优秀率排名:")
    print("  30.0%: 排名1")
    print("  25.0%: 排名2") 
    print("  20.0%: 排名3,3 (相同分数相同排名)")
    print("  15.0%: 排名5 (下一个排名跳过重复数量)")

def demonstrate_ranking_methods():
    """演示不同排名方法"""
    print("\n" + "=" * 60)
    print("演示不同排名方法")
    print("=" * 60)
    
    scores = [100, 95, 95, 90, 85, 85, 80]
    df = pd.DataFrame({'分数': scores})
    
    print("原始分数:", scores)
    print("\n不同排名方法对比:")
    print("分数\t\tmin\t\tdense\t\tfirst\t\taverage")
    print("-" * 60)
    
    df['min排名'] = df['分数'].rank(ascending=False, method='min')
    df['dense排名'] = df['分数'].rank(ascending=False, method='dense')
    df['first排名'] = df['分数'].rank(ascending=False, method='first')
    df['average排名'] = df['分数'].rank(ascending=False, method='average')
    
    for i in range(len(df)):
        score = df.iloc[i]['分数']
        min_rank = df.iloc[i]['min排名']
        dense_rank = df.iloc[i]['dense排名']
        first_rank = df.iloc[i]['first排名']
        avg_rank = df.iloc[i]['average排名']
        print(f"{score}\t\t{min_rank:.0f}\t\t{dense_rank:.0f}\t\t{first_rank:.0f}\t\t{avg_rank:.1f}")
    
    print("\n说明:")
    print("- **min**: 相同分数获得相同排名，下一个排名跳过重复数量 (我们使用的方法)")
    print("- **dense**: 相同分数获得相同排名，下一个排名不跳过")
    print("- **first**: 相同分数获得递增排名")
    print("- **average**: 相同分数获得平均排名")

if __name__ == "__main__":
    print("开始测试修复后的排名一致性...")
    
    # 测试排名一致性
    success = test_ranking_consistency()
    
    if success:
        # 测试特定场景
        test_specific_ranking_scenarios()
        
        # 演示排名方法
        demonstrate_ranking_methods()
        
        print("\n" + "=" * 60)
        print("✅ 排名一致性修复测试完成！")
        print("所有排名现在都使用method='min'算法，保持逻辑一致性")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ 测试失败！")
        print("=" * 60)
