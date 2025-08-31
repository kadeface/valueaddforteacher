import pandas as pd
import numpy as np
import os

class TeacherScoreCalculator:
    """教师教学成绩排名赋分计算器"""
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.excel_file = None
        self.subjects = []
        
    def load_excel_file(self):
        """加载Excel文件并识别科目标签"""
        try:
            self.excel_file = pd.ExcelFile(self.file_path)
            # 过滤出科目标签（排除sheet1等非科目）
            self.subjects = [sheet for sheet in self.excel_file.sheet_names 
                           if sheet not in ['sheet1'] and len(sheet) <= 4]
            print(f"成功加载Excel文件，识别到科目：{self.subjects}")
            return True
        except Exception as e:
            print(f"加载Excel文件失败: {e}")
            return False
    
    def get_scoring_rules(self, total_count):
        """根据总人数确定赋分区间"""
        if total_count <= 20:
            # 小规模调整
            intervals = [
                (1, 3, 8, 8.9),
                (4, 7, 6, 6.9),
                (8, 12, 5, 5.9),
                (13, 18, 4, 4.9),
                (19, 25, 3, 3.9),
                (26, 30, 2, 2.9),
                (31, total_count, 0, 0)
            ]
        else:
            # 原始176人规则
            intervals = [
                (1, 18, 8, 8.9),
                (19, 43, 6, 6.9),
                (44, 71, 5, 5.9),
                (72, 106, 4, 4.9),
                (107, 134, 3, 3.9),
                (135, 159, 2, 2.9),
                (160, total_count, 0, 0)
            ]
        return intervals
    
    def assign_score(self, rank, intervals, is_jinshan):
        """根据排名和学校类型赋分"""
        for start, end, regular_score, jinshan_score in intervals:
            if start <= rank <= end:
                return jinshan_score if is_jinshan else regular_score
        return 0
    
    def get_exam_columns(self, exam_name, subject):
        """获取指定考试的指标列名"""
        if exam_name == "中考":
            # 检查是否有后缀的列名（如语文）
            suffix_cols = [
                f'{exam_name}   {subject}   平均分   p1',
                f'{exam_name}   {subject}   优秀率   y1', 
                f'{exam_name}   {subject}   优良率   l1',
                f'{exam_name}   {subject}   合格率  h1',
                f'{exam_name}   {subject}   低分率    d1'
            ]
            # 检查无后缀的列名（如生物、地理）
            no_suffix_cols = [
                f'{exam_name}   {subject}   平均分',
                f'{exam_name}   {subject}   优秀率',
                f'{exam_name}   {subject}   优良率',
                f'{exam_name}   {subject}   合格率',
                f'{exam_name}   {subject}   低分率'
            ]
            return suffix_cols, no_suffix_cols
            
        elif exam_name == "二模":
            suffix_cols = [
                f'{exam_name}   {subject}   平均分   p2',
                f'{exam_name}   {subject}   优秀率   y2',
                f'{exam_name}   {subject}   优良率   l2', 
                f'{exam_name}   {subject}   合格率h2',
                f'{exam_name}     {subject}   低分率   d2'
            ]
            no_suffix_cols = [
                f'{exam_name}   {subject}   平均分',
                f'{exam_name}   {subject}   优秀率',
                f'{exam_name}   {subject}   优良率',
                f'{exam_name}   {subject}   合格率',
                f'{exam_name}   {subject}   低分率'
            ]
            return suffix_cols, no_suffix_cols
            
        elif exam_name == "九年上":
            suffix_cols = [
                f'{exam_name}   {subject}   平均分   p3',
                f'{exam_name}   {subject}   优秀率   y3',
                f'{exam_name}   {subject}   优良率   l3',
                f'{exam_name}   {subject}   合格率   h3',
                f'{exam_name}   {subject}   低分率   d3'
            ]
            no_suffix_cols = [
                f'{exam_name}   {subject}   平均分',
                f'{exam_name}   {subject}   优秀率',
                f'{exam_name}   {subject}   优良率',
                f'{exam_name}   {subject}   合格率',
                f'{exam_name}   {subject}   低分率'
            ]
            return suffix_cols, no_suffix_cols
            
        elif exam_name == "八年下":
            suffix_cols = [
                f'{exam_name}   {subject}   平均分   p4',
                f'{exam_name}   {subject}   优秀率   y4',
                f'{exam_name}   {subject}   优良率   l4',
                f'{exam_name}   {subject}   合格率   h4',
                f'{exam_name}   {subject}   低分率   d4'
            ]
            no_suffix_cols = [
                f'{exam_name}   {subject}   平均分',
                f'{exam_name}   {subject}   优秀率',
                f'{exam_name}   {subject}   优良率',
                f'{exam_name}   {subject}   合格率',
                f'{exam_name}   {subject}   低分率'
            ]
            return suffix_cols, no_suffix_cols
        
        return [], []
    
    def find_existing_columns(self, df, suffix_cols, no_suffix_cols):
        """查找实际存在的列名"""
        # 优先查找有后缀的列名
        existing_cols = [col for col in suffix_cols if col in df.columns]
        if len(existing_cols) == 5:
            return existing_cols, True  # True表示有后缀
        
        # 如果没有找到有后缀的列，查找无后缀的列
        existing_cols = [col for col in no_suffix_cols if col in df.columns]
        if len(existing_cols) == 5:
            return existing_cols, False  # False表示无后缀
        
        return [], False
    
    def calculate_exam_scores(self, df, exam_name, subject):
        """计算单个考试的得分"""
        suffix_cols, no_suffix_cols = self.get_exam_columns(exam_name, subject)
        existing_cols, has_suffix = self.find_existing_columns(df, suffix_cols, no_suffix_cols)
        
        if len(existing_cols) != 5:
            print(f"警告: {exam_name} 缺少必要的列")
            return df
        
        metric_names = ['平均分', '优秀率', '优良率', '合格率', '低分率']
        
        # 获取总人数
        total_count = len(df)
        intervals = self.get_scoring_rules(total_count)
        
        # 对每个指标进行排名和赋分
        for i, (col, name) in enumerate(zip(existing_cols, metric_names)):
            # 处理缺失值
            valid_data = df[col].dropna()
            if len(valid_data) == 0:
                print(f"警告: {exam_name} {name} 列没有有效数据")
                continue
            
            # 确定排序方向
            if name == '低分率':
                # 低分率：从低到高排序（越低越好）
                ascending = True
            else:
                # 其他指标：从高到低排序（越高越好）
                ascending = False
            
            # 排序并获取排名（兼容老版本pandas）
            try:
                sorted_df = df.sort_values(col, ascending=ascending, na_last=True)
            except TypeError:
                # 老版本pandas不支持na_last参数
                sorted_df = df.sort_values(col, ascending=ascending)
                # 手动将NaN值放到最后
                sorted_df = pd.concat([
                    sorted_df.dropna(subset=[col]), 
                    sorted_df[sorted_df[col].isna()]
                ])
            
            sorted_df = sorted_df.reset_index(drop=True)
            
            # 创建排名和得分列
            rank_col = f'{exam_name}_{name}_排名'
            score_col = f'{exam_name}_{name}_得分'
            
            # 计算排名和得分
            for idx, row in sorted_df.iterrows():
                rank = idx + 1
                is_jinshan = row['学校名称'] == '金山中学'
                score = self.assign_score(rank, intervals, is_jinshan)
                
                # 找到对应的原始行索引
                original_idx = df[(df['学校代码'] == row['学校代码']) & (df['班别'] == row['班别'])].index[0]
                df.loc[original_idx, rank_col] = rank
                df.loc[original_idx, score_col] = score
        
        # 计算加权总分
        total_score_col = f'{exam_name}_{subject}总分'
        df[total_score_col] = (
            df[f'{exam_name}_平均分_得分'] * 0.3 +
            df[f'{exam_name}_优秀率_得分'] * 0.2 +
            df[f'{exam_name}_优良率_得分'] * 0.2 +
            df[f'{exam_name}_合格率_得分'] * 0.2 +
            df[f'{exam_name}_低分率_得分'] * 0.1
        )
        
        return df
    
    def calculate_difference_scores(self, df, exam1_name, exam2_name, subject):
        """计算两个考试之间的差值并赋分"""
        suffix_cols1, no_suffix_cols1 = self.get_exam_columns(exam1_name, subject)
        suffix_cols2, no_suffix_cols2 = self.get_exam_columns(exam2_name, subject)
        
        existing_exam1_cols, has_suffix1 = self.find_existing_columns(df, suffix_cols1, no_suffix_cols1)
        existing_exam2_cols, has_suffix2 = self.find_existing_columns(df, suffix_cols2, no_suffix_cols2)
        
        if len(existing_exam1_cols) != 5 or len(existing_exam2_cols) != 5:
            print(f"警告: {exam1_name} 或 {exam2_name} 缺少必要的列")
            return df
        
        metric_names = ['平均分', '优秀率', '优良率', '合格率', '低分率']
        
        # 获取总人数
        total_count = len(df)
        intervals = self.get_scoring_rules(total_count)
        
        # 计算差值并赋分
        for i, (col1, col2, name) in enumerate(zip(existing_exam1_cols, existing_exam2_cols, metric_names)):
            # 计算差值
            diff_col = f'{exam1_name}-{exam2_name}_{name}_差值'
            df[diff_col] = df[col1] - df[col2]
            
            # 处理缺失值
            valid_diff = df[diff_col].dropna()
            if len(valid_diff) == 0:
                print(f"警告: {exam1_name}-{exam2_name} {name} 差值没有有效数据")
                continue
            
            # 确定排序方向
            if name == '低分率':
                # 低分率差值：负值表示进步
                ascending = True
            else:
                # 其他指标差值：正值表示进步
                ascending = False
            
            # 排序并获取排名（兼容老版本pandas）
            try:
                sorted_df = df.sort_values(diff_col, ascending=ascending, na_last=True)
            except TypeError:
                sorted_df = df.sort_values(diff_col, ascending=ascending)
                sorted_df = pd.concat([
                    sorted_df.dropna(subset=[diff_col]), 
                    sorted_df[sorted_df[diff_col].isna()]
                ])
            
            sorted_df = sorted_df.reset_index(drop=True)
            
            # 创建排名和得分列
            rank_col = f'{exam1_name}-{exam2_name}_{name}_差值排名'
            score_col = f'{exam1_name}-{exam2_name}_{name}_差值得分'
            
            # 计算排名和得分
            for idx, row in sorted_df.iterrows():
                rank = idx + 1
                is_jinshan = row['学校名称'] == '金山中学'
                score = self.assign_score(rank, intervals, is_jinshan)
                
                # 找到对应的原始行索引
                original_idx = df[(df['学校代码'] == row['学校代码']) & (df['班别'] == row['班别'])].index[0]
                df.loc[original_idx, rank_col] = rank
                df.loc[original_idx, score_col] = score
        
        # 计算加权总分
        total_score_col = f'{exam2_name}_{subject}总分'
        df[total_score_col] = (
            df[f'{exam1_name}-{exam2_name}_平均分_差值得分'] * 0.3 +
            df[f'{exam1_name}-{exam2_name}_优秀率_差值得分'] * 0.2 +
            df[f'{exam1_name}-{exam2_name}_优良率_差值得分'] * 0.2 +
            df[f'{exam1_name}-{exam2_name}_合格率_差值得分'] * 0.2 +
            df[f'{exam1_name}-{exam2_name}_低分率_差值得分'] * 0.1
        )
        
        return df
    
    def calculate_comprehensive_score(self, df, subject):
        """计算综合得分和排名"""
        # 获取所有总分列
        total_score_cols = [col for col in df.columns if col.endswith(f'{subject}总分')]
        
        if len(total_score_cols) == 0:
            print(f"警告: {subject} 没有找到总分列")
            return df
        
        # 根据考试次数确定加权规则
        if len(total_score_cols) == 4:
            # 四次考试
            df[f'{subject}综合得分'] = (
                df[total_score_cols[0]] * 0.4 +
                df[total_score_cols[1]] * 0.2 +
                df[total_score_cols[2]] * 0.2 +
                df[total_score_cols[3]] * 0.2
            )
        elif len(total_score_cols) == 3:
            # 三次考试
            df[f'{subject}综合得分'] = (
                df[total_score_cols[0]] * 0.4 +
                df[total_score_cols[1]] * 0.3 +
                df[total_score_cols[2]] * 0.3
            )
        elif len(total_score_cols) == 2:
            # 二次考试
            df[f'{subject}综合得分'] = (
                df[total_score_cols[0]] * 0.4 +
                df[total_score_cols[1]] * 0.6
            )
        else:
            # 一次考试
            df[f'{subject}综合得分'] = df[total_score_cols[0]]
        
        # 计算综合排名
        df[f'{subject}综合排名'] = df[f'{subject}综合得分'].rank(ascending=False, method='min')
        
        return df
    
    def process_subject(self, subject):
        """处理单个科目的计算"""
        print(f"\n开始处理科目: {subject}")
        
        try:
            # 读取科目数据
            df = pd.read_excel(self.file_path, sheet_name=subject)
            print(f"成功读取 {subject} 数据，共 {len(df)} 行")
            
            # 标准化列名
            df.columns = [col.strip() if isinstance(col, str) else col for col in df.columns]
            
            # 重命名关键列
            df = df.rename(columns={
                '学校   代码': '学校代码',
                '学校名称': '学校名称',
                '班   别': '班别'
            })
            
            # 1. 计算第一个考试（中考）的得分
            print(f"1. 计算中考得分...")
            df = self.calculate_exam_scores(df, "中考", subject)
            
            # 检查是否有更多考试
            suffix_cols, no_suffix_cols = self.get_exam_columns("二模", subject)
            existing_cols, has_suffix = self.find_existing_columns(df, suffix_cols, no_suffix_cols)
            
            if len(existing_cols) == 5:
                # 2. 计算第二个考试（二模）的差值得分
                print(f"2. 计算二模差值得分...")
                df = self.calculate_difference_scores(df, "中考", "二模", subject)
                
                # 检查是否有第三次考试
                suffix_cols3, no_suffix_cols3 = self.get_exam_columns("九年上", subject)
                existing_cols3, has_suffix3 = self.find_existing_columns(df, suffix_cols3, no_suffix_cols3)
                
                if len(existing_cols3) == 5:
                    # 3. 计算第三个考试（九年上）的差值得分
                    print(f"3. 计算九年上差值得分...")
                    df = self.calculate_difference_scores(df, "二模", "九年上", subject)
                    
                    # 检查是否有第四次考试
                    suffix_cols4, no_suffix_cols4 = self.get_exam_columns("八年下", subject)
                    existing_cols4, has_suffix4 = self.find_existing_columns(df, suffix_cols4, no_suffix_cols4)
                    
                    if len(existing_cols4) == 5:
                        # 4. 计算第四个考试（八年下）的差值得分
                        print(f"4. 计算八年下差值得分...")
                        df = self.calculate_difference_scores(df, "九年上", "八年下", subject)
            
            # 5. 计算综合得分和排名
            print(f"5. 计算综合得分和排名...")
            df = self.calculate_comprehensive_score(df, subject)
            
            # 保存结果
            output_file = f'{subject}排名赋分结果.xlsx'
            df.to_excel(output_file, index=False)
            print(f"结果已保存到: {output_file}")
            
            return df
            
        except Exception as e:
            print(f"处理科目 {subject} 时出错: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def run_calculation(self):
        """运行完整计算流程"""
        if not self.load_excel_file():
            return
        
        print(f"\n开始计算，共 {len(self.subjects)} 个科目")
        
        results = {}
        for subject in self.subjects:
            result = self.process_subject(subject)
            if result is not None:
                results[subject] = result
        
        print(f"\n计算完成！共处理 {len(results)} 个科目")
        return results

def main():
    """主函数"""
    file_path = 'data/2025Mid3.xls'
    
    if not os.path.exists(file_path):
        print(f"错误: 文件 {file_path} 不存在")
        return
    
    # 创建计算器实例
    calculator = TeacherScoreCalculator(file_path)
    
    # 运行计算
    results = calculator.run_calculation()
    
    if results:
        print("\n计算成功！结果文件已保存。")
        # 显示第一个科目的前几行结果作为示例
        first_subject = list(results.keys())[0]
        print(f"\n{first_subject} 科目结果预览（前5行）:")
        print(results[first_subject][['学校代码', '学校名称', '班别', f'{first_subject}综合得分', f'{first_subject}综合排名']].head())

if __name__ == "__main__":
    main()
