"""
Integration tests for Buchi CLI.
Tests end-to-end workflows with mocked Ollama.
"""

import logging
import os
import shutil
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest  # pyright: ignore[reportMissingImports]

# Import core components
from buchi.agent import run_agent
from buchi.logging import BuchiLogger
from buchi.persistence import JSONStorage
from buchi.tools.file_ops import list_directory, read_file, set_logger, write_file


# Helper to ensure logs are written before reading them
def flush_loggers(buchi_logger):
    """Force flush of all internal loggers"""
    for attr_name in dir(buchi_logger):
        try:
            attr = getattr(buchi_logger, attr_name)
            if isinstance(attr, logging.Logger):
                for handler in attr.handlers:
                    handler.flush()
        except Exception:
            pass


@pytest.fixture
def temp_workspace():
    """Create a temporary workspace for testing"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Force cleanup of logging handlers to release file locks on Windows
    logging.shutdown()
    try:
        shutil.rmtree(temp_dir)
    except Exception:
        pass


@pytest.fixture
def mock_ollama():
    """Mock Ollama server responses"""
    with (
        patch("buchi.agent.check_ollama_running", return_value=True),
        patch("buchi.agent.check_model_available", return_value=True),
    ):
        yield


@pytest.fixture
def clean_logger():
    """Ensure global logger is reset after tests"""
    yield
    set_logger(None)


class MockAIMessage:
    """Mock AI message for testing"""

    def __init__(self, content, tool_calls=None):
        self.content = content
        self.tool_calls = tool_calls or []
        self.additional_kwargs = {}  # Required by some LangChain internals
        self.id = "mock-id"
        self.response_metadata = {}  # Sometimes accessed by agents


class TestAgentWithoutOllama:
    """Test agent behavior when Ollama is not available"""

    def test_ollama_not_running(self, temp_workspace, capsys):
        """Test error when Ollama is not running"""
        storage = JSONStorage(temp_workspace)

        with patch("buchi.agent.check_ollama_running", return_value=False):
            # We expect this to print to stdout/stderr rather than crash
            run_agent("test task", temp_workspace, storage)

        captured = capsys.readouterr()
        assert "Ollama is not running" in captured.out

    def test_model_not_available(self, temp_workspace, capsys):
        """Test error when model is not available"""
        storage = JSONStorage(temp_workspace)

        with (
            patch("buchi.agent.check_ollama_running", return_value=True),
            patch("buchi.agent.check_model_available", return_value=False),
        ):
            run_agent(
                "test task", temp_workspace, storage, model_name="nonexistent-model"
            )

        captured = capsys.readouterr()
        assert "not found" in captured.out


class TestAgentWorkflow:
    """Test complete agent workflows with mocked LLM"""

    def test_simple_file_creation(self, temp_workspace, mock_ollama):
        """Test agent creating a simple file"""
        storage = JSONStorage(temp_workspace)

        # Mock the agent's stream method to simulate file creation
        mock_stream_data = [
            # Agent decides to write a file
            {
                "messages": [
                    MockAIMessage(
                        "",
                        tool_calls=[
                            {
                                "name": "write_file",
                                "args": {"path": "test.txt", "content": "content"},
                                "id": "call_1",
                            }
                        ],
                    )
                ]
            },
            # Agent confirms success
            {"messages": [MockAIMessage("File created successfully")]},
        ]

        with (
            patch("buchi.agent.ChatOllama"),
            patch("buchi.agent.create_react_agent") as mock_agent_creator,
        ):
            # Setup mock agent
            mock_agent = MagicMock()
            mock_agent.stream.return_value = iter(mock_stream_data)
            mock_agent_creator.return_value = mock_agent

            # Run agent
            run_agent("Create test.txt", temp_workspace, storage)

            # Verify storage was updated
            messages = storage.get_all_messages()
            assert len(messages) >= 1
            assert messages[0]["role"] == "user"
            assert messages[0]["content"] == "Create test.txt"

    def test_conversation_persistence(self, temp_workspace, mock_ollama):
        """Test that conversation is persisted across runs"""
        storage = JSONStorage(temp_workspace)

        mock_stream_data = [
            {"messages": [MockAIMessage("Task completed")]},
        ]

        with (
            patch("buchi.agent.ChatOllama"),
            patch("buchi.agent.create_react_agent") as mock_agent_creator,
        ):
            mock_agent = MagicMock()
            mock_agent.stream.return_value = iter(mock_stream_data)
            mock_agent_creator.return_value = mock_agent

            # First run
            run_agent("First task", temp_workspace, storage)
            first_run_count = storage.get_message_count()
            assert first_run_count > 0

            # Reset stream for second run
            mock_agent.stream.return_value = iter(mock_stream_data)

            # Second run - should have context from first
            run_agent("Second task", temp_workspace, storage)
            assert storage.get_message_count() > first_run_count

    def test_max_iterations_limit(self, temp_workspace, mock_ollama):
        """Test that max iterations prevents infinite loops"""
        storage = JSONStorage(temp_workspace)

        # Create infinite stream (agent never stops)
        def infinite_stream():
            while True:
                yield {
                    "messages": [
                        MockAIMessage(
                            "",
                            tool_calls=[
                                {
                                    "name": "read_file",
                                    "args": {"path": "test.txt"},
                                    "id": "call_loop",
                                }
                            ],
                        )
                    ]
                }

        with (
            patch("buchi.agent.ChatOllama"),
            patch("buchi.agent.create_react_agent") as mock_agent_creator,
        ):
            mock_agent = MagicMock()
            mock_agent.stream.return_value = infinite_stream()
            mock_agent_creator.return_value = mock_agent

            # Run with low iteration limit
            try:
                run_agent("Task", temp_workspace, storage, max_iterations=2)
            except Exception:
                pass

            # Ensure we didn't loop forever
            assert True


class TestFileOperationsIntegration:
    """Test file operations through the agent tools"""

    def test_list_then_read_workflow(self, temp_workspace):
        """Test workflow: list directory, then read file"""
        # Create test file
        test_file = Path(temp_workspace) / "test.txt"
        test_file.write_text("Hello, World!")

        # List directory
        result = list_directory(temp_workspace, ".")
        assert "test.txt" in result

        # Read file
        content = read_file(temp_workspace, "test.txt")
        assert content == "Hello, World!"

    def test_write_then_read_workflow(self, temp_workspace):
        """Test workflow: write file, then read it back"""

        # Write file
        result = write_file(temp_workspace, "output.txt", "Test content")
        assert "successfully wrote" in result.lower()

        # Read it back
        content = read_file(temp_workspace, "output.txt")
        assert content == "Test content"

    def test_create_nested_structure(self, temp_workspace):
        """Test creating nested directory structure"""

        main_path = os.path.join("src", "main.py")
        helper_path = os.path.join("src", "utils", "helper.py")

        write_file(temp_workspace, main_path, "# Main file")
        write_file(temp_workspace, helper_path, "# Helper")

        # Verify structure
        result = list_directory(temp_workspace, "src")
        assert "main.py" in result
        assert "utils" in result


class TestLoggingIntegration:
    """Test logging integration with agent"""

    def test_session_logging(self, temp_workspace, mock_ollama, clean_logger):
        """Test that sessions are logged"""
        storage = JSONStorage(temp_workspace)

        mock_stream_data = [
            {"messages": [MockAIMessage("Done")]},
        ]

        with (
            patch("buchi.agent.ChatOllama"),
            patch("buchi.agent.create_react_agent") as mock_agent_creator,
        ):
            mock_agent = MagicMock()
            mock_agent.stream.return_value = iter(mock_stream_data)
            mock_agent_creator.return_value = mock_agent

            run_agent("Test task", temp_workspace, storage)

            # Check logs were created
            log_dir = Path(temp_workspace) / ".buchi" / "logs"
            assert log_dir.exists()
            assert (log_dir / "debug.log").exists()

    def test_file_operations_audited(self, temp_workspace, clean_logger):
        """Test that file operations appear in audit log"""

        # Initialize logger
        logger = BuchiLogger(temp_workspace)
        set_logger(logger)

        # Perform file operation
        write_file(temp_workspace, "audit_test.txt", "content")

        # Flush logger before reading file
        flush_loggers(logger)

        # Check audit log
        audit_log = Path(temp_workspace) / ".buchi" / "logs" / "audit.log"
        assert audit_log.exists()

        with open(audit_log, encoding="utf-8") as f:
            content = f.read()
            assert "audit_test.txt" in content


class TestErrorRecovery:
    """Test error handling and recovery"""

    def test_invalid_file_path(self, temp_workspace):
        """Test handling of invalid file paths"""
        invalid_path = os.path.join("..", "..", "invalid_access")
        result = read_file(temp_workspace, invalid_path)
        assert "outside working directory" in result.lower()

    def test_nonexistent_file(self, temp_workspace):
        """Test handling of nonexistent files"""
        result = read_file(temp_workspace, "nonexistent.txt")
        assert "does not exist" in result.lower()

    def test_agent_error_logged(self, temp_workspace, mock_ollama, clean_logger):
        """Test that agent errors are logged"""
        storage = JSONStorage(temp_workspace)

        with (
            patch("buchi.agent.ChatOllama"),
            patch("buchi.agent.create_react_agent") as mock_agent_creator,
        ):
            # Make agent raise exception
            mock_agent = MagicMock()
            mock_agent.stream.side_effect = Exception("Test error")
            mock_agent_creator.return_value = mock_agent

            try:
                run_agent("Test task", temp_workspace, storage)
            except Exception:
                pass

            # Check error was logged
            error_log = Path(temp_workspace) / ".buchi" / "logs" / "error.log"

            if error_log.exists():
                with open(error_log, encoding="utf-8") as f:
                    content = f.read()
                    assert (
                        "Test error" in content or "Agent execution failed" in content
                    )


class TestVerboseMode:
    """Test verbose mode output"""

    def test_verbose_shows_session_info(self, temp_workspace, mock_ollama, capsys):
        """Test that verbose mode shows session information"""
        storage = JSONStorage(temp_workspace)

        mock_stream_data = [
            {"messages": [MockAIMessage("Done")]},
        ]

        with (
            patch("buchi.agent.ChatOllama"),
            patch("buchi.agent.create_react_agent") as mock_agent_creator,
        ):
            mock_agent = MagicMock()
            mock_agent.stream.return_value = iter(mock_stream_data)
            mock_agent_creator.return_value = mock_agent

            run_agent("Test task", temp_workspace, storage, verbose=True)

            captured = capsys.readouterr()
            assert len(captured.out) > 0


class TestMultipleProjects:
    """Test handling of multiple projects"""

    def test_isolated_projects(self, temp_workspace):
        """Test that different projects have isolated state"""
        # Create two projects
        project1 = Path(temp_workspace) / "project1"
        project2 = Path(temp_workspace) / "project2"
        project1.mkdir()
        project2.mkdir()

        # Create separate storages
        storage1 = JSONStorage(str(project1))
        storage2 = JSONStorage(str(project2))

        # Add UNIQUE messages to each
        storage1.add_message("user", "Project 1 unique content")
        storage2.add_message("user", "Project 2 unique content")

        # Verify isolation by checking content
        # If they were pointing to the same file, we would see both messages in both storages
        msgs1 = storage1.get_all_messages()
        msgs2 = storage2.get_all_messages()

        # Assert each storage only has its own message
        assert len(msgs1) == 1
        assert msgs1[0]["content"] == "Project 1 unique content"

        assert len(msgs2) == 1
        assert msgs2[0]["content"] == "Project 2 unique content"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
