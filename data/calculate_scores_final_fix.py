import pandas as pd
import numpy as np
import os

def calculate_scores_final_fix():
    """最终修复版本，确保所有指标都有完整的差值列、差值排名列、差值得分列"""
    
    file_path = 'data/2025Mid3.xls'
    
    # 只处理语文科目作为示例
    subject = '语文'
    print(f"开始处理科目: {subject}")
    
    try:
        # 读取科目数据
        df = pd.read_excel(file_path, sheet_name=subject)
        print(f"成功读取 {subject} 数据，共 {len(df)} 行")
        
        # 标准化列名
        df.columns = [col.strip() if isinstance(col, str) else col for col in df.columns]
        
        # 重命名关键列
        df = df.rename(columns={
            '学校   代码': '学校代码',
            '学校名称': '学校名称',
            '班   别': '班别'
        })
        
        # 获取总人数
        total_count = len(df)
        
        # 定义赋分规则
        if total_count <= 20:
            intervals = [(1, 3, 8, 8.9), (4, 7, 6, 6.9), (8, 12, 5, 5.9), 
                        (13, 18, 4, 4.9), (19, 25, 3, 3.9), (26, 30, 2, 2.9), (31, total_count, 0, 0)]
        else:
            intervals = [(1, 18, 8, 8.9), (19, 43, 6, 6.9), (44, 71, 5, 5.9), 
                        (72, 106, 4, 4.9), (107, 134, 3, 3.9), (135, 159, 2, 2.9), (160, total_count, 0, 0)]
        
        def assign_score(rank, is_jinshan):
            for start, end, regular_score, jinshan_score in intervals:
                if start <= rank <= end:
                    return jinshan_score if is_jinshan else regular_score
            return 0
        
        # 创建新的列列表，按照规则说明文档的要求
        new_cols = ['学校代码', '学校名称', '班别', '语文科任']
        
        # 第一个考试（中考）
        exam1_metrics = ['平均分   p1', '优秀率   y1', '优良率   l1', '合格率  h1', '低分率    d1']
        exam1_scores = []
        
        for metric in exam1_metrics:
            col_name = f'中考   {subject}   {metric}'
            if col_name in df.columns:
                new_cols.append(col_name)
                
                # 计算排名和得分
                col_data = df[col_name].dropna()
                if len(col_data) > 0:
                    # 确定排序方向
                    if '低分率' in metric:
                        ascending = True  # 低分率从低到高
                    else:
                        ascending = False  # 其他从高到低
                    
                    # 排序并计算排名
                    sorted_df = df.sort_values(col_name, ascending=ascending)
                    sorted_df = sorted_df.reset_index(drop=True)
                    
                    # 计算排名和得分
                    metric_name = metric.split()[0]
                    rank_col = f'中考_{metric_name}_排名'
                    score_col = f'中考_{metric_name}_得分'
                    
                    for idx, row in sorted_df.iterrows():
                        rank = idx + 1
                        is_jinshan = row['学校名称'] == '金山中学'
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
            total_score_col = f'中考_{subject}总分'
            df[total_score_col] = (
                df[exam1_scores[0]] * 0.3 +  # 平均分
                df[exam1_scores[1]] * 0.2 +  # 优秀率
                df[exam1_scores[2]] * 0.2 +  # 优良率
                df[exam1_scores[3]] * 0.2 +  # 合格率
                df[exam1_scores[4]] * 0.1    # 低分率
            )
            new_cols.append(total_score_col)
        
        # 第二个考试（二模）
        exam2_metrics = ['平均分   p2', '优秀率   y2', '优良率   l2', '合格率h2', '低分率   d2']
        exam2_scores = []
        
        # 定义指标名称映射
        metric_mapping = {
            '平均分   p1': '平均分', '平均分   p2': '平均分', '平均分   p3': '平均分', '平均分   p4': '平均分',
            '优秀率   y1': '优秀率', '优秀率   y2': '优秀率', '优秀率   y3': '优秀率', '优秀率   y4': '优秀率',
            '优良率   l1': '优良率', '优良率   l2': '优良率', '优良率   l3': '优良率', '优良率   l4': '优良率',
            '合格率  h1': '合格率', '合格率h2': '合格率', '合格率   h3': '合格率', '合格率   h4': '合格率',
            '低分率    d1': '低分率', '低分率   d2': '低分率', '低分率   d3': '低分率', '低分率   d4': '低分率'
        }
        
        for metric in exam2_metrics:
            col_name = f'二模   {subject}   {metric}'
            if col_name in df.columns:
                new_cols.append(col_name)
                
                # 获取对应的第一个考试列名
                metric_name = metric_mapping[metric]
                
                # 根据指标类型构建对应的第一个考试列名
                if metric_name == '平均分':
                    exam1_col = f'中考   {subject}   平均分   p1'
                elif metric_name == '优秀率':
                    exam1_col = f'中考   {subject}   优秀率   y1'
                elif metric_name == '优良率':
                    exam1_col = f'中考   {subject}   优良率   l1'
                elif metric_name == '合格率':
                    exam1_col = f'中考   {subject}   合格率  h1'
                elif metric_name == '低分率':
                    exam1_col = f'中考   {subject}   低分率    d1'
                else:
                    exam1_col = f'中考   {subject}   {metric_name}   p1'
                
                if exam1_col in df.columns:
                    # 计算差值
                    diff_col = f'中考-二模_{metric_name}_差值'
                    df[diff_col] = df[exam1_col] - df[col_name]
                    
                    # 计算差值排名和得分
                    diff_data = df[diff_col].dropna()
                    if len(diff_data) > 0:
                        # 确定排序方向
                        if '低分率' in metric:
                            ascending = True  # 低分率差值负值表示进步
                        else:
                            ascending = False  # 其他差值正值表示进步
                        
                        # 排序并计算排名
                        sorted_df = df.sort_values(diff_col, ascending=ascending)
                        sorted_df = sorted_df.reset_index(drop=True)
                        
                        # 计算排名和得分
                        diff_rank_col = f'中考-二模_{metric_name}_差值排名'
                        diff_score_col = f'中考-二模_{metric_name}_差值得分'
                        
                        for idx, row in sorted_df.iterrows():
                            rank = idx + 1
                            is_jinshan = row['学校名称'] == '金山中学'
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
                        exam2_scores.append(diff_score_col)
        
        # 计算第二个考试总分
        if len(exam2_scores) == 5:
            total_score_col = f'二模_{subject}总分'
            df[total_score_col] = (
                df[exam2_scores[0]] * 0.3 +  # 平均分差值
                df[exam2_scores[1]] * 0.2 +  # 优秀率差值
                df[exam2_scores[2]] * 0.2 +  # 优良率差值
                df[exam2_scores[3]] * 0.2 +  # 合格率差值
                df[exam2_scores[4]] * 0.1    # 低分率差值
            )
            new_cols.append(total_score_col)
        
        # 第三个考试（九年上）
        exam3_metrics = ['平均分   p3', '优秀率   y3', '优良率   l3', '合格率   h3', '低分率   d3']
        exam3_scores = []
        
        for metric in exam3_metrics:
            col_name = f'九年上   {subject}   {metric}'
            if col_name in df.columns:
                new_cols.append(col_name)
                
                # 获取对应的第二个考试列名
                metric_name = metric_mapping.get(metric, metric.split()[0])
                if metric_name == '平均分':
                    exam2_col = f'二模   {subject}   平均分   p2'
                elif metric_name == '优秀率':
                    exam2_col = f'二模   {subject}   优秀率   y2'
                elif metric_name == '优良率':
                    exam2_col = f'二模   {subject}   优良率   l2'
                elif metric_name == '合格率':
                    exam2_col = f'二模   {subject}   合格率h2'
                elif metric_name == '低分率':
                    exam2_col = f'二模   {subject}   低分率   d2'
                else:
                    exam2_col = f'二模   {subject}   {metric_name}   p2'
                
                if exam2_col in df.columns:
                    # 计算差值
                    diff_col = f'二模-九年上_{metric_name}_差值'
                    df[diff_col] = df[exam2_col] - df[col_name]
                    
                    # 计算差值排名和得分
                    diff_data = df[diff_col].dropna()
                    if len(diff_data) > 0:
                        # 确定排序方向
                        if '低分率' in metric:
                            ascending = True  # 低分率差值负值表示进步
                        else:
                            ascending = False  # 其他差值正值表示进步
                        
                        # 排序并计算排名
                        sorted_df = df.sort_values(diff_col, ascending=ascending)
                        sorted_df = sorted_df.reset_index(drop=True)
                        
                        # 计算排名和得分
                        diff_rank_col = f'二模-九年上_{metric_name}_差值排名'
                        diff_score_col = f'二模-九年上_{metric_name}_差值得分'
                        
                        for idx, row in sorted_df.iterrows():
                            rank = idx + 1
                            is_jinshan = row['学校名称'] == '金山中学'
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
                        exam3_scores.append(diff_score_col)
        
        # 计算第三个考试总分
        if len(exam3_scores) == 5:
            total_score_col = f'九年上_{subject}总分'
            df[total_score_col] = (
                df[exam3_scores[0]] * 0.3 +  # 平均分差值
                df[exam3_scores[1]] * 0.2 +  # 优秀率差值
                df[exam3_scores[2]] * 0.2 +  # 优良率差值
                df[exam3_scores[3]] * 0.2 +  # 合格率差值
                df[exam3_scores[4]] * 0.1    # 低分率差值
            )
            new_cols.append(total_score_col)
        
        # 第四个考试（八年下）
        exam4_metrics = ['平均分   p4', '优秀率   y4', '优良率   l4', '合格率   h4', '低分率   d4']
        exam4_scores = []
        
        for metric in exam4_metrics:
            col_name = f'八年下   {subject}   {metric}'
            if col_name in df.columns:
                new_cols.append(col_name)
                
                # 获取对应的第三个考试列名
                metric_name = metric_mapping.get(metric, metric.split()[0])
                if metric_name == '平均分':
                    exam3_col = f'九年上   {subject}   平均分   p3'
                elif metric_name == '优秀率':
                    exam3_col = f'九年上   {subject}   优秀率   y3'
                elif metric_name == '优良率':
                    exam3_col = f'九年上   {subject}   优良率   l3'
                elif metric_name == '合格率':
                    exam3_col = f'九年上   {subject}   合格率   h3'
                elif metric_name == '低分率':
                    exam3_col = f'九年上   {subject}   低分率   d3'
                else:
                    exam3_col = f'九年上   {subject}   {metric_name}   p3'
                
                if exam3_col in df.columns:
                    # 计算差值
                    diff_col = f'九年上-八年下_{metric_name}_差值'
                    df[diff_col] = df[exam3_col] - df[col_name]
                    
                    # 计算差值排名和得分
                    diff_data = df[diff_col].dropna()
                    if len(diff_data) > 0:
                        # 确定排序方向
                        if '低分率' in metric:
                            ascending = True  # 低分率差值负值表示进步
                        else:
                            ascending = False  # 其他差值正值表示进步
                        
                        # 排序并计算排名
                        sorted_df = df.sort_values(diff_col, ascending=ascending)
                        sorted_df = sorted_df.reset_index(drop=True)
                        
                        # 计算排名和得分
                        diff_rank_col = f'九年上-八年下_{metric_name}_差值排名'
                        diff_score_col = f'九年上-八年下_{metric_name}_差值得分'
                        
                        for idx, row in sorted_df.iterrows():
                            rank = idx + 1
                            is_jinshan = row['学校名称'] == '金山中学'
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
                        exam4_scores.append(diff_score_col)
        
        # 计算第四个考试总分
        if len(exam4_scores) == 5:
            total_score_col = f'八年下_{subject}总分'
            df[total_score_col] = (
                df[exam4_scores[0]] * 0.3 +  # 平均分差值
                df[exam4_scores[1]] * 0.2 +  # 优秀率差值
                df[exam4_scores[2]] * 0.2 +  # 优良率差值
                df[exam4_scores[3]] * 0.2 +  # 合格率差值
                df[exam4_scores[4]] * 0.1    # 低分率差值
            )
            new_cols.append(total_score_col)
        
        # 计算综合得分
        total_score_cols = [col for col in df.columns if col.endswith(f'{subject}总分')]
        if len(total_score_cols) == 4:
            df[f'{subject}综合得分'] = (
                df[total_score_cols[0]] * 0.4 +  # 中考总分
                df[total_score_cols[1]] * 0.2 +  # 二模总分
                df[total_score_cols[2]] * 0.2 +  # 九年上总分
                df[total_score_cols[3]] * 0.2    # 八年下总分
            )
        elif len(total_score_cols) == 3:
            df[f'{subject}综合得分'] = (
                df[total_score_cols[0]] * 0.4 +  # 中考总分
                df[total_score_cols[1]] * 0.3 +  # 二模总分
                df[total_score_cols[2]] * 0.3    # 九年上总分
            )
        elif len(total_score_cols) == 2:
            df[f'{subject}综合得分'] = (
                df[total_score_cols[0]] * 0.4 +  # 中考总分
                df[total_score_cols[1]] * 0.6    # 二模总分
            )
        else:
            df[f'{subject}综合得分'] = df[total_score_cols[0]]
        
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
        output_file = f'{subject}排名赋分结果_最终修复版.xlsx'
        final_df.to_excel(output_file, index=False)
        print(f"结果已保存到: {output_file}")
        
        return final_df
        
    except Exception as e:
        print(f"处理科目 {subject} 时出错: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = calculate_scores_final_fix()
    if result is not None:
        print("\n计算成功！")
        print(f"结果列数: {len(result.columns)}")
        print("前30列名:")
        for i, col in enumerate(result.columns[:30]):
            print(f"{i:2d}: {col}")
        
        # 检查差值列
        print("\n差值列检查:")
        diff_cols = [col for col in result.columns if '差值' in col]
        print(f"差值列数量: {len(diff_cols)}")
        for col in diff_cols:
            print(f"  {col}")
        
        # 检查是否所有指标都有差值列
        print("\n检查是否所有指标都有差值列:")
        metrics = ['平均分', '优秀率', '优良率', '合格率', '低分率']
        for metric in metrics:
            diff_cols_for_metric = [col for col in diff_cols if metric in col]
            print(f"  {metric}: {len(diff_cols_for_metric)} 个差值列")
            for col in diff_cols_for_metric:
                print(f"    {col}")
