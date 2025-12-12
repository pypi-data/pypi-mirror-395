from typing import Optional
from . import LLMProvider

class ClaudeProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
        self.api_key = api_key
        self.model = model
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=api_key)
        except ImportError:
            raise ImportError("Anthropic library not installed. Install with: pip install anthropic")

    def explain_code(self, source_code: str, context_code: Optional[dict] = None) -> str:
        if not source_code:
            return "No source code provided."

        context_str = ""
        if context_code:
            context_str = "\n\nContext (Called Functions):\n"
            for name, code in context_code.items():
                context_str += f"Function `{name}`:\n```python\n{code}\n```\n"

        prompt = f"""Short Description : overview the python code in maximum of 2 lines. 
                    Input Parameters : list the input parameters of the function
                    Output Response : list the output response of the function
                    Whats the business logic inside the codeblock. If the code block have multiple functions, then list the business logic of each function.

                    Target Code:
                    ```python
                    {source_code}
                    ```

                    {context_str}
                    """
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            return f"LLM Error: {str(e)}"
    
    def is_available(self) -> bool:
        return self.api_key is not None and len(self.api_key) > 0
