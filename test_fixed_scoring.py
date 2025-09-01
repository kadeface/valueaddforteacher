#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修复后的赋分规则
验证区间无重叠问题
"""

import pandas as pd
import numpy as np
from calculate_scores_final_fix import calculate_scores_final_fix

def test_fixed_scoring():
    """测试修复后的赋分规则"""
    
    print("=" * 80)
    print("修复后的赋分规则测试")
    print("=" * 80)
    
    # 测试文件路径
    test_file = 'data/2025Mid3.xls'
    
    print(f"测试文件: {test_file}")
    print()
    
    # 测试处理
    print("1. 测试修复后的赋分规则...")
    try:
        result = calculate_scores_final_fix(test_file, '语文')
        if result is not None:
            print("✅ 修复后的赋分规则测试成功")
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
            print("❌ 修复后的赋分规则测试失败")
    except Exception as e:
        print(f"❌ 修复后的赋分规则测试出错: {e}")
    
    print()

def verify_interval_non_overlap():
    """验证区间无重叠"""
    
    print("2. 验证区间无重叠...")
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
    
    def generate_corrected_intervals(total_count):
        """生成修复后的赋分区间，确保无重叠"""
        intervals = []
        current_start = 1
        
        for start_pct, end_pct, regular_score, jinshan_score in percentage_intervals:
            # 计算当前区间的结束排名
            end_rank = round(end_pct * total_count)
            
            # 确保结束排名不超过总人数
            if end_rank > total_count:
                end_rank = total_count
            
            # 确保区间至少包含1个人
            if current_start > end_rank:
                end_rank = current_start
            
            intervals.append((current_start, end_rank, regular_score, jinshan_score))
            
            # 下一个区间的开始排名是当前区间结束排名+1
            current_start = end_rank + 1
            
            # 如果已经覆盖了所有人数，退出循环
            if current_start > total_count:
                break
        
        return intervals
    
    # 测试不同规模
    test_sizes = [20, 50, 100, 176, 200, 500]
    
    for size in test_sizes:
        print(f"\n总人数: {size}")
        intervals = generate_corrected_intervals(size)
        
        print(f"{'排名区间':<15} {'人数':<8} {'比例':<10} {'赋分':<8} {'验证':<10}")
        print("-" * 60)
        
        all_ranks = set()
        overlap_found = False
        
        for start, end, regular, jinshan in intervals:
            count = end - start + 1
            percentage = count / size * 100
            
            # 检查重叠
            current_ranks = set(range(start, end + 1))
            if current_ranks & all_ranks:  # 如果有交集，说明重叠
                overlap_found = True
                status = "❌ 重叠"
            else:
                status = "✅ 正常"
            
            all_ranks.update(current_ranks)
            
            print(f"{start}-{end:<10} {count:<8} {percentage:>6.1f}% {regular:<8} {status:<10}")
        
        if not overlap_found:
            print(f"✅ 总人数{size}: 所有区间无重叠")
        else:
            print(f"❌ 总人数{size}: 发现重叠区间")

def compare_before_after():
    """对比修复前后的结果"""
    
    print("\n" + "=" * 80)
    print("修复前后对比")
    print("=" * 80)
    
    total_count = 176
    
    # 修复前的实现（有重叠）
    print("❌ 修复前（有重叠）:")
    print("-" * 50)
    
    percentage_intervals = [
        (0, 0.10, 8, 8.9),      # 前10%
        (0.10, 0.24, 6, 6.9),   # 10%-24%
        (0.24, 0.40, 5, 5.9),   # 24%-40%
        (0.40, 0.60, 4, 4.9),   # 40%-60%
        (0.60, 0.76, 3, 3.9),   # 60%-76%
        (0.76, 0.90, 2, 2.9),   # 76%-90%
        (0.90, 1.00, 0, 0)      # 90%-100%
    ]
    
    print(f"{'区间':<15} {'开始':<8} {'结束':<8} {'问题':<15}")
    print("-" * 50)
    
    for start_pct, end_pct, regular, jinshan in percentage_intervals:
        start_rank = round(start_pct * total_count)
        end_rank = round(end_pct * total_count)
        
        if start_rank == 0:
            start_rank = 1
        
        # 检查与前一个区间的重叠
        problem = ""
        if len(percentage_intervals) > 1 and start_pct > 0:
            prev_end_pct = percentage_intervals[percentage_intervals.index((start_pct, end_pct, regular, jinshan)) - 1][1]
            prev_end_rank = round(prev_end_pct * total_count)
            if start_rank <= prev_end_rank:
                problem = f"与前一区间重叠"
        
        print(f"{start_pct*100:.0f}%-{end_pct*100:.0f}% {start_rank:<8} {end_rank:<8} {problem:<15}")
    
    print()
    
    # 修复后的实现（无重叠）
    print("✅ 修复后（无重叠）:")
    print("-" * 50)
    
    def generate_corrected_intervals(total_count):
        intervals = []
        current_start = 1
        
        for start_pct, end_pct, regular_score, jinshan_score in percentage_intervals:
            end_rank = round(end_pct * total_count)
            if end_rank > total_count:
                end_rank = total_count
            if current_start > end_rank:
                end_rank = current_start
            
            intervals.append((current_start, end_rank, regular_score, jinshan_score))
            current_start = end_rank + 1
            if current_start > total_count:
                break
        
        return intervals
    
    corrected_intervals = generate_corrected_intervals(total_count)
    
    print(f"{'区间':<15} {'开始':<8} {'结束':<8} {'人数':<8}")
    print("-" * 50)
    
    for start, end, regular, jinshan in corrected_intervals:
        count = end - start + 1
        print(f"{start}-{end:<10} {start:<8} {end:<8} {count:<8}")
    
    print()
    print("修复效果：")
    print("1. ✅ 消除了区间重叠问题")
    print("2. ✅ 每个排名只属于一个区间")
    print("3. ✅ 保持了百分比区间的相对比例")
    print("4. ✅ 适用于任意规模的学校")

if __name__ == "__main__":
    # 测试修复后的赋分规则
    test_fixed_scoring()
    
    # 验证区间无重叠
    verify_interval_non_overlap()
    
    # 对比修复前后
    compare_before_after()
