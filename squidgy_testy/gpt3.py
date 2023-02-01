
import openai
import os
from .service import PromptService

class Gpt3PromptService(PromptService):

    def __init__(self):
        openai.api_key = os.environ['OPENAI_API_KEY']

    def invoke(
        self, 
        prompt: str, 
        stop=['\n\n'], 
        settings: dict[str, object] = {},
    ) -> str:
        response = openai.Completion.create(
            prompt=prompt,
            model=settings.get("model", "text-davinci-003"),
            temperature=0,
            max_tokens=settings.get("max_tokens", 160),
            stop=stop,
            top_p=settings.get("frequency_penalty", 1),
            frequency_penalty=settings.get("frequency_penalty", 0.3),
            presence_penalty=settings.get("presence_penalty", 0.15),
            timeout=15
        )

        return response['choices'][0]['text'].strip()

    def embed(
        self, 
        texts: list[str]
    ) -> list[float]:
        return openai.Embedding.create(input=texts, model="text-embedding-ada-002")