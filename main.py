# Feishu Bitable Automation
# 入口文件

import argparse
from src.feishu_client import FeishuBitableClient
from src.data_processor import DataProcessor
from src.scheduler import TaskScheduler


def cmd_sync(args):
    """单次执行数据同步"""
    print("开始数据同步...")

    # 1. 拉取数据
    client = FeishuBitableClient()
    records = client.list_records()
    print(f"拉取到 {len(records)} 条记录")

    # 2. 清洗 + 分析
    processor = DataProcessor()
    df = processor.process(records)

    # 3. 生成报告
    report_path = processor.generate_report()

    # 输出结果
    stats = processor.get_stats()
    print(f"\n处理完成：")
    print(f"  - 填充空值：{stats['empty_filled']} 处")
    print(f"  - 去除重复：{stats['duplicates_removed']} 条")
    print(f"  - 检测异常：{stats['outliers_detected']} 条")
    print(f"\n报告已生成: {report_path}")
    print("同步完成")


def cmd_schedule(args):
    """启动定时任务"""
    print(f"启动定时任务，间隔 {args.interval} 秒")
    sched = TaskScheduler()
    sched.add_sync_job(cmd_sync, args.interval)
    sched.start()


def main():
    parser = argparse.ArgumentParser(description="Feishu Bitable Automation")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    subparsers.add_parser("sync", help="单次执行数据同步")

    schedule_parser = subparsers.add_parser("schedule", help="启动定时任务")
    schedule_parser.add_argument("--interval", type=int, default=3600, help="执行间隔（秒）")

    args = parser.parse_args()

    if args.command == "sync":
        cmd_sync(args)
    elif args.command == "schedule":
        cmd_schedule(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
