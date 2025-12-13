"""
Core file operation tools for Buchi CLI with integrated logging.
Provides safe file manipulation within working directory boundaries.
"""

from pathlib import Path
from typing import Optional

# Global logger instance (set by agent)
_logger: Optional["BuchiLogger"] = None  # pyright: ignore[reportUndefinedVariable]  # noqa: F821
_backup_manager: Optional["BackupManager"] = None  # pyright: ignore[reportUndefinedVariable]  # noqa: F821


def set_logger(logger):
    """Set the logger instance for file operations"""
    global _logger
    _logger = logger


def set_backup_manager(backup_manager):
    """Set the backup manager instance"""
    global _backup_manager
    _backup_manager = backup_manager


def validate_path(working_dir: str, file_path: str) -> tuple[bool, str]:
    """
    Ensure file_path is within working_dir boundaries.

    Args:
        working_dir: Base directory for all operations
        file_path: Target file path (relative or absolute)

    Returns:
        Tuple of (is_valid, resolved_path_or_error_message)
    """
    try:
        abs_working = Path(working_dir).resolve()
        abs_target = (Path(working_dir) / file_path).resolve()

        # Check if target is within working directory
        if not abs_target.is_relative_to(abs_working):
            error_msg = f'Error: "{file_path}" is outside working directory'
            if _logger:
                _logger.warning(
                    "Path validation failed",
                    file_path=file_path,
                    reason="outside_boundary",
                )
            return False, error_msg

        return True, str(abs_target)
    except Exception as e:
        error_msg = f"Error validating path: {str(e)}"
        if _logger:
            _logger.error("Path validation exception", exception=e, file_path=file_path)
        return False, error_msg


def list_directory(working_dir: str, directory: str = ".") -> str:
    """
    List files and directories in the specified path.

    Args:
        working_dir: Base directory
        directory: Directory to list (relative to working_dir)

    Returns:
        String containing directory listing or error message
    """
    if _logger:
        _logger.debug(f"Listing directory: {directory}")

    valid, result = validate_path(working_dir, directory)
    if not valid:
        return result

    try:
        abs_path = Path(result)

        if not abs_path.exists():
            error_msg = f'Error: "{directory}" does not exist'
            if _logger:
                _logger.audit_tool_call(
                    "list_directory", {"directory": directory}, success=False
                )
            return error_msg

        if not abs_path.is_dir():
            error_msg = f'Error: "{directory}" is not a directory'
            if _logger:
                _logger.audit_tool_call(
                    "list_directory", {"directory": directory}, success=False
                )
            return error_msg

        # Get all items in directory
        items = []
        for item in sorted(abs_path.iterdir()):
            item_type = "dir" if item.is_dir() else "file"
            size = item.stat().st_size if item.is_file() else "-"
            items.append(f"  {item_type:4} | {str(size):>10} bytes | {item.name}")

        if _logger:
            _logger.audit_tool_call(
                "list_directory",
                {"directory": directory, "item_count": len(items)},
                success=True,
            )

        if not items:
            return f'Directory "{directory}" is empty'

        header = (
            f'Contents of "{directory}":\n  Type | Size       | Name\n  ' + "-" * 50
        )
        return header + "\n" + "\n".join(items)

    except PermissionError:
        error_msg = f'Error: Permission denied accessing "{directory}"'
        if _logger:
            _logger.error(
                "Permission denied", operation="list_directory", directory=directory
            )
            _logger.audit_tool_call(
                "list_directory", {"directory": directory}, success=False
            )
        return error_msg
    except Exception as e:
        error_msg = f"Error listing directory: {str(e)}"
        if _logger:
            _logger.error("List directory failed", exception=e, directory=directory)
            _logger.audit_tool_call(
                "list_directory", {"directory": directory}, success=False
            )
        return error_msg


def read_file(working_dir: str, file_path: str, max_chars: int = 100000) -> str:
    """
    Read and return file contents.

    Args:
        working_dir: Base directory
        file_path: File to read (relative to working_dir)
        max_chars: Maximum characters to read (prevents token overflow)

    Returns:
        File contents or error message
    """
    if _logger:
        _logger.debug(f"Reading file: {file_path}")

    valid, result = validate_path(working_dir, file_path)
    if not valid:
        if _logger:
            _logger.audit_file_read(file_path, success=False, error=result)
        return result

    try:
        abs_path = Path(result)

        if not abs_path.exists():
            error_msg = f'Error: "{file_path}" does not exist'
            if _logger:
                _logger.audit_file_read(
                    file_path, success=False, error="file_not_found"
                )
            return error_msg

        if not abs_path.is_file():
            error_msg = f'Error: "{file_path}" is not a file'
            if _logger:
                _logger.audit_file_read(file_path, success=False, error="not_a_file")
            return error_msg

        # Read file with encoding handling
        try:
            content = abs_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            error_msg = (
                f'Error: "{file_path}" is not a text file (binary content detected)'
            )
            if _logger:
                _logger.audit_file_read(file_path, success=False, error="binary_file")
            return error_msg

        # Track if truncated
        was_truncated = len(content) > max_chars

        # Truncate if too large
        if was_truncated:
            content = content[:max_chars]
            content += f"\n\n[... Content truncated at {max_chars} characters ...]"

        if _logger:
            _logger.audit_file_read(file_path, success=True)
            _logger.debug(
                f"File read complete: {file_path}",
                size_chars=len(content),
                truncated=was_truncated,
            )

        return content

    except PermissionError:
        error_msg = f'Error: Permission denied reading "{file_path}"'
        if _logger:
            _logger.error(
                "Permission denied", operation="read_file", file_path=file_path
            )
            _logger.audit_file_read(file_path, success=False, error="permission_denied")
        return error_msg
    except Exception as e:
        error_msg = f"Error reading file: {str(e)}"
        if _logger:
            _logger.error("Read file failed", exception=e, file_path=file_path)
            _logger.audit_file_read(file_path, success=False, error=str(e))
        return error_msg


def write_file(working_dir: str, file_path: str, content: str) -> str:
    """
    Write content to a file (creates or overwrites).

    Args:
        working_dir: Base directory
        file_path: File to write (relative to working_dir)
        content: Content to write

    Returns:
        Success message or error message
    """
    if _logger:
        _logger.debug(f"Writing file: {file_path}", size_chars=len(content))

    valid, result = validate_path(working_dir, file_path)
    if not valid:
        if _logger:
            _logger.audit_file_write(
                file_path, len(content), success=False, error=result
            )
        return result

    try:
        abs_path = Path(result)

        # Add backup BEFORE writing (if file exists)
        backup_id = None
        if abs_path.exists() and _backup_manager:
            backup_id = _backup_manager.create_backup(
                file_path,
                operation="write",
                session_id=_logger.get_session_id() if _logger else None,
            )
            if backup_id and _logger:
                _logger.debug(f"Created backup: {backup_id}", file=file_path)

        # Create parent directories if they don't exist
        abs_path.parent.mkdir(parents=True, exist_ok=True)

        # Write content
        abs_path.write_text(content, encoding="utf-8")

        # Get file size
        file_size = abs_path.stat().st_size

        if _logger:
            _logger.audit_file_write(file_path, file_size, success=True)
            _logger.debug(f"File write complete: {file_path}", size_bytes=file_size)

        # Return success message
        lines = content.count("\n") + 1
        chars = len(content)
        msg = (
            f'✓ Successfully wrote {chars} characters ({lines} lines) to "{file_path}"'
        )

        # Add backup info to message
        if backup_id:
            msg += f"\n  💾 Backup: {backup_id}"

        return msg

    except PermissionError:
        error_msg = f'Error: Permission denied writing to "{file_path}"'
        if _logger:
            _logger.error(
                "Permission denied", operation="write_file", file_path=file_path
            )
            _logger.audit_file_write(
                file_path, len(content), success=False, error="permission_denied"
            )
        return error_msg
    except Exception as e:
        error_msg = f"Error writing file: {str(e)}"
        if _logger:
            _logger.error("Write file failed", exception=e, file_path=file_path)
            _logger.audit_file_write(
                file_path, len(content), success=False, error=str(e)
            )
        return error_msg


def delete_file(working_dir: str, file_path: str) -> str:
    """
    Delete a file.

    Args:
        working_dir: Base directory
        file_path: File to delete (relative to working_dir)

    Returns:
        Success message or error message
    """
    if _logger:
        _logger.debug(f"Deleting file: {file_path}")

    valid, result = validate_path(working_dir, file_path)
    if not valid:
        if _logger:
            _logger.audit_file_delete(file_path, success=False, error=result)
        return result

    try:
        abs_path = Path(result)

        if not abs_path.exists():
            error_msg = f'Error: "{file_path}" does not exist'
            if _logger:
                _logger.audit_file_delete(
                    file_path, success=False, error="file_not_found"
                )
            return error_msg

        if abs_path.is_dir():
            error_msg = f'Error: "{file_path}" is a directory. Use a file manager to delete directories.'
            if _logger:
                _logger.audit_file_delete(
                    file_path, success=False, error="is_directory"
                )
            return error_msg

        # Add backup BEFORE deleting
        backup_id = None
        if _backup_manager:
            backup_id = _backup_manager.create_backup(
                file_path,
                operation="delete",
                session_id=_logger.get_session_id() if _logger else None,
            )
            if backup_id and _logger:
                _logger.debug(
                    f"Created backup before delete: {backup_id}", file=file_path
                )

        # Delete the file
        abs_path.unlink()

        if _logger:
            _logger.audit_file_delete(file_path, success=True)
            _logger.debug(f"File delete complete: {file_path}")

        msg = f'✓ Successfully deleted "{file_path}"'

        # Add backup info
        if backup_id:
            msg += f"\n  💾 Backup: {backup_id} (restore with: buchi undo)"

        return msg

    except PermissionError:
        error_msg = f'Error: Permission denied deleting "{file_path}"'
        if _logger:
            _logger.error(
                "Permission denied", operation="delete_file", file_path=file_path
            )
            _logger.audit_file_delete(
                file_path, success=False, error="permission_denied"
            )
        return error_msg
    except Exception as e:
        error_msg = f"Error deleting file: {str(e)}"
        if _logger:
            _logger.error("Delete file failed", exception=e, file_path=file_path)
            _logger.audit_file_delete(file_path, success=False, error=str(e))
        return error_msg
