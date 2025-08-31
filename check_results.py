import pandas as pd

def check_results():
    """检查结果文件的结构"""
    
    # 检查语文科目结果
    print("=== 语文科目结果检查 ===")
    df_yuwen = pd.read_excel('语文排名赋分结果.xlsx')
    print(f"语文科目结果列数: {len(df_yuwen.columns)}")
    print("列名:")
    for i, col in enumerate(df_yuwen.columns):
        print(f"{i}: {col}")
    
    print(f"\n数据行数: {len(df_yuwen)}")
    print("\n前3行数据预览:")
    print(df_yuwen.head(3))
    
    # 检查生物科目结果（只有2次考试）
    print("\n=== 生物科目结果检查 ===")
    df_shengwu = pd.read_excel('生物排名赋分结果.xlsx')
    print(f"生物科目结果列数: {len(df_shengwu.columns)}")
    print("列名:")
    for i, col in enumerate(df_shengwu.columns):
        print(f"{i}: {col}")
    
    print(f"\n数据行数: {len(df_shengwu)}")
    print("\n前3行数据预览:")
    print(df_shengwu.head(3))
    
    # 检查综合得分和排名
    print("\n=== 综合得分检查 ===")
    print("语文科目综合得分前10名:")
    yuwen_top10 = df_yuwen[['学校代码', '学校名称', '班别', '语文综合得分', '语文综合排名']].head(10)
    print(yuwen_top10)
    
    print("\n生物科目综合得分前10名:")
    shengwu_top10 = df_shengwu[['学校代码', '学校名称', '班别', '生物综合得分', '生物综合排名']].head(10)
    print(shengwu_top10)

if __name__ == "__main__":
    check_results()
