from typing import Optional
from . import LLMProvider

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)
        except ImportError:
            raise ImportError("OpenAI library not installed. Install with: pip install openai")

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
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"LLM Error: {str(e)}"
    
    def is_available(self) -> bool:
        return self.api_key is not None and len(self.api_key) > 0
