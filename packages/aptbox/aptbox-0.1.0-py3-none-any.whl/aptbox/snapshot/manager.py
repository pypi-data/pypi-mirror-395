# -*- coding: utf-8 -*-
"""
快照管理模块：负责检查、创建和存储软件包快照
"""

import os
import sys
import json
import datetime
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class SnapshotManager:
    """软件包快照管理器"""
    
    def __init__(self, snapshot_dir="/var/lib/aptbox/snapshots"):
        """
        初始化快照管理器
        
        Args:
            snapshot_dir: 快照存储目录
        """
        self.snapshot_dir = Path(snapshot_dir)
        self._ensure_dir_exists()
    
    def _ensure_dir_exists(self):
        """确保快照目录存在"""
        try:
            os.makedirs(self.snapshot_dir, exist_ok=True)
        except PermissionError:
            logger.error(f"无权限创建目录: {self.snapshot_dir}")
            logger.error("请使用sudo运行或指定一个有写入权限的目录")
            sys.exit(1)
        
    def check_previous_snapshot(self):
        """
        检查是否存在上一次快照
        
        Returns:
            tuple: (是否存在, 快照路径)
        """
        snapshots = sorted(self.snapshot_dir.glob("*.json"), key=os.path.getmtime)
        if not snapshots:
            return False, None
        return True, snapshots[-1]
    
    def create_snapshot(self, package_data):
        """
        创建软件包快照
        
        Args:
            package_data: 软件包数据列表
            
        Returns:
            Path: 快照文件路径
        """
        timestamp = datetime.datetime.now().isoformat()
        snapshot_data = {
            "timestamp": timestamp,
            "packages": package_data
        }
        
        filename = f"snapshot_{timestamp.replace(':', '-')}.json"
        snapshot_path = self.snapshot_dir / filename
        
        self.save_snapshot(snapshot_data, snapshot_path)
        return snapshot_path
    
    def save_snapshot(self, data, path):
        """
        保存快照数据到文件
        
        Args:
            data: 快照数据
            path: 文件路径
        """
        try:
            with open(path, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f"快照已保存到: {path}")
        except PermissionError:
            logger.error(f"无权限写入文件: {path}")
            logger.error("请使用sudo运行或指定一个有写入权限的目录")
            sys.exit(1)
    
    def load_snapshot(self, path):
        """
        从文件加载快照数据
        
        Args:
            path: 快照文件路径
            
        Returns:
            dict: 快照数据
        """
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"快照文件不存在: {path}")
            sys.exit(1)
        except PermissionError:
            logger.error(f"无权限读取文件: {path}")
            logger.error("请使用sudo运行或指定一个有读取权限的目录")
            sys.exit(1)
        except json.JSONDecodeError:
            logger.error(f"快照文件格式错误: {path}")
            sys.exit(1)
            
    def get_latest_snapshot(self):
        """
        获取最新的快照文件
        
        Returns:
            tuple: (快照路径, 快照数据)
        """
        has_snapshot, snapshot_path = self.check_previous_snapshot()
        if not has_snapshot:
            logger.error("没有找到任何快照文件")
            sys.exit(1)
        
        snapshot_data = self.load_snapshot(snapshot_path)
        return snapshot_path, snapshot_data
        
    def search_packages(self, keyword, limit=20, status=None, exact_match=False, date_filter=None, size_filter=None, sort_by=None):
        """
        在最新的快照中搜索软件包
        
        Args:
            keyword: 搜索关键词
            limit: 最大返回结果数量，默认20
            status: 按状态过滤，可选值: installed, not-installed, 或 None(不过滤)
            exact_match: 是否精确匹配包名，默认为False(模糊匹配)
            date_filter: 按安装日期过滤，格式为"YYYY-MM-DD"或"YYYY-MM-DD:YYYY-MM-DD"(日期范围)
            size_filter: 按包大小过滤，格式为"min_size:max_size"(KB)，如"1024:5120"表示1MB到5MB
            sort_by: 排序字段，可选值: name, size, date，默认为name
            
        Returns:
            tuple: (匹配的软件包列表, 总匹配数)
        """
        _, snapshot_data = self.get_latest_snapshot()
        
        results = []
        keyword = keyword.lower()
        
        # 解析日期过滤器
        date_range = None
        if date_filter:
            import datetime
            try:
                if ":" in date_filter:
                    # 日期范围
                    start_date_str, end_date_str = date_filter.split(":")
                    start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
                    end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
                    date_range = (start_date, end_date)
                else:
                    # 单一日期
                    target_date = datetime.datetime.strptime(date_filter, "%Y-%m-%d").date()
                    date_range = (target_date, target_date)
            except ValueError:
                # 日期格式错误，忽略过滤
                pass
                
        # 解析大小过滤器
        size_range = None
        if size_filter:
            try:
                if ":" in size_filter:
                    # 大小范围
                    min_size_str, max_size_str = size_filter.split(":")
                    min_size = int(min_size_str) if min_size_str else 0
                    max_size = int(max_size_str) if max_size_str else float('inf')
                    size_range = (min_size, max_size)
                else:
                    # 单一大小（精确匹配）
                    target_size = int(size_filter)
                    size_range = (target_size, target_size)
            except ValueError:
                # 大小格式错误，忽略过滤
                pass
        
        for package in snapshot_data["packages"]:
            name = package["name"].lower()
            description = package.get("description", "").lower()
            
            # 状态过滤
            if status and package.get("status") != status:
                continue
            
            # 日期过滤
            if date_range and "install_date" in package:
                import datetime
                try:
                    install_date_str = package["install_date"]
                    install_date = datetime.datetime.strptime(install_date_str, "%Y-%m-%d").date()
                    
                    # 检查日期是否在范围内
                    if not (date_range[0] <= install_date <= date_range[1]):
                        continue
                except (ValueError, TypeError):
                    # 日期格式错误，跳过此包
                    continue
                    
            # 大小过滤
            if size_range:
                try:
                    # 安装大小通常以KB为单位
                    installed_size = int(package.get("installed_size", 0))
                    
                    # 检查大小是否在范围内
                    if not (size_range[0] <= installed_size <= size_range[1]):
                        continue
                except (ValueError, TypeError):
                    # 大小格式错误，跳过此包
                    if size_range[0] > 0:  # 如果有最小值限制，没有大小信息的包跳过
                        continue
                
            # 精确匹配或模糊匹配
            if exact_match:
                if name == keyword:
                    results.append(package)
            else:
                if keyword in name or keyword in description:
                    results.append(package)
        
        total_matches = len(results)
        
        # 根据排序字段对结果进行排序
        if sort_by == "size":
            # 按大小排序（从大到小）
            results.sort(key=lambda x: int(x.get("installed_size", 0)), reverse=True)
            sorted_results = results
        elif sort_by == "date":
            # 按安装日期排序（从新到旧）
            def get_date(pkg):
                try:
                    import datetime
                    date_str = pkg.get("install_date", "1970-01-01")
                    return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                except (ValueError, TypeError):
                    import datetime
                    return datetime.datetime.strptime("1970-01-01", "%Y-%m-%d").date()
            
            results.sort(key=get_date, reverse=True)
            sorted_results = results
        else:
            # 默认按名称排序，优先返回名称中包含关键词的包
            if not exact_match:
                name_matches = [p for p in results if keyword in p["name"].lower()]
                desc_matches = [p for p in results if keyword not in p["name"].lower()]
                
                # 按名称排序
                name_matches.sort(key=lambda x: x["name"])
                desc_matches.sort(key=lambda x: x["name"])
                
                # 合并结果并限制数量
                sorted_results = name_matches + desc_matches
            else:
                # 精确匹配时直接排序
                sorted_results = sorted(results, key=lambda x: x["name"])
            
        limited_results = sorted_results[:limit]
                
        return limited_results, total_matches