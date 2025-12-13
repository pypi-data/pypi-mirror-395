import openai
import os
from .config import Config
from .pricing import PRICING_RATES

import datetime

class Agent:
    def __init__(self, system_prompt="You are a helpful assistant."):
        self.system_prompt = system_prompt
        self.model = Config.MODEL
        self.api_key = Config.API_KEY
        
        # Initialize the client based on provider
        if Config.PROVIDER == "openai":
            self.client = openai.OpenAI(api_key=self.api_key)
        else:
            # You can extend this for other providers like Anthropic, etc.
            raise ValueError(f"Unsupported provider: {Config.PROVIDER}")

    def process(self, user_instructions, content_to_manipulate):
        """
        Sends the instructions and content to the LLM.
        """
        # Construct the message
        # We present the user instructions and the content clearly to the model
        full_prompt = f"""
Instructions:
{user_instructions}

---
Content to Process:
{content_to_manipulate}
"""

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": full_prompt}
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )

        if response.usage:
            self._log_cost_analysis(response.usage)

        return response.choices[0].message.content

    def _log_cost_analysis(self, usage):
        # Pricing per 1M tokens (USD)
        pricing = PRICING_RATES

        # Handle model versions (e.g., gpt-4o-2024-05-13) by matching prefix
        model_key = self.model
        if model_key not in pricing:
            for key in pricing:
                if self.model.startswith(key):
                    model_key = key
                    break
        
        log_entry = [
            f"--- Usage Report ({datetime.datetime.now().isoformat()}) ---",
            f"Model: {self.model}",
            f"Input Tokens:  {usage.prompt_tokens}",
            f"Output Tokens: {usage.completion_tokens}",
            f"Total Tokens:  {usage.total_tokens}"
        ]

        if model_key in pricing:
            rates = pricing[model_key]
            input_cost = (usage.prompt_tokens / 1_000_000) * rates["input"]
            output_cost = (usage.completion_tokens / 1_000_000) * rates["output"]
            total_cost = input_cost + output_cost
            log_entry.append(f"Estimated Cost: ${total_cost:.6f}")
        else:
            log_entry.append("Cost estimation not available for this model.")
        
        log_entry.append("-" * 30 + "\n")

        try:
            log_dir = os.path.expanduser("~/.llm-editor/logs")
            os.makedirs(log_dir, exist_ok=True)
            log_file = os.path.join(log_dir, "usage.log")
            with open(log_file, "a", encoding="utf-8") as f:
                f.write("\n".join(log_entry))
        except Exception as e:
            print(f"DEBUG: Logging failed: {e}")
            # Fail silently on logging errors to avoid disrupting the main flow
        except Exception as e:
            # Fail silently on logging errors to avoid disrupting the main flow
            pass
