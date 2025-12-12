# -*- coding: utf-8 -*-
"""
APT交互模块：负责执行apt update操作和获取软件包信息
"""

import subprocess
import logging
import re

logger = logging.getLogger(__name__)

class AptManager:
    """APT管理器，负责与APT交互"""
    
    def update_apt(self, dry_run=False):
        """
        执行apt update操作
        
        Args:
            dry_run: 是否模拟运行，不实际执行更新
            
        Returns:
            bool: 更新是否成功
        """
        if dry_run:
            logger.info("模拟运行模式，跳过apt update")
            return True
            
        try:
            logger.info("执行apt update...")
            result = subprocess.run(
                ["apt", "update"], 
                check=True,
                capture_output=True,
                text=True
            )
            logger.info("apt update执行成功")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"apt update执行失败: {e}")
            logger.error(f"错误输出: {e.stderr}")
            return False
    
    def get_package_list(self):
        """
        获取当前APT源中的软件包列表
        
        Returns:
            list: 软件包信息列表
        """
        logger.info("获取软件包列表...")
        
        # 获取可用的软件包信息
        available_pkgs = self._get_available_packages()
        
        # 获取已安装的软件包信息
        installed_pkgs = self._get_installed_packages()
        
        # 合并信息
        for pkg_name in installed_pkgs:
            if pkg_name in available_pkgs:
                available_pkgs[pkg_name]["status"] = "installed"
            
        # 转换为列表格式
        package_list = []
        for name, info in available_pkgs.items():
            package_list.append({
                "name": name,
                "version": info.get("version", ""),
                "architecture": info.get("architecture", ""),
                "description": info.get("description", ""),
                "status": info.get("status", "not-installed")
            })
            
        logger.info(f"共获取到 {len(package_list)} 个软件包信息")
        return package_list
    
    def _get_available_packages(self):
        """
        获取可用的软件包信息
        
        Returns:
            dict: 软件包信息字典，以包名为键
        """
        try:
            result = subprocess.run(
                ["apt-cache", "dumpavail"], 
                check=True,
                capture_output=True,
                text=True
            )
            return self._parse_package_info(result.stdout)
        except subprocess.CalledProcessError as e:
            logger.error(f"获取可用软件包信息失败: {e}")
            return {}
    
    def _get_installed_packages(self):
        """
        获取已安装的软件包信息
        
        Returns:
            dict: 已安装的软件包字典，以包名为键
        """
        try:
            result = subprocess.run(
                ["dpkg", "--get-selections"], 
                check=True,
                capture_output=True,
                text=True
            )
            installed = {}
            for line in result.stdout.splitlines():
                parts = line.strip().split()
                if len(parts) >= 2 and parts[1] == "install":
                    installed[parts[0]] = {"status": "installed"}
            return installed
        except subprocess.CalledProcessError as e:
            logger.error(f"获取已安装软件包信息失败: {e}")
            return {}
    
    def _parse_package_info(self, data):
        """
        解析软件包信息
        
        Args:
            data: apt-cache dumpavail的输出
            
        Returns:
            dict: 软件包信息字典，以包名为键
        """
        packages = {}
        current_pkg = None
        
        for line in data.splitlines():
            if not line.strip():
                current_pkg = None
                continue
                
            if line.startswith("Package: "):
                pkg_name = line[9:].strip()
                current_pkg = pkg_name
                packages[current_pkg] = {"name": current_pkg}
            elif current_pkg and ": " in line:
                key, value = line.split(": ", 1)
                key = key.strip().lower()
                value = value.strip()
                
                if key == "version":
                    packages[current_pkg]["version"] = value
                elif key == "architecture":
                    packages[current_pkg]["architecture"] = value
                elif key == "description":
                    packages[current_pkg]["description"] = value
                    
        return packages