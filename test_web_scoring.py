#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Web应用赋分方式选择功能
"""

import requests
import json
import time
import os

def test_web_scoring_methods():
    """测试Web应用的赋分方式选择功能"""
    
    base_url = "http://localhost:8080"
    
    print("=" * 60)
    print("测试Web应用赋分方式选择功能")
    print("=" * 60)
    
    # 测试文件路径
    test_file = 'data/2025Mid3.xls'
    
    if not os.path.exists(test_file):
        print(f"❌ 测试文件不存在: {test_file}")
        return
    
    print(f"测试文件: {test_file}")
    print()
    
    # 1. 测试固定区间赋分
    print("1. 测试固定区间赋分...")
    try:
        # 上传文件
        with open(test_file, 'rb') as f:
            files = {'file': f}
            upload_response = requests.post(f"{base_url}/upload", files=files)
        
        if upload_response.status_code == 200:
            upload_result = upload_response.json()
            filepath = upload_result['filepath']
            
            # 处理文件（固定区间赋分）
            process_data = {
                'filepath': filepath,
                'subject': '语文',
                'scoring_method': 'fixed'
            }
            
            process_response = requests.post(
                f"{base_url}/process", 
                json=process_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if process_response.status_code == 200:
                print("✅ 固定区间赋分请求成功")
                
                # 等待处理完成
                for i in range(30):  # 最多等待30秒
                    status_response = requests.get(f"{base_url}/status")
                    status = status_response.json()
                    
                    if status.get('error'):
                        print(f"❌ 处理错误: {status['error']}")
                        break
                    elif not status.get('is_processing') and status.get('progress') == 100:
                        print("✅ 固定区间赋分处理完成")
                        print(f"   输出文件数: {len(status.get('output_files', []))}")
                        break
                    
                    time.sleep(1)
                else:
                    print("❌ 处理超时")
            else:
                print(f"❌ 处理请求失败: {process_response.status_code}")
        else:
            print(f"❌ 文件上传失败: {upload_response.status_code}")
            
    except Exception as e:
        print(f"❌ 固定区间赋分测试出错: {e}")
    
    print()
    
    # 2. 测试百分比区间赋分
    print("2. 测试百分比区间赋分...")
    try:
        # 上传文件
        with open(test_file, 'rb') as f:
            files = {'file': f}
            upload_response = requests.post(f"{base_url}/upload", files=files)
        
        if upload_response.status_code == 200:
            upload_result = upload_response.json()
            filepath = upload_result['filepath']
            
            # 处理文件（百分比区间赋分）
            process_data = {
                'filepath': filepath,
                'subject': '语文',
                'scoring_method': 'percentage'
            }
            
            process_response = requests.post(
                f"{base_url}/process", 
                json=process_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if process_response.status_code == 200:
                print("✅ 百分比区间赋分请求成功")
                
                # 等待处理完成
                for i in range(30):  # 最多等待30秒
                    status_response = requests.get(f"{base_url}/status")
                    status = status_response.json()
                    
                    if status.get('error'):
                        print(f"❌ 处理错误: {status['error']}")
                        break
                    elif not status.get('is_processing') and status.get('progress') == 100:
                        print("✅ 百分比区间赋分处理完成")
                        print(f"   输出文件数: {len(status.get('output_files', []))}")
                        break
                    
                    time.sleep(1)
                else:
                    print("❌ 处理超时")
            else:
                print(f"❌ 处理请求失败: {process_response.status_code}")
        else:
            print(f"❌ 文件上传失败: {upload_response.status_code}")
            
    except Exception as e:
        print(f"❌ 百分比区间赋分测试出错: {e}")
    
    print()
    print("=" * 60)
    print("测试完成")
    print("=" * 60)

def test_invalid_scoring_method():
    """测试无效的赋分方式"""
    
    base_url = "http://localhost:8080"
    
    print("3. 测试无效赋分方式...")
    
    try:
        # 上传文件
        test_file = 'data/2025Mid3.xls'
        with open(test_file, 'rb') as f:
            files = {'file': f}
            upload_response = requests.post(f"{base_url}/upload", files=files)
        
        if upload_response.status_code == 200:
            upload_result = upload_response.json()
            filepath = upload_result['filepath']
            
            # 使用无效的赋分方式
            process_data = {
                'filepath': filepath,
                'subject': '语文',
                'scoring_method': 'invalid_method'
            }
            
            process_response = requests.post(
                f"{base_url}/process", 
                json=process_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if process_response.status_code == 400:
                print("✅ 无效赋分方式被正确拒绝")
                error_data = process_response.json()
                print(f"   错误信息: {error_data.get('error', '未知错误')}")
            else:
                print(f"❌ 应该拒绝无效赋分方式，但返回状态码: {process_response.status_code}")
                
    except Exception as e:
        print(f"❌ 测试无效赋分方式出错: {e}")

if __name__ == "__main__":
    # 测试有效赋分方式
    test_web_scoring_methods()
    
    # 测试无效赋分方式
    test_invalid_scoring_method()
