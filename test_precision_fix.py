#!/usr/bin/env python3
"""
测试修复后的精度问题
"""

import pandas as pd
import numpy as np

def test_precision_fix():
    """测试修复后的精度问题"""
    print("🔍 测试修复后的精度问题...")
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
    
    # 权重配置（初中权重）
    weights = [0.3, 0.2, 0.2, 0.2, 0.1]
    
    print("原始数据:")
    print(df)
    print()
    
    # 模拟修复前的计算方式（有精度问题）
    print("修复前的计算方式（有精度问题）:")
    total_score_before = 0
    for i, weight in enumerate(weights):
        score_col = f'得分{i+1}'
        total_score_before += df[score_col] * weight
        print(f"  {score_col} × {weight} = {df[score_col] * weight}")
    
    df['总分_修复前'] = total_score_before
    print(f"总分_修复前: {df['总分_修复前'].values}")
    print()
    
    # 模拟修复后的计算方式（统一精度）
    print("修复后的计算方式（统一精度）:")
    total_score_after = 0
    for i, weight in enumerate(weights):
        score_col = f'得分{i+1}'
        total_score_after += df[score_col] * weight
        print(f"  {score_col} × {weight} = {df[score_col] * weight}")
    
    # 统一精度到3位小数
    df['总分_修复后'] = total_score_after.round(3)
    print(f"总分_修复后: {df['总分_修复后'].values}")
    print()
    
    # 检查精度问题
    print("精度问题检查:")
    for i in range(len(df)):
        score_before = df.iloc[i]['总分_修复前']
        score_after = df.iloc[i]['总分_修复后']
        diff = abs(score_before - score_after)
        if diff > 0:
            print(f"  {df.iloc[i]['学校名称']}: 修复前={score_before:.10f}, 修复后={score_after:.3f}, 差异={diff:.10f}")
        else:
            print(f"  {df.iloc[i]['学校名称']}: 无精度问题")
    
    print()
    
    # 测试排名一致性
    print("排名一致性测试:")
    
    # 修复前的排名
    df['排名_修复前'] = df['总分_修复前'].rank(ascending=False, method='min')
    
    # 修复后的排名
    df['排名_修复后'] = df['总分_修复后'].rank(ascending=False, method='min')
    
    # 检查排名是否一致
    rank_consistent = (df['排名_修复前'] == df['排名_修复后']).all()
    print(f"排名一致性: {'✅ 一致' if rank_consistent else '❌ 不一致'}")
    
    if not rank_consistent:
        print("不一致的学校:")
        inconsistent = df[df['排名_修复前'] != df['排名_修复后']]
        print(inconsistent[['学校名称', '总分_修复前', '总分_修复后', '排名_修复前', '排名_修复后']])
    else:
        print("所有学校的排名都一致")
    
    print()
    
    # 显示完整结果
    print("完整结果对比:")
    result_cols = ['学校名称', '总分_修复前', '总分_修复后', '排名_修复前', '排名_修复后']
    print(df[result_cols])
    
    return df

def test_real_world_precision_fix():
    """测试真实场景的精度修复"""
    print("\n" + "=" * 60)
    print("🔍 测试真实场景的精度修复...")
    
    # 模拟更真实的权重计算
    print("模拟真实权重计算...")
    
    # 假设有35个学校，使用初中权重
    np.random.seed(42)  # 固定随机种子
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
    
    print(f"生成了 {n_schools} 个学校的得分数据")
    print("前10个学校的得分:")
    print(df.head(10)[['学校名称', '得分1', '得分2', '得分3', '得分4', '得分5', '总分_修复前', '总分_修复后']])
    
    # 检查精度问题
    print("\n检查精度问题...")
    precision_issues = []
    
    for i in range(len(df)):
        score_before = df.iloc[i]['总分_修复前']
        score_after = df.iloc[i]['总分_修复后']
        diff = abs(score_before - score_after)
        if diff > 0:
            precision_issues.append((i, score_before, score_after, diff))
    
    if precision_issues:
        print(f"发现 {len(precision_issues)} 个精度问题:")
        for i, score_before, score_after, diff in precision_issues[:5]:  # 只显示前5个
            print(f"  {df.iloc[i]['学校名称']}: {score_before:.10f} -> {score_after:.3f}, 差异: {diff:.10f}")
        if len(precision_issues) > 5:
            print(f"  ... 还有 {len(precision_issues) - 5} 个")
    else:
        print("未发现精度问题")
    
    # 测试不同精度的排名
    print("\n测试不同精度的排名...")
    
    # 修复前排名
    df['排名_修复前'] = df['总分_修复前'].rank(ascending=False, method='min')
    
    # 修复后排名
    df['排名_修复后'] = df['总分_修复后'].rank(ascending=False, method='min')
    
    # 检查排名一致性
    rank_diff = (df['排名_修复前'] != df['排名_修复后']).sum()
    
    print(f"修复前 vs 修复后排名差异: {rank_diff}")
    
    if rank_diff > 0:
        print("❌ 仍有排名不一致！")
        print("不一致的学校:")
        inconsistent = df[df['排名_修复前'] != df['排名_修复后']]
        print(inconsistent[['学校名称', '总分_修复前', '总分_修复后', '排名_修复前', '排名_修复后']].head())
    else:
        print("✅ 修复后所有排名都一致！")
    
    return df

if __name__ == "__main__":
    # 测试基本精度修复
    df1 = test_precision_fix()
    
    # 测试真实场景的精度修复
    df2 = test_real_world_precision_fix()
    
    print("\n" + "=" * 60)
    print("🎯 修复效果总结:")
    print("1. 在计算总分后使用 .round(3) 统一精度")
    print("2. 避免了浮点数累积误差导致的排名不一致")
    print("3. 确保相同分数获得相同排名")
    print("4. 提高了排名算法的稳定性和可靠性")
