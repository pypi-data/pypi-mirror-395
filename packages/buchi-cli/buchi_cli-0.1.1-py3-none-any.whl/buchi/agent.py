"""
LangGraph agent implementation for Buchi CLI with integrated logging.
Modern agentic workflow using LangGraph's prebuilt ReAct agent.
"""

import difflib
import time
from pathlib import Path

import requests  # pyright: ignore[reportMissingModuleSource]
from langchain_core.messages import (  # pyright: ignore[reportMissingImports]
    AIMessage,
    HumanMessage,
    SystemMessage,
)
from langchain_core.tools import tool  # pyright: ignore[reportMissingImports]
from langchain_ollama import ChatOllama  # pyright: ignore[reportMissingImports]
from langgraph.prebuilt import (  # pyright: ignore[reportMissingImports]
    create_react_agent,  # pyright: ignore[reportMissingImports]
)
from rich.console import Console  # pyright: ignore[reportMissingImports]
from rich.panel import Panel  # pyright: ignore[reportMissingImports]
from rich.prompt import Confirm  # pyright: ignore[reportMissingImports]
from rich.syntax import Syntax  # pyright: ignore[reportMissingImports]

console = Console()


def check_ollama_running() -> bool:
    """Check if Ollama server is running"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def check_model_available(model_name: str) -> bool:
    """Check if the specified model is available in Ollama"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            models = response.json().get("models", [])
            return any(model_name in m.get("name", "") for m in models)
        return False
    except requests.exceptions.RequestException:
        return False


# Global variables
_WORKING_DIR = "."
_LOGGER = None


def set_working_dir(path: str):
    """Set the working directory for file operations"""
    global _WORKING_DIR
    _WORKING_DIR = path


def set_logger(logger):
    """Set the logger instance"""
    global _LOGGER
    _LOGGER = logger
    # Also set logger for file operations
    from buchi.tools.file_ops import set_logger as set_file_logger

    set_file_logger(logger)


# --- NEW HELPER FUNCTION FOR DIFFS ---


def print_diff(file_path: str, old_content: str, new_content: str):
    """Print a colorful diff of the changes using Rich"""
    diff = list(
        difflib.unified_diff(
            old_content.splitlines(keepends=True),
            new_content.splitlines(keepends=True),
            fromfile=f"Original: {file_path}",
            tofile=f"New: {file_path}",
        )
    )

    if not diff:
        console.print(f"[yellow]No changes detected for {file_path}[/yellow]")
        return

    # Create a diff string for syntax highlighting
    diff_text = "".join(diff)

    # Use Rich's Syntax for coloring diffs
    syntax = Syntax(diff_text, "diff", theme="monokai", line_numbers=False)

    console.print("\n[bold cyan]PROPOSED CHANGES:[/bold cyan]")
    console.print(Panel(syntax, title=f"Diff: {file_path}", border_style="blue"))


@tool
def list_directory(directory: str = ".") -> str:
    """List files and folders in a directory. Use '.' for current directory."""
    from buchi.tools.file_ops import list_directory as list_dir_fn

    start_time = time.time()
    result = list_dir_fn(_WORKING_DIR, directory)
    duration = time.time() - start_time

    if _LOGGER:
        _LOGGER.log_performance("list_directory", duration, directory=directory)

    console.print(f"[dim]Listed: {directory}[/dim]")
    return result


@tool
def read_file(file_path: str) -> str:
    """Read the contents of a text file."""
    from buchi.tools.file_ops import read_file as read_file_fn

    start_time = time.time()
    result = read_file_fn(_WORKING_DIR, file_path)
    duration = time.time() - start_time

    if _LOGGER:
        _LOGGER.log_performance("read_file", duration, file_path=file_path)

    console.print(f"[dim]Read: {file_path}[/dim]")
    return result


@tool
def write_file(file_path: str, content: str) -> str:
    """Write or overwrite content to a file. Creates directories if needed."""
    from buchi.tools.file_ops import read_file as read_file_fn
    from buchi.tools.file_ops import validate_path
    from buchi.tools.file_ops import write_file as write_file_fn

    # 1. Validate path first to avoid errors
    valid, _ = validate_path(_WORKING_DIR, file_path)
    if not valid:
        return write_file_fn(_WORKING_DIR, file_path, content)

    # 2. Read existing content to generate diff
    old_content = read_file_fn(_WORKING_DIR, file_path)
    if "Error:" in old_content:
        old_content = ""  # New file

    # 3. INTERACTIVE: Show Diff
    print_diff(file_path, old_content, content)

    # 4. INTERACTIVE: Ask for confirmation
    should_write = Confirm.ask(
        f"[bold yellow]Do you want to apply these changes to {file_path}?[/bold yellow]",
        default=True,
    )

    if not should_write:
        console.print("[red]Action cancelled by user.[/red]")
        if _LOGGER:
            _LOGGER.info("User rejected write_file", file_path=file_path)
        return "Action cancelled by user. Do not try to write this content to this file again."

    # 5. Perform the write if confirmed
    start_time = time.time()
    result = write_file_fn(_WORKING_DIR, file_path, content)
    duration = time.time() - start_time

    if _LOGGER:
        _LOGGER.log_performance(
            "write_file", duration, file_path=file_path, size=len(content)
        )

    # --- CHECK RESULT BEFORE PRINTING SUCCESS ---
    if result.startswith("Error"):
        console.print(f"[bold red]{result}[/bold red]")
    else:
        # Double check file existence to be sure
        abs_path = Path(_WORKING_DIR) / file_path
        if abs_path.exists():
            console.print(f"[green]✓ Wrote: {file_path}[/green]")
        else:
            console.print(f"[bold red]Error: Write reported success but file not found at {abs_path}[/bold red]")

    return result



@tool
def delete_file(file_path: str) -> str:
    """Delete a file."""
    from buchi.tools.file_ops import delete_file as delete_file_fn

    # INTERACTIVE: Confirmation for delete
    console.print(f"\n[bold red]⚠️  AGENT REQUESTS TO DELETE: {file_path}[/bold red]")

    should_delete = Confirm.ask(
        f"[bold yellow]Are you sure you want to DELETE {file_path}?[/bold yellow]",
        default=False,
    )

    if not should_delete:
        console.print("[red]Deletion cancelled by user.[/red]")
        if _LOGGER:
            _LOGGER.info("User rejected delete_file", file_path=file_path)
        return "Action cancelled by user."

    start_time = time.time()
    result = delete_file_fn(_WORKING_DIR, file_path)
    duration = time.time() - start_time

    if _LOGGER:
        _LOGGER.log_performance("delete_file", duration, file_path=file_path)

    # --- CHECK RESULT BEFORE PRINTING SUCCESS ---
    if result.startswith("Error"):
        console.print(f"[bold red]{result}[/bold red]")
    else:
        console.print(f"[dim]Deleted: {file_path}[/dim]")

    return result

# New function to run the agent
def run_agent(
    prompt: str,
    working_dir: str,
    storage,
    model_name: str = "qwen3-coder:480b-cloud",
    verbose: bool = False,
    max_iterations: int = 50,
):
    # Initialize logger
    from buchi.backup import BackupManager
    from buchi.logging import BuchiLogger

    logger = BuchiLogger(working_dir)
    set_logger(logger)

    session_start = time.time()
    logger.start_session(model_name, prompt)

    backup_manager = BackupManager(working_dir)

    from buchi.tools.file_ops import set_backup_manager

    set_backup_manager(backup_manager)

    try:
        # Check if Ollama is running
        if not check_ollama_running():
            # ... [Error handling code] ...
            console.print("[red]Ollama is not running![/red]")
            return

        if not check_model_available(model_name):
            # ... [Error handling code] ...
            console.print(f"[yellow]Model '{model_name}' not found[/yellow]")
            return

        set_working_dir(working_dir)
        logger.info("Working directory set", working_dir=working_dir)

        # Load history
        history_messages = storage.get_messages()

        # Initialize Ollama
        llm = ChatOllama(
            model=model_name, temperature=0.1, base_url="http://localhost:11434"
        )

        # Define tools
        tools = [list_directory, read_file, write_file, delete_file]

        # System Prompt
        system_prompt = f"""You are Buchi, a skilled AI coding assistant with file manipulation capabilities.

Working directory: {working_dir}

Your tools:
- list_directory: Explore project structure and list files
- read_file: Read file contents
- write_file: Create or modify files
- delete_file: Remove files

Best practices:
1. Always explore with list_directory before making changes
2. Read existing files to understand patterns
3. Write clean, well-commented code
4. Explain your actions clearly
5. Use relative paths from working directory

CRITICAL RULES:
1. You CANNOT modify files by just saying you did. You MUST use the `write_file` tool.
2. If you generate code in the chat, it is NOT saved. Call `write_file` to save it.
3. Always explore with `list_directory` before making changes.
4. If you are asked to edit a file, you must first read it, then overwrite it with the full new content using `write_file`.
5. Do not lie. If a tool fails or you didn't call it, do not say you completed the task.

IMPORTANT: After completing the user's request, provide a final summary and STOP.

Complete the user's request using the available tools."""

        agent = create_react_agent(model=llm, tools=tools)

        # Prepare messages
        messages = [SystemMessage(content=system_prompt)]

        # Add history
        context_messages = history_messages[-5:]
        for msg in context_messages:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))

        messages.append(HumanMessage(content=prompt))

        console.print(f"[dim]Starting LangGraph agent with {model_name}...[/dim]")

        # Removed the Live Spinner around the loop because it conflicts with
        # the interactive input (Confirm.ask) needed inside the tools.
        # Instead, print status messages directly.

        agent_start = time.time()
        tool_call_count = 0
        final_response = None
        iteration_count = 0

        # Run the agent stream
        for step in agent.stream(
            {"messages": messages},
            stream_mode="values",
            config={"recursion_limit": max_iterations},
        ):
            iteration_count += 1

            # Print a subtle 'thinking' indicator between steps
            console.print("[dim]Thinking...[/dim]", style="italic cyan")

            if iteration_count >= max_iterations:
                logger.warning(f"Reached max iterations ({max_iterations})")
                final_response = (
                    "Task partially completed. Maximum iteration limit reached."
                )
                break

            if "messages" in step and step["messages"]:
                last_message = step["messages"][-1]

                if hasattr(last_message, "tool_calls") and last_message.tool_calls:
                    tool_call_count += len(last_message.tool_calls)
                    # Tool calls will happen automatically by LangGraph invoking our wrappers
                    # Our wrappers handle the interaction/printing

                if isinstance(last_message, AIMessage):
                    if last_message.content:
                        final_response = last_message.content
                        has_tool_calls = (
                            hasattr(last_message, "tool_calls")
                            and last_message.tool_calls
                        )
                        if not has_tool_calls and final_response:
                            break

        agent_duration = time.time() - agent_start

        if final_response is None:
            final_response = "Task completed successfully."

        logger.log_performance(
            "agent_execution",
            agent_duration,
            tool_calls=tool_call_count,
            iterations=iteration_count,
            response_length=len(final_response),
        )

        storage.add_message("user", prompt)
        storage.add_message("assistant", final_response)
        logger.end_session(success=True, duration_seconds=time.time() - session_start)

        console.print("\n[green]Task completed[/green]\n")
        console.print(final_response)

    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
        logger.warning("Session interrupted by user")
        logger.end_session(success=False, duration_seconds=time.time() - session_start)
    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/red]")
        if _LOGGER:
            _LOGGER.error("Agent execution failed", exception=e)
            _LOGGER.end_session(
                success=False, duration_seconds=time.time() - session_start
            )
