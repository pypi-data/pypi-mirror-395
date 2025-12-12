#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
报告管理模块
"""

import os
import json
import glob
import logging
import datetime
from pathlib import Path

logger = logging.getLogger("aptbox")

class ReportManager:
    """报告管理类"""
    
    def __init__(self, report_dir):
        """
        初始化报告管理器
        
        Args:
            report_dir: 报告存储目录
        """
        self.report_dir = report_dir
        
        # 确保报告目录存在
        os.makedirs(report_dir, exist_ok=True)
    
    def list_reports(self):
        """
        列出所有报告
        
        Returns:
            list: 报告信息列表
        """
        # 获取所有报告文件（支持 .json 和 .md 格式）
        json_files = glob.glob(os.path.join(self.report_dir, "*.json"))
        md_files = glob.glob(os.path.join(self.report_dir, "*.md"))
        report_files = json_files + md_files
        
        if not report_files:
            logger.warning(f"未找到任何报告文件，目录: {self.report_dir}")
            return []
        
        reports = []
        for file_path in report_files:
            try:
                # 检查文件是否存在
                if not os.path.exists(file_path):
                    logger.warning(f"报告文件不存在: {file_path}")
                    continue
                
                # 根据文件扩展名解析内容
                file_ext = os.path.splitext(file_path)[1].lower()
                if file_ext == ".json":
                    # 解析 JSON 文件
                    with open(file_path, 'r', encoding='utf-8') as f:
                        report_data = json.load(f)
                    
                    # 提取报告基本信息
                    report_info = {
                        "id": os.path.basename(file_path).replace(".json", ""),
                        "path": file_path,
                        "timestamp": report_data.get("timestamp", "未知"),
                        "title": report_data.get("title", "未知报告")
                    }
                elif file_ext == ".md":
                    # 解析 Markdown 文件（提取文件名中的时间戳作为 timestamp）
                    file_name = os.path.basename(file_path)
                    timestamp = "未知"
                    
                    # 尝试从文件名中提取时间戳（例如：apt_report_20250823_125700.md）
                    if "_" in file_name:
                        parts = file_name.split("_")
                        if len(parts) >= 3 and parts[-1].endswith(".md"):
                            timestamp = f"{parts[-2]} {parts[-1].replace('.md', '').replace('_', ':')}"
                    
                    report_info = {
                        "id": file_name.replace(".md", ""),
                        "path": file_path,
                        "timestamp": timestamp,
                        "title": "APT 更新报告"
                    }
                else:
                    logger.warning(f"不支持的文件格式: {file_path}")
                    continue
                
                reports.append(report_info)
            except json.JSONDecodeError as e:
                logger.error(f"报告文件格式错误: {file_path}, 错误: {str(e)}")
            except Exception as e:
                logger.error(f"读取报告文件失败: {file_path}, 错误: {str(e)}")
        
        # 按时间倒序排序
        reports.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        
        return reports
    
    def get_report(self, report_id, report_type="summary"):
        """
        获取指定报告的内容
        
        Args:
            report_id: 报告ID
            report_type: 报告类型，可选值: summary, detail, stats
            
        Returns:
            dict: 报告内容
        """
        # 构建报告文件路径（支持 .json 和 .md 格式）
        json_path = os.path.join(self.report_dir, f"{report_id}.json")
        md_path = os.path.join(self.report_dir, f"{report_id}.md")
        
        # 检查文件是否存在
        if os.path.exists(json_path):
            report_path = json_path
            file_ext = ".json"
        elif os.path.exists(md_path):
            report_path = md_path
            file_ext = ".md"
        else:
            logger.error(f"报告文件不存在: {json_path} 或 {md_path}")
            return None
        
        try:
            # 根据文件扩展名解析内容
            if file_ext == ".json":
                # 读取 JSON 文件
                with open(report_path, 'r', encoding='utf-8') as f:
                    report_data = json.load(f)
                
                # 根据报告类型返回不同内容
                if report_type == "summary":
                    # 返回摘要信息
                    return {
                        "title": report_data.get("title", "未知报告"),
                        "timestamp": report_data.get("timestamp", "未知"),
                        "summary": report_data.get("summary", {})
                    }
                elif report_type == "detail":
                    # 返回详细信息
                    return {
                        "title": report_data.get("title", "未知报告"),
                        "timestamp": report_data.get("timestamp", "未知"),
                        "summary": report_data.get("summary", {}),
                        "new_packages": report_data.get("new_packages", []),
                        "removed_packages": report_data.get("removed_packages", []),
                        "updated_packages": report_data.get("updated_packages", [])
                    }
                elif report_type == "stats":
                    # 返回统计信息
                    # 如果报告中没有统计信息，则动态生成
                    if "statistics" not in report_data:
                        statistics = self._generate_statistics(report_data)
                    else:
                        statistics = report_data.get("statistics", {})
                    
                    return {
                        "title": report_data.get("title", "未知报告"),
                        "timestamp": report_data.get("timestamp", "未知"),
                        "statistics": statistics
                    }
                else:
                    # 默认返回完整报告
                    return report_data
            
            elif file_ext == ".md":
                # 读取 Markdown 文件
                with open(report_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 解析 Markdown 内容
                report_data = {
                    "title": "APT 更新报告",
                    "timestamp": "未知",
                    "summary": {
                        "new_count": 0,
                        "removed_count": 0,
                        "updated_count": 0
                    },
                    "new_packages": [],
                    "removed_packages": [],
                    "updated_packages": []
                }
                
                # 提取时间戳（从文件名中）
                file_name = os.path.basename(report_path)
                if "_" in file_name:
                    parts = file_name.split("_")
                    if len(parts) >= 3 and parts[-1].endswith(".md"):
                        report_data["timestamp"] = f"{parts[-2]} {parts[-1].replace('.md', '').replace('_', ':')}"
                
                # 解析 Markdown 内容
                lines = content.split("\n")
                for line in lines:
                    if line.startswith("- 新增软件包:"):
                        report_data["summary"]["new_count"] = int(line.split(":")[1].strip())
                    elif line.startswith("- 删除软件包:"):
                        report_data["summary"]["removed_count"] = int(line.split(":")[1].strip())
                    elif line.startswith("- 更新软件包:"):
                        report_data["summary"]["updated_count"] = int(line.split(":")[1].strip())
                
                # 根据报告类型返回不同内容
                if report_type == "summary":
                    return {
                        "title": report_data["title"],
                        "timestamp": report_data["timestamp"],
                        "summary": report_data["summary"]
                    }
                elif report_type == "detail":
                    return {
                        "title": report_data["title"],
                        "timestamp": report_data["timestamp"],
                        "summary": report_data["summary"],
                        "new_packages": report_data["new_packages"],
                        "removed_packages": report_data["removed_packages"],
                        "updated_packages": report_data["updated_packages"]
                    }
                elif report_type == "stats":
                    return {
                        "title": report_data["title"],
                        "timestamp": report_data["timestamp"],
                        "statistics": {
                            "total_packages": report_data["summary"]["new_count"] + report_data["summary"]["removed_count"] + report_data["summary"]["updated_count"]
                        }
                    }
                else:
                    return report_data
            
        except Exception as e:
            logger.error(f"读取报告文件失败: {report_path}, 错误: {str(e)}")
            return None
    
    def query_reports(self, field=None, value=None):
        """
        查询报告
        
        Args:
            field: 查询字段
            value: 查询值
            
        Returns:
            list: 匹配的报告列表
        """
        # 获取所有报告
        all_reports = self.list_reports()
        
        # 如果没有指定查询条件，返回所有报告
        if not field or not value:
            return all_reports
        
        # 过滤报告
        filtered_reports = []
        for report in all_reports:
            # 如果是基本字段，直接比较
            if field in report and str(report[field]).lower() == str(value).lower():
                filtered_reports.append(report)
                continue
            
            # 如果是内容字段，需要读取报告内容
            report_content = self.get_report(report["id"], "detail")
            if not report_content:
                continue
            
            # 检查字段是否在报告内容中
            if self._check_field_in_report(report_content, field, value):
                filtered_reports.append(report)
        
        return filtered_reports
    
    def _check_field_in_report(self, report_content, field, value):
        """
        检查字段是否在报告内容中
        
        Args:
            report_content: 报告内容
            field: 字段名
            value: 字段值
            
        Returns:
            bool: 是否匹配
        """
        # 检查顶层字段
        if field in report_content and str(report_content[field]).lower() == str(value).lower():
            return True
        
        # 检查summary字段
        if "summary" in report_content and field in report_content["summary"]:
            if str(report_content["summary"][field]).lower() == str(value).lower():
                return True
        
        # 检查packages字段
        for pkg_type in ["new_packages", "removed_packages", "updated_packages"]:
            if pkg_type in report_content:
                for pkg in report_content[pkg_type]:
                    if field in pkg and str(pkg[field]).lower() == str(value).lower():
                        return True
        
        return False
    
    def _generate_statistics(self, report_data):
        """
        生成报告统计信息
        
        Args:
            report_data: 报告数据
            
        Returns:
            dict: 统计信息
        """
        statistics = {
            "total_packages": 0,
            "installed_packages": 0,
            "upgradable_packages": 0,
            "categories": {}
        }
        
        # 统计新增包
        for pkg in report_data.get("new_packages", []):
            statistics["total_packages"] += 1
            
            # 统计已安装包
            if pkg.get("status") == "installed":
                statistics["installed_packages"] += 1
            
            # 统计分类
            category = pkg.get("section", "未分类")
            if category not in statistics["categories"]:
                statistics["categories"][category] = 0
            statistics["categories"][category] += 1
        
        # 统计删除包
        for pkg in report_data.get("removed_packages", []):
            # 删除的包不计入总数
            pass
        
        # 统计更新包
        for pkg in report_data.get("updated_packages", []):
            statistics["total_packages"] += 1
            statistics["upgradable_packages"] += 1
            
            # 统计已安装包
            if pkg.get("status") == "installed":
                statistics["installed_packages"] += 1
            
            # 统计分类
            category = pkg.get("section", "未分类")
            if category not in statistics["categories"]:
                statistics["categories"][category] = 0
            statistics["categories"][category] += 1
        
        return statistics