# -*- coding: utf-8 -*-
"""
快照比较模块：负责分析两次快照的差异
"""

import logging
from packaging import version

logger = logging.getLogger(__name__)

class SnapshotComparer:
    """快照比较器，负责比较两次快照的差异"""
    
    def compare_snapshots(self, before_snapshot, after_snapshot):
        """
        比较前后两次快照
        
        Args:
            before_snapshot: 更新前的快照数据
            after_snapshot: 更新后的快照数据
            
        Returns:
            dict: 比较结果
        """
        logger.info("比较快照差异...")
        
        # 转换包列表为字典，以包名为键
        before_pkgs = {pkg["name"]: pkg for pkg in before_snapshot["packages"]}
        after_pkgs = {pkg["name"]: pkg for pkg in after_snapshot["packages"]}
        
        # 识别新增、删除和更新的软件包
        new_packages = self.identify_new_packages(before_pkgs, after_pkgs)
        removed_packages = self.identify_removed_packages(before_pkgs, after_pkgs)
        updated_packages = self.identify_updated_packages(before_pkgs, after_pkgs)
        
        # 生成比较结果
        comparison_result = {
            "before_timestamp": before_snapshot["timestamp"],
            "after_timestamp": after_snapshot["timestamp"],
            "new_packages": new_packages,
            "removed_packages": removed_packages,
            "updated_packages": updated_packages,
            "summary": {
                "total_before": len(before_snapshot["packages"]),
                "total_after": len(after_snapshot["packages"]),
                "new_count": len(new_packages),
                "removed_count": len(removed_packages),
                "updated_count": len(updated_packages)
            }
        }
        
        logger.info(f"比较完成: 新增 {len(new_packages)}, 删除 {len(removed_packages)}, 更新 {len(updated_packages)}")
        return comparison_result
    
    def identify_new_packages(self, before_pkgs, after_pkgs):
        """
        识别新增的软件包
        
        Args:
            before_pkgs: 更新前的软件包字典
            after_pkgs: 更新后的软件包字典
            
        Returns:
            list: 新增的软件包列表
        """
        new_pkgs = []
        for pkg_name, pkg_info in after_pkgs.items():
            if pkg_name not in before_pkgs:
                new_pkgs.append(pkg_info)
        return new_pkgs
    
    def identify_removed_packages(self, before_pkgs, after_pkgs):
        """
        识别删除的软件包
        
        Args:
            before_pkgs: 更新前的软件包字典
            after_pkgs: 更新后的软件包字典
            
        Returns:
            list: 删除的软件包列表
        """
        removed_pkgs = []
        for pkg_name, pkg_info in before_pkgs.items():
            if pkg_name not in after_pkgs:
                removed_pkgs.append(pkg_info)
        return removed_pkgs
    
    def identify_updated_packages(self, before_pkgs, after_pkgs):
        """
        识别更新的软件包
        
        Args:
            before_pkgs: 更新前的软件包字典
            after_pkgs: 更新后的软件包字典
            
        Returns:
            list: 更新的软件包列表，每项包含更新前后的信息
        """
        updated_pkgs = []
        
        for pkg_name, after_info in after_pkgs.items():
            if pkg_name in before_pkgs:
                before_info = before_pkgs[pkg_name]
                
                # 如果版本不同，则认为是更新
                if before_info["version"] != after_info["version"]:
                    try:
                        # 尝试比较版本号
                        ver_before = version.parse(before_info["version"])
                        ver_after = version.parse(after_info["version"])
                        
                        # 只有当新版本号大于旧版本号时才视为更新
                        if ver_after > ver_before:
                            updated_pkgs.append({
                                "name": pkg_name,
                                "before": before_info,
                                "after": after_info
                            })
                    except Exception:
                        # 如果版本号解析失败，直接比较字符串
                        updated_pkgs.append({
                            "name": pkg_name,
                            "before": before_info,
                            "after": after_info
                        })
        
        return updated_pkgs