from typing import List
from openai import OpenAI

class Embed:
    def __init__(self):
        self.client = OpenAI()

    def run(self, text: str) -> List[float]:
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
