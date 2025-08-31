import pandas as pd

def debug_columns():
    """调试列名，查看实际的列结构"""
    file_path = 'data/2025Mid3.xls'
    
    # 检查语文科目（应该有4次考试）
    print("=== 语文科目列名 ===")
    df_yuwen = pd.read_excel(file_path, sheet_name='语文')
    print(f"语文科目列数: {len(df_yuwen.columns)}")
    print("前10列:")
    for i, col in enumerate(df_yuwen.columns[:10]):
        print(f"{i}: {col}")
    
    print("\n=== 生物科目列名 ===")
    df_shengwu = pd.read_excel(file_path, sheet_name='生物')
    print(f"生物科目列数: {len(df_shengwu.columns)}")
    print("所有列:")
    for i, col in enumerate(df_shengwu.columns):
        print(f"{i}: {col}")
    
    print("\n=== 地理科目列名 ===")
    df_dili = pd.read_excel(file_path, sheet_name='地理')
    print(f"地理科目列数: {len(df_dili.columns)}")
    print("所有列:")
    for i, col in enumerate(df_dili.columns):
        print(f"{i}: {col}")

if __name__ == "__main__":
    debug_columns()
