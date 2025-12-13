"""
单元测试文件
测试文件整理工具的核心功能
"""

import unittest
import sys
import os
import tempfile
import shutil
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from smart_file_organizer.utils import (  # pyright: ignore[reportMissingImports]
    organize_downloads,
    get_file_category,
    get_file_extension,
    generate_unique_filename,
    FILE_TYPE_CATEGORIES
)


class TestFileOrganizer(unittest.TestCase):
    """文件整理工具测试类"""
    
    def setUp(self):
        """
        测试前的准备工作
        创建临时测试目录和测试文件
        """
        # 创建临时根目录
        self.test_root = tempfile.mkdtemp(prefix="test_file_organizer_")
        self.test_root_path = Path(self.test_root)
        
        # 创建源目录（模拟下载目录）
        self.source_dir = self.test_root_path / "source"
        self.source_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建目标目录（可选）
        self.target_dir = self.test_root_path / "target"
        self.target_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建各种类型的测试文件
        self.test_files = {
            "test_image.jpg": "images",
            "test_image.png": "images",
            "test_document.pdf": "documents",
            "test_document.txt": "documents",
            "test_video.mp4": "videos",
            "test_audio.mp3": "audio",
            "test_archive.zip": "archives",
            "test_code.py": "code",
            "test_code.js": "code",
        }
        
        # 在源目录中创建测试文件
        for filename, _ in self.test_files.items():
            file_path = self.source_dir / filename
            file_path.write_text(f"Test content for {filename}")
        
        # 创建一个隐藏文件（应该被跳过）
        hidden_file = self.source_dir / ".hidden_file"
        hidden_file.write_text("This should be skipped")
        
        # 创建一个子目录（应该被跳过）
        subdir = self.source_dir / "subdirectory"
        subdir.mkdir()
        (subdir / "file_in_subdir.txt").write_text("File in subdirectory")
        
        # 创建一个无法分类的文件（应该被跳过）
        unknown_file = self.source_dir / "unknown_file.xyz"
        unknown_file.write_text("Unknown file type")
    
    def tearDown(self):
        """
        测试后的清理工作
        删除临时测试目录
        """
        if self.test_root_path.exists():
            shutil.rmtree(self.test_root_path)
    
    def test_organize_downloads(self):
        """
        测试文件分类功能
        验证文件能够正确按类型分类到对应目录
        """
        # 执行文件整理
        result = organize_downloads(
            source_dir=str(self.source_dir),
            target_base_dir=str(self.target_dir),
            dry_run=False
        )
        
        # 验证统计结果
        self.assertIsInstance(result, dict)
        self.assertIn("total_files", result)
        self.assertIn("organized_files", result)
        self.assertIn("skipped_files", result)
        self.assertIn("errors", result)
        self.assertIn("by_category", result)
        self.assertIn("errors_list", result)
        
        # 验证总文件数（包括所有非隐藏、非目录的文件）
        # 注意：子目录中的文件也会被统计，但会被跳过
        expected_total = len(self.test_files) + 1  # 9个测试文件 + 1个子目录中的文件
        self.assertEqual(result["total_files"], expected_total)
        
        # 验证已整理的文件数应该等于可分类的文件数（不包括子目录中的文件）
        expected_organized = len(self.test_files)
        self.assertEqual(result["organized_files"], expected_organized)
        
        # 验证跳过的文件数（隐藏文件、目录、无法分类的文件、子目录中的文件）
        # 1个隐藏文件 + 1个子目录 + 1个无法分类的文件 + 1个子目录中的文件 = 4个
        # 但子目录本身不算在跳过文件中，所以至少是3个
        self.assertGreaterEqual(result["skipped_files"], 3)
        
        # 验证没有错误
        self.assertEqual(result["errors"], 0)
        self.assertEqual(len(result["errors_list"]), 0)
        
        # 验证文件已移动到正确的分类目录
        for filename, expected_category in self.test_files.items():
            target_file = self.target_dir / expected_category / filename
            self.assertTrue(
                target_file.exists(),
                f"文件 {filename} 应该被移动到 {expected_category} 目录"
            )
            # 验证文件内容
            self.assertEqual(
                target_file.read_text(),
                f"Test content for {filename}",
                f"文件 {filename} 的内容应该保持不变"
            )
        
        # 验证源目录中的文件已被移动（不再存在）
        for filename in self.test_files.keys():
            source_file = self.source_dir / filename
            self.assertFalse(
                source_file.exists(),
                f"源文件 {filename} 应该已被移动"
            )
        
        # 验证隐藏文件仍在源目录（未被移动）
        hidden_file = self.source_dir / ".hidden_file"
        self.assertTrue(
            hidden_file.exists(),
            "隐藏文件应该被跳过，仍在源目录"
        )
        
        # 验证子目录仍在源目录（未被移动）
        subdir = self.source_dir / "subdirectory"
        self.assertTrue(
            subdir.exists(),
            "子目录应该被跳过，仍在源目录"
        )
        
        # 验证无法分类的文件仍在源目录（未被移动）
        unknown_file = self.source_dir / "unknown_file.xyz"
        self.assertTrue(
            unknown_file.exists(),
            "无法分类的文件应该被跳过，仍在源目录"
        )
        
        # 验证按类别统计
        self.assertIsInstance(result["by_category"], dict)
        for category, count in result["by_category"].items():
            self.assertGreater(count, 0, f"类别 {category} 应该有文件")
            # 验证统计数量与实际文件数一致
            expected_count = sum(
                1 for cat in self.test_files.values() if cat == category
            )
            self.assertEqual(
                count,
                expected_count,
                f"类别 {category} 的文件数统计不正确"
            )
    
    def test_same_filename_handling(self):
        """
        测试同名文件处理
        验证当目标位置已存在同名文件时，会添加时间戳生成新文件名
        """
        # 在目标目录中预先创建一个同名文件
        target_category_dir = self.target_dir / "images"
        target_category_dir.mkdir(parents=True, exist_ok=True)
        
        existing_file = target_category_dir / "test_image.jpg"
        existing_file.write_text("Existing file content")
        
        # 执行文件整理
        result = organize_downloads(
            source_dir=str(self.source_dir),
            target_base_dir=str(self.target_dir),
            dry_run=False
        )
        
        # 验证原始文件仍在目标目录
        self.assertTrue(
            existing_file.exists(),
            "原始文件应该仍然存在"
        )
        
        # 验证新文件使用了带时间戳的名称
        source_file = self.source_dir / "test_image.jpg"
        self.assertFalse(
            source_file.exists(),
            "源文件应该已被移动"
        )
        
        # 查找带时间戳的新文件
        image_files = list(target_category_dir.glob("test_image_*.jpg"))
        self.assertGreater(
            len(image_files),
            0,
            "应该存在带时间戳的新文件"
        )
        
        # 验证新文件的内容
        new_file = image_files[0]
        self.assertEqual(
            new_file.read_text(),
            "Test content for test_image.jpg",
            "新文件的内容应该正确"
        )
        
        # 验证文件名格式（包含时间戳）
        self.assertRegex(
            new_file.stem,
            r"test_image_\d{8}_\d{6}",
            "新文件名应该包含时间戳格式 YYYYMMDD_HHMMSS"
        )
    
    def test_organize_downloads_dry_run(self):
        """
        测试试运行模式
        验证在试运行模式下文件不会被实际移动
        """
        # 记录移动前的文件列表
        source_files_before = set(self.source_dir.iterdir())
        
        # 执行试运行模式的文件整理
        result = organize_downloads(
            source_dir=str(self.source_dir),
            target_base_dir=str(self.target_dir),
            dry_run=True
        )
        
        # 验证统计结果仍然正确
        self.assertEqual(result["organized_files"], len(self.test_files))
        
        # 验证源目录中的文件未被移动（仍然存在）
        source_files_after = set(self.source_dir.iterdir())
        self.assertEqual(
            source_files_before,
            source_files_after,
            "试运行模式下源文件应该未被移动"
        )
        
        # 验证目标目录中不存在文件（除了可能预先存在的）
        for filename, category in self.test_files.items():
            target_file = self.target_dir / category / filename
            self.assertFalse(
                target_file.exists(),
                f"试运行模式下文件 {filename} 不应该被移动到目标目录"
            )
    
    def test_organize_downloads_same_directory(self):
        """
        测试在源目录内整理文件
        验证当目标目录为 None 时，文件在源目录内分类
        """
        # 执行文件整理（目标目录为 None，使用源目录）
        result = organize_downloads(
            source_dir=str(self.source_dir),
            target_base_dir=None,
            dry_run=False
        )
        
        # 验证文件已在源目录内分类
        for filename, expected_category in self.test_files.items():
            target_file = self.source_dir / expected_category / filename
            self.assertTrue(
                target_file.exists(),
                f"文件 {filename} 应该在源目录的 {expected_category} 子目录中"
            )
    
    def test_get_file_category(self):
        """
        测试文件类别获取功能
        """
        # 测试各种文件扩展名
        test_cases = [
            ("jpg", "images"),
            ("png", "images"),
            ("pdf", "documents"),
            ("txt", "documents"),
            ("mp4", "videos"),
            ("mp3", "audio"),
            ("zip", "archives"),
            ("py", "code"),
            ("js", "code"),
            ("unknown", None),
            ("", None),
        ]
        
        for extension, expected_category in test_cases:
            with self.subTest(extension=extension):
                result = get_file_category(extension)
                self.assertEqual(
                    result,
                    expected_category,
                    f"扩展名 {extension} 应该返回类别 {expected_category}"
                )
    
    def test_get_file_extension(self):
        """
        测试文件扩展名获取功能
        """
        test_cases = [
            ("/path/to/file.jpg", "jpg"),
            ("file.PNG", "png"),
            ("document.pdf", "pdf"),
            ("file.tar.gz", "gz"),
            ("file", ""),
            (".hidden", ""),
        ]
        
        for file_path, expected_ext in test_cases:
            with self.subTest(file_path=file_path):
                result = get_file_extension(file_path)
                self.assertEqual(
                    result,
                    expected_ext,
                    f"文件路径 {file_path} 应该返回扩展名 {expected_ext}"
                )
    
    def test_generate_unique_filename(self):
        """
        测试唯一文件名生成功能
        """
        # 测试文件不存在的情况
        test_file = self.test_root_path / "test.txt"
        
        # 第一次调用应该返回原路径（文件不存在）
        unique_path = generate_unique_filename(test_file)
        self.assertEqual(unique_path, test_file)
        
        # 创建同名文件
        test_file.write_text("Existing content")
        
        # 再次调用应该返回带时间戳的路径（因为文件已存在）
        unique_path = generate_unique_filename(test_file)
        self.assertNotEqual(unique_path, test_file)
        self.assertRegex(
            unique_path.stem,
            r"test_\d{8}_\d{6}",
            "文件名应该包含时间戳"
        )
        self.assertEqual(unique_path.suffix, ".txt")
        self.assertEqual(unique_path.parent, test_file.parent)
        
        # 验证新路径的文件不存在
        self.assertFalse(unique_path.exists(), "生成的唯一路径应该不存在")


if __name__ == '__main__':
    # 设置测试详细程度
    unittest.main(verbosity=2)
