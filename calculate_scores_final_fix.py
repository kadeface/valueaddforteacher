import pandas as pd
import numpy as np
import os
import re

# 导入数据清洗模块
try:
    from data_cleaner import DataCleaner, clean_excel_data
    DATA_CLEANER_AVAILABLE = True
except ImportError:
    print("警告: 数据清洗模块未找到，将使用原始数据处理方式")
    DATA_CLEANER_AVAILABLE = False



def extract_exam_names(df, subject):
    """动态识别Excel表格中的考试名称"""
    
    # 定义可能的考试关键词
    exam_keywords = [
        '中考', '二模', '九年上', '八年下', '八年上', '七年下', '七年上', 
        '六年下', '六年上', '五年下', '五年上', '四年下', '四年上', 
        '三年下', '三年上','七年入' 
    ]
    
    # 存储找到的考试名称和对应的列
    found_exams = {}
    
    # 定义指标的同义词映射，提高容错性
    metric_synonyms = {
        '平均分': ['平均分', '平均', '均分', 'mean', '平均分'],
        '优秀率': ['优秀率', '优秀', '优秀率', 'excellent', '优秀率'],
        '优良率': ['优良率', '优良', '良好率', 'good', '优良率'],
        '合格率': ['合格率', '合格', '及格率', 'pass', '合格率'],
        '低分率': ['低分率', '低分', '不及格率', 'fail', '低分率']
    }
    
    # 改进的指标匹配函数，增强容错性
    def find_metric_in_column(col_name, target_metrics):
        # 预处理列名：去除多余空格，标准化格式
        col_processed = col_name.lower().strip()
        
        # 处理列名中的多个空格，将其合并为单个空格
        import re
        col_processed = re.sub(r'\s+', ' ', col_processed)
        
        for metric, synonyms in target_metrics.items():
            for syn in synonyms:
                syn_lower = syn.lower().strip()
                # 检查是否包含同义词（支持空格分隔的情况）
                if syn_lower in col_processed:
                    return metric
                # 检查是否包含同义词的字符组合（处理空格分隔的情况）
                if syn_lower.replace(' ', '') in col_processed.replace(' ', ''):
                    return metric
        return None
    
    # 记录匹配失败的列名，便于调试
    unmatched_columns = []
    
    # 遍历所有列名，寻找包含考试关键词的列
    for col in df.columns:
        if isinstance(col, str) and subject in col:
            for keyword in exam_keywords:
                if keyword in col:
                    # 使用改进的指标匹配逻辑
                    metric = find_metric_in_column(col, metric_synonyms)
                    if metric:
                        if keyword not in found_exams:
                            found_exams[keyword] = []
                        found_exams[keyword].append(col)
                    else:
                        unmatched_columns.append(col)
                    break
    
    # 输出匹配失败的列名，帮助用户了解数据格式
    if unmatched_columns:
        print(f"警告：以下列名未能匹配到指标：{unmatched_columns}")
    
    # 按考试顺序排序（中考第一，二模第二，其他按年级和学期排序）
    def sort_exam_key(key):
        if key == '中考':
            return 0
        elif key == '二模':
            return 1
        else:
            # 解析年级和学期
            match = re.match(r'(\d+)年([上下])', key)
            if match:
                grade = int(match.group(1))
                semester = 0 if match.group(2) == '上' else 1
                return 2 + (9 - grade) * 2 + semester
            return 999
    
    sorted_exams = sorted(found_exams.keys(), key=sort_exam_key)
    
    print(f"识别到的考试顺序: {sorted_exams}")
    for exam in sorted_exams:
        print(f"  {exam}: {len(found_exams[exam])} 个指标列")
    
    return sorted_exams, found_exams

def calculate_scores_final_fix(input_file_path=None, subject=None, scoring_method='fixed'):
    """最终修复版本，确保所有指标都有完整的差值列、差值排名列、差值得分列
    
    Args:
        input_file_path: 输入文件路径
        subject: 科目名称
        scoring_method: 赋分方式，'fixed'为固定区间，'percentage'为百分比区间
    """
    
    if input_file_path is None:
        input_file_path = 'data/2025Mid3.xls'
    
    if subject is None:
        # 如果没有指定科目，处理所有科目
        return process_all_subjects(input_file_path, scoring_method)
    else:
        # 处理指定科目
        return process_single_subject(input_file_path, subject, scoring_method)

def process_single_subject(input_file_path, subject, scoring_method='fixed'):
    """处理单个科目"""
    print(f"开始处理科目: {subject}")
    
    try:
        # 读取科目数据
        df = pd.read_excel(input_file_path, sheet_name=subject)
        print(f"成功读取 {subject} 数据，共 {len(df)} 行")
        
        # 数据清洗预处理
        if DATA_CLEANER_AVAILABLE:
            print("开始数据清洗...")
            cleaner = DataCleaner()
            df = cleaner.clean_dataframe(df)
            print("数据清洗完成")
        else:
            # 原始处理方式（兼容性）
            print("使用原始数据处理方式")
            # 标准化列名
            df.columns = [col.strip() if isinstance(col, str) else col for col in df.columns]
            
            # 重命名关键列
            df = df.rename(columns={
                '学校   代码': '学校代码',
                '学校名称': '学校名称',
                '班   别': '班别'
            })
        
        # 动态识别考试名称
        exam_names, exam_columns = extract_exam_names(df, subject)
        
        if len(exam_names) == 0:
            print(f"警告: 未找到任何考试数据")
            return None
        
        # 获取总人数
        total_count = len(df)
        
        # 定义赋分规则
        if total_count <= 20:
            intervals = [(1, 3, 8, 8.9), (4, 7, 6, 6.9), (8, 12, 5, 5.9), 
                        (13, 18, 4, 4.9), (19, 25, 3, 3.9), (26, 30, 2, 2.9), (31, total_count, 0, 0)]
        else:
            intervals = [(1, 18, 8, 8.9), (19, 43, 6, 6.9), (44, 71, 5, 5.9), 
                        (72, 106, 4, 4.9), (107, 134, 3, 3.9), (135, 159, 2, 2.9), (160, total_count, 0, 0)]
        
        # 定义百分比区间赋分规则
        # 百分比区间：10%, 14%, 16%, 20%, 16%, 14%, 10%
        # 对应赋分：8/8.9, 6/6.9, 5/5.9, 4/4.9, 3/3.9, 2/2.9, 0/0
        percentage_intervals = [
            (0, 0.10, 8, 8.9),      # 前10%
            (0.10, 0.24, 6, 6.9),   # 10%-24%
            (0.24, 0.40, 5, 5.9),   # 24%-40%
            (0.40, 0.60, 4, 4.9),   # 40%-60%
            (0.60, 0.76, 3, 3.9),   # 60%-76%
            (0.76, 0.90, 2, 2.9),   # 76%-90%
            (0.90, 1.00, 0, 0)      # 90%-100%
        ]
        
        def assign_score(rank, is_jinshan):
            for start, end, regular_score, jinshan_score in intervals:
                if start <= rank <= end:
                    return jinshan_score if is_jinshan else regular_score
            return 0
        
        def assign_score_by_percentage(rank, total_count, is_jinshan):
            """基于百分比的赋分函数"""
            percentage = rank / total_count
            for start_pct, end_pct, regular_score, jinshan_score in percentage_intervals:
                if start_pct <= percentage <= end_pct:
                    return jinshan_score if is_jinshan else regular_score
            return 0
        
        # 根据科目确定科任列名
        if subject == '语文':
            teacher_col = '语文科任'
        elif subject == '数学':
            teacher_col = '数学科任'
        elif subject == '英语':
            teacher_col = '英语科任'
        elif subject == '物理':
            teacher_col = '物理科任'
        elif subject == '化学':
            teacher_col = '化学科任'
        elif subject == '道法':
            teacher_col = '道法科任'
        elif subject == '历史':
            teacher_col = '历史科任'
        elif subject == '地理':
            teacher_col = '地理科任'
        elif subject == '生物':
            teacher_col = '生物科任'
        elif subject == '科学':
            teacher_col = '科学科任'
        else:
            teacher_col = f'{subject}科任'
        
        # 创建新的列列表
        new_cols = ['学校代码', '学校名称', '班别', teacher_col]
        
        # 存储每个考试的总分列名
        total_score_cols = []
        
        # 处理第一个考试（通常是中考）
        first_exam = exam_names[0]
        print(f"\n处理第一个考试: {first_exam}")
        
        # 第一个考试的处理逻辑
        exam1_scores = []
        # 使用与extract_exam_names函数相同的指标定义，保持一致性
        base_metrics = ['平均分', '优秀率', '优良率', '合格率', '低分率']
        
        for metric_name in base_metrics:
            # 尝试不同的列名格式（支持下划线和空格两种格式）
            possible_col_names = [
                f'{first_exam}_{subject}_{metric_name}_p1',      # 下划线格式
                f'{first_exam}_{subject}_{metric_name}_y1', 
                f'{first_exam}_{subject}_{metric_name}_l1',
                f'{first_exam}_{subject}_{metric_name}_h1',
                f'{first_exam}_{subject}_{metric_name}_d1',
                f'{first_exam}_{subject}_{metric_name}',        # 无后缀格式
                # 兼容性：同时支持空格格式
                f'{first_exam}   {subject}   {metric_name}   p1',
                f'{first_exam}   {subject}   {metric_name}   y1', 
                f'{first_exam}   {subject}   {metric_name}   l1',
                f'{first_exam}   {subject}   {metric_name}   h1',
                f'{first_exam}   {subject}   {metric_name}   d1',
                f'{first_exam}   {subject}   {metric_name}'  # 无后缀格式
            ]
            
            col_name = None
            for possible_name in possible_col_names:
                if possible_name in df.columns:
                    col_name = possible_name
                    break
            
            if col_name is not None:
                new_cols.append(col_name)
                
                # 计算排名和得分
                col_data = df[col_name].dropna()
                if len(col_data) > 0:
                    # 确定排序方向
                    if '低分率' in metric_name:
                        ascending = True  # 低分率从低到高
                    else:
                        ascending = False  # 其他从高到低
                    
                    # 对于低分率，排除金山中学
                    if '低分率' in metric_name:
                        # 排除金山中学，只对其他学校进行排名
                        non_jinshan_df = df[df['学校名称'] != '金山中学'].copy()
                        sorted_df = non_jinshan_df.sort_values(col_name, ascending=ascending)
                        sorted_df = sorted_df.reset_index(drop=True)
                        
                        # 计算排名和得分（只对非金山中学）
                        rank_col = f'{first_exam}_{metric_name}_排名'
                        score_col = f'{first_exam}_{metric_name}_得分'
                        
                        for idx, row in sorted_df.iterrows():
                            rank = idx + 1
                            if scoring_method == 'percentage':
                                score = assign_score_by_percentage(rank, len(non_jinshan_df), False)
                            else:
                                score = assign_score(rank, False)  # 非金山中学使用常规赋分
                            
                            # 找到对应的原始行索引
                            original_idx = df[(df['学校代码'] == row['学校代码']) & (df['班别'] == row['班别'])].index[0]
                            df.loc[original_idx, rank_col] = rank
                            df.loc[original_idx, score_col] = score
                        
                        # 金山中学的低分率排名设为空值，得分设为0分（用于总分计算）
                        jinshan_mask = df['学校名称'] == '金山中学'
                        df.loc[jinshan_mask, rank_col] = None
                        df.loc[jinshan_mask, score_col] = 0.0
                    else:
                        # 其他指标正常计算（包括金山中学）
                        sorted_df = df.sort_values(col_name, ascending=ascending)
                        sorted_df = sorted_df.reset_index(drop=True)
                        
                        # 计算排名和得分
                        rank_col = f'{first_exam}_{metric_name}_排名'
                        score_col = f'{first_exam}_{metric_name}_得分'
                        
                        for idx, row in sorted_df.iterrows():
                            rank = idx + 1
                            is_jinshan = row['学校名称'] == '金山中学'
                            if scoring_method == 'percentage':
                                score = assign_score_by_percentage(rank, total_count, is_jinshan)
                            else:
                                score = assign_score(rank, is_jinshan)
                            
                            # 找到对应的原始行索引
                            original_idx = df[(df['学校代码'] == row['学校代码']) & (df['班别'] == row['班别'])].index[0]
                            df.loc[original_idx, rank_col] = rank
                            df.loc[original_idx, score_col] = score
                    
                    # 添加排名和得分列
                    new_cols.append(rank_col)
                    new_cols.append(score_col)
                    
                    # 收集得分用于计算总分
                    exam1_scores.append(score_col)
        
        # 计算第一个考试总分
        if len(exam1_scores) == 5:
            total_score_col = f'{first_exam}_{subject}总分'
            df[total_score_col] = (
                df[exam1_scores[0]] * 0.3 +  # 平均分
                df[exam1_scores[1]] * 0.2 +  # 优秀率
                df[exam1_scores[2]] * 0.2 +  # 优良率
                df[exam1_scores[3]] * 0.2 +  # 合格率
                df[exam1_scores[4]] * 0.1    # 低分率
            )
            new_cols.append(total_score_col)
            total_score_cols.append(total_score_col)
        
        # 处理后续考试（计算差值）
        for i in range(1, len(exam_names)):
            current_exam = exam_names[i]
            previous_exam = exam_names[i-1]
            
            print(f"\n处理考试: {current_exam} (与 {previous_exam} 比较)")
            
            exam_scores = []
            
            for metric_name in base_metrics:
                # 尝试不同的列名格式（支持下划线和空格两种格式）
                possible_col_names = [
                    f'{current_exam}_{subject}_{metric_name}_p{i+1}',      # 下划线格式
                    f'{current_exam}_{subject}_{metric_name}_y{i+1}', 
                    f'{current_exam}_{subject}_{metric_name}_l{i+1}',
                    f'{current_exam}_{subject}_{metric_name}_h{i+1}',
                    f'{current_exam}_{subject}_{metric_name}_d{i+1}',
                    f'{current_exam}_{subject}_{metric_name}',             # 无后缀格式
                    # 兼容性：同时支持空格格式
                    f'{current_exam}   {subject}   {metric_name}   p{i+1}',
                    f'{current_exam}   {subject}   {metric_name}   y{i+1}', 
                    f'{current_exam}   {subject}   {metric_name}   l{i+1}',
                    f'{current_exam}   {subject}   {metric_name}   h{i+1}',
                    f'{current_exam}   {subject}   {metric_name}   d{i+1}',
                    f'{current_exam}   {subject}   {metric_name}'  # 无后缀格式
                ]
                
                col_name = None
                for possible_name in possible_col_names:
                    if possible_name in df.columns:
                        col_name = possible_name
                        break
                
                if col_name is not None:
                    new_cols.append(col_name)
                    print(f"  找到当前考试列: {col_name}")
                    
                    # 获取对应的前一个考试列名
                    # 尝试不同的前一个考试列名格式（支持下划线和空格两种格式）
                    prev_exam_possible_names = [
                        f'{previous_exam}_{subject}_{metric_name}_p{i}',      # 下划线格式
                        f'{previous_exam}_{subject}_{metric_name}_y{i}', 
                        f'{previous_exam}_{subject}_{metric_name}_l{i}',
                        f'{previous_exam}_{subject}_{metric_name}_h{i}',
                        f'{previous_exam}_{subject}_{metric_name}_d{i}',
                        f'{previous_exam}_{subject}_{metric_name}',             # 无后缀格式
                        # 兼容性：同时支持空格格式
                        f'{previous_exam}   {subject}   {metric_name}   p{i}',
                        f'{previous_exam}   {subject}   {metric_name}   y{i}', 
                        f'{previous_exam}   {subject}   {metric_name}   l{i}',
                        f'{previous_exam}   {subject}   {metric_name}   h{i}',
                        f'{previous_exam}   {subject}   {metric_name}   d{i}',
                        f'{previous_exam}   {subject}   {metric_name}'  # 无后缀格式
                    ]
                    
                    prev_exam_col = None
                    for possible_name in prev_exam_possible_names:
                        if possible_name in df.columns:
                            prev_exam_col = possible_name
                            break
                    
                    if prev_exam_col is not None:
                        print(f"  找到前一个考试列: {prev_exam_col}")
                        # 计算差值
                        diff_col = f'{previous_exam}-{current_exam}_{metric_name}_差值'
                        df[diff_col] = df[prev_exam_col] - df[col_name]
                        
                        # 计算差值排名和得分
                        diff_data = df[diff_col].dropna()
                        if len(diff_data) > 0:
                            # 确定排序方向
                            if '低分率' in metric_name:
                                ascending = True  # 低分率差值负值表示进步
                            else:
                                ascending = False  # 其他差值正值表示进步
                            
                            # 对于低分率，排除金山中学
                            if '低分率' in metric_name:
                                # 排除金山中学，只对其他学校进行排名
                                non_jinshan_df = df[df['学校名称'] != '金山中学'].copy()
                                sorted_df = non_jinshan_df.sort_values(diff_col, ascending=ascending)
                                sorted_df = sorted_df.reset_index(drop=True)
                                
                                # 计算排名和得分（只对非金山中学）
                                diff_rank_col = f'{previous_exam}-{current_exam}_{metric_name}_差值排名'
                                diff_score_col = f'{previous_exam}-{current_exam}_{metric_name}_差值得分'
                                
                                for idx, row in sorted_df.iterrows():
                                    rank = idx + 1
                                    if scoring_method == 'percentage':
                                        score = assign_score_by_percentage(rank, len(non_jinshan_df), False)
                                    else:
                                        score = assign_score(rank, False)  # 非金山中学使用常规赋分
                                    
                                    # 找到对应的原始行索引
                                    original_idx = df[(df['学校代码'] == row['学校代码']) & (df['班别'] == row['班别'])].index[0]
                                    df.loc[original_idx, diff_rank_col] = rank
                                    df.loc[original_idx, diff_score_col] = score
                                
                                # 金山中学的低分率排名设为空值，得分设为0分（用于总分计算）
                                jinshan_mask = df['学校名称'] == '金山中学'
                                df.loc[jinshan_mask, diff_rank_col] = None
                                df.loc[jinshan_mask, diff_score_col] = 0.0
                            else:
                                # 其他指标正常计算（包括金山中学）
                                sorted_df = df.sort_values(diff_col, ascending=ascending)
                                sorted_df = sorted_df.reset_index(drop=True)
                                
                                # 计算排名和得分
                                diff_rank_col = f'{previous_exam}-{current_exam}_{metric_name}_差值排名'
                                diff_score_col = f'{previous_exam}-{current_exam}_{metric_name}_差值得分'
                                
                                for idx, row in sorted_df.iterrows():
                                    rank = idx + 1
                                    is_jinshan = row['学校名称'] == '金山中学'
                                    if scoring_method == 'percentage':
                                        score = assign_score_by_percentage(rank, total_count, is_jinshan)
                                    else:
                                        score = assign_score(rank, is_jinshan)
                                    
                                    # 找到对应的原始行索引
                                    original_idx = df[(df['学校代码'] == row['学校代码']) & (df['班别'] == row['班别'])].index[0]
                                    df.loc[original_idx, diff_rank_col] = rank
                                    df.loc[original_idx, diff_score_col] = score
                            
                            # 添加差值、差值排名、差值得分列
                            new_cols.append(diff_col)
                            new_cols.append(diff_rank_col)
                            new_cols.append(diff_score_col)
                            
                            # 收集差值得分用于计算总分
                            exam_scores.append(diff_score_col)
                    else:
                        print(f"  警告: 未找到前一个考试列: {metric_name}，跳过差值计算")
            
            # 计算当前考试总分
            if len(exam_scores) == 5:
                total_score_col = f'{current_exam}_{subject}总分'
                df[total_score_col] = (
                    df[exam_scores[0]] * 0.3 +  # 平均分差值
                    df[exam_scores[1]] * 0.2 +  # 优秀率差值
                    df[exam_scores[2]] * 0.2 +  # 优良率差值
                    df[exam_scores[3]] * 0.2 +  # 合格率差值
                    df[exam_scores[4]] * 0.1    # 低分率差值
                )
                new_cols.append(total_score_col)
                total_score_cols.append(total_score_col)
        
        # 计算综合得分
        if len(total_score_cols) == 4:
            df[f'{subject}综合得分'] = (
                df[total_score_cols[0]] * 0.4 +  # 第一个考试总分
                df[total_score_cols[1]] * 0.2 +  # 第二个考试总分
                df[total_score_cols[2]] * 0.2 +  # 第三个考试总分
                df[total_score_cols[3]] * 0.2    # 第四个考试总分
            )
        elif len(total_score_cols) == 3:
            df[f'{subject}综合得分'] = (
                df[total_score_cols[0]] * 0.4 +  # 第一个考试总分
                df[total_score_cols[1]] * 0.3 +  # 第二个考试总分
                df[total_score_cols[2]] * 0.3    # 第三个考试总分
            )
        elif len(total_score_cols) == 2:
            df[f'{subject}综合得分'] = (
                df[total_score_cols[0]] * 0.4 +  # 第一个考试总分
                df[total_score_cols[1]] * 0.6    # 第二个考试总分
            )
        elif len(total_score_cols) == 1:
            df[f'{subject}综合得分'] = df[total_score_cols[0]]
        else:
            print(f"警告: {subject} 没有生成任何总分列，无法计算综合得分")
            df[f'{subject}综合得分'] = 0.0
        
        # 计算综合排名
        df[f'{subject}综合排名'] = df[f'{subject}综合得分'].rank(ascending=False, method='min')
        
        # 添加综合列
        new_cols.append(f'{subject}综合得分')
        new_cols.append(f'{subject}综合排名')
        
        # 添加剩余的列（如果有的话）
        remaining_cols = [col for col in df.columns if col not in new_cols]
        new_cols.extend(remaining_cols)
        
        # 创建最终的DataFrame
        final_df = df[new_cols].copy()
        
        # 保存结果
        output_file = f'{subject}排名赋分结果_动态识别版.xlsx'
        final_df.to_excel(output_file, index=False)
        print(f"结果已保存到: {output_file}")
        
        return final_df
        
    except Exception as e:
        print(f"处理科目 {subject} 时出错: {e}")
        import traceback
        traceback.print_exc()
        return None

def process_all_subjects(input_file_path, scoring_method='fixed'):
    """处理所有科目"""
    # 获取Excel文件中的所有科目
    xl_file = pd.ExcelFile(input_file_path)
    subjects = [sheet for sheet in xl_file.sheet_names if sheet != 'sheet1']
    
    print(f"发现科目: {subjects}")
    print(f"使用赋分方式: {scoring_method}")
    print("=" * 50)
    
    all_results = {}
    
    # 处理每个科目
    for subject in subjects:
        print(f"\n开始处理科目: {subject}")
        try:
            result = process_single_subject(input_file_path, subject, scoring_method)
            if result is not None:
                all_results[subject] = result
                print(f"✅ {subject} 处理成功！")
                print(f"   结果列数: {len(result.columns)}")
                
                # 检查差值列
                diff_cols = [col for col in result.columns if '差值' in col]
                print(f"   差值列数量: {len(diff_cols)}")
                
                # 检查是否所有指标都有差值列
                # 使用与extract_exam_names函数相同的指标定义，保持一致性
                metrics = ['平均分', '优秀率', '优良率', '合格率', '低分率']
                for metric in metrics:
                    diff_cols_for_metric = [col for col in diff_cols if metric in col]
                    print(f"   {metric}: {len(diff_cols_for_metric)} 个差值列")
            else:
                print(f"❌ {subject} 处理失败！")
        except Exception as e:
            print(f"❌ {subject} 处理出错: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("所有科目处理完成！")
    print(f"成功处理科目数: {len(all_results)}")
    print("成功科目列表:")
    for subject in all_results.keys():
        print(f"  ✅ {subject}")
    
    if len(all_results) > 0:
        print(f"\n第一个成功科目的详细信息:")
        first_subject = list(all_results.keys())[0]
        first_result = all_results[first_subject]
        print(f"科目: {first_subject}")
        print(f"列数: {len(first_result.columns)}")
        print("前30列名:")
        for i, col in enumerate(first_result.columns[:30]):
            print(f"{i:2d}: {col}")
    
    return all_results

if __name__ == "__main__":
    # 直接运行命令行模式
    print("教师排名赋分计算器启动...")
    result = calculate_scores_final_fix()
    if result is not None:
        print("\n计算成功！")
        print(f"结果列数: {len(result)}")
        print("成功科目列表:")
        for subject in result.keys():
            print(f"  ✅ {subject}")
    else:
        print("计算失败！")
