import pandas as pd

def debug_output_structure():
    """详细检查输出结构，对比规则说明文档的要求"""
    
    print("=== 检查语文科目输出结构 ===")
    df_yuwen = pd.read_excel('语文排名赋分结果.xlsx')
    
    print(f"总列数: {len(df_yuwen.columns)}")
    print("\n所有列名:")
    for i, col in enumerate(df_yuwen.columns):
        print(f"{i:2d}: {col}")
    
    print("\n=== 检查是否按照规则说明文档的结构输出 ===")
    
    # 检查中考语文平均分p1后面是否有对应的排名和得分列
    print("\n检查中考语文平均分p1的结构:")
    p1_col = '中考   语文   平均分   p1'
    if p1_col in df_yuwen.columns:
        p1_idx = df_yuwen.columns.get_loc(p1_col)
        print(f"中考语文平均分p1在第{p1_idx}列")
        
        # 检查后面两列是否是排名和得分
        if p1_idx + 1 < len(df_yuwen.columns):
            next_col1 = df_yuwen.columns[p1_idx + 1]
            print(f"下一列: {next_col1}")
        if p1_idx + 2 < len(df_yuwen.columns):
            next_col2 = df_yuwen.columns[p1_idx + 2]
            print(f"下下列: {next_col2}")
    
    # 检查中考语文优秀率y1后面是否有对应的排名和得分列
    print("\n检查中考语文优秀率y1的结构:")
    y1_col = '中考   语文   优秀率   y1'
    if y1_col in df_yuwen.columns:
        y1_idx = df_yuwen.columns.get_loc(y1_col)
        print(f"中考语文优秀率y1在第{y1_idx}列")
        
        # 检查后面两列是否是排名和得分
        if y1_idx + 1 < len(df_yuwen.columns):
            next_col1 = df_yuwen.columns[y1_idx + 1]
            print(f"下一列: {next_col1}")
        if y1_idx + 2 < len(df_yuwen.columns):
            next_col2 = df_yuwen.columns[y1_idx + 2]
            print(f"下下列: {next_col2}")
    
    # 检查是否有差值列
    print("\n检查是否有差值列:")
    diff_cols = [col for col in df_yuwen.columns if '差值' in col]
    print(f"差值列数量: {len(diff_cols)}")
    if diff_cols:
        print("差值列:")
        for col in diff_cols[:5]:  # 只显示前5个
            print(f"  {col}")
    
    # 检查是否有总分列
    print("\n检查是否有总分列:")
    total_cols = [col for col in df_yuwen.columns if '总分' in col]
    print(f"总分列数量: {len(total_cols)}")
    if total_cols:
        print("总分列:")
        for col in total_cols:
            print(f"  {col}")
    
    # 检查是否有综合得分和排名列
    print("\n检查是否有综合得分和排名列:")
    comprehensive_cols = [col for col in df_yuwen.columns if '综合' in col]
    print(f"综合列数量: {len(comprehensive_cols)}")
    if comprehensive_cols:
        print("综合列:")
        for col in comprehensive_cols:
            print(f"  {col}")

if __name__ == "__main__":
    debug_output_structure()
