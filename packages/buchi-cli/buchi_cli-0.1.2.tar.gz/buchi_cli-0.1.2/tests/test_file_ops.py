"""
Unit tests for file operations.
Tests path validation, file manipulation, and error handling.
"""

import os
import shutil
import tempfile
from pathlib import Path

import pytest  # pyright: ignore[reportMissingImports]

from buchi.tools.file_ops import (
    delete_file,
    list_directory,
    read_file,
    set_logger,
    validate_path,
    write_file,
)


class MockLogger:
    """Mock logger for testing"""

    def __init__(self):
        self.logs = []

    def debug(self, msg, **kwargs):
        self.logs.append(("debug", msg, kwargs))

    def audit_file_read(self, path, success, error=None):
        self.logs.append(("audit_read", path, success, error))

    def audit_file_write(self, path, size, success, error=None):
        self.logs.append(("audit_write", path, size, success, error))

    def audit_file_delete(self, path, success, error=None):
        self.logs.append(("audit_delete", path, success, error))

    def audit_tool_call(self, tool, args, success):
        self.logs.append(("audit_tool", tool, args, success))

    def error(self, msg, exception=None, **kwargs):
        self.logs.append(("error", msg, exception, kwargs))

    def warning(self, msg, **kwargs):
        self.logs.append(("warning", msg, kwargs))


@pytest.fixture
def temp_workspace():
    """Create a temporary workspace for testing"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def mock_logger():
    """Create a mock logger"""
    logger = MockLogger()
    set_logger(logger)
    yield logger
    set_logger(None)  # Reset


class TestPathValidation:
    """Test path validation security"""

    def test_valid_relative_path(self, temp_workspace):
        valid, result = validate_path(temp_workspace, "test.txt")
        assert valid is True
        assert temp_workspace in result

    def test_valid_nested_path(self, temp_workspace):
        """Test that nested paths are valid"""
        # FIX: Normalize the expected path suffix to match the OS separator
        nested_suffix = os.path.normpath("folder/subfolder/test.txt")

        valid, result = validate_path(temp_workspace, "folder/subfolder/test.txt")
        assert valid is True
        assert result.endswith(nested_suffix)

    def test_reject_parent_traversal(self, temp_workspace):
        """Test that ../.. paths are rejected"""
        valid, result = validate_path(temp_workspace, "../../../etc/passwd")
        assert valid is False
        assert "outside working directory" in result

    def test_reject_absolute_outside_workspace(self, temp_workspace):
        """Test that absolute paths outside workspace are rejected"""
        # FIX: Use a platform-appropriate absolute path for the test
        if os.name == "nt":
            abs_path = "C:\\Windows\\System32\\drivers\\etc\\hosts"
        else:
            abs_path = "/etc/passwd"

        valid, result = validate_path(temp_workspace, abs_path)
        assert valid is False
        assert "outside working directory" in result

    def test_dot_in_path(self, temp_workspace):
        """Test that . in path is handled correctly"""
        valid, result = validate_path(temp_workspace, "./test.txt")
        assert valid is True


class TestListDirectory:
    """Test directory listing functionality"""

    def test_list_empty_directory(self, temp_workspace, mock_logger):
        """Test listing an empty directory"""
        result = list_directory(temp_workspace, ".")
        assert "empty" in result.lower()

    def test_list_directory_with_files(self, temp_workspace, mock_logger):
        """Test listing directory with files"""
        # Create test files
        (Path(temp_workspace) / "file1.txt").touch()
        (Path(temp_workspace) / "file2.py").touch()
        (Path(temp_workspace) / "subdir").mkdir()

        result = list_directory(temp_workspace, ".")

        assert "file1.txt" in result
        assert "file2.py" in result
        assert "subdir" in result
        assert "file" in result.lower()  # Should show file type
        assert "dir" in result.lower()  # Should show dir type

    def test_list_nonexistent_directory(self, temp_workspace, mock_logger):
        """Test listing nonexistent directory"""
        result = list_directory(temp_workspace, "nonexistent")
        assert "does not exist" in result.lower()

    def test_list_file_instead_of_directory(self, temp_workspace, mock_logger):
        """Test listing a file (should fail)"""
        test_file = Path(temp_workspace) / "test.txt"
        test_file.touch()

        result = list_directory(temp_workspace, "test.txt")
        assert "not a directory" in result.lower()

    def test_list_outside_workspace(self, temp_workspace, mock_logger):
        """Test listing outside workspace (should fail)"""
        result = list_directory(temp_workspace, "../../")
        assert "outside working directory" in result.lower()


class TestReadFile:
    """Test file reading functionality"""

    def test_read_text_file(self, temp_workspace, mock_logger):
        """Test reading a text file"""
        test_file = Path(temp_workspace) / "test.txt"
        content = "Hello, World!\nThis is a test."
        # Ensure we write UTF-8 to avoid platform dependent encoding issues during setup
        test_file.write_text(content, encoding="utf-8")

        result = read_file(temp_workspace, "test.txt")
        assert result == content

        # Check logging
        assert any(log[0] == "audit_read" for log in mock_logger.logs)

    def test_read_nonexistent_file(self, temp_workspace, mock_logger):
        """Test reading nonexistent file"""
        result = read_file(temp_workspace, "nonexistent.txt")
        assert "does not exist" in result.lower()

    def test_read_directory_as_file(self, temp_workspace, mock_logger):
        """Test reading a directory (should fail)"""
        (Path(temp_workspace) / "testdir").mkdir()
        result = read_file(temp_workspace, "testdir")
        assert "not a file" in result.lower()

    def test_read_outside_workspace(self, temp_workspace, mock_logger):
        """Test reading outside workspace (should fail)"""
        # FIX: Use platform safe path traversal
        path = os.path.join("..", "..", "etc", "passwd")
        result = read_file(temp_workspace, path)
        assert "outside working directory" in result.lower()

    def test_read_large_file_truncation(self, temp_workspace, mock_logger):
        """Test that large files are truncated"""
        test_file = Path(temp_workspace) / "large.txt"
        large_content = "x" * 150000  # Exceeds 100k limit
        test_file.write_text(large_content, encoding="utf-8")

        result = read_file(temp_workspace, "large.txt")
        assert len(result) < len(large_content)
        assert "truncated" in result.lower()

    def test_read_binary_file(self, temp_workspace, mock_logger):
        """Test reading binary file (should fail gracefully)"""
        test_file = Path(temp_workspace) / "binary.bin"
        test_file.write_bytes(b"\x00\x01\x02\x03\xff\xfe")

        result = read_file(temp_workspace, "binary.bin")
        assert "not a text file" in result.lower() or "binary" in result.lower()


class TestWriteFile:
    """Test file writing functionality"""

    def test_write_new_file(self, temp_workspace, mock_logger):
        """Test writing a new file"""
        content = "Hello, World!"
        result = write_file(temp_workspace, "new.txt", content)

        assert "successfully wrote" in result.lower()

        # Verify file exists and content matches
        written_file = Path(temp_workspace) / "new.txt"
        assert written_file.exists()
        # Read back with utf-8 to verify content
        assert written_file.read_text(encoding="utf-8") == content

        # Check logging
        assert any(log[0] == "audit_write" for log in mock_logger.logs)

    def test_overwrite_existing_file(self, temp_workspace, mock_logger):
        """Test overwriting an existing file"""
        test_file = Path(temp_workspace) / "test.txt"
        test_file.write_text("Original content", encoding="utf-8")

        new_content = "New content"
        result = write_file(temp_workspace, "test.txt", new_content)

        assert "successfully wrote" in result.lower()
        assert test_file.read_text(encoding="utf-8") == new_content

    def test_write_nested_file(self, temp_workspace, mock_logger):
        """Test writing file in nested directory (should create dirs)"""
        content = "Nested file"
        # FIX: Ensure separators are normalized for the check
        rel_path = os.path.join("a", "b", "c", "nested.txt")
        result = write_file(temp_workspace, rel_path, content)

        assert "successfully wrote" in result.lower()

        nested_file = Path(temp_workspace) / rel_path
        assert nested_file.exists()
        assert nested_file.read_text(encoding="utf-8") == content

    def test_write_outside_workspace(self, temp_workspace, mock_logger):
        """Test writing outside workspace (should fail)"""
        result = write_file(temp_workspace, "../../bad.txt", "content")
        assert "outside working directory" in result.lower()

    def test_write_empty_file(self, temp_workspace, mock_logger):
        """Test writing empty file"""
        result = write_file(temp_workspace, "empty.txt", "")
        assert "successfully wrote" in result.lower()

        empty_file = Path(temp_workspace) / "empty.txt"
        assert empty_file.exists()
        assert empty_file.read_text(encoding="utf-8") == ""


class TestDeleteFile:
    """Test file deletion functionality"""

    def test_delete_existing_file(self, temp_workspace, mock_logger):
        """Test deleting an existing file"""
        test_file = Path(temp_workspace) / "delete_me.txt"
        test_file.write_text("content", encoding="utf-8")

        result = delete_file(temp_workspace, "delete_me.txt")

        assert "successfully deleted" in result.lower()
        assert not test_file.exists()

        # Check logging
        assert any(log[0] == "audit_delete" for log in mock_logger.logs)

    def test_delete_nonexistent_file(self, temp_workspace, mock_logger):
        """Test deleting nonexistent file"""
        result = delete_file(temp_workspace, "nonexistent.txt")
        assert "does not exist" in result.lower()

    def test_delete_directory(self, temp_workspace, mock_logger):
        """Test deleting a directory (should fail)"""
        (Path(temp_workspace) / "testdir").mkdir()
        result = delete_file(temp_workspace, "testdir")
        assert "directory" in result.lower()

    def test_delete_outside_workspace(self, temp_workspace, mock_logger):
        """Test deleting outside workspace (should fail)"""
        result = delete_file(temp_workspace, "../../bad.txt")
        assert "outside working directory" in result.lower()


class TestFileOperationsIntegration:
    """Integration tests for file operations"""

    def test_full_workflow(self, temp_workspace, mock_logger):
        """Test complete workflow: list, write, read, delete"""
        # List empty directory
        result = list_directory(temp_workspace, ".")
        assert "empty" in result.lower()

        # Write file
        write_file(temp_workspace, "workflow.txt", "Test content")

        # List directory (should show file)
        result = list_directory(temp_workspace, ".")
        assert "workflow.txt" in result

        # Read file
        result = read_file(temp_workspace, "workflow.txt")
        assert result == "Test content"

        # Delete file
        delete_file(temp_workspace, "workflow.txt")

        # List directory (should be empty)
        result = list_directory(temp_workspace, ".")
        assert "empty" in result.lower()

    def test_nested_structure_creation(self, temp_workspace, mock_logger):
        """Test creating nested file structure"""
        files = [
            os.path.join("src", "main.py"),
            os.path.join("src", "utils", "helpers.py"),
            os.path.join("tests", "test_main.py"),
            "README.md",
        ]

        for file_path in files:
            write_file(temp_workspace, file_path, f"# {file_path}")

        # Verify all files exist
        for file_path in files:
            full_path = Path(temp_workspace) / file_path
            assert full_path.exists()
            assert full_path.read_text(encoding="utf-8") == f"# {file_path}"

        # List directories
        result = list_directory(temp_workspace, ".")
        assert "src" in result
        assert "tests" in result
        assert "README.md" in result


class TestErrorHandling:
    """Test error handling and edge cases"""

    def test_invalid_characters_in_path(self, temp_workspace, mock_logger):
        """Test handling of invalid path characters"""
        # Most OSes handle this, but test anyway
        result = write_file(temp_workspace, "test\x00.txt", "content")
        # Should either work or fail gracefully
        assert isinstance(result, str)

    def test_very_long_filename(self, temp_workspace, mock_logger):
        """Test handling of very long filename"""
        long_name = "a" * 300 + ".txt"
        result = write_file(temp_workspace, long_name, "content")
        # Should either work or fail gracefully with error message
        assert isinstance(result, str)

    def test_special_characters_in_content(self, temp_workspace, mock_logger):
        """Test writing special characters"""
        special_content = "Hello 世界 🌍 \n\t\r Special: @#$%^&*()"

        # Ensure we write with explicit encoding to avoid Windows CP1252 errors
        result = write_file(temp_workspace, "special.txt", special_content)
        assert "successfully wrote" in result.lower()

        read_result = read_file(temp_workspace, "special.txt")

        # This handles the fact that Windows writes \r\n but Python reads \n.
        def normalize(text):
            return text.replace("\r\n", "\n").replace("\r", "\n")

        assert normalize(read_result) == normalize(special_content)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
