# 教师排名赋分计算器

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

一个专业的教师教学成绩排名和赋分计算系统，支持多科目批量处理、智能数据清洗和Web界面操作。

## 📋 项目概述

教师排名赋分计算器是一个用于计算教师教学成绩排名和赋分的Python程序。系统支持网页界面和命令行两种运行模式，能够自动处理Excel文件中的多个科目数据，计算各指标的排名、赋分和综合得分。

### ✨ 主要特性

- 🎯 **多科目支持**：支持语文、数学、英语、物理、化学、道法、历史、地理、生物等9个科目
- 🌐 **Web界面**：提供友好的网页操作界面，支持文件上传和实时进度显示
- 📊 **智能数据处理**：自动识别Excel文件结构，支持多种列名格式
- 🧮 **复杂计算规则**：实现多考试、多指标的加权计算和排名
- 📈 **结果可视化**：生成详细的Excel结果文件，包含排名、赋分和综合得分
- 🔧 **容错处理**：智能数据清洗，处理各种异常情况
- 📦 **批量处理**：支持单个科目或所有科目的批量计算

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Flask 2.0+
- pandas
- numpy
- openpyxl

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/kadeface/valueaddforteacher.git
cd valueaddforteacher
```

2. **创建虚拟环境**
```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate  # Windows
```

3. **安装依赖**
```bash
pip install flask pandas numpy openpyxl
```

### 运行方式

#### 方式1：Web界面（推荐）

```bash
# 激活虚拟环境
source .venv/bin/activate

# 启动Web服务
python3 web_app.py
```

启动成功后，在浏览器中访问：
- **本地访问**：`http://localhost:8080`
- **局域网访问**：`http://10.33.5.127:8080`

#### 方式2：命令行模式

```bash
# 处理所有科目
python3 calculate_scores_final_fix.py

# 处理指定科目
python3 -c "
import calculate_scores_final_fix
result = calculate_scores_final_fix.process_single_subject('data/2025Mid3.xls', '语文')
print('处理完成')
"
```

## 📊 数据格式要求

### Excel文件结构

- **文件格式**：`.xls` 或 `.xlsx`
- **工作表**：每个科目一个工作表（如：语文、数学、英语等）
- **排除工作表**：`sheet1` 等非科目工作表会被自动忽略

### 必需列名

- `学校代码`：学校标识（支持多种格式：`学校代码`、`学校   代码`等）
- `学校名称`：学校名称（支持多种格式：`学校名称`、`学校  名称`等）
- `班别`：班级信息（支持多种格式：`班别`、`班   别`等）
- `{科目}科任`：对应科目的任课教师（如：语文科任、数学科任）

### 考试数据列

程序会自动识别考试名称，支持以下格式：

#### 下划线格式（推荐）
```
{考试名}_{科目}_{指标}_{后缀}
例如：中考_语文_平均分_p1
```

#### 空格格式（兼容）
```
{考试名}   {科目}   {指标}   {后缀}
例如：中考   语文   平均分   p1
```

### 支持的考试类型

- 中考、二模
- 九年上、八年下、八年上
- 七年下、七年上、七年入
- 六年下、六年上
- 五年下、五年上
- 四年下、四年上
- 三年下、三年上

### 支持的指标类型

- 平均分（p）
- 优秀率（y）
- 优良率（l）
- 合格率（h）
- 低分率（d）

## ⚙️ 计算规则

### 赋分方式

系统支持两种赋分方式：

#### 1. 固定区间赋分（默认）

**总人数 ≤ 20人时**
- 第1-3名：8分（金山中学8.9分）
- 第4-7名：6分（金山中学6.9分）
- 第8-12名：5分（金山中学5.9分）
- 第13-18名：4分（金山中学4.9分）
- 第19-25名：3分（金山中学3.9分）
- 第26-30名：2分（金山中学2.9分）
- 第31名及以后：0分

**总人数 > 20人时（原始176人规则）**
- 第1-18名：8分（金山中学8.9分）
- 第19-43名：6分（金山中学6.9分）
- 第44-71名：5分（金山中学5.9分）
- 第72-106名：4分（金山中学4.9分）
- 第107-134名：3分（金山中学3.9分）
- 第135-159名：2分（金山中学2.9分）
- 第160名及以后：0分

#### 2. 百分比区间赋分（新增）

基于排名百分比的赋分方式，适用于不同规模的学校：

| 排名区间 | 比例 | 常规赋分 | 金山赋分 | 说明 |
|---------|------|---------|---------|------|
| 0%-10% | 10% | 8 | 8.9 | 前10% |
| 10%-24% | 14% | 6 | 6.9 | 10%-24% |
| 24%-40% | 16% | 5 | 5.9 | 24%-40% |
| 40%-60% | 20% | 4 | 4.9 | 40%-60% |
| 60%-76% | 16% | 3 | 3.9 | 60%-76% |
| 76%-90% | 14% | 2 | 2.9 | 76%-90% |
| 90%-100% | 10% | 0 | 0 | 90%-100% |

**示例**：如果总共有100人，排名第5的人
- 百分比 = 5/100 = 5%
- 属于前10%区间
- 常规赋分 = 8分
- 金山中学赋分 = 8.9分

### 排名规则

#### 第一次考试（中考）
直接对5个指标进行排名：
- **平均分、优秀率、优良率、合格率**：从高到低排序（越高越好）
- **低分率**：从低到高排序（越低越好）

#### 第二、三、四次考试
计算相邻两次考试的差值，然后对差值进行排名：
- **差值计算**：前一次考试 - 后一次考试
- **平均分、优秀率、优良率、合格率差值**：正值表示进步，从高到低排序
- **低分率差值**：负值表示进步，从低到高排序

### 加权计算规则

#### 单次考试加权总分
```
总分 = 平均分得分 × 0.3 + 优秀率得分 × 0.2 + 优良率得分 × 0.2 + 合格率得分 × 0.2 + 低分率得分 × 0.1
```

#### 综合得分计算
```
综合得分 = 第一次考试总分 × 0.4 + 第二次考试总分 × 0.3 + 第三次考试总分 × 0.2 + 第四次考试总分 × 0.1
```

## 🏗️ 项目结构

```
valueaddforteacher/
├── web_app.py                    # Web应用主程序
├── calculate_scores_final_fix.py # 核心计算模块
├── data_cleaner.py              # 数据清洗模块
├── templates/                   # Web模板文件
│   └── index.html              # 主页面模板
├── data/                       # 数据文件目录（已忽略）
├── uploads/                    # 上传文件目录（已忽略）
├── outputs/                    # 输出文件目录（已忽略）
├── .venv/                      # Python虚拟环境
├── .gitignore                  # Git忽略文件
├── 运行程序说明.md             # 详细运行说明
├── 计算规则说明文档.md         # 计算规则详细说明
└── README.md                   # 项目说明文档
```

## 🔧 核心模块说明

### web_app.py
Flask Web应用，提供文件上传、处理和下载功能。

### calculate_scores_final_fix.py
核心计算模块，包含：
- 动态考试名称识别
- 智能列名匹配
- 排名和赋分计算
- 加权得分计算

### data_cleaner.py
数据清洗模块，提供：
- 列名标准化
- 数据格式验证
- 异常数据处理

## 📝 使用示例

### Web界面操作

1. **上传文件**：选择包含教师数据的Excel文件
2. **选择科目**：选择"所有科目"或特定科目
3. **开始处理**：点击"开始处理"按钮
4. **查看进度**：实时显示处理进度
5. **下载结果**：处理完成后下载结果文件

### 命令行操作

```bash
# 处理默认文件的所有科目（使用固定区间赋分）
python3 calculate_scores_final_fix.py

# 处理指定文件的所有科目（使用固定区间赋分）
python3 -c "
import calculate_scores_final_fix
result = calculate_scores_final_fix('path/to/your/file.xls')
print('处理完成')
"

# 处理指定文件的特定科目（使用固定区间赋分）
python3 -c "
import calculate_scores_final_fix
result = calculate_scores_final_fix('path/to/your/file.xls', '语文', 'fixed')
print('语文科目处理完成')
"

# 处理指定文件的特定科目（使用百分比区间赋分）
python3 -c "
import calculate_scores_final_fix
result = calculate_scores_final_fix('path/to/your/file.xls', '语文', 'percentage')
print('语文科目处理完成')
"

# 处理所有科目（使用百分比区间赋分）
python3 -c "
import calculate_scores_final_fix
result = calculate_scores_final_fix('path/to/your/file.xls', scoring_method='percentage')
print('所有科目处理完成')
"
```

## 📊 输出结果

系统会生成包含以下信息的Excel文件：

- **基本信息**：学校代码、学校名称、班别、科任教师
- **各考试指标**：平均分、优秀率、优良率、合格率、低分率
- **排名信息**：各指标的排名
- **赋分结果**：各指标的赋分
- **加权得分**：单次考试加权总分
- **综合得分**：最终综合排名得分

## 🐛 故障排除

### 常见问题

1. **文件上传失败**
   - 检查文件格式是否为.xls或.xlsx
   - 确保文件大小不超过16MB
   - 检查文件是否损坏

2. **列名识别失败**
   - 确保包含必需的列名（学校代码、学校名称、班别、科任）
   - 检查列名格式是否正确
   - 查看控制台输出的警告信息

3. **计算结果异常**
   - 检查数据是否完整
   - 确认考试名称格式是否正确
   - 查看错误日志获取详细信息

### 测试百分比区间功能

```bash
# 运行百分比区间功能测试
python3 test_percentage_scoring.py
```

### 调试模式

```bash
# 启用详细日志输出
python3 -c "
import logging
logging.basicConfig(level=logging.DEBUG)
import calculate_scores_final_fix
result = calculate_scores_final_fix('data/2025Mid3.xls')
"
```

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进项目。

### 开发环境设置

1. Fork项目
2. 创建功能分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -m 'Add some feature'`
4. 推送分支：`git push origin feature/your-feature`
5. 提交Pull Request

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 👥 作者

- **开发者**：kadeface
- **项目地址**：https://github.com/kadeface/valueaddforteacher

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者和用户。

---

**注意**：本项目仅供教育机构内部使用，请确保遵守相关数据保护法规。
