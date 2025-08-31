import pandas as pd
import numpy as np

def analyze_excel_structure():
    """分析Excel文件的结构"""
    try:
        # 读取Excel文件
        file_path = 'data/2025Mid3.xls'
        excel_file = pd.ExcelFile(file_path)
        
        print("Excel文件中的工作表:")
        print(excel_file.sheet_names)
        print("\n" + "="*50 + "\n")
        
        # 分析每个工作表
        for sheet_name in excel_file.sheet_names:
            print(f"工作表: {sheet_name}")
            print("-" * 30)
            
            # 读取工作表
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            print(f"数据形状: {df.shape}")
            print(f"列名: {list(df.columns)}")
            print(f"前5行数据:")
            print(df.head())
            print("\n" + "="*50 + "\n")
            
    except Exception as e:
        print(f"读取文件时出错: {e}")

if __name__ == "__main__":
    analyze_excel_structure()
