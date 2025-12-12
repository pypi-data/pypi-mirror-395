# aptbox

<div align="center">

![aptbox Logo](https://img.shields.io/badge/aptbox-v0.1.0-blue.svg)
[![Python Version](https://img.shields.io/badge/python-3.6+-brightgreen.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()

**🔧 智能APT软件包快照与比较工具**

一个功能强大的APT包管理系统增强工具，支持软件包更新追踪、快照比较，以及无缝的APT命令穿透。

[GitHub](https://github.com/fengyucn/aptbox) | [PyPI](https://pypi.org/project/aptbox/) | [文档](#文档) | [安装](#安装) | [使用](#使用方法)

</div>

## ✨ 主要特性

### 🎯 APT命令穿透（核心亮点）
- **完全兼容**: 支持所有APT子命令，无需学习新语法
- **无缝集成**: `aptbox install <package>` 完全等同于 `apt install <package>`
- **保持原味**: 完全保留原APT命令的行为、参数和退出码
- **智能识别**: 自动区分aptbox特有命令和APT穿透命令

### 📸 快照管理
- **智能快照**: 自动在`apt update`前后生成软件包状态快照
- **增量比较**: 只在有变化时生成新快照，节省存储空间
- **历史追踪**: 完整记录系统软件包的变更历史

### 🔍 强大搜索
- **多维搜索**: 支持按名称、描述、状态、日期、大小等多维度搜索
- **灵活过滤**: 精确匹配、模糊匹配、范围过滤等多种搜索方式
- **结果导出**: 支持JSON、CSV格式导出搜索结果

### 📊 报告系统
- **详细报告**: 生成包含新增、删除、更新软件包的完整报告
- **多种格式**: 支持摘要、详细、统计等多种报告类型
- **数据导出**: 可将报告导出为JSON或CSV格式

### ⚡ Tab键自动补全
- **智能补全**: 支持所有子命令和参数的Tab键自动补全
- **APT穿透补全**: 完美支持APT命令的参数和包名补全
- **自动安装**: 一键安装补全脚本，提升命令行效率

## 🚀 快速开始

### 安装

#### 通过PyPI安装（推荐）
```bash
pip install aptbox
```

#### 从源码安装
```bash
git clone https://github.com/fengyucn/aptbox.git
cd aptbox
pip install -e .
```

#### 配置Tab键自动补全
```bash
# 安装补全功能（推荐）
aptbox completion install

# 检查补全状态
aptbox completion status

# 如果需要卸载补全功能
aptbox completion uninstall
```

安装完成后，重启终端或运行 `source ~/.bashrc` 使补全生效。

### 基本使用

#### 1. APT命令穿透 - 无缝替换apt
```bash
# 完全等同于 apt 命令，无需改变使用习惯
sudo aptbox update
sudo aptbox upgrade
sudo aptbox install vim
sudo aptbox remove nginx
sudo aptbox search python3
sudo aptbox show curl
sudo aptbox autoremove
sudo aptbox full-upgrade
```

#### 2. 快照和比较功能
```bash
# 基本用法：执行update并生成变化报告
sudo aptbox

# 强制生成新快照
sudo aptbox update --force

# 模拟运行（不实际执行apt update）
sudo aptbox update --dry-run

# 显示详细输出
sudo aptbox --verbose
```

#### 3. 搜索功能
```bash
# 搜索包含"python"的软件包
aptbox search python

# 精确搜索
aptbox search python3 --exact

# 按状态过滤
aptbox search python --status installed

# 按大小搜索（大于10MB）
aptbox search "" --size 10240:

# 按日期范围搜索
aptbox search "" --date 2025-07-01:2025-08-01

# 导出搜索结果
aptbox search python --output results.json
```

#### 4. 报告管理
```bash
# 列出所有报告
aptbox report list

# 显示详细报告
aptbox report show --id 20250823-120000 --type detail

# 导出报告
aptbox report show --id 20250823-120000 --output report.json
```

## 📖 详细文档

### APT穿透命令支持

aptbox支持所有标准的APT子命令：

| 命令分类 | 支持的子命令 | 示例 |
|---------|-------------|------|
| **包管理** | `install`, `remove`, `purge` | `aptbox install vim` |
| **系统更新** | `update`, `upgrade`, `full-upgrade` | `aptbox upgrade` |
| **信息查询** | `search`, `show`, `list`, `info` | `aptbox search python` |
| **系统维护** | `autoremove`, `autoclean`, `clean` | `aptbox autoremove` |
| **源管理** | `sources`, `edit-sources` | `aptbox sources` |
| **其他** | 所有其他apt子命令 | `aptbox <any-apt-command>` |

### 搜索参数详解

```bash
aptbox search <关键词> [选项]
```

**参数说明：**
- `关键词`: 搜索关键词（支持包名和描述搜索）
- `--limit N`: 限制结果数量（默认20）
- `--status STATUS`: 按状态过滤（installed/not-installed）
- `--exact`: 精确匹配包名
- `--date DATE`: 按日期过滤（`YYYY-MM-DD`或`YYYY-MM-DD:YYYY-MM-DD`）
- `--size SIZE`: 按大小过滤（KB格式：`min:max`）
- `--sort SORT`: 排序方式（name/size/date）
- `--output FILE`: 导出结果到文件

### 报告系统

**报告类型：**
- `summary`: 摘要信息（默认）
- `detail`: 详细变更列表
- `stats`: 统计信息

**查询过滤：**
- 按软件包名：`--filter "package:python3"`
- 按日期：`--filter "date:2025-08-23"`
- 按类别：`--filter "category:系统工具"`

## 🛠️ 高级配置

### 配置文件

创建 `~/.aptbox.conf`：

```ini
[paths]
snapshot_dir = /var/lib/aptbox/snapshots
report_dir = /var/lib/aptbox/reports

[behavior]
auto_cleanup = true
keep_snapshots = 10
```

### 环境变量

```bash
export APTBOX_SNAPSHOT_DIR="/custom/snapshots"
export APTBOX_REPORT_DIR="/custom/reports"
export APTBOX_TEMP_DIR="true"
```

## 📁 项目结构

```
aptbox/
├── aptbox/                 # 主要代码包
│   ├── main.py            # 命令行入口
│   ├── snapshot/          # 快照管理模块
│   ├── apt/               # APT交互模块
│   ├── compare/           # 快照比较模块
│   └── report/            # 报告生成模块
├── tests/                 # 测试文件
├── docs/                  # 文档
├── setup.py              # 安装配置
├── pyproject.toml        # 现代Python打包配置
├── README.md             # 项目说明
├── LICENSE               # 许可证

## 🔧 高级功能

### Tab键自动补全详解

aptbox支持智能的Tab键自动补全，极大提升命令行使用效率：

#### 安装补全功能
```bash
# 查看当前补全状态
aptbox completion status

# 安装补全功能（需要root权限或自动降级到用户安装）
aptbox completion install

# 卸载补全功能
aptbox completion uninstall
```

#### 补全功能示例

**1. 主命令补全**
```bash
$ aptbox [Tab][Tab]
report      search      update      completion
```

**2. 子命令选项补全**
```bash
$ aptbox update --[Tab][Tab]
--force        --dry-run      --help         --report-dir    --snapshot-dir  --temp-dir      --verbose

$ aptbox search --[Tab][Tab]
--date       --exact      --help       --limit      --output     --report-dir --search-dir --size       --sort       --status     --verbose
```

**3. 参数值补全**
```bash
$ aptbox search --status [Tab][Tab]
installed      not-installed

$ aptbox report --type [Tab][Tab]
detail      stats       summary

$ aptbox report [Tab][Tab]
list        query       show
```

**4. APT穿透命令补全**
```bash
$ aptbox install [Tab][Tab]
python3         python3-pip     git             vim             curl
docker.io       nginx           mysql-server    postgresql

$ aptbox install python3-[Tab][Tab]
python3-pip      python3-venv     python3-dev      python3-full
```

**5. 文件路径补全**
```bash
$ aptbox search python --output [Tab][Tab]
# 自动补全文件路径

$ aptbox report --output [Tab][Tab]
# 自动补全文件路径
```

#### 补全功能特性

- ✅ **智能识别**: 自动区分aptbox原生命令和APT穿透命令
- ✅ **完整覆盖**: 支持所有aptbox子命令和参数
- ✅ **APT兼容**: 完美支持所有APT命令和参数补全
- ✅ **动态提示**: 根据上下文提供智能的补全建议
- ✅ **包名建议**: 提供常用软件包名的快速补全

安装后重启终端即可享受Tab补全带来的便捷体验！

### 贡献
└── CLAUDE.md             # AI助手指导文档
```

## 🔧 系统要求

- **操作系统**: Linux (Debian/Ubuntu及衍生发行版)
- **Python版本**: 3.6+
- **权限要求**:
  - 快照功能：需要用户权限
  - APT穿透命令：需要root权限（同apt命令）
- **依赖包**: `packaging`

## 🤝 贡献指南

我们欢迎所有形式的贡献！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 开发环境设置

```bash
git clone https://github.com/fengyucn/aptbox.git
cd aptbox
pip install -e ".[dev]"  # 安装开发依赖
```

## 📋 更新日志

### v0.1.0 (2025-01-01)
- ✨ 新增APT命令穿透功能
- 📸 实现软件包快照管理
- 🔍 添加强大搜索功能
- 📊 完善报告系统
- 🛠️ 完整的命令行界面

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE)。

## 🙏 致谢

- 感谢 [APT](https://wiki.debian.org/Apt) 项目提供的强大包管理基础
- 感谢所有贡献者和用户的支持

## 📞 联系方式


- **GitHub**: [fengyucn](https://github.com/fengyucn)
- **问题反馈**: [Issues](https://github.com/fengyucn/aptbox/issues)

---

<div align="center">

**⭐ 如果这个项目对您有帮助，请给我们一个星标！**

[🔝 回到顶部](#aptbox)

</div>
