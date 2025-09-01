#!/usr/bin/env python3
"""
深度分析精度问题
"""

import pandas as pd
import numpy as np

def debug_deep_precision_issue():
    """深度分析精度问题"""
    print("🔍 深度分析精度问题...")
    print("=" * 60)
    
    # 模拟真实场景
    np.random.seed(42)
    n_schools = 35
    
    # 生成随机得分
    scores = np.random.choice([0, 2, 3, 4, 5, 6, 8], size=(n_schools, 5), p=[0.1, 0.15, 0.2, 0.2, 0.15, 0.15, 0.05])
    
    # 权重
    weights = [0.3, 0.2, 0.2, 0.2, 0.1]
    
    # 计算总分（修复前）
    total_scores_before = np.dot(scores, weights)
    
    # 计算总分（修复后）
    total_scores_after = np.dot(scores, weights).round(3)
    
    # 创建DataFrame
    df = pd.DataFrame({
        '学校代码': [f'{i:03d}' for i in range(1, n_schools + 1)],
        '学校名称': [f'学校{i}' for i in range(1, n_schools + 1)],
        '得分1': scores[:, 0],
        '得分2': scores[:, 1],
        '得分3': scores[:, 2],
        '得分4': scores[:, 3],
        '得分5': scores[:, 4],
        '总分_修复前': total_scores_before,
        '总分_修复后': total_scores_after
    })
    
    print("前15个学校的详细得分:")
    print(df.head(15)[['学校名称', '得分1', '得分2', '得分3', '得分4', '得分5', '总分_修复前', '总分_修复后']])
    
    # 检查是否有完全相同的分数
    print("\n检查完全相同的分数:")
    score_counts = df['总分_修复前'].value_counts()
    duplicate_scores = score_counts[score_counts > 1]
    if len(duplicate_scores) > 0:
        print("发现重复分数:")
        for score, count in duplicate_scores.items():
            schools = df[df['总分_修复前'] == score]['学校名称'].tolist()
            print(f"  分数 {score:.10f}: {count} 个学校 - {schools}")
    else:
        print("没有发现重复分数")
    
    # 检查修复后的重复分数
    print("\n检查修复后的重复分数:")
    score_counts_after = df['总分_修复后'].value_counts()
    duplicate_scores_after = score_counts_after[score_counts_after > 1]
    if len(duplicate_scores_after) > 0:
        print("发现重复分数:")
        for score, count in duplicate_scores_after.items():
            schools = df[df['总分_修复后'] == score]['学校名称'].tolist()
            print(f"  分数 {score:.3f}: {count} 个学校 - {schools}")
    else:
        print("没有发现重复分数")
    
    # 计算排名
    df['排名_修复前'] = df['总分_修复前'].rank(ascending=False, method='min')
    df['排名_修复后'] = df['总分_修复后'].rank(ascending=False, method='min')
    
    # 找出排名不一致的学校
    inconsistent_mask = df['排名_修复前'] != df['排名_修复后']
    inconsistent_schools = df[inconsistent_mask]
    
    print(f"\n排名不一致的学校数量: {len(inconsistent_schools)}")
    
    if len(inconsistent_schools) > 0:
        print("\n排名不一致的详细分析:")
        for _, school in inconsistent_schools.iterrows():
            print(f"\n{school['学校名称']}:")
            print(f"  得分: {school['得分1']}, {school['得分2']}, {school['得分3']}, {school['得分4']}, {school['得分5']}")
            print(f"  总分_修复前: {school['总分_修复前']:.10f}")
            print(f"  总分_修复后: {school['总分_修复后']:.3f}")
            print(f"  排名_修复前: {school['排名_修复前']:.0f}")
            print(f"  排名_修复后: {school['排名_修复后']:.0f}")
            
            # 找出与这个学校分数相同的其他学校
            same_score_before = df[df['总分_修复前'] == school['总分_修复前']]
            same_score_after = df[df['总分_修复后'] == school['总分_修复后']]
            
            print(f"  修复前相同分数的学校: {same_score_before['学校名称'].tolist()}")
            print(f"  修复后相同分数的学校: {same_score_after['学校名称'].tolist()}")
    
    # 分析排名不一致的根本原因
    print("\n" + "=" * 60)
    print("🔍 分析排名不一致的根本原因...")
    
    # 检查是否有分数在round前后发生变化
    score_changed_mask = df['总分_修复前'] != df['总分_修复后']
    score_changed_schools = df[score_changed_mask]
    
    print(f"分数发生变化的学校数量: {len(score_changed_schools)}")
    
    if len(score_changed_schools) > 0:
        print("分数发生变化的学校:")
        for _, school in score_changed_schools.iterrows():
            print(f"  {school['学校名称']}: {school['总分_修复前']:.10f} -> {school['总分_修复后']:.3f}")
    
    # 检查排名不一致是否与分数变化相关
    print("\n排名不一致与分数变化的关系:")
    inconsistent_and_changed = df[inconsistent_mask & score_changed_mask]
    inconsistent_not_changed = df[inconsistent_mask & ~score_changed_mask]
    
    print(f"  排名不一致且分数变化: {len(inconsistent_and_changed)} 个")
    print(f"  排名不一致但分数未变化: {len(inconsistent_not_changed)} 个")
    
    if len(inconsistent_not_changed) > 0:
        print("\n排名不一致但分数未变化的学校（这是关键问题）:")
        for _, school in inconsistent_not_changed.iterrows():
            print(f"  {school['学校名称']}: 分数={school['总分_修复前']:.10f}, 排名变化={school['排名_修复前']:.0f}->{school['排名_修复后']:.0f}")
            
            # 深入分析这个学校的排名变化
            original_score = school['总分_修复前']
            original_rank = school['排名_修复前']
            new_rank = school['排名_修复后']
            
            # 找出排名变化的原因
            print(f"    分析: 原始分数 {original_score:.10f}")
            
            # 检查是否有其他学校的分数在round后变得与这个学校相同
            other_schools = df[df['学校名称'] != school['学校名称']]
            for _, other in other_schools.iterrows():
                if abs(other['总分_修复后'] - school['总分_修复后']) < 1e-10:
                    print(f"      与 {other['学校名称']} 分数相同: {other['总分_修复后']:.3f}")
                    print(f"      但原始分数不同: {other['总分_修复前']:.10f}")
    
    return df

def test_ranking_methods():
    """测试不同的排名方法"""
    print("\n" + "=" * 60)
    print("🔍 测试不同的排名方法...")
    
    # 创建测试数据
    test_scores = [3.6000000000000001, 3.6000000000000001, 3.5999999999999996, 3.5999999999999996]
    test_names = ['学校A', '学校B', '学校C', '学校D']
    
    df_test = pd.DataFrame({
        '学校名称': test_names,
        '分数': test_scores
    })
    
    print("测试数据:")
    print(df_test)
    print()
    
    # 测试不同的排名方法
    print("不同排名方法的结果:")
    
    # min方法
    df_test['排名_min'] = df_test['分数'].rank(ascending=False, method='min')
    print("method='min':")
    for _, row in df_test.iterrows():
        print(f"  {row['学校名称']}: {row['分数']:.10f} -> 第{row['排名_min']:.0f}名")
    
    print()
    
    # dense方法
    df_test['排名_dense'] = df_test['分数'].rank(ascending=False, method='dense')
    print("method='dense':")
    for _, row in df_test.iterrows():
        print(f"  {row['学校名称']}: {row['分数']:.10f} -> 第{row['排名_dense']:.0f}名")
    
    print()
    
    # 使用round后的分数
    df_test['分数_round3'] = df_test['分数'].round(3)
    df_test['排名_round3_min'] = df_test['分数_round3'].rank(ascending=False, method='min')
    print("round(3) + method='min':")
    for _, row in df_test.iterrows():
        print(f"  {row['学校名称']}: {row['分数_round3']:.3f} -> 第{row['排名_round3_min']:.0f}名")
    
    return df_test

if __name__ == "__main__":
    # 深度分析精度问题
    df1 = debug_deep_precision_issue()
    
    # 测试不同的排名方法
    df2 = test_ranking_methods()
    
    print("\n" + "=" * 60)
    print("🎯 深度分析结论:")
    print("1. 浮点数精度问题不仅影响单个学校的分数")
    print("2. 还会影响学校之间的相对排名关系")
    print("3. 即使分数没有变化，排名也可能因为其他学校的变化而改变")
    print("4. 解决方案：在计算总分后立即使用.round(3)，然后进行排名")
