# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

APT软件包快照与比较工具 - 用于跟踪和比较APT软件包更新的Python工具，可以在执行`apt update`前后生成软件包快照，并比较变化。

## 常用命令

### 安装和设置
```bash
# 从源码安装（开发模式）
pip install -e .

# 查看项目依赖
cat req.txt
```

### 运行和测试
```bash
# 基本使用（需要root权限）
sudo aptbox
sudo aptbox update

# 搜索功能
aptbox search python --limit 50 --status installed
aptbox search python3 --exact --output results.json

# 报告管理
aptbox report list
aptbox report show --id 20250823-120000 --type detail

# APT命令穿透（所有apt子命令都支持）
aptbox upgrade
aptbox install vim
aptbox remove nginx
aptbox list --installed
aptbox search python3
aptbox show curl
aptbox autoremove
aptbox full-upgrade

# 开发模式运行
python aptbox_cli.py
python -m aptbox.main
```

### 开发工具
```bash
# 直接运行模块
python -m aptbox.main --help
```

## 核心架构

### 模块结构
项目采用模块化设计，主要包含以下核心组件：

1. **快照管理模块** (`aptbox/snapshot/manager.py`)
   - `SnapshotManager`类：负责软件包快照的创建、加载和管理
   - 核心方法：`create_snapshot()`, `load_snapshot()`, `search_packages()`

2. **APT交互模块** (`aptbox/apt/manager.py`)
   - `AptManager`类：负责执行APT相关操作
   - 核心方法：`update_apt()`, `get_package_list()`

3. **快照比较模块** (`aptbox/compare/comparer.py`)
   - `SnapshotComparer`类：比较前后两次快照的差异
   - 核心方法：`compare_snapshots()`, 识别新增、删除、更新的软件包

4. **报告生成模块** (`aptbox/report/`)
   - `ReportGenerator`类：生成可读的变更报告
   - `ReportManager`类：管理和查询历史报告

### 数据流程
1. 检查是否存在上一次快照
2. 生成更新前快照（或使用现有快照）
3. 执行`apt update`操作
4. 生成更新后快照
5. 比较两次快照差异
6. 生成Markdown格式的变更报告

### 快照数据结构
快照以JSON格式存储，包含：
```json
{
  "timestamp": "2025-08-23T12:00:00",
  "packages": [
    {
      "name": "package-name",
      "version": "1.0.0",
      "architecture": "amd64",
      "description": "Package description",
      "status": "installed/not-installed",
      "installed_size": 1024
    }
  ]
}
```

## 配置文件

### 主配置文件
- 配置文件示例：`aptbox.conf.example`
- 默认快照目录：`/var/lib/aptbox/snapshots`
- 默认报告目录：`/var/lib/aptbox/reports`

### 支持的配置项
```ini
[paths]
snapshot_dir = /var/lib/aptbox/snapshots
report_dir = /var/lib/aptbox/reports

[behavior]
auto_cleanup = true
keep_snapshots = 5
```

## 主要功能特性

#### APT命令穿透功能
支持将所有不属于aptbox的子命令穿透到系统的apt命令，实现无缝集成：

**支持的apt子命令示例：**
- `aptbox install <package>` - 安装软件包
- `aptbox remove <package>` - 移除软件包
- `aptbox upgrade` - 升级系统
- `aptbox full-upgrade` - 完整升级
- `aptbox list --installed` - 列出已安装包
- `aptbox search <keyword>` - 搜索可用包
- `aptbox show <package>` - 显示包详情
- `aptbox autoremove` - 自动移除不需要的包
- 以及所有其他apt子命令

**穿透机制特点：**
- 完全保持原有apt命令的行为和参数
- 保持apt命令的退出码
- 显示穿透日志以便调试
- 支持所有apt命令的参数和选项

### 命令行接口
- `aptbox update`：执行更新和快照比较（aptbox核心功能）
- `aptbox search`：在快照中搜索软件包，支持多种过滤条件
- `aptbox report`：管理和查询历史报告
- `aptbox <apt-command>`：穿透到系统apt命令，支持所有apt子命令

### 搜索功能参数
- `--limit`：限制结果数量
- `--status`：按安装状态过滤
- `--exact`：精确匹配包名
- `--date`：按安装日期过滤
- `--size`：按包大小过滤
- `--sort`：结果排序方式

### 报告功能
- 支持多种报告类型：摘要、详细、统计
- 导出功能：JSON、CSV格式
- 报告查询和过滤功能

## 依赖项

- Python 3.6+
- packaging库
- 标准库：subprocess, json, datetime, difflib, argparse

## 开发注意事项

- 工具需要root权限执行`apt update`
- 支持临时目录模式（无root权限时使用）
- 快照文件使用时间戳命名便于管理
- 所有模块都配置了统一的日志记录器