import requests
from typing import Optional
from . import LLMProvider

class OllamaProvider(LLMProvider):
    def __init__(self, model: str = "llama3.1", host: str = "http://localhost:11434"):
        self.model = model
        self.host = host
        self.api_url = f"{host}/api/generate"

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
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
            response = requests.post(self.api_url, json=payload, timeout=60)
            response.raise_for_status()
            return response.json().get("response", "No response from LLM.")
        except Exception as e:
            return f"LLM Error: {str(e)}"
    
    def is_available(self) -> bool:
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
