# -*- coding: utf-8 -*-
"""
报告生成模块：负责生成可读的变更报告
"""

import os
import sys
import datetime
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class ReportGenerator:
    """报告生成器，负责生成可读的变更报告"""
    
    def __init__(self, report_dir="/var/lib/aptbox/reports"):
        """
        初始化报告生成器
        
        Args:
            report_dir: 报告存储目录
        """
        self.report_dir = Path(report_dir)
        self._ensure_dir_exists()
    
    def _ensure_dir_exists(self):
        """确保报告目录存在"""
        try:
            os.makedirs(self.report_dir, exist_ok=True)
        except PermissionError:
            logger.error(f"无权限创建目录: {self.report_dir}")
            logger.error("请使用sudo运行或指定一个有写入权限的目录")
            sys.exit(1)
    
    def generate_report(self, comparison_result):
        """
        根据比较结果生成报告
        
        Args:
            comparison_result: 快照比较结果
            
        Returns:
            tuple: (报告内容, 报告文件路径)
        """
        logger.info("生成变更报告...")
        
        # 获取时间信息
        before_time = self._format_timestamp(comparison_result["before_timestamp"])
        after_time = self._format_timestamp(comparison_result["after_timestamp"])
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 生成报告内容
        report = []
        report.append("# APT软件包变更报告")
        report.append(f"生成时间: {current_time}")
        report.append("")
        
        # 添加摘要信息
        summary = comparison_result["summary"]
        report.append("## 摘要")
        report.append(f"- 更新前软件包总数: {summary['total_before']}")
        report.append(f"- 更新后软件包总数: {summary['total_after']}")
        report.append(f"- 新增软件包: {summary['new_count']}")
        report.append(f"- 删除软件包: {summary['removed_count']}")
        report.append(f"- 更新软件包: {summary['updated_count']}")
        report.append("")
        
        # 添加时间信息
        report.append("## 时间信息")
        report.append(f"- 更新前快照时间: {before_time}")
        report.append(f"- 更新后快照时间: {after_time}")
        report.append(f"- 报告生成时间: {current_time}")
        report.append("")
        
        # 添加更新的软件包信息
        if comparison_result["updated_packages"]:
            report.append("## 更新的软件包")
            for pkg in comparison_result["updated_packages"]:
                name = pkg["name"]
                old_ver = pkg["before"]["version"]
                new_ver = pkg["after"]["version"]
                report.append(f"- {name}: {old_ver} -> {new_ver}")
            report.append("")
        
        # 添加新增的软件包信息
        if comparison_result["new_packages"]:
            report.append("## 新增的软件包")
            for pkg in comparison_result["new_packages"]:
                name = pkg["name"]
                ver = pkg["version"]
                report.append(f"- {name}: {ver}")
            report.append("")
        
        # 添加删除的软件包信息
        if comparison_result["removed_packages"]:
            report.append("## 删除的软件包")
            for pkg in comparison_result["removed_packages"]:
                name = pkg["name"]
                ver = pkg["version"]
                report.append(f"- {name}: {ver}")
            report.append("")
        
        # 生成报告文件
        report_content = "\n".join(report)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"apt_report_{timestamp}.md"
        report_path = self.report_dir / report_filename
        
        self.save_report(report_content, report_path)
        
        return report_content, report_path
    
    def save_report(self, report, path):
        """
        将报告保存到文件
        
        Args:
            report: 报告内容
            path: 文件路径
        """
        try:
            with open(path, 'w') as f:
                f.write(report)
            logger.info(f"报告已保存到: {path}")
        except PermissionError:
            logger.error(f"无权限写入文件: {path}")
            logger.error("请使用sudo运行或指定一个有写入权限的目录")
            sys.exit(1)
    
    def _format_timestamp(self, timestamp):
        """
        格式化时间戳
        
        Args:
            timestamp: ISO格式的时间戳
            
        Returns:
            str: 格式化后的时间字符串
        """
        try:
            dt = datetime.datetime.fromisoformat(timestamp)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            return timestamp