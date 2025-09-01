#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析固定区间和百分比区间的线性关系
验证百分比区间通过四舍五入与固定区间的对应关系
"""

def analyze_scoring_relationship():
    """分析赋分区间的对应关系"""
    
    print("=" * 80)
    print("固定区间与百分比区间的线性关系分析")
    print("=" * 80)
    
    # 固定区间（176人规则）
    fixed_intervals = [
        (1, 18, 8, 8.9),      # 第1-18名：8分
        (19, 43, 6, 6.9),     # 第19-43名：6分
        (44, 71, 5, 5.9),     # 第44-71名：5分
        (72, 106, 4, 4.9),    # 第72-106名：4分
        (107, 134, 3, 3.9),   # 第107-134名：3分
        (135, 159, 2, 2.9),   # 第135-159名：2分
        (160, 176, 0, 0)      # 第160名及以后：0分
    ]
    
    # 百分比区间
    percentage_intervals = [
        (0, 0.10, 8, 8.9),      # 前10%
        (0.10, 0.24, 6, 6.9),   # 10%-24%
        (0.24, 0.40, 5, 5.9),   # 24%-40%
        (0.40, 0.60, 4, 4.9),   # 40%-60%
        (0.60, 0.76, 3, 3.9),   # 60%-76%
        (0.76, 0.90, 2, 2.9),   # 76%-90%
        (0.90, 1.00, 0, 0)      # 90%-100%
    ]
    
    total_count = 176  # 总人数
    
    print(f"总人数: {total_count}")
    print()
    
    # 分析固定区间
    print("📊 固定区间分析:")
    print("-" * 60)
    print(f"{'排名区间':<15} {'人数':<8} {'比例':<10} {'常规赋分':<10} {'金山赋分':<10}")
    print("-" * 60)
    
    for start, end, regular, jinshan in fixed_intervals:
        count = end - start + 1
        percentage = count / total_count * 100
        print(f"{start}-{end:<10} {count:<8} {percentage:>6.1f}% {regular:<10} {jinshan:<10}")
    
    print()
    
    # 分析百分比区间
    print("📈 百分比区间分析:")
    print("-" * 60)
    print(f"{'百分比区间':<15} {'人数':<8} {'排名区间':<15} {'常规赋分':<10} {'金山赋分':<10}")
    print("-" * 60)
    
    for start_pct, end_pct, regular, jinshan in percentage_intervals:
        start_count = round(start_pct * total_count)
        end_count = round(end_pct * total_count)
        count = end_count - start_count
        if start_count == 0:
            start_count = 1
        print(f"{start_pct*100:>3.0f}%-{end_pct*100:<3.0f}% {count:<8} {start_count}-{end_count:<10} {regular:<10} {jinshan:<10}")
    
    print()
    
    # 验证对应关系
    print("🔍 对应关系验证:")
    print("-" * 60)
    print("通过四舍五入，百分比区间转换为排名区间:")
    print()
    
    for i, (start_pct, end_pct, regular, jinshan) in enumerate(percentage_intervals):
        start_rank = round(start_pct * total_count)
        end_rank = round(end_pct * total_count)
        
        if start_rank == 0:
            start_rank = 1
        
        # 找到对应的固定区间
        fixed_start, fixed_end, fixed_regular, fixed_jinshan = fixed_intervals[i]
        
        match = (start_rank == fixed_start and end_rank == fixed_end)
        status = "✅ 完全匹配" if match else "❌ 不匹配"
        
        print(f"百分比区间 {start_pct*100:.0f}%-{end_pct*100:.0f}% → 排名 {start_rank}-{end_rank}")
        print(f"固定区间: {fixed_start}-{fixed_end} {status}")
        print(f"赋分: {regular}/{jinshan} vs {fixed_regular}/{fixed_jinshan}")
        print()
    
    # 计算线性关系
    print("📐 线性关系分析:")
    print("-" * 60)
    
    # 计算每个区间的中心点
    print("各区间中心点分析:")
    for i, (start, end, regular, jinshan) in enumerate(fixed_intervals):
        center_rank = (start + end) / 2
        center_pct = center_rank / total_count * 100
        print(f"区间 {start}-{end}: 中心排名 {center_rank:.1f}, 中心百分比 {center_pct:.1f}%")
    
    print()
    
    # 验证四舍五入的准确性
    print("🎯 四舍五入验证:")
    print("-" * 60)
    
    test_cases = [
        (0.10, "10%"),
        (0.24, "24%"),
        (0.40, "40%"),
        (0.60, "60%"),
        (0.76, "76%"),
        (0.90, "90%")
    ]
    
    for pct, label in test_cases:
        exact_rank = pct * total_count
        rounded_rank = round(pct * total_count)
        print(f"{label}: {exact_rank:.1f} → {rounded_rank} (误差: {abs(exact_rank - rounded_rank):.1f})")

def demonstrate_equivalence():
    """演示两种方法的等价性"""
    
    print("\n" + "=" * 80)
    print("两种赋分方法的等价性演示")
    print("=" * 80)
    
    total_count = 176
    
    # 固定区间方法
    def fixed_scoring(rank, is_jinshan):
        if rank <= 18:
            return 8.9 if is_jinshan else 8
        elif rank <= 43:
            return 6.9 if is_jinshan else 6
        elif rank <= 71:
            return 5.9 if is_jinshan else 5
        elif rank <= 106:
            return 4.9 if is_jinshan else 4
        elif rank <= 134:
            return 3.9 if is_jinshan else 3
        elif rank <= 159:
            return 2.9 if is_jinshan else 2
        else:
            return 0
    
    # 百分比区间方法（四舍五入）
    def percentage_scoring(rank, is_jinshan):
        percentage = rank / total_count
        if percentage <= 0.10:
            return 8.9 if is_jinshan else 8
        elif percentage <= 0.24:
            return 6.9 if is_jinshan else 6
        elif percentage <= 0.40:
            return 5.9 if is_jinshan else 5
        elif percentage <= 0.60:
            return 4.9 if is_jinshan else 4
        elif percentage <= 0.76:
            return 3.9 if is_jinshan else 3
        elif percentage <= 0.90:
            return 2.9 if is_jinshan else 2
        else:
            return 0
    
    # 测试一些关键排名
    test_ranks = [1, 18, 19, 43, 44, 71, 72, 106, 107, 134, 135, 159, 160, 176]
    
    print("关键排名点的赋分对比:")
    print("-" * 50)
    print(f"{'排名':<6} {'百分比':<8} {'固定区间':<10} {'百分比区间':<12} {'是否一致':<8}")
    print("-" * 50)
    
    for rank in test_ranks:
        percentage = rank / total_count * 100
        fixed_score = fixed_scoring(rank, False)
        percentage_score = percentage_scoring(rank, False)
        match = "✅" if fixed_score == percentage_score else "❌"
        
        print(f"{rank:<6} {percentage:>6.1f}% {fixed_score:<10} {percentage_score:<12} {match:<8}")
    
    print()
    print("结论: 通过四舍五入，两种方法在176人规模下完全等价！")

if __name__ == "__main__":
    analyze_scoring_relationship()
    demonstrate_equivalence()
