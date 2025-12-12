#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
APT软件包快照与比较工具主程序
"""

import os
import sys
import logging
import argparse
import tempfile
from pathlib import Path

from aptbox.snapshot.manager import SnapshotManager
from aptbox.apt.manager import AptManager
from aptbox.compare.comparer import SnapshotComparer
from aptbox.report.generator import ReportGenerator

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("aptbox")

def parse_args():
    """解析命令行参数"""
    import sys
    
    # 检查是否是apt穿透模式
    if len(sys.argv) > 1 and sys.argv[1] not in ['update', 'search', 'report', 'completion', '--help', '-h', '--snapshot-dir', '--report-dir', '--verbose', '--temp-dir']:
        # 这是一个apt穿透命令
        class AptPassthroughArgs:
            def __init__(self, command, apt_command, apt_args):
                self.command = command
                self.apt_command = apt_command  
                self.apt_args = apt_args
                self.verbose = '--verbose' in sys.argv or '-v' in sys.argv
                self.temp_dir = '--temp-dir' in sys.argv
                self.snapshot_dir = '/var/lib/aptbox/snapshots/'
                self.report_dir = '/var/lib/aptbox/reports/'
        
        return AptPassthroughArgs('apt_passthrough', sys.argv[1], sys.argv[2:])
    
    parser = argparse.ArgumentParser(
        description="APT软件包快照与比较工具"
    )
    
    # 创建子命令解析器
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # 定义添加全局选项的函数
    def add_global_options(parser):
        parser.add_argument(
            "--snapshot-dir",
            default="/var/lib/aptbox/snapshots/",
            help="指定快照存储目录"
        )
        parser.add_argument(
            "--report-dir",
            default="/var/lib/aptbox/reports/",
            help="指定报告存储目录"
        )
        parser.add_argument(
            "--verbose",
            action="store_true",
            help="显示详细输出"
        )
        parser.add_argument(
            "--temp-dir",
            action="store_true",
            help="使用临时目录存储快照和报告（适用于无root权限的情况）"
        )
    
    # 添加全局选项到主解析器
    add_global_options(parser)
    
    # update 子命令
    update_parser = subparsers.add_parser("update", help="执行apt update并生成快照报告")
    add_global_options(update_parser)
    update_parser.add_argument(
        "--force",
        action="store_true",
        help="强制生成快照，即使存在上一次快照"
    )
    update_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="模拟运行，不执行apt update"
    )
    
    # search 子命令
    search_parser = subparsers.add_parser("search", help="在最近的快照中搜索软件包")
    add_global_options(search_parser)
    search_parser.add_argument(
        "keyword",
        help="搜索关键词"
    )
    search_parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="最大显示结果数量，默认为20"
    )
    search_parser.add_argument(
        "--status",
        choices=["installed", "not-installed"],
        help="按安装状态过滤"
    )
    search_parser.add_argument(
        "--exact",
        action="store_true",
        help="精确匹配包名（默认为模糊匹配）"
    )
    search_parser.add_argument(
        "--output", "-o",
        help="将搜索结果导出到指定的JSON文件"
    )
    search_parser.add_argument(
        "--date", "-d",
        help="按安装日期过滤，格式为'YYYY-MM-DD'或'YYYY-MM-DD:YYYY-MM-DD'(日期范围)"
    )
    search_parser.add_argument(
        "--size", "-s",
        help="按包大小过滤(KB)，格式为'min_size:max_size'，如'1024:5120'表示1MB到5MB"
    )
    search_parser.add_argument(
        "--sort",
        choices=["name", "size", "date"],
        default="name",
        help="结果排序方式，可选值: name, size, date，默认为name"
    )
    
    # report 子命令
    report_parser = subparsers.add_parser("report", help="管理软件包报告")
    add_global_options(report_parser)
    report_parser.add_argument("action", choices=["list", "show", "query"], help="报告操作")
    report_parser.add_argument("--id", help="报告ID（用于show操作）")
    report_parser.add_argument("--type", choices=["summary", "detail", "stats"], default="summary", 
                              help="报告类型，可选值: summary(摘要), detail(详细), stats(统计)，默认为summary")
    report_parser.add_argument("--filter", help="报告过滤条件，格式为'字段:值'，如'category:系统工具'")
    report_parser.add_argument("--output", "-o", help="将报告导出到指定的文件，支持JSON和CSV格式")

    # completion 子命令
    completion_parser = subparsers.add_parser("completion", help="配置Tab键自动补全功能")
    add_global_options(completion_parser)
    completion_parser.add_argument(
        "action",
        choices=["install", "uninstall", "status"],
        help="补全操作: install(安装), uninstall(卸载), status(查看状态)"
    )
    completion_parser.add_argument(
        "--shell",
        choices=["bash", "zsh"],
        default="bash",
        help="指定shell类型，默认为bash"
    )

    # 解析参数
    args = parser.parse_args()
    
    # 如果没有指定子命令，默认为update
    if args.command is None:
        args.command = "update"
        args.force = False
        args.dry_run = False
    
    return args

def update_command(args, snapshot_dir, report_dir):
    """执行update子命令"""
    # 初始化各模块
    snapshot_manager = SnapshotManager(snapshot_dir)
    apt_manager = AptManager()
    snapshot_comparer = SnapshotComparer()
    report_generator = ReportGenerator(report_dir)
    
    # 检查是否存在上一次快照
    has_previous, previous_path = snapshot_manager.check_previous_snapshot()
    
    if has_previous and not args.force:
        logger.info(f"发现上一次快照: {previous_path}，将使用它作为更新前的快照")
        before_snapshot_path = previous_path
    else:
        # 生成更新前的快照
        logger.info("生成更新前的快照...")
        before_packages = apt_manager.get_package_list()
        before_snapshot_path = snapshot_manager.create_snapshot(before_packages)
        logger.info(f"更新前快照已保存: {before_snapshot_path}")
    
    # 执行apt update
    logger.info("执行apt update...")
    update_success = apt_manager.update_apt(args.dry_run)
    if not update_success:
        logger.error("apt update执行失败，退出程序")
        sys.exit(1)
    
    # 生成更新后的快照
    logger.info("生成更新后的快照...")
    after_packages = apt_manager.get_package_list()
    after_snapshot_path = snapshot_manager.create_snapshot(after_packages)
    logger.info(f"更新后快照已保存: {after_snapshot_path}")
    
    # 加载快照数据
    before_snapshot = snapshot_manager.load_snapshot(before_snapshot_path)
    after_snapshot = snapshot_manager.load_snapshot(after_snapshot_path)
    
    # 比较快照
    logger.info("比较快照差异...")
    comparison_result = snapshot_comparer.compare_snapshots(before_snapshot, after_snapshot)
    
    # 生成报告
    logger.info("生成变更报告...")
    report_content, report_path = report_generator.generate_report(comparison_result)
    
    # 输出报告路径
    logger.info(f"变更报告已生成: {report_path}")
    
    # 输出摘要
    summary = comparison_result["summary"]
    print("\n=== APT软件包变更摘要 ===")
    print(f"新增软件包: {summary['new_count']}")
    print(f"删除软件包: {summary['removed_count']}")
    print(f"更新软件包: {summary['updated_count']}")
    print(f"详细报告: {report_path}")

def apt_passthrough_command(args):
    """穿透到系统apt命令"""
    import subprocess
    import sys
    
    # 构建apt命令
    apt_cmd = ["apt", args.apt_command] + args.apt_args
    
    logger.info(f"穿透到系统apt命令: {' '.join(apt_cmd)}")
    
    try:
        # 执行apt命令，保持原有的退出码
        # 使用STDERR重定向来抑制apt的警告信息，但保留输出
        result = subprocess.run(apt_cmd, check=False)
        sys.exit(result.returncode)
    except FileNotFoundError:
        logger.error("未找到apt命令，请确保系统已安装APT包管理器")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("用户中断操作")
        sys.exit(130)
    except Exception as e:
        logger.error(f"执行apt命令时发生错误: {e}")
        sys.exit(1)

def report_command(args, report_dir):
    """执行report子命令"""
    from aptbox.report.manager import ReportManager
    
    # 初始化报告管理器
    report_manager = ReportManager(report_dir)
    
    # 根据操作类型执行相应的功能
    if args.action == "list":
        # 列出所有报告
        reports = report_manager.list_reports()
        
        if not reports:
            print("没有找到任何报告")
            return
            
        print(f"\n=== 报告列表 ({len(reports)} 个) ===")
        for idx, report in enumerate(reports, 1):
            # 格式化报告信息
            report_id = report.get("id", "未知")
            timestamp = report.get("timestamp", "未知")
            title = report.get("title", "未知")
            
            # 显示报告摘要信息
            print(f"{idx}. ID: {report_id}")
            print(f"   标题: {title}")
            print(f"   时间: {timestamp}")
            print(f"   路径: {report.get('path', '未知')}")
            print()
            
    elif args.action == "show":
        # 显示指定报告
        if not args.id:
            print("错误: 显示报告需要指定 --id 参数")
            return
            
        # 获取报告内容
        report_content = report_manager.get_report(args.id, args.type)
        
        if not report_content:
            print(f"未找到ID为 {args.id} 的报告")
            return
            
        # 显示报告内容
        print(f"\n=== 报告详情 (ID: {args.id}, 类型: {args.type}) ===")
        
        # 根据报告类型格式化输出
        if args.type == "summary":
            # 显示摘要信息
            print(f"标题: {report_content.get('title', '未知')}")
            print(f"时间: {report_content.get('timestamp', '未知')}")
            print(f"变更摘要:")
            summary = report_content.get("summary", {})
            print(f"  - 新增软件包: {summary.get('new_count', 0)}")
            print(f"  - 删除软件包: {summary.get('removed_count', 0)}")
            print(f"  - 更新软件包: {summary.get('updated_count', 0)}")
            
        elif args.type == "detail":
            # 显示详细信息
            print(f"标题: {report_content.get('title', '未知')}")
            print(f"时间: {report_content.get('timestamp', '未知')}")
            
            # 显示新增软件包
            new_packages = report_content.get("new_packages", [])
            if new_packages:
                print(f"\n新增软件包 ({len(new_packages)}):")
                for pkg in new_packages[:10]:  # 只显示前10个
                    print(f"  - {pkg.get('name', '未知')} ({pkg.get('version', '未知')})")
                if len(new_packages) > 10:
                    print(f"    ... 还有 {len(new_packages) - 10} 个未显示")
            
            # 显示删除软件包
            removed_packages = report_content.get("removed_packages", [])
            if removed_packages:
                print(f"\n删除软件包 ({len(removed_packages)}):")
                for pkg in removed_packages[:10]:
                    print(f"  - {pkg.get('name', '未知')} ({pkg.get('version', '未知')})")
                if len(removed_packages) > 10:
                    print(f"    ... 还有 {len(removed_packages) - 10} 个未显示")
            
            # 显示更新软件包
            updated_packages = report_content.get("updated_packages", [])
            if updated_packages:
                print(f"\n更新软件包 ({len(updated_packages)}):")
                for pkg in updated_packages[:10]:
                    old_ver = pkg.get("old_version", "未知")
                    new_ver = pkg.get("new_version", "未知")
                    print(f"  - {pkg.get('name', '未知')}: {old_ver} -> {new_ver}")
                if len(updated_packages) > 10:
                    print(f"    ... 还有 {len(updated_packages) - 10} 个未显示")
                    
        elif args.type == "stats":
            # 显示统计信息
            print(f"标题: {report_content.get('title', '未知')}")
            print(f"时间: {report_content.get('timestamp', '未知')}")
            
            stats = report_content.get("statistics", {})
            print("\n软件包统计:")
            print(f"  - 总软件包数: {stats.get('total_packages', 0)}")
            print(f"  - 已安装软件包: {stats.get('installed_packages', 0)}")
            print(f"  - 可升级软件包: {stats.get('upgradable_packages', 0)}")
            
            # 显示分类统计
            categories = stats.get("categories", {})
            if categories:
                print("\n软件包分类统计:")
                for category, count in categories.items():
                    print(f"  - {category}: {count}")
        
        # 导出报告
        if args.output:
            try:
                # 根据文件扩展名决定导出格式
                if args.output.lower().endswith('.json'):
                    # 导出为JSON
                    import json
                    with open(args.output, 'w', encoding='utf-8') as f:
                        json.dump(report_content, f, ensure_ascii=False, indent=2)
                elif args.output.lower().endswith('.csv'):
                    # 导出为CSV
                    import csv
                    with open(args.output, 'w', newline='', encoding='utf-8') as f:
                        # 根据报告类型决定CSV结构
                        if args.type == "summary":
                            writer = csv.writer(f)
                            writer.writerow(['标题', '时间', '新增包数', '删除包数', '更新包数'])
                            summary = report_content.get("summary", {})
                            writer.writerow([
                                report_content.get('title', ''),
                                report_content.get('timestamp', ''),
                                summary.get('new_count', 0),
                                summary.get('removed_count', 0),
                                summary.get('updated_count', 0)
                            ])
                        elif args.type == "detail":
                            # 导出详细信息需要多个表格，这里简化处理
                            writer = csv.writer(f)
                            # 导出新增包
                            writer.writerow(['类型', '包名', '版本'])
                            for pkg in report_content.get("new_packages", []):
                                writer.writerow(['新增', pkg.get('name', ''), pkg.get('version', '')])
                            for pkg in report_content.get("removed_packages", []):
                                writer.writerow(['删除', pkg.get('name', ''), pkg.get('version', '')])
                            for pkg in report_content.get("updated_packages", []):
                                writer.writerow(['更新', pkg.get('name', ''), 
                                               f"{pkg.get('old_version', '')} -> {pkg.get('new_version', '')}"]) 
                else:
                    # 默认导出为文本
                    with open(args.output, 'w', encoding='utf-8') as f:
                        f.write(f"=== 报告详情 (ID: {args.id}, 类型: {args.type}) ===\n")
                        f.write(f"标题: {report_content.get('title', '未知')}\n")
                        f.write(f"时间: {report_content.get('timestamp', '未知')}\n")
                        # 根据报告类型写入不同内容
                        # 此处省略详细实现...
                
                print(f"\n报告已导出到: {args.output}")
            except Exception as e:
                logger.error(f"导出报告失败: {str(e)}")
                
    elif args.action == "query":
        # 查询报告
        filter_condition = args.filter
        
        # 解析过滤条件
        filter_field = None
        filter_value = None
        if filter_condition:
            try:
                filter_field, filter_value = filter_condition.split(':', 1)
            except ValueError:
                print("错误: 过滤条件格式不正确，应为'字段:值'")
                return
        
        # 执行查询
        query_results = report_manager.query_reports(filter_field, filter_value)
        
        if not query_results:
            print("未找到匹配的报告")
            return
            
        print(f"\n=== 查询结果 ({len(query_results)} 个) ===")
        for idx, report in enumerate(query_results, 1):
            print(f"{idx}. ID: {report.get('id', '未知')}")
            print(f"   标题: {report.get('title', '未知')}")
            print(f"   时间: {report.get('timestamp', '未知')}")
            
            # 显示匹配的字段
            if filter_field and filter_field in report:
                print(f"   匹配: {filter_field} = {report.get(filter_field, '未知')}")
            
            print()
        
        # 导出查询结果
        if args.output:
            try:
                if args.output.lower().endswith('.json'):
                    # 导出为JSON
                    import json
                    with open(args.output, 'w', encoding='utf-8') as f:
                        json.dump(query_results, f, ensure_ascii=False, indent=2)
                elif args.output.lower().endswith('.csv'):
                    # 导出为CSV
                    import csv
                    with open(args.output, 'w', newline='', encoding='utf-8') as f:
                        # 获取所有可能的字段
                        fields = set()
                        for report in query_results:
                            fields.update(report.keys())
                        
                        # 写入CSV
                        writer = csv.DictWriter(f, fieldnames=sorted(fields))
                        writer.writeheader()
                        for report in query_results:
                            writer.writerow(report)
                else:
                    # 默认导出为文本
                    with open(args.output, 'w', encoding='utf-8') as f:
                        f.write(f"=== 查询结果 ({len(query_results)} 个) ===\n")
                        for idx, report in enumerate(query_results, 1):
                            f.write(f"{idx}. ID: {report.get('id', '未知')}\n")
                            f.write(f"   标题: {report.get('title', '未知')}\n")
                            f.write(f"   时间: {report.get('timestamp', '未知')}\n")
                            f.write("\n")
                
                print(f"\n查询结果已导出到: {args.output}")
            except Exception as e:
                logger.error(f"导出查询结果失败: {str(e)}")

def completion_command(args):
    """执行completion子命令"""
    import shutil
    import os

    completion_dir = "/etc/bash_completion.d"
    completion_file = f"{completion_dir}/aptbox"

    # 获取脚本所在目录的completion文件路径
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source_file = os.path.join(script_dir, "..", "completion", "aptbox-completion.bash")

    if args.action == "install":
        # 安装补全功能
        try:
            # 检查是否有root权限
            if os.geteuid() != 0:
                print("⚠️  安装系统级补全需要root权限，尝试安装到用户目录...")
                # 用户级安装
                user_completion_dir = os.path.expanduser("~/.local/share/bash-completion/completions")
                user_completion_file = f"{user_completion_dir}/aptbox"

                # 创建目录
                os.makedirs(user_completion_dir, exist_ok=True)

                # 查找源文件
                possible_paths = [
                    os.path.join(script_dir, "completion", "aptbox-completion.bash"),
                    "/usr/local/lib/python*/dist-packages/aptbox/completion/aptbox-completion.bash",
                    "/usr/lib/python*/dist-packages/aptbox/completion/aptbox-completion.bash"
                ]

                source_found = False
                for path in possible_paths:
                    found_files = []
                    if "*" in path:
                        # 使用glob处理通配符
                        import glob
                        found_files = glob.glob(path)
                    else:
                        if os.path.exists(path):
                            found_files = [path]

                    if found_files:
                        source_file = found_files[0]
                        source_found = True
                        break

                if not source_found:
                    # 尝试使用包内相对路径
                    import aptbox
                    package_dir = os.path.dirname(aptbox.__file__)
                    source_file = os.path.join(package_dir, "..", "completion", "aptbox-completion.bash")
                    if not os.path.exists(source_file):
                        print("❌ 无法找到补全脚本文件")
                        return

                # 复制文件
                shutil.copy2(source_file, user_completion_file)
                print(f"✅ 补全功能已安装到用户目录: {user_completion_file}")
                print("💡 请运行以下命令使补全生效：")
                print("   source ~/.bashrc")
                print("   或者重新打开终端")

            else:
                # 系统级安装
                # 创建补全目录
                os.makedirs(completion_dir, exist_ok=True)

                # 查找源文件
                possible_paths = [
                    "/usr/local/lib/python*/dist-packages/aptbox/completion/aptbox-completion.bash",
                    "/usr/lib/python*/dist-packages/aptbox/completion/aptbox-completion.bash",
                    os.path.join(script_dir, "completion", "aptbox-completion.bash")
                ]

                source_found = False
                for path in possible_paths:
                    found_files = []
                    if "*" in path:
                        import glob
                        found_files = glob.glob(path)
                    else:
                        if os.path.exists(path):
                            found_files = [path]

                    if found_files:
                        source_file = found_files[0]
                        source_found = True
                        break

                if not source_found:
                    print("❌ 无法找到补全脚本文件")
                    return

                # 复制文件
                shutil.copy2(source_file, completion_file)
                print(f"✅ 补全功能已安装到系统目录: {completion_file}")
                print("💡 请运行以下命令使补全生效：")
                print("   source ~/.bashrc")
                print("   或者重新打开终端")

        except Exception as e:
            print(f"❌ 安装失败: {str(e)}")

    elif args.action == "uninstall":
        # 卸载补全功能
        try:
            if os.path.exists(completion_file):
                if os.geteuid() != 0:
                    print("⚠️  卸载系统级补全需要root权限")
                    # 尝试删除用户级安装
                    user_completion_file = os.path.expanduser("~/.local/share/bash-completion/completions/aptbox")
                    if os.path.exists(user_completion_file):
                        os.remove(user_completion_file)
                        print(f"✅ 用户级补全功能已卸载: {user_completion_file}")
                    else:
                        print("ℹ️  未找到用户级补全文件")
                else:
                    os.remove(completion_file)
                    print(f"✅ 系统级补全功能已卸载: {completion_file}")
            else:
                # 检查用户级安装
                user_completion_file = os.path.expanduser("~/.local/share/bash-completion/completions/aptbox")
                if os.path.exists(user_completion_file):
                    os.remove(user_completion_file)
                    print(f"✅ 用户级补全功能已卸载: {user_completion_file}")
                else:
                    print("ℹ️  未找到已安装的补全文件")

        except Exception as e:
            print(f"❌ 卸载失败: {str(e)}")

    elif args.action == "status":
        # 查看补全状态
        print("🔍 检查aptbox补全功能状态...")

        system_installed = os.path.exists(completion_file)
        user_completion_file = os.path.expanduser("~/.local/share/bash-completion/completions/aptbox")
        user_installed = os.path.exists(user_completion_file)

        if system_installed:
            print(f"✅ 系统级补全已安装: {completion_file}")
        if user_installed:
            print(f"✅ 用户级补全已安装: {user_completion_file}")

        if not system_installed and not user_installed:
            print("❌ 未检测到补全功能安装")
            print("💡 运行 'aptbox completion install' 来安装补全功能")
        else:
            print("💡 补全功能应该已经生效，如果未生效请运行:")
            print("   source ~/.bashrc")
            print("   或者重新打开终端")

def search_command(args, snapshot_dir):
    """执行search子命令"""
    snapshot_manager = SnapshotManager(snapshot_dir)
    
    # 获取搜索参数
    limit = args.limit
    status = args.status
    exact_match = args.exact
    output_file = args.output
    date_filter = args.date
    size_filter = args.size
    sort_by = args.sort if hasattr(args, 'sort') else "name"
    
    # 构建搜索条件描述
    search_desc = f"关键词: {args.keyword}"
    if status:
        search_desc += f", 状态: {status}"
    if exact_match:
        search_desc += ", 精确匹配"
    if date_filter:
        search_desc += f", 安装日期: {date_filter}"
    if size_filter:
        search_desc += f", 大小(KB): {size_filter}"
    if sort_by and sort_by != "name":
        search_desc += f", 排序: {sort_by}"
    
    logger.info(f"在最近的快照中搜索 - {search_desc}")
    results, total_matches = snapshot_manager.search_packages(
        args.keyword, limit, status, exact_match, date_filter, size_filter, sort_by
    )
    
    if not results:
        print(f"未找到匹配条件的软件包")
        return
    
    # 输出搜索结果
    print(f"\n=== 搜索结果: {total_matches} 个匹配项 (显示前 {len(results)} 个) ===")
    print(f"搜索条件: {search_desc}")
    
    # 格式化输出
    for package in results:
        print(f"\n包名: {package['name']}")
        print(f"版本: {package.get('version', '未知')}")
        
        # 根据状态使用不同颜色
        status = package.get('status', '未知')
        if status == 'installed':
            status_str = f"状态: \033[92m{status}\033[0m"  # 绿色
        else:
            status_str = f"状态: {status}"
        print(status_str)
        
        # 格式化显示包大小
        if 'installed_size' in package:
            try:
                size_kb = int(package['installed_size'])
                if size_kb < 1024:
                    size_str = f"{size_kb} KB"
                elif size_kb < 1024 * 1024:
                    size_str = f"{size_kb/1024:.2f} MB"
                else:
                    size_str = f"{size_kb/(1024*1024):.2f} GB"
                print(f"大小: {size_str}")
            except (ValueError, TypeError):
                pass
        
        # 显示安装日期
        if 'install_date' in package:
            print(f"安装日期: {package.get('install_date', '未知')}")
        
        if 'description' in package:
            print(f"描述: {package['description']}")
    
    if total_matches > limit:
        print(f"\n注意: 还有 {total_matches - limit} 个匹配项未显示。使用 --limit 参数增加显示数量。")
    
    # 导出结果到文件
    if output_file:
        try:
            import json
            import datetime
            
            # 准备导出数据
            export_data = {
                "search_criteria": {
                    "keyword": args.keyword,
                    "status": status,
                    "exact_match": exact_match
                },
                "timestamp": datetime.datetime.now().isoformat(),
                "total_matches": total_matches,
                "results": [
                    # 转换为可序列化的字典
                    {k: v for k, v in pkg.items() if not callable(v)}
                    for pkg in results
                ]
            }
            
            # 写入文件
            with open(output_file, 'w', encoding='utf-8') as f:
                # 确保JSON格式正确
                import json
                # 先转换为标准Python对象
                clean_data = {
                    "search_criteria": {
                        "keyword": args.keyword,
                        "status": status if status else None,
                        "exact_match": exact_match
                    },
                    "timestamp": datetime.datetime.now().isoformat(),
                    "total_matches": total_matches,
                    "results": []
                }
                
                # 手动处理结果列表，确保所有值都是可序列化的
                for pkg in results:
                    clean_pkg = {}
                    for k, v in pkg.items():
                        if isinstance(v, (str, int, float, bool, type(None))):
                            clean_pkg[k] = v
                        else:
                            clean_pkg[k] = str(v)
                    clean_data["results"].append(clean_pkg)
                
                # 写入JSON
                json.dump(clean_data, f, ensure_ascii=False, indent=2)
                
            print(f"\n搜索结果已导出到: {output_file}")
        except Exception as e:
            logger.error(f"导出结果失败: {str(e)}")

def main():
    """主程序入口"""
    args = parse_args()
    
    # 设置日志级别
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # 处理apt穿透命令（不需要目录设置）
    if args.command == "apt_passthrough":
        apt_passthrough_command(args)
        return
    
    # 如果使用临时目录或者是dry-run模式，则使用临时目录
    if args.temp_dir or (hasattr(args, 'dry_run') and args.dry_run):
        import tempfile
        temp_snapshot_dir = tempfile.mkdtemp(prefix="aptbox_snapshot_")
        temp_report_dir = tempfile.mkdtemp(prefix="aptbox_report_")
        logger.info(f"使用临时目录存储快照: {temp_snapshot_dir}")
        logger.info(f"使用临时目录存储报告: {temp_report_dir}")
        snapshot_dir = temp_snapshot_dir
        report_dir = temp_report_dir
    else:
        snapshot_dir = args.snapshot_dir
        report_dir = args.report_dir
    
    # 创建必要的目录
    os.makedirs(snapshot_dir, exist_ok=True)
    os.makedirs(report_dir, exist_ok=True)
    
    # 根据子命令执行相应的功能
    if args.command == "update":
        update_command(args, snapshot_dir, report_dir)
    elif args.command == "search":
        search_command(args, snapshot_dir)
    elif args.command == "report":
        report_command(args, report_dir)
    elif args.command == "completion":
        completion_command(args)

if __name__ == "__main__":
    main()