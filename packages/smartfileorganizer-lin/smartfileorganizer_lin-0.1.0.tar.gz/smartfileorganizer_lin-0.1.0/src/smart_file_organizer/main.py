"""
主程序入口
智能文件整理工具的命令行接口
"""

import sys
import os
import argparse
from pathlib import Path
from typing import Optional
from smart_file_organizer.utils import organize_downloads, setup_logging


def expand_user_path(path: str) -> Path:
    """
    展开用户路径（如 ~/Downloads）
    
    Args:
        path: 路径字符串
        
    Returns:
        展开后的 Path 对象
        
    Example:
        >>> expand_user_path("~/Downloads")
        Path('/Users/username/Downloads')
    """
    return Path(path).expanduser()


def main() -> None:
    """
    主函数 - 命令行入口点
    
    使用 argparse 解析命令行参数，调用 organize_downloads 函数进行文件整理。
    包含详细的错误处理和日志记录。
    """
    parser = argparse.ArgumentParser(
        prog="smart-file-organizer",
        description="Smart File Organizer - 智能文件整理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                              # 整理默认目录 (~/Downloads)
  %(prog)s --source ~/Documents         # 整理指定目录
  %(prog)s --source ~/Downloads --dry-run  # 试运行模式
        """
    )
    
    parser.add_argument(
        "--source",
        type=str,
        default="~/Downloads",
        help="源目录路径（默认: ~/Downloads）"
    )
    
    parser.add_argument(
        "--target",
        type=str,
        default=None,
        dest="target_dir",
        help="目标目录路径（可选，默认为源目录）"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        dest="dry_run",
        help="模拟运行模式，不实际移动文件，仅显示将要执行的操作"
    )
    
    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        dest="log_level",
        help="日志级别（默认: INFO）"
    )
    
    args = parser.parse_args()
    
    # 设置日志级别映射（使用字典字面量，Python 3.10+ 特性）
    log_level_map: dict[str, int] = {
        "DEBUG": 10,
        "INFO": 20,
        "WARNING": 30,
        "ERROR": 40
    }
    
    # 初始化日志系统
    logger = setup_logging(log_level=log_level_map[args.log_level])
    logger.info("=" * 60)
    logger.info("Smart File Organizer 启动")
    logger.info("=" * 60)
    
    # 展开并验证源目录
    try:
        source_path = expand_user_path(args.source)
        logger.debug(f"源目录路径（展开前）: {args.source}")
        logger.debug(f"源目录路径（展开后）: {source_path}")
    except Exception as e:
        logger.error(f"无法展开源目录路径 '{args.source}': {str(e)}", exc_info=True)
        sys.exit(1)
    
    if not source_path.exists():
        error_msg = f"源目录不存在: {source_path}"
        logger.error(error_msg)
        print(f"错误: {error_msg}", file=sys.stderr)
        sys.exit(1)
    
    if not source_path.is_dir():
        error_msg = f"路径不是目录: {source_path}"
        logger.error(error_msg)
        print(f"错误: {error_msg}", file=sys.stderr)
        sys.exit(1)
    
    # 展开目标目录（如果提供）
    target_path: Optional[Path] = None
    if args.target_dir:
        try:
            target_path = expand_user_path(args.target_dir)
            logger.debug(f"目标目录路径（展开前）: {args.target_dir}")
            logger.debug(f"目标目录路径（展开后）: {target_path}")
        except Exception as e:
            logger.error(f"无法展开目标目录路径 '{args.target_dir}': {str(e)}", exc_info=True)
            sys.exit(1)
    
    # 记录运行参数
    logger.info(f"源目录: {source_path}")
    if target_path:
        logger.info(f"目标目录: {target_path}")
    else:
        logger.info("目标目录: 使用源目录")
    logger.info(f"试运行模式: {args.dry_run}")
    logger.info(f"日志级别: {args.log_level}")
    
    try:
        # 执行文件整理
        logger.info("开始执行文件整理...")
        result = organize_downloads(
            source_dir=str(source_path),
            target_base_dir=str(target_path) if target_path else None,
            dry_run=args.dry_run
        )
        
        # 打印统计结果到控制台
        print("\n" + "=" * 60)
        print("整理完成！")
        print("=" * 60)
        print(f"总文件数:     {result['total_files']}")
        print(f"已整理:       {result['organized_files']}")
        print(f"已跳过:       {result['skipped_files']}")
        print(f"错误数:       {result['errors']}")
        
        if result['by_category']:
            print("\n按类别统计:")
            for category, count in sorted(result['by_category'].items()):
                print(f"  {category:12s}: {count}")
        
        if result['errors'] > 0 and result['errors_list']:
            print(f"\n错误详情 (前10条):")
            for error in result['errors_list'][:10]:
                print(f"  - {error}")
            if len(result['errors_list']) > 10:
                print(f"  ... 还有 {len(result['errors_list']) - 10} 个错误")
        
        print("=" * 60)
        
        # 记录最终统计信息到日志
        logger.info("文件整理完成")
        logger.info(f"统计结果: 总文件={result['total_files']}, "
                   f"已整理={result['organized_files']}, "
                   f"已跳过={result['skipped_files']}, "
                   f"错误={result['errors']}")
        
        # 根据结果设置退出码
        if result['errors'] > 0:
            logger.warning(f"整理过程中发生了 {result['errors']} 个错误")
            sys.exit(1)
        else:
            logger.info("文件整理成功完成，无错误")
            sys.exit(0)
        
    except KeyboardInterrupt:
        logger.warning("用户中断操作（Ctrl+C）")
        print("\n操作已取消", file=sys.stderr)
        sys.exit(130)  # 130 是 SIGINT 的标准退出码
        
    except FileNotFoundError as e:
        error_msg = f"文件或目录未找到: {str(e)}"
        logger.error(error_msg, exc_info=True)
        print(f"错误: {error_msg}", file=sys.stderr)
        sys.exit(1)
        
    except PermissionError as e:
        error_msg = f"权限不足: {str(e)}"
        logger.error(error_msg, exc_info=True)
        print(f"错误: {error_msg}", file=sys.stderr)
        sys.exit(1)
        
    except Exception as e:
        error_msg = f"执行失败: {str(e)}"
        logger.error(error_msg, exc_info=True)
        print(f"错误: {error_msg}", file=sys.stderr)
        print("详细信息请查看日志文件: /tmp/smart_file_organizer.log", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
