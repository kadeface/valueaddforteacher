#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试四舍五入逻辑的正确性
验证区间长度计算是否准确
"""

def test_rounding_logic():
    """测试四舍五入逻辑"""
    
    print("=" * 80)
    print("四舍五入逻辑测试")
    print("=" * 80)
    
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
    
    total_count = 176
    
    print(f"总人数: {total_count}")
    print()
    
    print("📊 详细计算过程:")
    print("-" * 80)
    print(f"{'区间':<15} {'区间长度':<12} {'计算过程':<20} {'四舍五入':<10} {'排名区间':<15}")
    print("-" * 80)
    
    current_start = 1
    
    for start_pct, end_pct, regular, jinshan in percentage_intervals:
        # 计算区间长度
        interval_length_exact = (end_pct - start_pct) * total_count
        interval_length_rounded = round(interval_length_exact)
        
        # 计算结束排名
        end_rank = current_start + interval_length_rounded - 1
        
        # 显示计算过程
        calculation = f"({end_pct:.2f}-{start_pct:.2f})×{total_count}"
        print(f"{start_pct*100:.0f}%-{end_pct*100:.0f}% {interval_length_exact:<12.2f} {calculation:<20} {interval_length_rounded:<10} {current_start}-{end_rank:<10}")
        
        current_start = end_rank + 1
    
    print()
    
    # 验证总和
    print("🔍 验证总和:")
    print("-" * 40)
    
    total_people = 0
    current_start = 1
    
    for start_pct, end_pct, regular, jinshan in percentage_intervals:
        interval_length = round((end_pct - start_pct) * total_count)
        if interval_length < 1:
            interval_length = 1
        
        end_rank = current_start + interval_length - 1
        if end_rank > total_count:
            end_rank = total_count
        
        people_in_interval = end_rank - current_start + 1
        total_people += people_in_interval
        
        print(f"{start_pct*100:.0f}%-{end_pct*100:.0f}%: {current_start}-{end_rank} ({people_in_interval}人)")
        
        current_start = end_rank + 1
    
    print(f"总人数: {total_people} (应该是 {total_count})")
    
    if total_people == total_count:
        print("✅ 总人数匹配正确")
    else:
        print(f"❌ 总人数不匹配，差异: {total_people - total_count}")

def compare_old_vs_new():
    """对比新旧算法的差异"""
    
    print("\n" + "=" * 80)
    print("新旧算法对比")
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
    
    total_count = 176
    
    print(f"总人数: {total_count}")
    print()
    
    print("❌ 旧算法（直接对结束百分比四舍五入）:")
    print("-" * 60)
    print(f"{'区间':<15} {'结束百分比':<12} {'结束排名':<12} {'人数':<8}")
    print("-" * 60)
    
    current_start = 1
    for start_pct, end_pct, regular, jinshan in percentage_intervals:
        end_rank_old = round(end_pct * total_count)
        people_old = end_rank_old - current_start + 1
        print(f"{start_pct*100:.0f}%-{end_pct*100:.0f}% {end_pct*100:<12.0f}% {end_rank_old:<12} {people_old:<8}")
        current_start = end_rank_old + 1
    
    print()
    print("✅ 新算法（对区间长度四舍五入）:")
    print("-" * 60)
    print(f"{'区间':<15} {'区间长度':<12} {'四舍五入':<12} {'排名区间':<15}")
    print("-" * 60)
    
    current_start = 1
    for start_pct, end_pct, regular, jinshan in percentage_intervals:
        interval_length_exact = (end_pct - start_pct) * total_count
        interval_length_rounded = round(interval_length_exact)
        end_rank_new = current_start + interval_length_rounded - 1
        print(f"{start_pct*100:.0f}%-{end_pct*100:.0f}% {interval_length_exact:<12.2f} {interval_length_rounded:<12} {current_start}-{end_rank_new:<10}")
        current_start = end_rank_new + 1

def test_specific_case():
    """测试特定案例：10%-24%区间"""
    
    print("\n" + "=" * 80)
    print("特定案例测试：10%-24%区间")
    print("=" * 80)
    
    total_count = 176
    start_pct = 0.10
    end_pct = 0.24
    
    print(f"总人数: {total_count}")
    print(f"区间: {start_pct*100:.0f}%-{end_pct*100:.0f}%")
    print()
    
    # 旧算法
    end_rank_old = round(end_pct * total_count)
    people_old = end_rank_old - round(start_pct * total_count) + 1
    
    print("❌ 旧算法:")
    print(f"  结束排名 = round({end_pct} × {total_count}) = round({end_pct * total_count}) = {end_rank_old}")
    print(f"  开始排名 = round({start_pct} × {total_count}) = round({start_pct * total_count}) = {round(start_pct * total_count)}")
    print(f"  人数 = {end_rank_old} - {round(start_pct * total_count)} + 1 = {people_old}")
    print(f"  区间: {round(start_pct * total_count)}-{end_rank_old}")
    
    print()
    
    # 新算法
    interval_length_exact = (end_pct - start_pct) * total_count
    interval_length_rounded = round(interval_length_exact)
    
    print("✅ 新算法:")
    print(f"  区间长度 = ({end_pct} - {start_pct}) × {total_count} = {interval_length_exact}")
    print(f"  四舍五入 = round({interval_length_exact}) = {interval_length_rounded}")
    print(f"  人数 = {interval_length_rounded}")
    print(f"  区间: 19-{18 + interval_length_rounded}")
    
    print()
    print("结论:")
    print(f"  旧算法人数: {people_old}")
    print(f"  新算法人数: {interval_length_rounded}")
    print(f"  差异: {interval_length_rounded - people_old}")

if __name__ == "__main__":
    test_rounding_logic()
    compare_old_vs_new()
    test_specific_case()
