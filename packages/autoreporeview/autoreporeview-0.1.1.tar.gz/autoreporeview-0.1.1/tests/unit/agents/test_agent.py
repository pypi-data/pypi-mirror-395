from unittest.mock import Mock, patch
from app.agents.agent import Agent


def test_invoke_returns_string(agent: Agent) -> None:
    with patch.object(agent.agent, "invoke") as mock_invoke:
        mock_invoke.return_value = {
            "messages": [Mock(content="Hello! I'm doing well, thank you for asking.")]
        }

        response = agent.invoke("Hello, how are you?")

    assert response == "Hello! I'm doing well, thank you for asking."
