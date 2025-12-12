from typing import Union, Tuple
from types import ModuleType
from openai import OpenAI
import google.generativeai as genai
from groq import Groq
from ._settings import AISettings

AIClient = Union[OpenAI, Groq, ModuleType]

class CreateClient:
    def __init__(self, provider: str, api_key):
        self.provider = provider.lower().strip()
        self.client = None

        if self.provider == "openai":
            self.client = OpenAI(api_key=api_key)

        elif self.provider == "gemini":
            genai.configure(api_key=api_key)
            self.client = genai

        elif self.provider == "groq":
            self.client = Groq(api_key=api_key)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")


    def get_client(self) -> Tuple[AIClient, AISettings]:
        if self.client is None:
            raise RuntimeError(f"Client not initialized for provider {self.provider}")
        return self.client