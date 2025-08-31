import pandas as pd

def verify_final_fix():
    """验证最终修复版的完整输出结构"""
    
    print("=== 验证最终修复版的语文科目输出结构 ===")
    df_yuwen = pd.read_excel('语文排名赋分结果_最终修复版.xlsx')
    
    print(f"总列数: {len(df_yuwen.columns)}")
    print("\n前40列名:")
    for i, col in enumerate(df_yuwen.columns[:40]):
        print(f"{i:2d}: {col}")
    
    print("\n=== 检查列顺序是否符合规则说明文档 ===")
    
    # 检查基础列
    print("\n基础列检查:")
    base_cols = ['学校代码', '学校名称', '班别', '语文科任']
    for i, col in enumerate(base_cols):
        if col in df_yuwen.columns:
            idx = df_yuwen.columns.get_loc(col)
            print(f"  {col}: 第{idx}列 ✓")
        else:
            print(f"  {col}: 未找到 ✗")
    
    # 检查第一个考试（中考）的结构
    print("\n第一个考试（中考）结构检查:")
    exam1_cols = ['中考   语文   平均分   p1', '中考   语文   优秀率   y1', '中考   语文   优良率   l1', '中考   语文   合格率  h1', '中考   语文   低分率    d1']
    for col in exam1_cols:
        if col in df_yuwen.columns:
            idx = df_yuwen.columns.get_loc(col)
            print(f"  {col}: 第{idx}列")
            
            # 检查后面是否有对应的排名和得分列
            if idx + 1 < len(df_yuwen.columns):
                next_col1 = df_yuwen.columns[idx + 1]
                if '排名' in next_col1:
                    print(f"    下一列(排名): {next_col1} ✓")
                else:
                    print(f"    下一列(排名): {next_col1} ✗")
            
            if idx + 2 < len(df_yuwen.columns):
                next_col2 = df_yuwen.columns[idx + 2]
                if '得分' in next_col2:
                    print(f"    下下列(得分): {next_col2} ✓")
                else:
                    print(f"    下下列(得分): {next_col2} ✗")
    
    # 检查第二个考试（二模）的结构
    print("\n第二个考试（二模）结构检查:")
    exam2_cols = ['二模   语文   平均分   p2', '二模   语文   优秀率   y2', '二模   语文   优良率   l2', '二模   语文   合格率h2', '二模   语文   低分率   d2']
    for col in exam2_cols:
        if col in df_yuwen.columns:
            idx = df_yuwen.columns.get_loc(col)
            print(f"  {col}: 第{idx}列")
            
            # 检查后面是否有对应的差值、差值排名、差值得分列
            metric_name = col.split('   ')[-1].split()[0]
            diff_col = f'中考-二模_{metric_name}_差值'
            if diff_col in df_yuwen.columns:
                diff_idx = df_yuwen.columns.get_loc(diff_col)
                print(f"    差值列: {diff_col} (第{diff_idx}列) ✓")
                
                # 检查差值排名和差值得分
                if diff_idx + 1 < len(df_yuwen.columns):
                    next_col1 = df_yuwen.columns[diff_idx + 1]
                    if '差值排名' in next_col1:
                        print(f"    差值排名: {next_col1} ✓")
                    else:
                        print(f"    差值排名: {next_col1} ✗")
                
                if diff_idx + 2 < len(df_yuwen.columns):
                    next_col2 = df_yuwen.columns[diff_idx + 2]
                    if '差值得分' in next_col2:
                        print(f"    差值得分: {next_col2} ✓")
                    else:
                        print(f"    差值得分: {next_col2} ✗")
            else:
                print(f"    差值列: {diff_col} 未找到 ✗")
    
    # 检查是否有总分列
    print("\n总分列检查:")
    total_cols = [col for col in df_yuwen.columns if '总分' in col]
    for col in total_cols:
        idx = df_yuwen.columns.get_loc(col)
        print(f"  {col}: 第{idx}列")
    
    # 检查是否有差值列
    print("\n差值列检查:")
    diff_cols = [col for col in df_yuwen.columns if '差值' in col]
    if diff_cols:
        print(f"差值列数量: {len(diff_cols)}")
        for col in diff_cols[:10]:  # 显示前10个
            idx = df_yuwen.columns.get_loc(col)
            print(f"  {col}: 第{idx}列")
    else:
        print("没有找到差值列")
    
    # 检查综合列
    print("\n综合列检查:")
    comprehensive_cols = [col for col in df_yuwen.columns if '综合' in col]
    for col in comprehensive_cols:
        idx = df_yuwen.columns.get_loc(col)
        print(f"  {col}: 第{idx}列")
    
    # 检查列的顺序模式
    print("\n=== 检查列的顺序模式 ===")
    print("期望的模式: 指标 → 排名 → 得分 → 指标 → 差值 → 差值排名 → 差值得分...")
    
    # 检查第一个指标的模式
    col = '中考   语文   平均分   p1'
    if col in df_yuwen.columns:
        idx = df_yuwen.columns.get_loc(col)
        print(f"\n{col} (第{idx}列):")
        
        # 检查后续列的模式
        for j in range(1, 6):
            if idx + j < len(df_yuwen.columns):
                next_col = df_yuwen.columns[idx + j]
                print(f"  第{idx+j}列: {next_col}")

if __name__ == "__main__":
    verify_final_fix()
