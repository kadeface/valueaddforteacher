#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
深入调试排名不一致问题
分析为什么会出现相同分数采用不同排名方式的情况
"""

import pandas as pd
import numpy as np

def create_test_data():
    """创建测试数据，模拟你截图中的情况"""
    print("=" * 60)
    print("创建测试数据，模拟截图中的排名不一致情况")
    print("=" * 60)
    
    # 根据你的截图数据创建测试数据
    test_data = {
        '学校代码': [f'S{i:03d}' for i in range(1, 36)],
        '学校名称': [f'学校{i}' for i in range(1, 36)],
        '班别': [f'班{i}' for i in range(1, 36)],
        '语文科任': [f'教师{i}' for i in range(1, 36)],
        '语文综合得分': [
            3.79, 3.76, 3.74, 3.73, 3.73, 3.72, 3.71, 3.70, 3.69, 3.68,
            3.67, 3.66, 3.66, 3.65, 3.64, 3.63, 3.62, 3.61, 3.60, 3.59,
            3.58, 3.57, 3.56, 3.55, 3.54, 3.53, 3.52, 3.51, 3.51, 3.50,
            3.49, 3.48, 3.47, 3.46, 3.46
        ]
    }
    
    df = pd.DataFrame(test_data)
    
    print("测试数据概览:")
    print(f"  总行数: {len(df)}")
    print(f"  唯一分数数量: {df['语文综合得分'].nunique()}")
    print(f"  重复分数数量: {len(df) - df['语文综合得分'].nunique()}")
    
    # 找出重复的分数
    duplicate_scores = df['语文综合得分'].value_counts()
    duplicate_scores = duplicate_scores[duplicate_scores > 1]
    print(f"\n重复的分数:")
    for score, count in duplicate_scores.items():
        print(f"  {score}: {count}次")
    
    return df

def test_different_ranking_methods(df):
    """测试不同的排名方法"""
    print("\n" + "=" * 60)
    print("测试不同的排名方法")
    print("=" * 60)
    
    # 方法1: method='min' (当前使用的方法)
    df['排名_min'] = df['语文综合得分'].rank(ascending=False, method='min')
    
    # 方法2: method='dense' (密集排名)
    df['排名_dense'] = df['语文综合得分'].rank(ascending=False, method='dense')
    
    # 方法3: method='first' (按顺序排名)
    df['排名_first'] = df['语文综合得分'].rank(ascending=False, method='first')
    
    # 方法4: method='average' (平均排名)
    df['排名_average'] = df['语文综合得分'].rank(ascending=False, method='average')
    
    print("不同排名方法的结果对比:")
    print("分数\t\tmin\t\tdense\t\tfirst\t\taverage")
    print("-" * 80)
    
    for i in range(len(df)):
        score = df.iloc[i]['语文综合得分']
        min_rank = df.iloc[i]['排名_min']
        dense_rank = df.iloc[i]['排名_dense']
        first_rank = df.iloc[i]['排名_first']
        avg_rank = df.iloc[i]['排名_average']
        print(f"{score:.2f}\t\t{min_rank:.0f}\t\t{dense_rank:.0f}\t\t{first_rank:.0f}\t\t{avg_rank:.1f}")
    
    return df

def analyze_ranking_inconsistency(df):
    """分析排名不一致的具体情况"""
    print("\n" + "=" * 60)
    print("深入分析排名不一致问题")
    print("=" * 60)
    
    # 找出重复分数的情况
    duplicate_scores = df['语文综合得分'].value_counts()
    duplicate_scores = duplicate_scores[duplicate_scores > 1]
    
    print("重复分数的排名分析:")
    for score, count in duplicate_scores.items():
        print(f"\n分数 {score} (出现{count}次):")
        
        # 找出这个分数的所有行
        score_rows = df[df['语文综合得分'] == score]
        
        for idx, row in score_rows.iterrows():
            min_rank = row['排名_min']
            dense_rank = row['排名_dense']
            first_rank = row['排名_first']
            avg_rank = row['排名_average']
            
            print(f"  行{idx}: 学校{row['学校名称']}, 班{row['班别']}")
            print(f"    min排名: {min_rank:.0f}, dense排名: {dense_rank:.0f}")
            print(f"    first排名: {first_rank:.0f}, average排名: {avg_rank:.1f}")
    
    print("\n问题分析:")
    print("1. **method='min'**: 相同分数获得相同排名，下一个排名跳过重复数量")
    print("2. **method='dense'**: 相同分数获得相同排名，下一个排名不跳过")
    print("3. **method='first'**: 相同分数获得递增排名")
    print("4. **method='average'**: 相同分数获得平均排名")

def simulate_manual_ranking():
    """模拟手动排名的过程"""
    print("\n" + "=" * 60)
    print("模拟手动排名过程")
    print("=" * 60)
    
    # 创建简单的测试数据
    scores = [100, 95, 95, 90, 85, 85, 80]
    
    print("原始分数:", scores)
    print("排序后分数:", sorted(scores, reverse=True))
    
    print("\n手动排名过程:")
    print("分数\t\t手动排名\t\tpandas.rank(method='min')")
    print("-" * 50)
    
    # 手动排名
    sorted_scores = sorted(scores, reverse=True)
    manual_ranks = []
    current_rank = 1
    
    for i, score in enumerate(sorted_scores):
        if i > 0 and score < sorted_scores[i-1]:
            current_rank = i + 1
        manual_ranks.append(current_rank)
    
    # pandas排名
    df_test = pd.DataFrame({'分数': scores})
    pandas_ranks = df_test['分数'].rank(ascending=False, method='min')
    
    for i, score in enumerate(sorted_scores):
        manual_rank = manual_ranks[i]
        pandas_rank = pandas_ranks[scores.index(score)]
        print(f"{score}\t\t{manual_rank}\t\t\t{pandas_rank:.0f}")

def investigate_potential_causes():
    """调查可能的原因"""
    print("\n" + "=" * 60)
    print("调查排名不一致的可能原因")
    print("=" * 60)
    
    print("可能的原因分析:")
    print("\n1. **数据来源不一致**:")
    print("   - 综合得分可能来自不同的计算过程")
    print("   - 某些分数可能经过了不同的处理逻辑")
    
    print("\n2. **计算精度问题**:")
    print("   - 浮点数计算可能产生微小的精度差异")
    print("   - 这些差异可能导致看似相同的分数实际不同")
    
    print("\n3. **数据处理顺序问题**:")
    print("   - 不同阶段的数据处理可能使用了不同的排名方法")
    print("   - 综合排名和指标排名可能使用了不同的算法")
    
    print("\n4. **边界条件处理**:")
    print("   - 最低分(3.46)可能使用了特殊的处理逻辑")
    print("   - 系统可能对某些特定情况使用了不同的排名方式")
    
    print("\n5. **代码逻辑分支**:")
    print("   - 可能存在条件判断，对某些分数使用不同的排名方法")
    print("   - 需要检查代码中是否有if-else分支导致不一致")

def recommend_solutions():
    """推荐解决方案"""
    print("\n" + "=" * 60)
    print("推荐解决方案")
    print("=" * 60)
    
    print("1. **统一排名方法**:")
    print("   - 所有排名都使用pandas.rank()方法")
    print("   - 推荐使用method='dense'，保持排名逻辑一致性")
    
    print("\n2. **检查数据精度**:")
    print("   - 使用round()函数统一数据精度")
    print("   - 避免浮点数精度差异导致的排名问题")
    
    print("\n3. **代码审查**:")
    print("   - 检查是否有条件分支导致不同的排名逻辑")
    print("   - 确保所有排名计算使用相同的算法")
    
    print("\n4. **测试验证**:")
    print("   - 创建单元测试验证排名一致性")
    print("   - 使用不同的测试数据集验证排名逻辑")

if __name__ == "__main__":
    print("开始深入调试排名不一致问题...")
    
    # 创建测试数据
    df = create_test_data()
    
    # 测试不同排名方法
    df = test_different_ranking_methods(df)
    
    # 分析排名不一致
    analyze_ranking_inconsistency(df)
    
    # 模拟手动排名
    simulate_manual_ranking()
    
    # 调查可能原因
    investigate_potential_causes()
    
    # 推荐解决方案
    recommend_solutions()
    
    print("\n" + "=" * 60)
    print("调试完成！")
    print("=" * 60)
