import pandas as pd
import numpy as np
import re
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataCleaner:
    """数据清洗器：处理表头标准化和数据类型转换"""
    
    def __init__(self):
        # 表头标准化映射
        self.header_mapping = {
            # 学校相关
            '学校   代码': '学校代码',
            '学校代码': '学校代码',
            '学校  代码': '学校代码',
            '学校名称': '学校名称',
            '学校  名称': '学校名称',
            
            # 班级相关
            '班   别': '班别',
            '班别': '班别',
            '班级': '班别',
            '班  别': '班别',
            
            # 科任教师相关
            '语文科任': '语文科任',
            '数学科任': '数学科任',
            '英语科任': '英语科任',
            '物理科任': '物理科任',
            '化学科任': '化学科任',
            '道法科任': '道法科任',
            '历史科任': '历史科任',
            '地理科任': '地理科任',
            '生物科任': '生物科任',
            '科学科任': '科学科任',
        }
        
        # 考试列名标准化规则
        self.exam_column_patterns = {
            # 考试名称标准化
            'exam_names': ['中考', '二模', '九年上', '八年下', '八年上', '七年下', '七年上', 
                          '六年下', '六年上', '五年下', '五年上', '四年下', '四年上', 
                          '三年下', '三年上', '七年入'],
            
            # 科目名称标准化
            'subjects': ['语文', '数学', '英语', '物理', '化学', '道法', '历史', '地理', '生物', '科学'],
            
            # 指标名称标准化
            'metrics': ['平均分', '优秀率', '优良率', '合格率', '低分率'],
            
            # 后缀标准化
            'suffixes': ['p1', 'p2', 'p3', 'p4', 'y1', 'y2', 'y3', 'y4', 
                        'l1', 'l2', 'l3', 'l4', 'h1', 'h2', 'h3', 'h4', 
                        'd1', 'd2', 'd3', 'd4']
        }
        
        # 列名分隔符配置
        self.separator = '_'  # 使用下划线作为分隔符
        
        # 数值列模式（用于识别需要转换的列）
        self.numeric_patterns = [
            r'.*平均分.*',
            r'.*优秀率.*',
            r'.*优良率.*',
            r'.*合格率.*',
            r'.*低分率.*',
            r'.*总分.*',
            r'.*得分.*',
            r'.*排名.*',
            r'.*差值.*'
        ]
        
        # 需要转换为数值的列后缀
        self.numeric_suffixes = ['p1', 'p2', 'p3', 'p4', 'y1', 'y2', 'y3', 'y4', 
                               'l1', 'l2', 'l3', 'l4', 'h1', 'h2', 'h3', 'h4', 
                               'd1', 'd2', 'd3', 'd4']
    
    def clean_headers(self, df):
        """清洗和标准化表头"""
        logger.info("开始清洗表头...")
        
        # 创建新的列名列表
        new_columns = []
        cleaned_mapping = {}
        
        for col in df.columns:
            original_col = col
            cleaned_col = col
            
            # 1. 去除首尾空格
            if isinstance(col, str):
                cleaned_col = col.strip()
            
            # 2. 先应用标准化映射（在空格处理之前）
            if cleaned_col in self.header_mapping:
                cleaned_col = self.header_mapping[cleaned_col]
                logger.info(f"应用列名映射: '{original_col}' -> '{cleaned_col}'")
            else:
                # 3. 对于非关键列名，处理空格和特殊字符
                if isinstance(col, str):
                    # 去除多余空格（将多个空格替换为下划线）
                    cleaned_col = re.sub(r'\s+', '_', cleaned_col)
                    
                    # 去除特殊字符（保留中文、英文、数字、下划线、连字符）
                    cleaned_col = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\-_]', '', cleaned_col)
                    
                    # 标准化下划线（确保单个下划线分隔，去除多余下划线）
                    cleaned_col = re.sub(r'_+', '_', cleaned_col)
            
            # 4. 标准化考试列名
            cleaned_col = self._standardize_exam_column_name(cleaned_col)
            
            # 4. 记录清洗映射关系
            if original_col != cleaned_col:
                cleaned_mapping[original_col] = cleaned_col
                logger.info(f"表头清洗: '{original_col}' -> '{cleaned_col}'")
            
            new_columns.append(cleaned_col)
        
        # 更新DataFrame的列名
        df.columns = new_columns
        
        # 检查是否有重复列名
        duplicate_cols = df.columns[df.columns.duplicated()].tolist()
        if duplicate_cols:
            logger.warning(f"发现重复列名: {duplicate_cols}")
            # 为重复列名添加后缀（简单方法）
            new_columns = []
            seen_columns = {}
            
            for col in df.columns:
                if col in seen_columns:
                    seen_columns[col] += 1
                    new_col = f"{col}_{seen_columns[col]}"
                    new_columns.append(new_col)
                    logger.info(f"重命名重复列: '{col}' -> '{new_col}'")
                else:
                    seen_columns[col] = 0
                    new_columns.append(col)
            
            df.columns = new_columns
            logger.info("已自动处理重复列名")
        
        logger.info(f"表头清洗完成，共处理 {len(cleaned_mapping)} 个列名")
        return df, cleaned_mapping
    
    def convert_data_types(self, df):
        """转换数据类型和验证数据"""
        logger.info("开始数据类型转换和验证...")
        
        conversion_stats = {
            'numeric_converted': 0,
            'null_values_filled': 0,
            'invalid_values_fixed': 0
        }
        
        for col in df.columns:
            if not isinstance(col, str):
                continue
                
            # 1. 识别数值列
            is_numeric_col = False
            for pattern in self.numeric_patterns:
                if re.match(pattern, col):
                    is_numeric_col = True
                    break
            
            # 检查列后缀
            if not is_numeric_col:
                for suffix in self.numeric_suffixes:
                    if col.endswith(suffix) or f'   {suffix}' in col:
                        is_numeric_col = True
                        break
            
            if is_numeric_col:
                logger.info(f"处理数值列: {col}")
                
                # 2. 数据类型转换
                original_dtype = df[col].dtype
                
                # 处理空值和异常值
                df[col] = self._clean_numeric_column(df[col])
                
                # 转换为数值类型
                try:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                    conversion_stats['numeric_converted'] += 1
                    
                    # 检查转换后的数据类型
                    new_dtype = df[col].dtype
                    if original_dtype != new_dtype:
                        logger.info(f"  类型转换: {original_dtype} -> {new_dtype}")
                    
                    # 3. 数值范围验证
                    self._validate_numeric_range(df[col], col)
                    
                except Exception as e:
                    logger.error(f"  列 {col} 数值转换失败: {e}")
        
        # 4. 处理空值
        null_counts = df.isnull().sum()
        total_null = null_counts.sum()
        if total_null > 0:
            logger.info(f"发现 {total_null} 个空值")
            conversion_stats['null_values_filled'] = total_null
        
        logger.info(f"数据类型转换完成:")
        logger.info(f"  数值列转换: {conversion_stats['numeric_converted']}")
        logger.info(f"  空值处理: {conversion_stats['null_values_filled']}")
        
        return df, conversion_stats
    
    def _standardize_exam_column_name(self, column_name):
        """标准化考试列名，确保格式一致"""
        if not isinstance(column_name, str):
            return column_name
        
        # 标准化下划线（确保单个下划线分隔）
        standardized_col = re.sub(r'_+', '_', column_name.strip())
        
        # 检查是否是考试列名
        is_exam_column = False
        for exam_name in self.exam_column_patterns['exam_names']:
            if exam_name in standardized_col:
                is_exam_column = True
                break
        
        if not is_exam_column:
            return standardized_col
        
        # 标准化考试列名格式
        # 目标格式: "考试名_科目_指标_后缀"
        
        # 1. 识别考试名称
        exam_name = None
        for exam in self.exam_column_patterns['exam_names']:
            if exam in standardized_col:
                exam_name = exam
                break
        
        # 2. 识别科目名称
        subject_name = None
        for subject in self.exam_column_patterns['subjects']:
            if subject in standardized_col:
                subject_name = subject
                break
        
        # 3. 识别指标名称
        metric_name = None
        for metric in self.exam_column_patterns['metrics']:
            if metric in standardized_col:
                metric_name = metric
                break
        
        # 4. 识别后缀
        suffix = None
        for suffix_pattern in self.exam_column_patterns['suffixes']:
            if suffix_pattern in standardized_col:
                suffix = suffix_pattern
                break
        
        # 5. 重新组装标准格式
        if exam_name and subject_name and metric_name:
            if suffix:
                standardized_col = f"{exam_name}_{subject_name}_{metric_name}_{suffix}"
            else:
                standardized_col = f"{exam_name}_{subject_name}_{metric_name}"
            
            logger.debug(f"考试列名标准化: '{column_name}' -> '{standardized_col}'")
        
        return standardized_col
    
    def _clean_numeric_column(self, series):
        """清理数值列的数据"""
        if series.dtype in ['int64', 'float64']:
            return series
        
        # 处理字符串类型的数值
        if series.dtype == 'object':
            # 去除百分号
            series = series.astype(str).str.replace('%', '')
            
            # 去除空格
            series = series.str.strip()
            
            # 处理特殊字符
            series = series.str.replace('，', '.')  # 中文逗号转英文点
            series = series.str.replace(',', '.')  # 英文逗号转英文点
            
            # 处理空字符串
            series = series.replace(['', 'nan', 'None', 'NULL'], np.nan)
            
            # 处理异常值
            series = series.replace(['#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', 
                                   '-NaN', '-nan', '1.#IND', '1.#QNAN', 'N/A', 'NA', 
                                   'NULL', 'NaN', 'nan'], np.nan)
        
        return series
    
    def _validate_numeric_range(self, series, col_name):
        """验证数值范围"""
        if series.dtype in ['int64', 'float64']:
            # 检查是否有无穷大值
            if np.isinf(series).any():
                logger.warning(f"  列 {col_name} 包含无穷大值")
                series.replace([np.inf, -np.inf], np.nan, inplace=True)
            
            # 检查异常值（超过3个标准差）
            if len(series.dropna()) > 0:
                mean_val = series.mean()
                std_val = series.std()
                if std_val > 0:
                    outliers = series[(series < mean_val - 3*std_val) | 
                                    (series > mean_val + 3*std_val)]
                    if len(outliers) > 0:
                        logger.warning(f"  列 {col_name} 发现 {len(outliers)} 个异常值")
    
    def clean_dataframe(self, df):
        """完整的数据清洗流程"""
        logger.info("=" * 50)
        logger.info("开始数据清洗流程")
        logger.info("=" * 50)
        
        # 1. 表头清洗
        df, header_mapping = self.clean_headers(df)
        
        # 2. 数据类型转换和验证
        df, conversion_stats = self.convert_data_types(df)
        
        # 3. 生成清洗报告
        self._generate_cleaning_report(df, header_mapping, conversion_stats)
        
        logger.info("=" * 50)
        logger.info("数据清洗流程完成")
        logger.info("=" * 50)
        
        return df
    
    def _generate_cleaning_report(self, df, header_mapping, conversion_stats):
        """生成清洗报告"""
        logger.info("\n📊 数据清洗报告:")
        logger.info(f"  原始列数: {len(df.columns)}")
        logger.info(f"  清洗后列数: {len(df.columns)}")
        logger.info(f"  表头标准化: {len(header_mapping)} 个列名被修改")
        logger.info(f"  数值列转换: {conversion_stats['numeric_converted']} 个")
        logger.info(f"  空值处理: {conversion_stats['null_values_filled']} 个")
        
        # 统计考试列名标准化情况
        exam_columns = [col for col in df.columns if any(exam in col for exam in self.exam_column_patterns['exam_names'])]
        logger.info(f"  考试列名: {len(exam_columns)} 个")
        
        # 显示前几列作为示例
        logger.info(f"\n前10列名示例:")
        for i, col in enumerate(df.columns[:10]):
            logger.info(f"  {i+1:2d}: {col}")
        
        if len(df.columns) > 10:
            logger.info(f"  ... 还有 {len(df.columns) - 10} 列")
        
        # 显示考试列名示例
        if exam_columns:
            logger.info(f"\n考试列名示例:")
            for i, col in enumerate(exam_columns[:5]):
                logger.info(f"  {i+1:2d}: {col}")
            if len(exam_columns) > 5:
                logger.info(f"  ... 还有 {len(exam_columns) - 5} 个考试列名")

def clean_excel_data(file_path, sheet_name=None):
    """便捷函数：清洗Excel数据"""
    try:
        # 读取Excel文件
        if sheet_name:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            logger.info(f"成功读取工作表: {sheet_name}")
        else:
            df = pd.read_excel(file_path)
            logger.info(f"成功读取Excel文件")
        
        logger.info(f"原始数据形状: {df.shape}")
        
        # 创建清洗器并执行清洗
        cleaner = DataCleaner()
        cleaned_df = cleaner.clean_dataframe(df)
        
        return cleaned_df
        
    except Exception as e:
        logger.error(f"数据清洗失败: {e}")
        raise

if __name__ == "__main__":
    # 测试代码
    print("数据清洗模块测试")
    
    # 创建测试数据
    test_data = {
        '学校   代码': ['001', '002', '003'],
        '学校名称': ['学校A', '学校B', '学校C'],
        '班   别': ['1班', '2班', '3班'],
        '语文科任': ['张老师', '李老师', '王老师'],
        '中考   语文   平均分   p1': ['85.5', '92.3', '78.9'],
        '中考   语文   优秀率   p1': ['25%', '35%', '20%'],
        '中考   语文   优良率   p1': ['60%', '70%', '55%'],
        '中考   语文   合格率   p1': ['95%', '98%', '92%'],
        '中考   语文   低分率   p1': ['5%', '2%', '8%']
    }
    
    test_df = pd.DataFrame(test_data)
    print("原始数据:")
    print(test_df.head())
    print("\n列名:", test_df.columns.tolist())
    
    # 执行清洗
    cleaner = DataCleaner()
    cleaned_df = cleaner.clean_dataframe(test_df)
    
    print("\n清洗后数据:")
    print(cleaned_df.head())
    print("\n清洗后列名:", cleaned_df.columns.tolist())
