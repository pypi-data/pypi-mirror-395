# APT软件包快照与比较工具设计文档

## 1. 项目概述

### 1.1 项目背景
APT (Advanced Package Tool) 是Debian和Ubuntu等Linux发行版使用的包管理系统。在系统维护过程中，管理员需要了解每次`apt update`操作带来的变化，包括新增、删除和更新的软件包信息。本工具旨在自动化这一过程，提供清晰的变更报告。

### 1.2 项目目标
开发一个工具，能够：
1. 在执行`apt update`前后生成软件包快照
2. 比较两次快照的差异
3. 生成详细的变更报告
4. 支持使用已有快照以避免重复生成

## 2. 系统设计

### 2.1 整体架构
系统将采用模块化设计，主要包含以下组件：
- 快照管理模块：负责检查、创建和存储软件包快照
- APT交互模块：负责执行apt update操作
- 快照比较模块：负责分析两次快照的差异
- 报告生成模块：负责生成可读的变更报告

### 2.2 数据流程
1. 检查是否存在上一次快照
2. 如存在且未强制生成，则使用上一次快照作为更新前的快照
3. 如不存在或强制生成，则生成当前状态快照
4. 执行apt update操作
5. 生成更新后的快照
6. 比较两次快照
7. 生成变更报告

### 2.3 数据结构
快照文件将采用JSON格式存储，包含以下信息：
```json
{
  "timestamp": "2025-08-23T12:00:00",
  "packages": [
    {
      "name": "package-name",
      "version": "1.0.0",
      "architecture": "amd64",
      "description": "Package description",
      "status": "installed/not-installed"
    },
    ...
  ]
}
```

## 3. 模块设计

### 3.1 快照管理模块
- **功能**：检查、创建和管理软件包快照
- **主要方法**：
  - `check_previous_snapshot()`: 检查是否存在上一次快照
  - `create_snapshot()`: 解析当前APT源中的软件包信息并生成快照
  - `save_snapshot(data, path)`: 将快照数据保存到指定路径

### 3.2 APT交互模块
- **功能**：执行APT相关操作
- **主要方法**：
  - `update_apt()`: 执行apt update操作
  - `get_package_list()`: 获取当前APT源中的软件包列表

### 3.3 快照比较模块
- **功能**：比较两次快照的差异
- **主要方法**：
  - `compare_snapshots(before, after)`: 比较前后两次快照
  - `identify_new_packages(before, after)`: 识别新增的软件包
  - `identify_removed_packages(before, after)`: 识别删除的软件包
  - `identify_updated_packages(before, after)`: 识别更新的软件包

### 3.4 报告生成模块
- **功能**：生成可读的变更报告
- **主要方法**：
  - `generate_report(comparison_result)`: 根据比较结果生成报告
  - `save_report(report, path)`: 将报告保存到指定路径

## 4. 实现细节

### 4.1 软件包信息获取
将使用`apt-cache dump`和`apt-cache dumpavail`命令获取当前APT源中的软件包信息。

### 4.2 快照存储
快照将存储在预定义的目录中，文件名包含时间戳以便区分。

### 4.3 比较算法
比较两次快照时，将：
1. 使用软件包名称作为唯一标识符
2. 比较版本号以确定更新情况
3. 检查是否有新增或删除的软件包

### 4.4 报告格式
报告将包含以下部分：
1. 摘要信息（总更新数量、新增数量、删除数量）
2. 详细列表（按类别分组的软件包变更）
3. 时间信息（执行时间、生成时间）

## 5. 技术选型

### 5.1 开发语言
选择Python作为主要开发语言，原因如下：
- 强大的文本处理能力
- 丰富的系统交互库
- 跨平台兼容性
- 简洁的语法，便于维护

### 5.2 依赖库
- `subprocess`: 执行系统命令
- `json`: 处理JSON格式数据
- `datetime`: 处理时间相关操作
- `difflib`: 辅助比较文本差异
- `argparse`: 处理命令行参数

## 6. 接口设计

### 6.1 命令行接口
```
aptbox [update] [options]
  --snapshot-dir DIR    指定快照存储目录
  --report-dir DIR      指定报告存储目录
  --force               强制生成快照，即使存在上一次快照
  --dry-run             模拟运行，不执行apt update
  --verbose             显示详细输出
  --temp-dir            使用临时目录存储快照和报告（适用于无root权限的情况）
  --help                显示帮助信息

aptbox search keyword [options]
  --limit 数量          限制显示结果的数量，默认为20
  --status 状态         按安装状态过滤，可选值: installed, not-installed
  --exact               精确匹配包名（默认为模糊匹配）
  --output, -o 文件路径 将搜索结果导出到指定的JSON文件
  --date, -d 日期       按安装日期过滤，格式为'YYYY-MM-DD'或'YYYY-MM-DD:YYYY-MM-DD'(日期范围)
  --size, -s 大小       按包大小过滤(KB)，格式为'min_size:max_size'，如'1024:5120'表示1MB到5MB
  --sort 排序方式       结果排序方式，可选值: name, size, date，默认为name

aptbox report action [options]
  action                报告操作，可选值: list(列出所有报告), show(显示指定报告), query(查询报告)
  --id 报告ID           报告ID（用于show操作）
  --type 报告类型       报告类型，可选值: summary(摘要), detail(详细), stats(统计)，默认为summary
  --filter 过滤条件     报告过滤条件，格式为"字段:值"，如"category:系统工具"
  --output, -o 文件路径 将报告导出到指定的文件，支持JSON和CSV格式
```

### 6.2 配置文件
支持通过配置文件设置默认参数：
``ini
[paths]
snapshot_dir = /var/lib/aptbox/snapshots
report_dir = /var/lib/aptbox/reports

[behavior]
auto_cleanup = true
keep_snapshots = 5
```

## 7. 测试策略

### 7.1 单元测试
为每个模块编写单元测试，确保各功能正常工作。

### 7.2 集成测试
测试整个工作流程，确保各模块协同工作正常。

### 7.3 测试场景
1. 首次运行（无上一次快照）
2. 有上一次快照的情况
3. 强制生成快照
4. 无网络连接情况
5. APT源无变化情况

## 8. 部署与使用

### 8.1 安装方法
```
# 通过pip安装
pip install aptbox

# 或从源码安装
git clone https://github.com/username/aptbox.git
cd aptbox
python setup.py install
```

### 8.2 使用示例
```
# 基本使用
sudo aptbox

# 指定快照目录
sudo aptbox --snapshot-dir /path/to/snapshots

# 强制生成快照
sudo aptbox --force
```

## 9. 项目规划

### 9.1 开发阶段
1. **阶段一**：核心功能实现（快照生成、比较）
2. **阶段二**：报告生成优化
3. **阶段三**：用户界面改进
4. **阶段四**：性能优化

### 9.2 未来扩展
1. 图形用户界面
2. 定时自动检查更新
3. 与系统通知集成
4. 支持其他包管理系统（如yum、dnf）

## 10. 总结

本设计文档概述了APT软件包快照与比较工具的设计和实现方案。该工具将帮助系统管理员更好地了解和管理APT更新带来的变化，提高系统维护效率。通过模块化设计和清晰的接口，该工具具有良好的可扩展性和可维护性。