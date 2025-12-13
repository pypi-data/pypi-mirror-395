"""
Buchi CLI - Command-line interface for AI coding assistant
"""

from pathlib import Path

import typer  # pyright: ignore[reportMissingImports]
from rich.console import Console  # pyright: ignore[reportMissingImports]

# Create Typer app with rich markup support
app = typer.Typer(
    name="buchi",
    help="AI coding assistant powered by Ollama",
    add_completion=False,
    rich_markup_mode="rich",
)

console = Console()


@app.command(name="run")
def run(
    prompt: str = typer.Argument(..., help="Task for the coding agent to perform"),
    working_dir: str = typer.Option(
        ".", "-d", "--dir", help="Working directory for the agent"
    ),
    model: str = typer.Option(
        "qwen3-coder:480b-cloud", "-m", "--model", help="Ollama model to use"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Show detailed execution logs"
    ),
    max_iterations: int = typer.Option(
        50, "--max-iterations", help="Maximum agent iterations (prevents runaway loops)"
    ),
):
    """
    Run Buchi AI coding assistant with a task.

    Example:
        buchi run "Create a login endpoint"
        buchi run "Add tests" --max-iterations 30
    """
    from buchi.agent import run_agent
    from buchi.persistence import JSONStorage

    console.print("[bold blue]Buchi CLI[/bold blue]")
    console.print(f"[dim]Model: {model}[/dim]")
    console.print(f"[dim]Directory: {working_dir}[/dim]")
    console.print(f"[dim]Max iterations: {max_iterations}[/dim]\n")

    # Initialize storage
    storage = JSONStorage(working_dir)

    # Show conversation context
    summary = storage.get_summary()
    if summary["total_messages"] > 0:
        limit = summary["current_limit"]
        total = summary["total_messages"]
        showing = min(limit, total) if limit > 0 else total
        console.print(f"[dim]Context: {showing}/{total} messages[/dim]\n")

    console.print(f"[bold]Task:[/bold] {prompt}\n")

    # Run the agent with max_iterations
    run_agent(prompt, working_dir, storage, model, verbose, max_iterations)


@app.command()
def history(
    working_dir: str = typer.Option(".", "-d", "--dir", help="Working directory"),
    limit: int = typer.Option(None, "-n", help="Number of messages to show"),
    full: bool = typer.Option(False, "--full", help="Show all messages"),
):
    """
    Show conversation history for the current project.

    Example:
        buchi history
        buchi history -n 5
        buchi history --full
    """
    from buchi.persistence import JSONStorage

    storage = JSONStorage(working_dir)

    # Get messages based on options
    if full:
        messages = storage.get_all_messages()
    elif limit:
        messages = storage.get_all_messages()[-limit:]
    else:
        messages = storage.get_all_messages()[-10:]  # Default: last 10

    if not messages:
        console.print("[yellow]No conversation history[/yellow]")
        return

    total = storage.get_message_count()
    console.print(f"[dim]Showing {len(messages)} of {total} messages[/dim]\n")

    # Display messages
    for msg in messages:
        timestamp = msg["timestamp"][:19].replace("T", " ")
        role_color = "green" if msg["role"] == "user" else "blue"
        role_icon = "👤" if msg["role"] == "user" else "🤖"

        console.print(
            f"[{role_color}]{role_icon} {msg['role'].upper()}[/{role_color}] "
            f"[dim]{timestamp}[/dim]"
        )
        console.print(f"{msg['content']}\n")


@app.command()
def clear(
    working_dir: str = typer.Option(".", "-d", "--dir", help="Working directory"),
):
    """
    Clear conversation history for the current project.

    Example:
        buchi clear
    """
    from buchi.persistence import JSONStorage

    storage = JSONStorage(working_dir)
    count = storage.get_message_count()

    if count == 0:
        console.print("[yellow]No history to clear[/yellow]")
        return

    # Confirm before clearing
    confirm = typer.confirm(f"Clear {count} messages from this project?")
    if confirm:
        storage.clear_messages()
        console.print(f"[green]✓ Cleared {count} messages[/green]")
    else:
        console.print("[dim]Cancelled[/dim]")


@app.command()
def limit(
    new_limit: int | None = typer.Argument(
        None, help="New message limit (0 = unlimited)"
    ),
    working_dir: str = typer.Option(".", "-d", "--dir", help="Working directory"),
):
    """
    View or change the message limit for AI context.

    Examples:
        buchi limit          # View current limit
        buchi limit 30       # Set limit to 30 messages
        buchi limit 0        # Set unlimited
    """
    from buchi.persistence import JSONStorage

    storage = JSONStorage(working_dir)

    if new_limit is None:
        # Show current limit
        current = storage.get_message_limit()
        total = storage.get_message_count()

        console.print(
            f"[bold]Current message limit:[/bold] "
            f"{current if current > 0 else 'unlimited'}"
        )
        console.print(f"[bold]Total messages:[/bold] {total}")

        if current > 0 and total > current:
            console.print(
                f"[dim]AI will see the last {current} of {total} messages[/dim]"
            )
        else:
            console.print(f"[dim]AI will see all {total} messages[/dim]")
    else:
        # Set new limit
        try:
            storage.set_message_limit(new_limit)
            limit_text = new_limit if new_limit > 0 else "unlimited"
            console.print(f"[green]✓ Message limit set to: {limit_text}[/green]")
        except ValueError as e:
            console.print(f"[red]Error: {e}[/red]")
            raise typer.Exit(1) from None


@app.command()
def info(working_dir: str = typer.Option(".", "-d", "--dir", help="Working directory")):
    """
    Show conversation statistics for the current project.

    Example:
        buchi info
    """
    from buchi.persistence import JSONStorage

    storage = JSONStorage(working_dir)
    summary = storage.get_summary()

    if summary["total_messages"] == 0:
        console.print("[yellow]No conversation history[/yellow]")
        return

    # Create info display
    console.print("\n[bold blue]📊 Buchi Statistics[/bold blue]\n")
    console.print(f"[bold]Project:[/bold] {Path(working_dir).resolve().name}")
    console.print(f"[bold]Total messages:[/bold] {summary['total_messages']}")
    console.print(
        f"[bold]Message limit:[/bold] "
        f"{summary['current_limit'] if summary['current_limit'] > 0 else 'unlimited'}"
    )
    console.print(
        f"[bold]First interaction:[/bold] {summary['first_interaction'][:10]}"
    )
    console.print(f"[bold]Last interaction:[/bold] {summary['last_interaction'][:10]}")
    console.print(f"\n[dim]Storage: {working_dir}/.buchi/conversations.json[/dim]\n")


@app.command()
def models():
    """
    List available Ollama models.

    Example:
        buchi models
    """
    import subprocess

    try:
        result = subprocess.run(
            ["ollama", "list"], capture_output=True, text=True, check=True
        )

        console.print("[bold]Available Ollama Models:[/bold]\n")
        console.print(result.stdout)
        console.print("[dim]Use with: buchi run 'your task' --model MODEL_NAME[/dim]")

    except subprocess.CalledProcessError:
        console.print("[red]Error: Could not list Ollama models[/red]")
        console.print("Make sure Ollama is installed and running")
        raise typer.Exit(1) from None
    except FileNotFoundError:
        console.print("[red]Error: Ollama not found[/red]")
        console.print("Install from: https://ollama.ai")
        raise typer.Exit(1) from None


@app.command()
def logs(
    working_dir: str = typer.Option(".", "-d", "--dir", help="Working directory"),
    log_type: str = typer.Option(
        "debug", "-t", "--type", help="Log type: debug, audit, or error"
    ),
    lines: int = typer.Option(
        20, "-n", "--lines", help="Number of recent log lines to show"
    ),
    follow: bool = typer.Option(
        False, "-f", "--follow", help="Follow log output (tail -f style)"
    ),
):
    """
    View log files for the current project.

    Examples:
        buchi logs                     # Show last 20 debug logs
        buchi logs -t audit -n 50      # Show last 50 audit logs
        buchi logs -t error            # Show recent errors
        buchi logs -f                  # Follow debug logs in real-time
    """
    import json
    from pathlib import Path

    log_dir = Path(working_dir) / ".buchi" / "logs"
    log_file = log_dir / f"{log_type}.log"

    if not log_file.exists():
        console.print(f"[yellow]No {log_type} logs found[/yellow]")
        console.print("[dim]Run a task first to generate logs[/dim]")
        return

    try:
        if follow:
            # Follow mode (like tail -f)
            import time

            console.print(f"[dim]Following {log_type}.log (Ctrl+C to stop)[/dim]\n")

            with open(log_file) as f:
                # Go to end of file
                f.seek(0, 2)

                while True:
                    line = f.readline()
                    if line:
                        try:
                            log_entry = json.loads(line)
                            timestamp = log_entry.get("timestamp", "")[:19]
                            level = log_entry.get("level", "INFO")
                            message = log_entry.get("message", "")

                            level_colors = {
                                "DEBUG": "dim",
                                "INFO": "blue",
                                "WARNING": "yellow",
                                "ERROR": "red",
                            }
                            color = level_colors.get(level, "white")

                            console.print(
                                f"[{color}]{timestamp} [{level}][/{color}] {message}"
                            )
                        except json.JSONDecodeError:
                            console.print(line.strip())
                    else:
                        time.sleep(0.1)
        else:
            # Show last N lines
            with open(log_file) as f:
                all_lines = f.readlines()

            recent_lines = all_lines[-lines:]

            console.print(
                f"[bold]Last {len(recent_lines)} {log_type} log entries:[/bold]\n"
            )

            for line in recent_lines:
                try:
                    log_entry = json.loads(line)

                    timestamp = log_entry.get("timestamp", "")[:19]
                    level = log_entry.get("level", "INFO")
                    message = log_entry.get("message", "")
                    session_id = log_entry.get("session_id", "")

                    level_colors = {
                        "DEBUG": "dim",
                        "INFO": "blue",
                        "WARNING": "yellow",
                        "ERROR": "red",
                    }
                    color = level_colors.get(level, "white")

                    console.print(
                        f"[{color}]{timestamp} [{level}][/{color}] "
                        f"[dim][{session_id[:8]}][/dim] {message}"
                    )

                    # Show extra data if present
                    if log_entry.get("exception"):
                        console.print(
                            f"[red]  Exception: {log_entry['exception'][:200]}...[/red]"
                        )

                except json.JSONDecodeError:
                    console.print(f"[dim]{line.strip()}[/dim]")

            console.print(f"\n[dim]Full logs: {log_file}[/dim]")

    except KeyboardInterrupt:
        console.print("\n[dim]Stopped following logs[/dim]")
    except Exception as e:
        console.print(f"[red]Error reading logs: {e}[/red]")


@app.command()
def log_stats(
    working_dir: str = typer.Option(".", "-d", "--dir", help="Working directory"),
):
    """
    Show statistics about log files.

    Example:
        buchi log-stats
    """
    from buchi.logging import BuchiLogger

    stats = BuchiLogger.get_log_stats(working_dir)

    if not stats["exists"]:
        console.print("[yellow]No logs found for this project[/yellow]")
        return

    console.print("\n[bold blue]📊 Log Statistics[/bold blue]\n")
    console.print(f"[bold]Log directory:[/bold] {stats['log_dir']}")
    console.print(f"[bold]Total files:[/bold] {stats['total_files']}")
    console.print(f"[bold]Total size:[/bold] {stats['total_size_mb']} MB\n")

    if stats["files"]:
        console.print("[bold]By log type:[/bold]")
        for log_type, info in stats["files"].items():
            console.print(
                f"  {log_type:8} - {info['count']} file(s), {info['size_mb']} MB"
            )

    console.print("\n[dim]View logs with: buchi logs[/dim]")


@app.command()
def log_clean(
    working_dir: str = typer.Option(".", "-d", "--dir", help="Working directory"),
    days: int = typer.Option(
        30, "--days", help="Delete logs older than this many days"
    ),
    all: bool = typer.Option(False, "--all", help="Delete all logs"),
):
    """
    Clean up old log files.

    Examples:
        buchi log-clean              # Delete logs older than 30 days
        buchi log-clean --days 7     # Delete logs older than 7 days
        buchi log-clean --all        # Delete all logs
    """
    from pathlib import Path

    from buchi.logging import BuchiLogger

    if all:
        log_dir = Path(working_dir) / ".buchi" / "logs"
        if not log_dir.exists():
            console.print("[yellow]No logs to clean[/yellow]")
            return

        # Count files
        log_files = list(log_dir.glob("*.log*"))
        count = len(log_files)

        if count == 0:
            console.print("[yellow]No logs to clean[/yellow]")
            return

        # Confirm
        confirm = typer.confirm(f"Delete all {count} log files?")
        if not confirm:
            console.print("[dim]Cancelled[/dim]")
            return

        # Delete all
        for log_file in log_files:
            try:
                log_file.unlink()
            except OSError:
                pass

        console.print(f"[green]✓ Deleted {count} log files[/green]")
    else:
        # Delete old logs
        deleted = BuchiLogger.cleanup_old_logs(working_dir, days)

        if deleted == 0:
            console.print(f"[yellow]No logs older than {days} days found[/yellow]")
        else:
            console.print(
                f"[green]✓ Deleted {deleted} log files older than {days} days[/green]"
            )


@app.command()
def undo(
    count: int = typer.Option(1, "-n", help="Number of operations to undo"),
    working_dir: str = typer.Option(".", "-d", "--dir", help="Working directory"),
):
    """
    Undo recent file operations by restoring from backups.

    Examples:
        buchi undo           # Undo last operation
        buchi undo -n 3      # Undo last 3 operations
    """
    from buchi.backup import BackupManager

    backup_manager = BackupManager(working_dir)
    restored = backup_manager.undo_last_operation(count)

    if not restored:
        console.print("[yellow]No operations to undo[/yellow]")
        return

    console.print(f"[green]✓ Restored {len(restored)} file(s):[/green]")
    for file_path in restored:
        console.print(f"  📄 {file_path}")


@app.command(name="backups")
def backups_list(
    working_dir: str = typer.Option(".", "-d", "--dir", help="Working directory"),
    limit: int = typer.Option(
        10, "-n", "--limit", help="Number of recent backups to show"
    ),
):
    """
    Show backup statistics and storage usage.
    """
    from buchi.backup import BackupManager

    manager = BackupManager(working_dir)
    stats = manager.get_backup_stats()

    if stats["total_backups"] == 0:
        console.print("[yellow]No backups found.[/yellow]")
        return

    # Show Summary
    console.print("\n[bold blue]📦 Backup Storage Stats[/bold blue]\n")
    console.print(f"[bold]Total Backups:[/bold]    {stats['total_backups']}")
    console.print(f"[bold]Storage Used:[/bold]     {stats['total_size_mb']} MB")

    if stats["oldest_backup"]:
        console.print(
            f"[bold]Oldest Backup:[/bold]    {stats['oldest_backup'][:19].replace('T', ' ')}"
        )
        console.print(
            f"[bold]Newest Backup:[/bold]    {stats['newest_backup'][:19].replace('T', ' ')}"
        )

    console.print(f"[dim]Location: {working_dir}/.buchi/backups[/dim]\n")

    # Show Recent
    recent = manager.list_backups(limit=limit)
    console.print(f"[bold]Recent Backups (last {len(recent)}):[/bold]")

    for b in reversed(recent):
        timestamp = b["timestamp"][11:19]  # HH:MM:SS
        operation = b["operation"].upper()
        op_color = "green" if operation == "WRITE" else "red"
        size_kb = round(b["file_size"] / 1024, 1)

        console.print(
            f"  [cyan]{timestamp}[/cyan]  "
            f"[{op_color}]{operation:<6}[/{op_color}] "
            f"{b['file_path']} "
            f"[dim]({size_kb} KB)[/dim]"
        )
    console.print("")


@app.command(name="backup-clean")
def backup_clean(
    working_dir: str = typer.Option(".", "-d", "--dir", help="Working directory"),
    days: int = typer.Option(
        30, "--days", help="Delete backups older than this many days"
    ),
    all: bool = typer.Option(False, "--all", help="Delete ALL backups (dangerous)"),
    force: bool = typer.Option(False, "-f", "--force", help="Skip confirmation"),
):
    """
    Clean up old backups to free up disk space.

    Examples:
        buchi backup-clean              # Delete backups > 30 days old
        buchi backup-clean --days 7     # Delete backups > 7 days old
        buchi backup-clean --all        # Delete EVERYTHING
    """
    from buchi.backup import BackupManager

    manager = BackupManager(working_dir)

    # Get initial size for comparison
    stats_before = manager.get_backup_stats()
    if stats_before["total_backups"] == 0:
        console.print("[yellow]No backups to clean.[/yellow]")
        return

    # Logic for "Delete ALL"
    if all:
        if not force:
            console.print(
                f"[bold red]⚠️  WARNING: You are about to delete ALL {stats_before['total_backups']} backups![/bold red]"
            )
            if not typer.confirm("Are you sure you want to proceed?"):
                console.print("[dim]Aborted.[/dim]")
                return

        # Passing days=0 to cleanup_old_backups usually needs specific handling or very large negative number
        # Depending on your implementation of cleanup_old_backups, verify if days=0 deletes all.
        # Assuming typical logic: passing a huge negative number or special handling in manager.
        # For safety based on your backup.py, let's just loop delete:

        count = 0
        all_backups = manager.list_backups(limit=10000)  # Get all
        for b in all_backups:
            if manager.delete_backup(b["id"]):
                count += 1
        deleted_count = count

    # Logic for "Delete Older Than X Days"
    else:
        if not force:
            console.print(f"Cleaning backups older than [bold]{days} days[/bold]...")

        deleted_count = manager.cleanup_old_backups(days=days)

    # Report results
    if deleted_count == 0:
        console.print(
            f"[yellow]No backups older than {days} days found to delete.[/yellow]"
        )
    else:
        # Calculate space saved
        stats_after = manager.get_backup_stats()
        saved_mb = round(
            stats_before["total_size_mb"] - stats_after["total_size_mb"], 2
        )

        console.print(
            f"\n[green]✓ Successfully deleted {deleted_count} backups.[/green]"
        )
        console.print(f"[bold]Space Reclaimed:[/bold] {saved_mb} MB")
        console.print(f"[dim]Remaining: {stats_after['total_size_mb']} MB[/dim]")


def main():
    """Entry point for the CLI"""
    app()


if __name__ == "__main__":
    main()
