from unittest.mock import patch
from uuid import uuid4
import pytest
from app.services.summarize_service import SummarizeService


def test_formulating_prompt(
    summarize_service: SummarizeService,
) -> None:
    diff = str(uuid4())
    prompt = summarize_service.prepare_prompt(diff)

    assert (
        prompt
        == f"""
            Below is the result of running 'git diff A B'. 
            Please summarize the changes made between these two commits, 
            focusing on modified files, added or removed lines, 
            and any significant functional updates or refactorings.
            Also summarize the changes for each person that contributed.
                
            Rules:
                1. Return only a text with summary
            
            -----------
            {diff}
            -----------
        """
    ), prompt


def test_summarize(
    summarize_service: SummarizeService,
) -> None:
    diff = "diff --git a/file.txt b/file.txt\nindex 83db48f..f735c2d 100644\n--- a/file.txt\n+++ b/file.txt\n@@ -1 +1,2 @@\n-Hello World\n+Hello, World!\n+This is a new line."
    with patch.object(
        summarize_service.agent,
        "invoke",
        return_value="Summary of changes",
    ) as mock_invoke:
        summary = summarize_service.summarize(diff)
        mock_invoke.assert_called_with(summarize_service.prepare_prompt(diff))

    assert isinstance(summary, str)
    assert len(summary) > 0


def test_summarize_handles_connection_error(
    summarize_service: SummarizeService,
) -> None:
    """Test that APIConnectionError is converted to ConnectionError."""
    diff = "test diff"

    class APIConnectionError(Exception):
        pass

    connection_error = APIConnectionError("Failed to connect")

    with patch.object(
        summarize_service.agent,
        "invoke",
        side_effect=connection_error,
    ):
        with pytest.raises(ConnectionError) as exc_info:
            summarize_service.summarize(diff)

        assert "Failed to connect to API" in str(exc_info.value)
        assert "API URL is correct" in str(exc_info.value)


def test_summarize_handles_connection_error_by_type_name(
    summarize_service: SummarizeService,
) -> None:
    """Test that exceptions with 'Connection' in type name are converted to ConnectionError."""
    diff = "test diff"

    class ConnectionTimeoutError(Exception):
        pass

    connection_error = ConnectionTimeoutError("Connection failed")

    with patch.object(
        summarize_service.agent,
        "invoke",
        side_effect=connection_error,
    ):
        with pytest.raises(ConnectionError) as exc_info:
            summarize_service.summarize(diff)

        assert "Failed to connect to API" in str(exc_info.value)


def test_summarize_handles_authentication_error(
    summarize_service: SummarizeService,
) -> None:
    """Test that AuthenticationError is converted to ValueError."""
    diff = "test diff"

    class AuthenticationError(Exception):
        pass

    auth_error = AuthenticationError("Invalid key")

    with patch.object(
        summarize_service.agent,
        "invoke",
        side_effect=auth_error,
    ):
        with pytest.raises(ValueError) as exc_info:
            summarize_service.summarize(diff)

        assert "Authentication failed" in str(exc_info.value)
        assert "Use 'configure' command" in str(exc_info.value)


def test_summarize_handles_401_error(summarize_service: SummarizeService) -> None:
    """Test that 401 error is converted to ValueError."""
    diff = "test diff"
    auth_error = Exception("401 Unauthorized")

    with patch.object(
        summarize_service.agent,
        "invoke",
        side_effect=auth_error,
    ):
        with pytest.raises(ValueError) as exc_info:
            summarize_service.summarize(diff)

        assert "Authentication failed" in str(exc_info.value)


def test_summarize_handles_403_error(summarize_service: SummarizeService) -> None:
    """Test that 403 error is converted to ValueError."""
    diff = "test diff"
    auth_error = Exception("403 Forbidden")

    with patch.object(
        summarize_service.agent,
        "invoke",
        side_effect=auth_error,
    ):
        with pytest.raises(ValueError) as exc_info:
            summarize_service.summarize(diff)

        assert "Authentication failed" in str(exc_info.value)


def test_summarize_handles_api_error(summarize_service: SummarizeService) -> None:
    """Test that APIError is converted to RuntimeError."""
    diff = "test diff"

    class APIError(Exception):
        pass

    api_error = APIError("Bad request")

    with patch.object(
        summarize_service.agent,
        "invoke",
        side_effect=api_error,
    ):
        with pytest.raises(RuntimeError) as exc_info:
            summarize_service.summarize(diff)

        assert "API error occurred" in str(exc_info.value)
        assert "API URL and model name are correct" in str(exc_info.value)


def test_summarize_handles_400_error(summarize_service: SummarizeService) -> None:
    """Test that 400 error is converted to RuntimeError."""
    diff = "test diff"
    api_error = Exception("400 Bad Request")

    with patch.object(
        summarize_service.agent,
        "invoke",
        side_effect=api_error,
    ):
        with pytest.raises(RuntimeError) as exc_info:
            summarize_service.summarize(diff)

        assert "API error occurred" in str(exc_info.value)


def test_summarize_handles_429_error(summarize_service: SummarizeService) -> None:
    """Test that 429 error is converted to RuntimeError."""
    diff = "test diff"
    api_error = Exception("429 Too Many Requests")

    with patch.object(
        summarize_service.agent,
        "invoke",
        side_effect=api_error,
    ):
        with pytest.raises(RuntimeError) as exc_info:
            summarize_service.summarize(diff)

        assert "API error occurred" in str(exc_info.value)


def test_summarize_reraises_value_error(summarize_service: SummarizeService) -> None:
    """Test that ValueError is re-raised as-is."""
    diff = "test diff"
    value_error = ValueError("Original value error")

    with patch.object(
        summarize_service.agent,
        "invoke",
        side_effect=value_error,
    ):
        with pytest.raises(ValueError, match="Original value error"):
            summarize_service.summarize(diff)


def test_summarize_handles_other_errors(summarize_service: SummarizeService) -> None:
    """Test that other errors are converted to RuntimeError."""
    diff = "test diff"
    other_error = KeyError("Something went wrong")

    with patch.object(
        summarize_service.agent,
        "invoke",
        side_effect=other_error,
    ):
        with pytest.raises(RuntimeError) as exc_info:
            summarize_service.summarize(diff)

        assert "An error occurred while generating summary" in str(exc_info.value)
        assert "Something went wrong" in str(exc_info.value)
