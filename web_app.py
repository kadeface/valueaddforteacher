from flask import Flask, render_template, request, jsonify, send_file
import os
import pandas as pd
import numpy as np
from werkzeug.utils import secure_filename
import tempfile
import zipfile
from calculate_scores_final_fix import calculate_scores_final_fix
import threading
import time

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

# 确保上传和输出目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# 全局变量存储处理状态
processing_status = {
    'is_processing': False,
    'progress': 0,
    'message': '',
    'error': None,
    'output_files': []
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': '没有选择文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    
    if not file.filename.endswith(('.xls', '.xlsx')):
        return jsonify({'error': '只支持Excel文件(.xls, .xlsx)'}), 400
    
    # 保存上传的文件
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    return jsonify({'success': True, 'filename': filename, 'filepath': filepath})

@app.route('/process', methods=['POST'])
def process_file():
    global processing_status
    
    if processing_status['is_processing']:
        return jsonify({'error': '正在处理中，请稍候'}), 400
    
    data = request.get_json()
    filepath = data.get('filepath')
    subject = data.get('subject', '')  # 空字符串表示处理所有科目
    education_level = data.get('education_level', 'middle')  # 教育阶段，默认初中
    
    if not filepath or not os.path.exists(filepath):
        return jsonify({'error': '文件不存在'}), 400
    
    # 开始处理
    processing_status['is_processing'] = True
    processing_status['progress'] = 0
    processing_status['message'] = '开始处理...'
    processing_status['error'] = None
    processing_status['output_files'] = []
    
    # 在新线程中处理文件
    thread = threading.Thread(target=process_file_thread, args=(filepath, subject, education_level))
    thread.daemon = True
    thread.start()
    
    return jsonify({'success': True, 'message': '开始处理文件'})

def process_file_thread(filepath, subject, education_level):
    global processing_status
    
    try:
        processing_status['message'] = '正在读取Excel文件...'
        processing_status['progress'] = 10
        
        # 调用计算函数
        if subject:
            # 处理单个科目
            processing_status['message'] = f'正在处理科目: {subject}...'
            processing_status['progress'] = 30
            
            result_df = calculate_scores_final_fix(filepath, subject, education_level)
            if result_df is not None:
                output_filename = f"{subject}_计算结果.xlsx"
                output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
                result_df.to_excel(output_path, index=False)
                processing_status['output_files'].append(output_path)
                processing_status['message'] = f'科目 {subject} 处理完成'
                processing_status['progress'] = 100
            else:
                processing_status['error'] = f'科目 {subject} 处理失败'
        else:
            # 处理所有科目
            processing_status['message'] = '正在处理所有科目...'
            processing_status['progress'] = 30
            
            # 读取Excel文件获取所有sheet名称
            excel_file = pd.ExcelFile(filepath)
            subject_sheets = [sheet for sheet in excel_file.sheet_names 
                            if sheet not in ['sheet1', 'Sheet1', '汇总', '总览']]
            
            total_subjects = len(subject_sheets)
            processed_count = 0
            
            for i, subject_name in enumerate(subject_sheets):
                processing_status['message'] = f'正在处理科目: {subject_name} ({i+1}/{total_subjects})...'
                processing_status['progress'] = 30 + int(50 * (i / total_subjects))
                
                result_df = calculate_scores_final_fix(filepath, subject_name, education_level)
                if result_df is not None:
                    output_filename = f"{subject_name}_计算结果.xlsx"
                    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
                    result_df.to_excel(output_path, index=False)
                    processing_status['output_files'].append(output_path)
                    processed_count += 1
                
                time.sleep(0.1)  # 让用户看到进度
            
            processing_status['message'] = f'所有科目处理完成，共处理 {processed_count} 个科目'
            processing_status['progress'] = 100
        
    except Exception as e:
        processing_status['error'] = f'处理过程中出现错误: {str(e)}'
        processing_status['progress'] = 0
    
    finally:
        processing_status['is_processing'] = False

@app.route('/status')
def get_status():
    return jsonify(processing_status)

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({'error': '文件不存在'}), 404

@app.route('/download_all')
def download_all():
    if not processing_status['output_files']:
        return jsonify({'error': '没有可下载的文件'}), 400
    
    # 创建ZIP文件
    zip_path = os.path.join(app.config['OUTPUT_FOLDER'], '所有计算结果.zip')
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file_path in processing_status['output_files']:
            if os.path.exists(file_path):
                zipf.write(file_path, os.path.basename(file_path))
    
    return send_file(zip_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
