from unittest.mock import Mock, patch

import pytest
from pytest import CaptureFixture
import typer

from app import __main__ as main


def test_summary_function_prints_changes(capsys: CaptureFixture[str]) -> None:
    mock_summarize_service = Mock()
    mock_summarize_service.summarize.return_value = "Test summary"

    with (
        patch.object(main.git_service, "get_diff", return_value="test diff"),
        patch("app.__main__.SummarizeService", return_value=mock_summarize_service),
    ):
        main.summary("path", "commitA", "commitB")
    captured = capsys.readouterr()
    assert type(captured.out) is str
    mock_summarize_service.summarize.assert_called_once_with("test diff")


def test_summary_handles_value_error(capsys: CaptureFixture[str]) -> None:
    mock_summarize_service = Mock()
    mock_summarize_service.summarize.side_effect = ValueError("Config error")

    with (
        patch.object(main.git_service, "get_diff", return_value="test diff"),
        patch("app.__main__.SummarizeService", return_value=mock_summarize_service),
        pytest.raises(typer.Exit) as exc_info,
    ):
        main.summary("path", "commitA", "commitB")

    assert exc_info.value.exit_code == 1
    captured = capsys.readouterr()
    assert "Configuration error: Config error" in captured.err


def test_summary_handles_connection_error(capsys: CaptureFixture[str]) -> None:
    mock_summarize_service = Mock()
    mock_summarize_service.summarize.side_effect = ConnectionError("Connection failed")

    with (
        patch.object(main.git_service, "get_diff", return_value="test diff"),
        patch("app.__main__.SummarizeService", return_value=mock_summarize_service),
        pytest.raises(typer.Exit) as exc_info,
    ):
        main.summary("path", "commitA", "commitB")

    assert exc_info.value.exit_code == 1
    captured = capsys.readouterr()
    assert "Connection error: Connection failed" in captured.err


def test_summary_handles_runtime_error(capsys: CaptureFixture[str]) -> None:
    mock_summarize_service = Mock()
    mock_summarize_service.summarize.side_effect = RuntimeError("Runtime error")

    with (
        patch.object(main.git_service, "get_diff", return_value="test diff"),
        patch("app.__main__.SummarizeService", return_value=mock_summarize_service),
        pytest.raises(typer.Exit) as exc_info,
    ):
        main.summary("path", "commitA", "commitB")

    assert exc_info.value.exit_code == 1
    captured = capsys.readouterr()
    assert "Error: Runtime error" in captured.err


def test_summary_handles_unexpected_error(capsys: CaptureFixture[str]) -> None:
    mock_summarize_service = Mock()
    mock_summarize_service.summarize.side_effect = KeyError("Unexpected error")

    with (
        patch.object(main.git_service, "get_diff", return_value="test diff"),
        patch("app.__main__.SummarizeService", return_value=mock_summarize_service),
        pytest.raises(typer.Exit) as exc_info,
    ):
        main.summary("path", "commitA", "commitB")

    assert exc_info.value.exit_code == 1
    captured = capsys.readouterr()
    assert "Unexpected error: 'Unexpected error'" in captured.err


def test_configure_with_empty_api_key(capsys: CaptureFixture[str]) -> None:
    with (
        patch("app.__main__.getpass.getpass", return_value=""),
        pytest.raises(typer.Exit) as exc_info,
    ):
        main.configure("https://api.openai.com/v1", "")

    assert exc_info.value.exit_code == 1
    captured = capsys.readouterr()
    assert "Error: API key cannot be empty" in captured.err


def test_configure_success(capsys: CaptureFixture[str]) -> None:
    with (
        patch("app.__main__.getpass.getpass", return_value="test-key"),
        patch("app.__main__.config.set_model_config") as mock_set_config,
    ):
        main.configure("https://api.openai.com/v1", "gpt-4")

    mock_set_config.assert_called_once_with(
        "https://api.openai.com/v1", "test-key", "gpt-4"
    )
    captured = capsys.readouterr()
    assert "Configuration saved successfully!" in captured.out


def test_configure_handles_exception(capsys: CaptureFixture[str]) -> None:
    with (
        patch("app.__main__.getpass.getpass", return_value="test-key"),
        patch(
            "app.__main__.config.set_model_config", side_effect=Exception("Save failed")
        ),
        pytest.raises(typer.Exit) as exc_info,
    ):
        main.configure("https://api.openai.com/v1", "")

    assert exc_info.value.exit_code == 1
    captured = capsys.readouterr()
    assert "Error saving configuration: Save failed" in captured.err


def test_show_config_when_not_configured(capsys: CaptureFixture[str]) -> None:
    with patch("app.__main__.config.get_model_config", return_value=None):
        main.show_config()

    captured = capsys.readouterr()
    assert (
        "Model is not configured. Use the 'configure' command to set up."
        in captured.out
    )


def test_show_config_with_model_name(capsys: CaptureFixture[str]) -> None:
    config = {
        "api_url": "https://api.openai.com/v1",
        "api_key": "test-key",
        "model_name": "gpt-4",
    }
    with patch("app.__main__.config.get_model_config", return_value=config):
        main.show_config()

    captured = capsys.readouterr()
    assert "API URL: https://api.openai.com/v1" in captured.out
    assert "Model name: gpt-4" in captured.out


def test_show_config_without_model_name(capsys: CaptureFixture[str]) -> None:
    config = {
        "api_url": "https://api.openai.com/v1",
        "api_key": "test-key",
    }
    with patch("app.__main__.config.get_model_config", return_value=config):
        main.show_config()

    captured = capsys.readouterr()
    assert "API URL: https://api.openai.com/v1" in captured.out
    assert "Model name:" not in captured.out
