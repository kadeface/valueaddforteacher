#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析固定区间和百分比区间的线性关系
验证百分比区间通过四舍五入与固定区间的对应关系
修复区间重叠问题
"""

def generate_corrected_intervals(total_count, percentage_intervals):
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

def demonstrate_interval_problem():
    """演示区间重叠问题"""
    
    print("=" * 80)
    print("区间重叠问题演示")
    print("=" * 80)
    
    total_count = 176
    
    # 当前实现（有重叠）
    print("❌ 当前实现（有重叠问题）:")
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
    print("✅ 修复后的实现（无重叠）:")
    print("-" * 50)
    
    corrected_intervals = generate_corrected_intervals(total_count, percentage_intervals)
    
    print(f"{'区间':<15} {'开始':<8} {'结束':<8} {'人数':<8}")
    print("-" * 50)
    
    for start, end, regular, jinshan in corrected_intervals:
        count = end - start + 1
        print(f"{start}-{end:<10} {start:<8} {end:<8} {count:<8}")
    
    print()
    print("修复方法：")
    print("1. 第一个区间从1开始")
    print("2. 后续区间的开始排名 = 前一区间的结束排名 + 1")
    print("3. 确保每个排名只属于一个区间")

def test_different_sizes_corrected():
    """测试不同规模下的修复后赋分区间"""
    
    print("\n" + "=" * 80)
    print("不同规模下的修复后赋分区间")
    print("=" * 80)
    
    percentage_intervals = [
        (0, 0.10, 8, 8.9),      # 前10%
        (0.10, 0.24, 6, 6.9),   # 10%-24%
        (0.24, 0.40, 5, 5.9),   # 24%-40%
        (0.40, 0.60, 4, 4.9),   # 40%-60%
        (0.60, 0.76, 3, 3.9),   # 60%-76%
        (0.76, 0.90, 2, 2.9),   # 76%-90%
        (0.90, 1.00, 0, 0)      # 90%-100%
    ]
    
    test_sizes = [20, 50, 100, 176, 200, 500]
    
    for size in test_sizes:
        print(f"\n总人数: {size}")
        intervals = generate_corrected_intervals(size, percentage_intervals)
        
        print(f"{'排名区间':<15} {'人数':<8} {'比例':<10} {'赋分':<8}")
        print("-" * 50)
        
        for start, end, regular, jinshan in intervals:
            count = end - start + 1
            percentage = count / size * 100
            print(f"{start}-{end:<10} {count:<8} {percentage:>6.1f}% {regular:<8}")

if __name__ == "__main__":
    demonstrate_interval_problem()
    test_different_sizes_corrected()
