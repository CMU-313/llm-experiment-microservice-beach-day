from ollama import Client
import json
import re
import os

MODEL_NAME = "llama3.1:8b" # @param ["qwen3:0.6b", "deepseek-r1:1.5b", "gemma3:270m", "llama3.1:8b", "mistral:7b", "smollm2:135m"]

# Get OLLAMA_HOST, if specified, or default to host.docker.internal:11434 for Docker environments.
OLLAMA_URL = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")

client = Client(host=OLLAMA_URL)


def query_llm_robust(post: str) -> tuple[bool, str]:
    context = """\
    You are a professional assistant that translates text in all languages to English text and determines whether a given text is in English or not.
    - Reply with ONLY the following JSON format: {"is_english": true/false, "translation": "<text>"}.
    - If the text is English, translation should be identical to the original text.
    - If the text is non-English, provide a direct English translation.
    - Do not add any commentary or extra text.
    - Be robust to dialects, slang, or unintelligible/malformed text.
    """

    try:
        response = client.chat(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": post},
            ]
        )

        
        output = response.message.content.strip()
        match = re.search(r'\{.*\}', output, flags=re.DOTALL)
        if match:
            parsed = json.loads(match.group())
            is_english = bool(parsed.get("is_english", False))
            translation = str(parsed.get("translation", post))
        else:
            raise ValueError("Output not in correct JSON format")

    except Exception:
        is_english = False
        translation = post

    return is_english, translation

def translate_content(content: str) -> tuple[bool, str]:
    return query_llm_robust(content)