#!/usr/bin/env python3
"""
测试三位小数精度问题是否导致排名不一致
"""

import pandas as pd
import numpy as np

def test_precision_issue():
    """测试精度问题"""
    print("🔍 测试三位小数精度问题...")
    print("=" * 60)
    
    # 模拟数据：相同的分数但可能有精度差异
    data = {
        '学校代码': ['001', '002', '003', '004', '005'],
        '学校名称': ['学校A', '学校B', '学校C', '学校D', '学校E'],
        '班别': ['1班', '1班', '1班', '1班', '1班'],
        '得分1': [8.0, 8.0, 6.0, 6.0, 4.0],
        '得分2': [6.0, 6.0, 4.0, 4.0, 2.0],
        '得分3': [4.0, 4.0, 2.0, 2.0, 0.0],
        '得分4': [2.0, 2.0, 0.0, 0.0, 0.0],
        '得分5': [0.0, 0.0, 0.0, 0.0, 0.0]
    }
    
    df = pd.DataFrame(data)
    
    # 权重配置
    weights = [0.3, 0.2, 0.2, 0.2, 0.1]
    
    print("原始数据:")
    print(df)
    print()
    
    # 计算总分（模拟原始计算方式）
    print("计算总分...")
    total_score = 0
    for i, weight in enumerate(weights):
        score_col = f'得分{i+1}'
        total_score += df[score_col] * weight
        print(f"  {score_col} × {weight} = {df[score_col] * weight}")
    
    df['总分'] = total_score
    print(f"总分: {df['总分'].values}")
    print()
    
    # 检查是否有精度问题
    print("检查精度问题...")
    for i in range(len(df)):
        for j in range(i+1, len(df)):
            score1 = df.iloc[i]['总分']
            score2 = df.iloc[j]['总分']
            diff = abs(score1 - score2)
            if diff < 1e-10:  # 极小差异
                print(f"  {df.iloc[i]['学校名称']} 和 {df.iloc[j]['学校名称']} 总分相同: {score1}")
            elif diff < 0.001:  # 小于0.001的差异
                print(f"  ⚠️  {df.iloc[i]['学校名称']} 和 {df.iloc[j]['学校名称']} 总分差异极小: {diff:.10f}")
    
    print()
    
    # 使用不同精度进行排名
    print("不同精度的排名结果:")
    
    # 原始精度
    df['排名_原始'] = df['总分'].rank(ascending=False, method='min')
    print("原始精度排名:")
    for _, row in df.iterrows():
        print(f"  {row['学校名称']}: {row['总分']:.10f} -> 第{row['排名_原始']:.0f}名")
    
    print()
    
    # 四舍五入到3位小数
    df['总分_3位'] = df['总分'].round(3)
    df['排名_3位'] = df['总分_3位'].rank(ascending=False, method='min')
    print("3位小数排名:")
    for _, row in df.iterrows():
        print(f"  {row['学校名称']}: {row['总分_3位']:.3f} -> 第{row['排名_3位']:.0f}名")
    
    print()
    
    # 四舍五入到2位小数
    df['总分_2位'] = df['总分'].round(2)
    df['排名_2位'] = df['总分_2位'].rank(ascending=False, method='min')
    print("2位小数排名:")
    for _, row in df.iterrows():
        print(f"  {row['学校名称']}: {row['总分_2位']:.2f} -> 第{row['排名_2位']:.0f}名")
    
    print()
    
    # 检查排名是否一致
    print("排名一致性检查:")
    rank_consistent = (df['排名_原始'] == df['排名_3位']).all() and (df['排名_3位'] == df['排名_2位']).all()
    print(f"  原始 vs 3位小数: {(df['排名_原始'] == df['排名_3位']).all()}")
    print(f"  3位小数 vs 2位小数: {(df['排名_3位'] == df['排名_2位']).all()}")
    print(f"  总体一致性: {'✅ 一致' if rank_consistent else '❌ 不一致'}")
    
    print()
    
    # 显示所有列
    print("完整结果:")
    print(df[['学校名称', '总分', '总分_3位', '总分_2位', '排名_原始', '排名_3位', '排名_2位']])
    
    return df

def test_real_world_scenario():
    """测试真实场景的精度问题"""
    print("\n" + "=" * 60)
    print("🔍 测试真实场景的精度问题...")
    
    # 模拟更真实的权重计算
    print("模拟真实权重计算...")
    
    # 假设有35个学校，使用初中权重
    np.random.seed(42)  # 固定随机种子
    n_schools = 35
    
    # 生成随机得分
    scores = np.random.choice([0, 2, 3, 4, 5, 6, 8], size=(n_schools, 5), p=[0.1, 0.15, 0.2, 0.2, 0.15, 0.15, 0.05])
    
    # 权重
    weights = [0.3, 0.2, 0.2, 0.2, 0.1]
    
    # 计算总分
    total_scores = np.dot(scores, weights)
    
    # 创建DataFrame
    df = pd.DataFrame({
        '学校代码': [f'{i:03d}' for i in range(1, n_schools + 1)],
        '学校名称': [f'学校{i}' for i in range(1, n_schools + 1)],
        '得分1': scores[:, 0],
        '得分2': scores[:, 1],
        '得分3': scores[:, 2],
        '得分4': scores[:, 3],
        '得分5': scores[:, 4],
        '总分': total_scores
    })
    
    print(f"生成了 {n_schools} 个学校的得分数据")
    print("前10个学校的得分:")
    print(df.head(10)[['学校名称', '得分1', '得分2', '得分3', '得分4', '得分5', '总分']])
    
    # 检查精度问题
    print("\n检查精度问题...")
    precision_issues = []
    
    for i in range(len(df)):
        for j in range(i+1, len(df)):
            score1 = df.iloc[i]['总分']
            score2 = df.iloc[j]['总分']
            diff = abs(score1 - score2)
            if diff < 1e-10:
                precision_issues.append((i, j, score1, score2, diff))
            elif diff < 0.001:
                precision_issues.append((i, j, score1, score2, diff))
    
    if precision_issues:
        print(f"发现 {len(precision_issues)} 个精度问题:")
        for i, j, score1, score2, diff in precision_issues[:5]:  # 只显示前5个
            print(f"  {df.iloc[i]['学校名称']} vs {df.iloc[j]['学校名称']}: {score1:.10f} vs {score2:.10f}, 差异: {diff:.10f}")
        if len(precision_issues) > 5:
            print(f"  ... 还有 {len(precision_issues) - 5} 个")
    else:
        print("未发现精度问题")
    
    # 测试不同精度的排名
    print("\n测试不同精度的排名...")
    
    # 原始精度
    df['排名_原始'] = df['总分'].rank(ascending=False, method='min')
    
    # 3位小数
    df['总分_3位'] = df['总分'].round(3)
    df['排名_3位'] = df['总分_3位'].rank(ascending=False, method='min')
    
    # 2位小数
    df['总分_2位'] = df['总分'].round(2)
    df['排名_2位'] = df['总分_2位'].rank(ascending=False, method='min')
    
    # 检查排名一致性
    rank_diff_3 = (df['排名_原始'] != df['排名_3位']).sum()
    rank_diff_2 = (df['排名_3位'] != df['排名_2位']).sum()
    
    print(f"原始 vs 3位小数排名差异: {rank_diff_3}")
    print(f"3位小数 vs 2位小数排名差异: {rank_diff_2}")
    
    if rank_diff_3 > 0 or rank_diff_2 > 0:
        print("❌ 发现排名不一致！")
        print("不一致的学校:")
        inconsistent = df[df['排名_原始'] != df['排名_3位']]
        if len(inconsistent) > 0:
            print("原始 vs 3位小数不一致:")
            print(inconsistent[['学校名称', '总分', '总分_3位', '排名_原始', '排名_3位']].head())
    else:
        print("✅ 所有精度下的排名都一致")
    
    return df

if __name__ == "__main__":
    # 测试基本精度问题
    df1 = test_precision_issue()
    
    # 测试真实场景
    df2 = test_real_world_scenario()
    
    print("\n" + "=" * 60)
    print("🎯 结论:")
    print("如果发现排名不一致，说明存在精度问题")
    print("建议在计算总分后使用 .round() 统一精度")
    print("或者在比较分数时使用 np.isclose() 进行近似比较")
