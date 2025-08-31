import pandas as pd

def check_fixed_results():
    """检查修复后的输出结构"""
    
    print("=== 检查修复后的语文科目输出结构 ===")
    df_yuwen = pd.read_excel('语文排名赋分结果_修复版.xlsx')
    
    print(f"总列数: {len(df_yuwen.columns)}")
    print("\n前20列名:")
    for i, col in enumerate(df_yuwen.columns[:20]):
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
        for col in diff_cols[:5]:  # 只显示前5个
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

if __name__ == "__main__":
    check_fixed_results()
