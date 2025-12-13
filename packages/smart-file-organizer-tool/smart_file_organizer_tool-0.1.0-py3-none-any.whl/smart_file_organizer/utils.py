"""
工具函数模块
提供文件整理相关的工具函数
"""

import os
import shutil
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from collections import defaultdict


# 文件类型分类映射
FILE_TYPE_CATEGORIES: Dict[str, List[str]] = {
    "images": ["jpg", "jpeg", "png", "gif", "bmp", "svg", "webp", "ico", "tiff", "tif", "heic", "heif"],
    "documents": ["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "txt", "rtf", "odt", "ods", "odp", "pages", "numbers", "key"],
    "videos": ["mp4", "avi", "mov", "wmv", "flv", "mkv", "webm", "m4v", "mpg", "mpeg", "3gp", "3g2"],
    "audio": ["mp3", "wav", "flac", "aac", "ogg", "wma", "m4a", "opus", "aiff", "au"],
    "archives": ["zip", "rar", "7z", "tar", "gz", "bz2", "xz", "tar.gz", "tar.bz2", "tar.xz", "dmg", "iso"],
    "code": ["py", "js", "html", "css", "java", "cpp", "c", "h", "hpp", "cs", "php", "rb", "go", "rs", "swift", "kt", "ts", "tsx", "jsx", "vue", "json", "xml", "yaml", "yml", "sh", "bash", "zsh", "ps1", "bat", "cmd", "sql", "md", "markdown"]
}


def setup_logging(log_file: str = "/tmp/smart_file_organizer.log", 
                  log_level: int = logging.INFO) -> logging.Logger:
    """
    配置日志系统，同时输出到文件和控制台
    
    Args:
        log_file: 日志文件路径，默认为 /tmp/smart_file_organizer.log
        log_level: 日志级别，默认为 INFO
        
    Returns:
        配置好的 Logger 对象
        
    Example:
        >>> logger = setup_logging()
        >>> logger.info("这是一条日志信息")
    """
    # 创建日志目录（如果不存在）
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 创建 logger
    logger = logging.getLogger("smart_file_organizer")
    logger.setLevel(log_level)
    
    # 避免重复添加处理器
    if logger.handlers:
        return logger
    
    # 创建格式化器
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 文件处理器
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    # 添加处理器到 logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def get_file_category(extension: str) -> Optional[str]:
    """
    根据文件扩展名获取文件类别
    
    Args:
        extension: 文件扩展名（不含点号，小写）
        
    Returns:
        文件类别名称，如果无法分类则返回 None
        
    Example:
        >>> get_file_category("jpg")
        'images'
        >>> get_file_category("pdf")
        'documents'
    """
    extension_lower = extension.lower()
    
    for category, extensions in FILE_TYPE_CATEGORIES.items():
        if extension_lower in extensions:
            return category
    
    return None


def get_file_extension(file_path: str) -> str:
    """
    获取文件扩展名
    
    Args:
        file_path: 文件路径
        
    Returns:
        文件扩展名（不含点号，小写）
        
    Example:
        >>> get_file_extension("/path/to/file.jpg")
        'jpg'
    """
    _, ext = os.path.splitext(file_path)
    return ext.lstrip('.').lower()


def generate_unique_filename(target_path: Path) -> Path:
    """
    生成唯一的文件名，如果文件已存在则添加时间戳
    
    Args:
        target_path: 目标文件路径
        
    Returns:
        唯一的文件路径
        
    Example:
        >>> path = Path("/tmp/file.txt")
        >>> unique_path = generate_unique_filename(path)
    """
    if not target_path.exists():
        return target_path
    
    # 文件已存在，添加时间戳
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    stem = target_path.stem
    suffix = target_path.suffix
    parent = target_path.parent
    
    new_name = f"{stem}_{timestamp}{suffix}"
    return parent / new_name


def organize_downloads(source_dir: str, 
                      target_base_dir: Optional[str] = None,
                      dry_run: bool = False) -> Dict[str, Any]:
    """
    整理下载目录，按文件类型分类
    
    功能特性：
    - 支持的类型：images, documents, videos, audio, archives, code
    - 跳过目录和隐藏文件
    - 处理同名文件（添加时间戳）
    - 返回统计结果
    
    Args:
        source_dir: 源目录路径（通常是下载目录）
        target_base_dir: 目标基础目录，如果为 None 则使用源目录
        dry_run: 是否为试运行模式（不实际移动文件）
        
    Returns:
        包含统计信息的字典：
        {
            "total_files": 总文件数,
            "organized_files": 已整理文件数,
            "skipped_files": 跳过文件数,
            "errors": 错误数,
            "by_category": {
                "images": 数量,
                "documents": 数量,
                ...
            },
            "errors_list": [错误信息列表]
        }
        
    Raises:
        FileNotFoundError: 当源目录不存在时
        PermissionError: 当没有权限访问目录时
        
    Example:
        >>> result = organize_downloads("/Users/username/Downloads")
        >>> print(f"整理了 {result['organized_files']} 个文件")
    """
    logger = setup_logging()
    
    # 验证源目录
    source_path = Path(source_dir)
    if not source_path.exists():
        error_msg = f"源目录不存在: {source_dir}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
    
    if not source_path.is_dir():
        error_msg = f"路径不是目录: {source_dir}"
        logger.error(error_msg)
        raise NotADirectoryError(error_msg)
    
    # 设置目标目录
    if target_base_dir is None:
        target_base_dir = str(source_path)
    target_base_path = Path(target_base_dir)
    target_base_path.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"开始整理目录: {source_dir}")
    logger.info(f"目标目录: {target_base_dir}")
    logger.info(f"试运行模式: {dry_run}")
    
    # 统计信息
    stats: Dict[str, Any] = {
        "total_files": 0,
        "organized_files": 0,
        "skipped_files": 0,
        "errors": 0,
        "by_category": defaultdict(int),
        "errors_list": []
    }
    
    try:
        # 遍历源目录中的所有文件
        for item in source_path.iterdir():
            try:
                # 跳过目录
                if item.is_dir():
                    logger.debug(f"跳过目录: {item.name}")
                    stats["skipped_files"] += 1
                    continue
                
                # 跳过隐藏文件（以点开头的文件）
                if item.name.startswith('.'):
                    logger.debug(f"跳过隐藏文件: {item.name}")
                    stats["skipped_files"] += 1
                    continue
                
                stats["total_files"] += 1
                
                # 获取文件扩展名和类别
                extension = get_file_extension(str(item))
                category = get_file_category(extension)
                
                if category is None:
                    # 无法分类的文件，跳过
                    logger.debug(f"无法分类的文件: {item.name} (扩展名: {extension})")
                    stats["skipped_files"] += 1
                    continue
                
                # 创建目标目录
                category_dir = target_base_path / category
                category_dir.mkdir(parents=True, exist_ok=True)
                
                # 生成目标文件路径
                target_file = category_dir / item.name
                target_file = generate_unique_filename(target_file)
                
                # 移动文件
                if not dry_run:
                    try:
                        shutil.move(str(item), str(target_file))
                        logger.info(f"已移动: {item.name} -> {category}/{target_file.name}")
                    except Exception as e:
                        error_msg = f"移动文件失败 {item.name}: {str(e)}"
                        logger.error(error_msg)
                        stats["errors"] += 1
                        stats["errors_list"].append(error_msg)
                        continue
                else:
                    logger.info(f"[试运行] 将移动: {item.name} -> {category}/{target_file.name}")
                
                stats["organized_files"] += 1
                stats["by_category"][category] += 1
                
            except Exception as e:
                error_msg = f"处理文件 {item.name} 时出错: {str(e)}"
                logger.error(error_msg, exc_info=True)
                stats["errors"] += 1
                stats["errors_list"].append(error_msg)
                continue
        
        # 转换 defaultdict 为普通字典
        stats["by_category"] = dict(stats["by_category"])
        
        # 记录统计信息
        logger.info("=" * 50)
        logger.info("整理完成！统计信息：")
        logger.info(f"总文件数: {stats['total_files']}")
        logger.info(f"已整理: {stats['organized_files']}")
        logger.info(f"已跳过: {stats['skipped_files']}")
        logger.info(f"错误数: {stats['errors']}")
        logger.info("按类别统计：")
        for category, count in stats["by_category"].items():
            logger.info(f"  {category}: {count}")
        logger.info("=" * 50)
        
        return stats
        
    except PermissionError as e:
        error_msg = f"权限错误: {str(e)}"
        logger.error(error_msg)
        raise PermissionError(error_msg) from e
    except Exception as e:
        error_msg = f"整理过程中发生未知错误: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise


def organize_files(source_dir: str, target_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    整理文件（organize_downloads 的别名，保持向后兼容）
    
    Args:
        source_dir: 源目录路径
        target_dir: 目标目录路径（可选）
        
    Returns:
        统计信息字典
    """
    return organize_downloads(source_dir, target_dir)
