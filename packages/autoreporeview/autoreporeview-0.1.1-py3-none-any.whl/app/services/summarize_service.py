from ..agents.agent import Agent
from ..models.llm_factory import LLMFactory


class SummarizeService:
    def __init__(self) -> None:
        llm = LLMFactory.create_llm()
        self.agent = Agent(
            llm,
            tools=[],
        )

    def prepare_prompt(self, diff: str) -> str:
        return f"""
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

    def summarize(self, diff: str) -> str:
        prompt = self.prepare_prompt(diff)
        try:
            return self.agent.invoke(prompt)
        except Exception as e:
            error_type = type(e).__name__
            error_msg = str(e)

            # Extract meaningful error message
            if "APIConnectionError" in error_type or "Connection" in error_type:
                raise ConnectionError(
                    f"Failed to connect to API. Please check:\n"
                    f"  - Your internet connection\n"
                    f"  - API URL is correct (use 'show-config' to check)\n"
                    f"  - API server is accessible\n\n"
                    f"Error details: {error_msg}"
                ) from None
            elif (
                "AuthenticationError" in error_type
                or "401" in error_msg
                or "403" in error_msg
            ):
                raise ValueError(
                    f"Authentication failed. Please check your API key.\n"
                    f"Use 'configure' command to update your API key.\n\n"
                    f"Error details: {error_msg}"
                ) from None
            elif "APIError" in error_type or "400" in error_msg or "429" in error_msg:
                raise RuntimeError(
                    f"API error occurred. Please check:\n"
                    f"  - API URL and model name are correct\n"
                    f"  - You have sufficient API credits/quota\n"
                    f"  - The model name is valid for your API provider\n\n"
                    f"Error details: {error_msg}"
                ) from None
            elif isinstance(e, ValueError):
                raise
            else:
                # For any other error, show a clean message
                raise RuntimeError(
                    f"An error occurred while generating summary: {error_msg}"
                ) from None
