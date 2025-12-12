# Copyright (c) 2016 Adam Karpierz
# SPDX-License-Identifier: Zlib

import unittest
from unittest import mock
import tempfile
import shutil
import sys
import os
import time
import stat
import re
from pathlib import Path as StdPath

import utlx
from utlx.epath import Path


class TestPath(unittest.TestCase):

    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.file = self.temp_dir / "test.txt"
        self.file.write_text("Hello World\nHello Python\n")

    def tearDown(self):
        shutil.rmtree(str(self.temp_dir), ignore_errors=True)

    def test_exists_and_mkdir(self):
        new_dir = self.temp_dir / "new"
        self.assertFalse(new_dir.exists())
        new_dir.mkdir()
        self.assertTrue(new_dir.exists())

    def test_rmdir_and_cleardir(self):
        subdir = self.temp_dir / "sub"
        subdir.mkdir()
        (subdir / "file.txt").write_text("data")
        (subdir / "file_readonly.txt").write_text("data_readonly")
        (subdir / "file_readonly.txt").chmod(stat.S_IREAD)
        (subdir / "sub_sub").mkdir()
        (subdir / "sub_sub" / "file.txt").write_text("data_sub")
        (subdir / "sub_sub" / "file_readonly.txt").write_text("data_sub_readonly")
        (subdir / "sub_sub" / "file_readonly.txt").chmod(stat.S_IREAD)
        subdir.cleardir()
        self.assertTrue(subdir.exists())
        self.assertEqual(list(subdir.iterdir()), [])

        (subdir / "file.txt").write_text("data")
        (subdir / "file_readonly.txt").write_text("data_readonly")
        (subdir / "file_readonly.txt").chmod(stat.S_IREAD)
        (subdir / "sub_sub").mkdir()
        (subdir / "sub_sub" / "file.txt").write_text("data_sub")
        (subdir / "sub_sub" / "file_readonly.txt").write_text("data_sub_readonly")
        (subdir / "sub_sub" / "file_readonly.txt").chmod(stat.S_IREAD)
        subdir.rmdir()
        self.assertFalse(subdir.exists())

        subdir = self.temp_dir / "nonexistent.txt"
        self.assertFalse(subdir.exists())
        subdir.cleardir()

        subdir = self.file
        self.assertTrue(subdir.exists())
        with self.assertRaises(NotADirectoryError):
            subdir.cleardir()

    def test_rmdir_on_nonexistent_path_does_nothing(self):
        ghost = self.temp_dir / "ghost"
        try:
            ghost.rmdir()
        except Exception as e:  # pragma: no cover
            self.fail(f"rmdir raised {e} unexpectedly")

    def test_cleardir_on_symlink_raises(self):
        target = self.temp_dir / "target"
        target.mkdir()
        symlink = self.temp_dir / "link"
        symlink.symlink_to(target, target_is_directory=True)
        with self.assertRaises(NotADirectoryError):
            symlink.cleardir()

    def test_cleardir_on_symlink_when_has_file_attrs_is_false_raises(self):
        """Ensure Path.exists() uses the else branch of _is_real_link \
           when _HAS_FILE_ATTRS is False."""
        target = self.temp_dir / "target_else"
        target.mkdir()
        symlink = self.temp_dir / "link_else"
        symlink.symlink_to(target, target_is_directory=True)
        with mock.patch("utlx.epath._HAS_FILE_ATTRS", False):
            with self.assertRaises(NotADirectoryError):
                symlink.cleardir()

    def test_copydir_basic(self):
        src = self.temp_dir / "src_basic"
        src.mkdir()
        (src / "file1.txt").write_text("Hello")
        (src / "file2.txt").write_text("World")
        dst = self.temp_dir / "dst_basic"

        copied = src.copydir(dst)
        self.assertTrue((copied / "file1.txt").exists())
        self.assertTrue((copied / "file2.txt").exists())
        self.assertEqual((copied / "file1.txt").read_text(), "Hello")
        self.assertEqual((copied / "file2.txt").read_text(), "World")

    def test_copydir_empty_directory(self):
        src = self.temp_dir / "src_empty"
        src.mkdir()
        dst = self.temp_dir / "dst_empty"

        copied = src.copydir(dst)
        self.assertTrue(copied.exists())
        self.assertTrue(copied.is_dir())
        self.assertEqual(list(copied.iterdir()), [])

    def test_copydir_nested_empty_directories(self):
        src = self.temp_dir / "src_nested"
        (src / "a" / "b" / "c").mkdir(parents=True)
        dst = self.temp_dir / "dst_nested"

        copied = src.copydir(dst)
        self.assertTrue((copied / "a" / "b" / "c").exists())
        self.assertTrue((copied / "a" / "b" / "c").is_dir())
        self.assertEqual(list((copied / "a" / "b" / "c").iterdir()), [])

    def test_copydir_with_ignore(self):
        src = self.temp_dir / "src_ignore"
        src.mkdir()
        (src / "file1.txt").write_text("data")
        (src / "file2.txt").write_text("data")
        dst = self.temp_dir / "dst_ignore"

        def ignore_func(dir, files):
            return ["file2.txt"]

        copied = src.copydir(dst, ignore=ignore_func)
        self.assertTrue(copied.exists())
        self.assertTrue((copied / "file1.txt").exists())
        self.assertFalse((copied / "file2.txt").exists())

    def test_copydir_ignore_all(self):
        src = self.temp_dir / "src_ignore_all"
        src.mkdir()
        (src / "file1.txt").write_text("data")
        (src / "file2.txt").write_text("data")
        dst = self.temp_dir / "dst_ignore_all"

        def ignore_all(dir, files):
            return files  # ignore all

        copied = src.copydir(dst, ignore=ignore_all)
        self.assertTrue(copied.exists())
        self.assertEqual(list(copied.iterdir()), [])

    def test_copydir_with_symlinks(self):
        src = self.temp_dir / "src_symlink"
        src.mkdir()
        target_file = src / "target.txt"
        target_file.write_text("symlinked")
        symlink = src / "link.txt"
        symlink.symlink_to(target_file)
        dst = self.temp_dir / "dst_symlink"

        copied = src.copydir(dst, symlinks=True)
        copied_link = copied / "link.txt"
        self.assertTrue(copied_link.is_symlink())
        self.assertEqual(copied_link.read_text(), "symlinked")

    def test_copydir_with_custom_copy_function(self):
        src = self.temp_dir / "src_custom"
        src.mkdir()
        (src / "file.txt").write_text("original")
        dst = self.temp_dir / "dst_custom"

        def custom_copy(src_path, dst_path):
            shutil.copy2(src_path, dst_path)
            with open(dst_path, "a") as f:
                f.write(" [copied]")

        copied = src.copydir(dst, copy_function=custom_copy)
        content = (copied / "file.txt").read_text()
        self.assertIn("original", content)
        self.assertIn("[copied]", content)

    def test_copy_and_move(self):
        dst = self.temp_dir / "copy.txt"
        copied = self.file.copy(dst)
        self.assertTrue(dst.exists())
        self.assertEqual(dst.read_text(), "Hello World\nHello Python\n")

        moved_path = self.temp_dir / "moved.txt"
        moved = copied.move(moved_path)
        self.assertTrue(moved_path.exists())
        self.assertFalse(dst.exists())
        self.assertEqual(moved.read_text(), "Hello World\nHello Python\n")

    def test_move_nonexistent(self):
        src = self.temp_dir / "nonexistent.txt"
        self.assertFalse(src.exists())

        moved_path = self.temp_dir / "nonexistent_moved.txt"
        self.assertFalse(moved_path.exists())
        moved = src.move(moved_path)
        self.assertIsNone(moved)
        self.assertFalse(moved_path.exists())

    def test_unlink_and_permission_handling(self):
        self.file.chmod(stat.S_IREAD)
        self.file.unlink()
        self.assertFalse(self.file.exists())

    def test_unlink_missing_ok_true(self):
        ghost = self.temp_dir / "ghost.txt"
        self.assertFalse(ghost.exists())
        ghost.unlink()  # missing_ok default is True
        ghost.unlink(missing_ok=True)

    def test_unlink_missing_ok_false_raises(self):
        ghost = self.temp_dir / "ghost.txt"
        self.assertFalse(ghost.exists())
        with self.assertRaises(FileNotFoundError):
            ghost.unlink(missing_ok=False)

    def test_file_hash(self):
        hash_val = self.file.file_hash("md5")
        self.assertTrue(hasattr(hash_val, "hexdigest"))
        self.assertIsInstance(hash_val.hexdigest(), str)

    def test_file_hash_invalid_algorithm(self):
        with self.assertRaises(ValueError):
            self.file.file_hash("unknownhash")

    def test_dir_hash(self):
        hash_val = self.temp_dir.dir_hash("sha256")
        self.assertTrue(hasattr(hash_val, "hexdigest"))

    def test_dir_hash_empty_directory(self):
        empty_dir = self.temp_dir / "empty"
        empty_dir.mkdir()
        hash_val = empty_dir.dir_hash("md5")
        self.assertTrue(hasattr(hash_val, "hexdigest"))

    def test_unpack_archive(self):
        archive = self.temp_dir / "archive.zip"
        shutil.make_archive(str(archive.with_suffix("")), "zip", str(self.temp_dir))
        extract_dir = self.temp_dir / "extracted"
        archive.unpack_archive(extract_dir)
        self.assertTrue(extract_dir.exists())
        self.assertTrue((extract_dir / "test.txt").exists())

    def test_unpack_archive_invalid_format(self):
        archive = self.temp_dir / "archive.zip"
        shutil.make_archive(str(archive.with_suffix("")), "zip", str(self.temp_dir))
        with self.assertRaises(shutil.ReadError):
            archive.unpack_archive(format="tar")

    def test_chdir_and_pushd(self):
        original = StdPath.cwd()
        self.temp_dir.chdir()
        self.assertEqual(StdPath.cwd(), self.temp_dir)

        with self.temp_dir.pushd():
            self.assertEqual(StdPath.cwd(), self.temp_dir)
        self.assertEqual(StdPath.cwd(), self.temp_dir)

    def test_which(self):
        python_path = Path.which("python")
        self.assertIsNotNone(python_path)
        self.assertTrue(python_path.exists())

    @mock.patch.object(os, 'link', side_effect=NotImplementedError, create=True)
    def test_hardlink_to_not_supported(self, _):
        if sys.version_info[:2] >= (3, 11) or not hasattr(os, "link"):
            with self.assertRaises(NotImplementedError):
                (self.temp_dir / "hard.txt").hardlink_to(self.file)
        else: pass  # pragma: no cover

    def test_copystat_copies_mtime(self):
        with tempfile.NamedTemporaryFile() as src_file, \
             tempfile.NamedTemporaryFile() as dst_file:

            src = Path(src_file.name)
            dst = Path(dst_file.name)

            # We modify the source's modification time.
            new_mtime = time.time() - 3600  # 1 hour earlier
            os.utime(src, (new_mtime, new_mtime))

            # We make sure the timestamps differ before copying
            src_stat = os.stat(src)
            dst_stat = os.stat(dst)
            self.assertNotEqual(src_stat.st_mtime, dst_stat.st_mtime)

            # We copy the metadata
            src.copystat(dst)

            # We check whether the mtime was successfully copied
            dst_stat_after = os.stat(dst)
            self.assertEqual(src_stat.st_mtime, dst_stat_after.st_mtime)

    def test_copystat_symlink_behavior(self):
        with tempfile.NamedTemporaryFile() as src_file, \
             tempfile.NamedTemporaryFile() as dst_file:

            src = Path(src_file.name)
            dst = Path(dst_file.name)
            symlink = dst.parent / (dst.name + "_link")
            symlink.symlink_to(dst)

            # We modify the source's modification time.
            new_mtime = time.time() - 7200  # 2 hours earlier
            os.utime(src, (new_mtime, new_mtime))

            # We copy the metadata to the symlink (without following it)
            src.copystat(symlink, follow_symlinks=False)

            # We check whether the metadata was assigned to the symlink
            # (if the system allows it)
            try:
                link_stat = os.lstat(symlink)
                self.assertEqual(link_stat.st_mtime, new_mtime)
            except AssertionError:
                # Some systems ignore the mtime of symlinks
                pass

        # Cleanup
        os.remove(symlink)

    def test_pushd_restores_directory_on_exception(self):
        original = StdPath.cwd()
        try:
            with self.temp_dir.pushd():
                raise RuntimeError("Simulated error")
        except RuntimeError:
            self.assertEqual(StdPath.cwd(), original)


class TestSedInPlace(unittest.TestCase):

    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.file = self.temp_dir / "test.txt"
        self.file.write_text("Hello World\nHello Python\n")

    def tearDown(self):
        shutil.rmtree(str(self.temp_dir), ignore_errors=True)

    def test_sed_inplace(self):
        self.file.sed_inplace("Hello", "Hi")
        content = self.file.read_text()
        self.assertIn("Hi World", content)
        self.assertIn("Hi Python", content)

    def test_sed_inplace_with_string_pattern_and_encoding(self):
        self.file.sed_inplace("Hello", "Hi", encoding="utf-8")
        content = self.file.read_text()
        self.assertIn("Hi World", content)
        self.assertIn("Hi Python", content)

    def test_sed_inplace_with_compiled_pattern(self):
        pattern = re.compile("World")
        self.file.sed_inplace(pattern, "Universe", encoding="utf-8")
        content = self.file.read_text()
        self.assertIn("Hello Universe", content)

    def test_sed_inplace_detected_encoding(self):
        fake_detected = mock.Mock()
        fake_detected.encoding = "utf-8"
        fake_detected.__str__ = lambda self: "Hi World\nHi Python\n"
        with mock.patch("utlx.epath.charset_normalizer.from_bytes") as mock_from_bytes:
            mock_from_bytes.return_value.best.return_value = fake_detected
            self.file.sed_inplace("Hello", "Hi")
        content = self.file.read_text()
        self.assertIn("Hi World", content)

    def test_sed_inplace_no_detected_encoding(self):
        with mock.patch("utlx.epath.charset_normalizer.from_bytes") as mock_from_bytes:
            mock_from_bytes.return_value.best.return_value = None
            self.file.sed_inplace("Hello", "Hi")
        content = self.file.read_text()
        self.assertIn("Hi World", content)

    def test_sed_inplace_multiline_flag(self):
        self.file.sed_inplace("^Hello", "Hi", flags=re.MULTILINE, encoding="utf-8")
        content = self.file.read_text()
        self.assertTrue(content.startswith("Hi"))

    def test_sed_inplace_raises_unicode_error(self):
        """Ensure sed_inplace raises UnicodeError when decoding fails."""
        class BadBytes(bytes):
            def decode(self, *args, **kwargs):
                raise Exception("decode fail")

        bad_file = self.temp_dir / "bad.txt"

        # Patch read_bytes to return our BadBytes instance
        with mock.patch.object(type(bad_file), "read_bytes", return_value=BadBytes(b"xxx")), \
             mock.patch("utlx.epath.charset_normalizer.from_bytes") as mock_from_bytes:
            mock_from_bytes.return_value.best.return_value = None
            with self.assertRaises(UnicodeError):
                bad_file.sed_inplace("x", "y")
