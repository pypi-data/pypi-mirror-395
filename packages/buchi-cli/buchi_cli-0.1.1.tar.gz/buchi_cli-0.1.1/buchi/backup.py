"""
Backup and rollback system for Buchi CLI.
Automatically backs up files before modifications and allows undo.
"""

import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path


class BackupManager:
    """Manages file backups and rollback operations"""

    def __init__(self, working_dir: str):
        """
        Initialize backup manager.

        Args:
            working_dir: Project directory
        """
        self.working_dir = Path(working_dir).resolve()
        self.backup_dir = self.working_dir / ".buchi" / "backups"
        self.backup_index = self.backup_dir / "index.json"

        # Create backup directory
        self.backup_dir.mkdir(parents=True, exist_ok=True)

        # Initialize index
        if not self.backup_index.exists():
            self._save_index([])

    def _save_index(self, backups: list[dict]):
        """Save backup index"""
        with open(self.backup_index, "w") as f:
            json.dump({"backups": backups}, f, indent=2)

    def _load_index(self) -> list[dict]:
        """Load backup index"""
        try:
            with open(self.backup_index) as f:
                data = json.load(f)
                return data.get("backups", [])
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _get_file_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of file content"""
        if not file_path.exists() or not file_path.is_file():
            return ""

        md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            md5.update(f.read())
        return md5.hexdigest()

    def create_backup(
        self, file_path: str, operation: str, session_id: str = None
    ) -> str | None:
        """
        Create a backup before modifying/deleting a file.

        Args:
            file_path: Relative path to file
            operation: Type of operation (write, delete)
            session_id: Optional session ID for grouping

        Returns:
            Backup ID or None if file doesn't exist
        """
        abs_path = self.working_dir / file_path

        # Only backup if file exists
        if not abs_path.exists() or not abs_path.is_file():
            return None

        # Generate backup ID
        timestamp = datetime.now().isoformat()
        backup_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hashlib.md5(file_path.encode()).hexdigest()[:8]}"

        # Create backup file
        backup_file = self.backup_dir / backup_id
        shutil.copy2(abs_path, backup_file)

        # Calculate hash
        file_hash = self._get_file_hash(abs_path)

        # Add to index
        backups = self._load_index()
        backup_entry = {
            "id": backup_id,
            "file_path": file_path,
            "operation": operation,
            "timestamp": timestamp,
            "session_id": session_id,
            "file_size": abs_path.stat().st_size,
            "file_hash": file_hash,
            "backup_file": str(backup_file.name),
        }
        backups.append(backup_entry)
        self._save_index(backups)

        return backup_id

    def restore_backup(self, backup_id: str) -> bool:
        """
        Restore a file from backup.

        Args:
            backup_id: ID of backup to restore

        Returns:
            True if successful, False otherwise
        """
        backups = self._load_index()

        # Find backup
        backup = next((b for b in backups if b["id"] == backup_id), None)
        if not backup:
            return False

        # Restore file
        backup_file = self.backup_dir / backup["backup_file"]
        if not backup_file.exists():
            return False

        target_path = self.working_dir / backup["file_path"]
        target_path.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(backup_file, target_path)
        return True

    def undo_last_operation(self, count: int = 1) -> list[str]:
        """
        Undo the last N operations.

        Args:
            count: Number of operations to undo

        Returns:
            list of restored file paths
        """
        backups = self._load_index()
        if not backups:
            return []

        # Get last N backups
        to_restore = backups[-count:]
        restored = []

        for backup in reversed(to_restore):
            if self.restore_backup(backup["id"]):
                restored.append(backup["file_path"])

        return restored

    def undo_session(self, session_id: str) -> list[str]:
        """
        Undo all operations from a specific session.

        Args:
            session_id: Session ID to undo

        Returns:
            list of restored file paths
        """
        backups = self._load_index()
        session_backups = [b for b in backups if b.get("session_id") == session_id]

        restored = []
        for backup in reversed(session_backups):
            if self.restore_backup(backup["id"]):
                restored.append(backup["file_path"])

        return restored

    def list_backups(self, limit: int = 10, session_id: str = None) -> list[dict]:
        """
        list recent backups.

        Args:
            limit: Maximum number of backups to return
            session_id: Filter by session ID

        Returns:
            list of backup entries
        """
        backups = self._load_index()

        if session_id:
            backups = [b for b in backups if b.get("session_id") == session_id]

        return backups[-limit:]

    def get_backup_stats(self) -> dict:
        """
        Get backup statistics.

        Returns:
            dictionary with backup stats
        """
        backups = self._load_index()

        if not backups:
            return {
                "total_backups": 0,
                "total_size_bytes": 0,
                "total_size_mb": 0.0,
                "oldest_backup": None,
                "newest_backup": None,
            }

        total_size = sum(
            (self.backup_dir / b["backup_file"]).stat().st_size
            for b in backups
            if (self.backup_dir / b["backup_file"]).exists()
        )

        return {
            "total_backups": len(backups),
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "oldest_backup": backups[0]["timestamp"],
            "newest_backup": backups[-1]["timestamp"],
        }

    def cleanup_old_backups(self, days: int = 30) -> int:
        """
        Delete backups older than specified days.

        Args:
            days: Delete backups older than this many days

        Returns:
            Number of backups deleted
        """
        from datetime import datetime, timedelta

        backups = self._load_index()
        cutoff = datetime.now() - timedelta(days=days)

        to_keep = []
        deleted = 0

        for backup in backups:
            backup_time = datetime.fromisoformat(backup["timestamp"])
            if backup_time > cutoff:
                to_keep.append(backup)
            else:
                # Delete backup file
                backup_file = self.backup_dir / backup["backup_file"]
                if backup_file.exists():
                    backup_file.unlink()
                    deleted += 1

        self._save_index(to_keep)
        return deleted

    def delete_backup(self, backup_id: str) -> bool:
        """
        Delete a specific backup.

        Args:
            backup_id: ID of backup to delete

        Returns:
            True if successful
        """
        backups = self._load_index()

        # Find and remove backup
        backup = next((b for b in backups if b["id"] == backup_id), None)
        if not backup:
            return False

        # Delete file
        backup_file = self.backup_dir / backup["backup_file"]
        if backup_file.exists():
            backup_file.unlink()

        # Update index
        backups = [b for b in backups if b["id"] != backup_id]
        self._save_index(backups)

        return True
