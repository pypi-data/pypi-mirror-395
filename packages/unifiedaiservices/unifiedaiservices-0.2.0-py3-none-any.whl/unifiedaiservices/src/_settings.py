from typing import List, Dict
from types import ModuleType
import re
from openai import OpenAI
from groq import Groq
import google.generativeai as genai

class BaseProvider:
    def get_models(self) -> List[Dict]:
        raise NotImplementedError()

    def get_model_info(self, model_id: str) -> Dict:
        raise NotImplementedError()
    
    def exists_model(self, model_id: str) -> bool:
        try:
            model = any(m["id"] == model_id for m in self.get_models())
            if not model:
                return False
            return True
        except Exception as e:
            raise RuntimeError(f"Error checking model existence: {str(e)}")

    def create_data(self) -> list[dict]:
        raise NotImplementedError()

    def print_models(self):
        models = self.get_models()
        for model in models:
            print("model", model)
        
    def generate_ai(self, data: dict):
        raise NotImplementedError("This method should be overridden by subclasses.")


class OpenAIProvider(BaseProvider):
    def __init__(self, client: OpenAI):
        self.client = client
        self.data_prompt = {}
        self.openai_models = {
            "chat": {
                "gpt-3.5-turbo": {"model_prompt": "", "user_prompt": ""},
                "gpt-3.5-turbo-1106": {"model_prompt": "", "user_prompt": ""},
                "gpt-3.5-turbo-0125": {"model_prompt": "", "user_prompt": ""},
                "gpt-3.5-turbo-instruct": {"model_prompt": "", "user_prompt": ""},
                "gpt-3.5-turbo-instruct-0914": {"model_prompt": "", "user_prompt": ""},
                "gpt-4o": {"model_prompt": "", "user_prompt": ""},
                "gpt-4o-2024-05-13": {"model_prompt": "", "user_prompt": ""},
                "gpt-4o-2024-08-06": {"model_prompt": "", "user_prompt": ""},
                "gpt-4o-2024-11-20": {"model_prompt": "", "user_prompt": ""},
                "gpt-4o-mini": {"model_prompt": "", "user_prompt": ""},
                "gpt-4o-mini-2024-07-18": {"model_prompt": "", "user_prompt": ""},
                "gpt-5.1": {"model_prompt": "", "user_prompt": ""},
                "gpt-5.1-2025-11-13": {"model_prompt": "", "user_prompt": ""},
                "gpt-5.1-chat-latest": {"model_prompt": "", "user_prompt": ""},
                "gpt-5-chat-latest": {"model_prompt": "", "user_prompt": ""},
                "gpt-5": {"model_prompt": "", "user_prompt": ""},
                "gpt-5-2025-08-07": {"model_prompt": "", "user_prompt": ""},
                "gpt-5-pro": {"model_prompt": "", "user_prompt": ""},
                "gpt-5-pro-2025-10-06": {"model_prompt": "", "user_prompt": ""},
                "gpt-5-mini": {"model_prompt": "", "user_prompt": ""},
                "gpt-5-mini-2025-08-07": {"model_prompt": "", "user_prompt": ""},
                "gpt-5-nano": {"model_prompt": "", "user_prompt": ""},
                "gpt-5-nano-2025-08-07": {"model_prompt": "", "user_prompt": ""},
                "o1": {"model_prompt": "", "user_prompt": ""},
                "o1-2024-12-17": {"model_prompt": "", "user_prompt": ""},
                "o3": {"model_prompt": "", "user_prompt": ""},
                "o3-2025-04-16": {"model_prompt": "", "user_prompt": ""},
                "o3-mini": {"model_prompt": "", "user_prompt": ""},
                "o3-mini-2025-01-31": {"model_prompt": "", "user_prompt": ""},
                "o4-mini": {"model_prompt": "", "user_prompt": ""},
                "o4-mini-2025-04-16": {"model_prompt": "", "user_prompt": ""},
                "gpt-4.1": {"model_prompt": "", "user_prompt": ""},
                "gpt-4.1-2025-04-14": {"model_prompt": "", "user_prompt": ""},
                "gpt-4.1-mini": {"model_prompt": "", "user_prompt": ""},
                "gpt-4.1-mini-2025-04-14": {"model_prompt": "", "user_prompt": ""},
                "gpt-4.1-nano": {"model_prompt": "", "user_prompt": ""},
                "gpt-4.1-nano-2025-04-14": {"model_prompt": "", "user_prompt": ""},
            },

            "code": {
                "gpt-5.1-codex": {"prompt": ""},
                "gpt-5.1-codex-mini": {"prompt": ""},
                "gpt-5-codex": {"prompt": ""},
                "davinci-002": {"prompt": ""},
                "babbage-002": {"prompt": ""},
            },

            "image_generation": {
                "dall-e-2": {"prompt": "", "size": ""},
                "dall-e-3": {"prompt": "", "size": ""},
                "gpt-image-1": {"prompt": "", "size": ""},
                "gpt-image-1-mini": {"prompt": "", "size": ""},
                "sora-2": {"prompt": "", "size": ""},
                "sora-2-pro": {"prompt": "", "size": ""},
            },

            "tts": {
                "tts-1": {"voice": "", "input": ""},
                "tts-1-hd": {"voice": "", "input": ""},
                "tts-1-hd-1106": {"voice": "", "input": ""},
                "tts-1-1106": {"voice": "", "input": ""},
                "gpt-4o-mini-tts": {"voice": "", "input": ""},
            },

            "speech_to_text": {
                "whisper-1": {"audio_url": ""},
                "gpt-4o-transcribe": {"audio_url": ""},
                "gpt-4o-transcribe-diarize": {"audio_url": ""},
                "gpt-4o-mini-transcribe": {"audio_url": ""},
            },

            "audio_chat": {
                "gpt-audio": {"audio_url": "", "input": ""},
                "gpt-audio-2025-08-28": {"audio_url": "", "input": ""},
                "gpt-audio-mini": {"audio_url": "", "input": ""},
                "gpt-audio-mini-2025-10-06": {"audio_url": "", "input": ""},
                "gpt-4o-audio-preview": {"audio_url": "", "input": ""},
                "gpt-4o-audio-preview-2024-10-01": {"audio_url": "", "input": ""},
                "gpt-4o-audio-preview-2024-12-17": {"audio_url": "", "input": ""},
                "gpt-4o-audio-preview-2025-06-03": {"audio_url": "", "input": ""},
                "gpt-4o-mini-audio-preview": {"audio_url": "", "input": ""},
                "gpt-4o-mini-audio-preview-2024-12-17": {"audio_url": "", "input": ""},
            },

            "embedding": {
                "text-embedding-3-small": {"input": ""},
                "text-embedding-3-large": {"input": ""},
                "text-embedding-ada-002": {"input": ""},
            },

            "moderation": {
                "omni-moderation-latest": {"input": ""},
                "omni-moderation-2024-09-26": {"input": ""},
            },

            "search": {
                "gpt-5-search-api": {"query": ""},
                "gpt-5-search-api-2025-10-14": {"query": ""},
                "gpt-4o-search-preview": {"query": ""},
                "gpt-4o-search-preview-2025-03-11": {"query": ""},
                "gpt-4o-mini-search-preview": {"query": ""},
                "gpt-4o-mini-search-preview-2025-03-11": {"query": ""},
            }
        }
    def get_models(self) -> List[Dict]:
        models_list = []

        for category, models in self.openai_models.items():
            # models הוא dict של מודלים בתוך הקטגוריה
            for model_id, prompt_fields in models.items():
                models_list.append({
                    "id": model_id,
                    "category": category,
                    "prompt": list(prompt_fields.keys())  # ["model_prompt", "user_prompt"] וכו'
                })

        return models_list
    
    def get_model_info(self, model_id: str) -> Dict:
        try:
            if not self.exists_model(model_id):
                raise ValueError(f"Model {model_id} does not exist.")

            # מפה מהירה לאיתור הקטגוריה והשדות
            model_map = {m["id"]: m for m in self.get_models()}

            info = self.client.models.retrieve(model_id)

            return {
                "id": model_id,
                "info": info,
                "category": model_map[model_id]["category"],
                "prompt": model_map[model_id]["prompt"]
            }

        except Exception as e:
            raise RuntimeError(f"Error retrieving model info: {str(e)}")

    def create_data(
        self,
        model_id,
        user_prompt=None,
        model_prompt=None,
        prompt=None,
        temperature=None,
        max_tokens=None,
        size=None,
        audio_url=None,
        voice=None,
        text=None,
        query=None,
        output_path=None
    ) -> list[dict]:
        try:
            if not self.exists_model(model_id):
                raise ValueError(f"Model {model_id} does not exist in OpenAI models.")
        except Exception as e:
            raise RuntimeError(f"Error checking model existence: {str(e)}")

        model_info = {m["id"]: m for m in self.get_models()}[model_id]
        category = model_info["category"]
        data = [{"category": category}]

        if category == "chat":
            data.append({"model": model_id or input("enter model prompt"), "model_prompt": model_prompt or input("enter model prompt"), "user_prompt": user_prompt or "you are a helpful assistant.", "temperature": temperature or 0.7, "max_tokens": max_tokens or None})
        elif category == "code":
            data.append({"model": model_id, "prompt": prompt or input("enter code prompt"), "max_tokens": max_tokens or None})
        elif category == "image_generation":
            data.append({"model": model_id, "prompt": prompt or input("enter prompt"), "size": size or None})
        elif category == "tts":
            data.append({"model": model_id, "voice": voice or input("enter voice"), "input": text})
        elif category == "speech_to_text":
            data.append({"model": model_id, "audio_url": audio_url or input("enter audio url")})
        elif category == "audio_chat":
            data.append({"model": model_id, "audio_url": audio_url or input("enter audio url"), "input" : text or input("enter input")})
        elif category in ["embedding", "moderation"]:
            data.append({"model": model_id, "input": text or input("enter input")})
        elif category == "search":
            data.append({"model": model_id, "query": query or input("enter query")})
        self.data_prompt = data
        return data

    def generate_ai(self, data: dict):
        if len(data) == 0:
            raise ValueError("Data is empty. Cannot generate AI response.")
        try:
            category = data.get("category")
            model = data.get("model")

            if category == "chat":
                messages = []
                if data.get("model_prompt"):
                    messages.append({"role": "system", "content": data["model_prompt"]})
                if data.get("user_prompt"):
                    messages.append({"role": "user", "content": data["user_prompt"]})

                return self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=data.get("temperature", 0.7),
                    max_tokens=data.get("max_tokens")
                )

            elif category == "code":
                return self.client.completions.create(
                    model=model,
                    prompt=data["prompt"],
                    max_tokens=data.get("max_tokens")
                )

            elif category == "image_generation":
                return self.client.images.generate(
                    model=model,
                    prompt=data["prompt"],
                    size=data.get("size", "1024x1024")
                )

            elif category == "tts":
                return self.client.audio.speech.create(
                    model=model,
                    voice=data.get("voice", "alloy"),
                    input=data["input"]
                )

            elif category == "audio_generation":
                return self.client.audio.transcriptions.create(
                    model=model,
                    file=data["audio_url"],
                    prompt=data.get("input")
                )

            elif category == "audio_chat":
                messages = [{"role": "user", "content": data["input"]}]
                return self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    audio=data["audio_url"]
                )

            elif category == "embedding":
                return self.client.embeddings.create(
                    model=model,
                    input=data["input"]
                )

            elif category == "moderation":
                return self.client.moderations.create(
                    model=model,
                    input=data["input"]
                )

            elif category == "search":
                return self.client.search.create(
                    model=model,
                    query=data["input"],
                    documents=data["documents"]
                )

            else:
                raise ValueError(f"Unsupported category: {category}")

        except Exception as e:
            print(f"OpenAIProvider Error: {e}")
            return None

class GroqProvider(BaseProvider):
    def __init__(self, client: Groq):
        self.client = client
        self.data_prompt = {}
        self.groq_models = {
            "chat": {
                "llama-3.1-8b-instant": {"model_prompt": "", "user_prompt": ""},
                "allam-2-7b": {"model_prompt": "", "user_prompt": ""},
                "groq/compound-mini": {"model_prompt": "", "user_prompt": ""},
                "meta-llama/llama-4-scout-17b-16e-instruct": {"model_prompt": "", "user_prompt": ""},
                "openai/gpt-oss-120b": {"model_prompt": "", "user_prompt": ""},
                "moonshotai/kimi-k2-instruct-0905": {"model_prompt": "", "user_prompt": ""},
                "llama-3.3-70b-versatile": {"model_prompt": "", "user_prompt": ""},
                "groq/compound": {"model_prompt": "", "user_prompt": ""},
                "qwen/qwen3-32b": {"model_prompt": "", "user_prompt": ""},
                "openai/gpt-oss-20b": {"model_prompt": "", "user_prompt": ""},
                "moonshotai/kimi-k2-instruct": {"model_prompt": "", "user_prompt": ""},
                "meta-llama/llama-4-maverick-17b-128e-instruct": {"model_prompt": "", "user_prompt": ""}
            },

            "tts": {
                "playai-tts": {"voice": "", "input": ""},
                "playai-tts-arabic": {"voice": "", "input": ""}
            },

            "speech_to_text": {
                "whisper-large-v3": {"audio_url": ""},
                "whisper-large-v3-turbo": {"audio_url": ""}
            },

            "moderation": {
                "meta-llama/llama-guard-4-12b": {"input": ""},
                "meta-llama/llama-prompt-guard-2-22m": {"input": ""},
                "meta-llama/llama-prompt-guard-2-86m": {"input": ""},
                "openai/gpt-oss-safeguard-20b": {"input": ""}
            }
        }

    def get_models(self) -> List[Dict]:
        models_list = []

        for category, models in self.groq_models.items():
            # models הוא dict של מודלים בתוך הקטגוריה
            for model_id, prompt_fields in models.items():
                models_list.append({
                    "id": model_id,
                    "category": category,
                    "prompt": list(prompt_fields.keys())  # ["model_prompt", "user_prompt"] וכו'
                })

        return models_list
    
    def get_model_info(self, model_id: str) -> Dict:
        try:
            if not self.exists_model(model_id):
                raise ValueError(f"Model {model_id} does not exist.")

            # מפה מהירה לאיתור הקטגוריה והשדות
            model_map = {m["id"]: m for m in self.get_models()}

            info = self.client.models.retrieve(model_id)

            return {
                "id": model_id,
                "info": info,
                "category": model_map[model_id]["category"],
                "prompt": model_map[model_id]["prompt"]
            }

        except Exception as e:
            raise RuntimeError(f"Error retrieving model info: {str(e)}")


    def create_data(
        self,
        model_id,
        user_prompt=None,
        model_prompt=None,
        audio_url=None,
        voice=None,
        text=None,
    ) -> list[dict]:

        try:
            if not self.exists_model(model_id, provider="groq"):
                raise ValueError(f"Model {model_id} does not exist in Groq models.")
        except Exception as e:
            raise RuntimeError(f"Error checking Groq model existence: {str(e)}")

        model_info = {m["id"]: m for m in self.get_models()}[model_id]
        category = model_info["category"]

        data = []

        if category == "chat":
            data.append({
                "model": model_id,
                "model_prompt": model_prompt or input("enter model prompt"),
                "user_prompt": user_prompt or input("enter user prompt"),
            })

        elif category == "tts":
            data.append({
                "model": model_id,
                "voice": voice or input("enter voice"),
                "input": text or input("enter input")
            })

        elif category == "speech_to_text":
            data.append({
                "model": model_id,
                "audio_url": audio_url or input("enter audio url")
            })

        elif category == "moderation":
            data.append({
                "model": model_id,
                "input": text or input("enter input")
            })
        self.data_prompt = data

        return data
        
    def generate_ai(self, data: dict):
        try:
            category = data.get("category")
            model = data.get("model")

            if category == "chat":
                messages = []
                if data.get("model_prompt"):
                    messages.append({"role": "system", "content": data["model_prompt"]})
                if data.get("user_prompt"):
                    messages.append({"role": "user", "content": data["user_prompt"]})

                return self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=data.get("temperature", 0.7),
                    max_tokens=data.get("max_tokens")
                )

            elif category == "tts":
                return self.client.audio.speech.create(
                    model=model,
                    voice=data.get("voice", "alloy"),
                    input=data["input"]
                )

            elif category == "moderation":
                return self.client.moderations.create(
                    model=model,
                    input=data["input"]
                )

            elif category == "speech_to_text":
                return self.client.audio.transcriptions.create(
                    model=model,
                    file=data["audio_url"],
                    prompt=data.get("input")
                )

            else:
                raise ValueError(f"Unsupported category: {category}")

        except Exception as e:
            print(f"GroqProvider Error: {e}")
            return None


class GoogleProvider(BaseProvider):
    def __init__(self, client: genai):
        self.client = client
        self.data_prompt = {}
        self.google_models = {
            "chat": {
                "models/gemini-2.5-pro-preview-03-25": {"model_prompt": "", "user_prompt": ""},
                "models/gemini-2.5-flash": {"model_prompt": "", "user_prompt": ""},
                "models/gemini-2.5-flash-lite": {"model_prompt": "", "user_prompt": ""},  # נוסף
                "models/gemini-2.5-flash-image": {"model_prompt": "", "user_prompt": ""},  # נוסף
                "models/gemini-2.5-flash-lite-preview-09-2025": {"model_prompt": "", "user_prompt": ""},  # נוסף

                "models/gemini-2.5-pro-preview-05-06": {"model_prompt": "", "user_prompt": ""},
                "models/gemini-2.5-pro-preview-06-05": {"model_prompt": "", "user_prompt": ""},
                "models/gemini-2.5-pro": {"model_prompt": "", "user_prompt": ""},

                "models/gemini-2.0-flash-exp": {"model_prompt": "", "user_prompt": ""},
                "models/gemini-2.0-flash": {"model_prompt": "", "user_prompt": ""},
                "models/gemini-2.0-flash-001": {"model_prompt": "", "user_prompt": ""},

                "models/gemini-2.0-flash-lite-001": {"model_prompt": "", "user_prompt": ""},
                "models/gemini-2.0-flash-lite": {"model_prompt": "", "user_prompt": ""},
                "models/gemini-2.0-flash-lite-preview-02-05": {"model_prompt": "", "user_prompt": ""},
                "models/gemini-2.0-flash-lite-preview": {"model_prompt": "", "user_prompt": ""},

                "models/gemini-2.0-pro-exp": {"model_prompt": "", "user_prompt": ""},
                "models/gemini-2.0-pro-exp-02-05": {"model_prompt": "", "user_prompt": ""},

                "models/gemini-exp-1206": {"model_prompt": "", "user_prompt": ""},

                "models/gemini-flash-latest": {"model_prompt": "", "user_prompt": ""},
                "models/gemini-flash-lite-latest": {"model_prompt": "", "user_prompt": ""},
                "models/gemini-pro-latest": {"model_prompt": "", "user_prompt": ""},

                "models/gemini-2.5-flash-preview-09-2025": {"model_prompt": "", "user_prompt": ""},

                "models/gemini-2.5-flash-live-preview": {"model_prompt": "", "user_prompt": ""},
                "models/gemini-2.0-flash-live-001": {"model_prompt": "", "user_prompt": ""},
                "models/gemini-live-2.5-flash-preview": {"model_prompt": "", "user_prompt": ""},

                # Gemma models
                "models/gemma-3-1b-it": {"model_prompt": "", "user_prompt": ""},
                "models/gemma-3-4b-it": {"model_prompt": "", "user_prompt": ""},
                "models/gemma-3-12b-it": {"model_prompt": "", "user_prompt": ""},
                "models/gemma-3-27b-it": {"model_prompt": "", "user_prompt": ""},
                "models/gemma-3n-e4b-it": {"model_prompt": "", "user_prompt": ""},
                "models/gemma-3n-e2b-it": {"model_prompt": "", "user_prompt": ""},

                # Robotics + Computer Use
                "models/gemini-robotics-er-1.5-preview": {"model_prompt": "", "user_prompt": ""},
                "models/gemini-2.5-computer-use-preview-10-2025": {"model_prompt": "", "user_prompt": ""},

                # Gemini 3
                "models/gemini-3-pro-preview": {"model_prompt": "", "user_prompt": ""}
            },

            "thinking": {
                "models/gemini-2.0-flash-thinking-exp-01-21": {"model_prompt": "", "user_prompt": ""},
                "models/gemini-2.0-flash-thinking-exp": {"model_prompt": "", "user_prompt": ""},
                "models/gemini-2.0-flash-thinking-exp-1219": {"model_prompt": "", "user_prompt": ""}
            },

            "embeddings": {
                "models/embedding-gecko-001": {"input": ""},
                "models/embedding-001": {"input": ""},
                "models/text-embedding-004": {"input": ""},
                "models/gemini-embedding-exp-03-07": {"input": ""},
                "models/gemini-embedding-exp": {"input": ""},
                "models/gemini-embedding-001": {"input": ""}
            },

            "tts": {
                "models/gemini-2.5-flash-preview-tts": {"text": "", "voice": ""},
                "models/gemini-2.5-pro-preview-tts": {"text": "", "voice": ""},
                "models/gemini-2.5-flash-native-audio-latest": {"text": "", "voice": ""},
                "models/gemini-2.5-flash-native-audio-preview-09-2025": {"text": "", "voice": ""}
            },

            "image": {
                "models/gemini-2.0-flash-exp-image-generation": {"prompt": "", "size": ""},

                "models/gemini-2.5-flash-image-preview": {"prompt": "", "size": ""},
                "models/gemini-2.5-flash-image": {"prompt": "", "size": ""},

                # חדש – תומך גם בתמונה
                "models/gemini-2.5-flash-lite-preview-09-2025": {"prompt": "", "size": ""},

                "models/imagen-4.0-generate-preview-06-06": {"prompt": "", "size": ""},
                "models/imagen-4.0-ultra-generate-preview-06-06": {"prompt": "", "size": ""},
                "models/imagen-4.0-generate-001": {"prompt": "", "size": ""},
                "models/imagen-4.0-ultra-generate-001": {"prompt": "", "size": ""},
                "models/imagen-4.0-fast-generate-001": {"prompt": "", "size": ""},
                "models/nano-banana-pro-preview": {"prompt": "", "size": ""},
                "models/gemini-3-pro-image-preview": {"prompt": "", "size": ""}
            },

            "video": {
                "models/veo-2.0-generate-001": {"prompt": ""},
                "models/veo-3.0-generate-001": {"prompt": ""},
                "models/veo-3.0-fast-generate-001": {"prompt": ""},
                "models/veo-3.1-generate-preview": {"prompt": ""},
                "models/veo-3.1-fast-generate-preview": {"prompt": ""}
            },

            "other": {
                "models/aqa": {},
                "models/nano-banana-pro-preview": {}
            }
        }


    def get_models(self) -> List[Dict]:
        models_list = []

        for category, models in self.google_models.items():
            # models הוא dict של מודלים בתוך הקטגוריה
            for model_id, prompt_fields in models.items():
                models_list.append({
                    "id": model_id,
                    "category": category,
                    "prompt": list(prompt_fields.keys())  # ["model_prompt", "user_prompt"] וכו'
                })

        return models_list
    
    def get_model_info(self, model_id: str) -> Dict:
        try:
            if not self.exists_model(model_id):
                raise ValueError(f"Model {model_id} does not exist.")

            # מפה מהירה לאיתור הקטגוריה והשדות
            model_map = {m["id"]: m for m in self.get_models()}

            info = self.client.models.retrieve(model_id)

            return {
                "id": model_id,
                "info": info,
                "category": model_map[model_id]["category"],
                "prompt": model_map[model_id]["prompt"]
            }

        except Exception as e:
            raise RuntimeError(f"Error retrieving model info: {str(e)}")

    def create_data(
        self,
        model_id,
        user_prompt=None,
        model_prompt=None,
        audio_url=None,
        voice=None,
        text=None,
        size=None,
    ) -> list[dict]:
        try:
            if not self.exists_model(model_id):
                raise ValueError(f"Model {model_id} does not exist in Google models.")
        except Exception as e:
            raise RuntimeError(f"Error checking model existence: {str(e)}")
        model_info = {m["id"]: m for m in self.get_models()}[model_id]
        category = model_info["category"]

        data = []

        if category == "chat":
            data.append({
                "model": model_id,
                "model_prompt": model_prompt or input("enter model prompt"),
                "user_prompt": user_prompt or input("enter user prompt")
            })

        elif category == "tts":
            data.append({
                "model": model_id,
                "voice": voice or input("enter voice"),
                "input": text or input("enter input"),
            })

        elif category in ["embeddings", "speech_to_text", "moderation", "image", "video", "other"]:
            # התאמות ספציפיות לפי קטגוריה
            if category == "embeddings":
                data.append({
                    "model": model_id,
                    "input": text or input("enter input"),
                })
            elif category == "speech_to_text":
                data.append({
                    "model": model_id,
                    "audio_url": audio_url or input("enter audio url"),
                })
            elif category == "moderation":
                data.append({
                    "model": model_id,
                    "input": text or input("enter input"),
                })
            elif category == "image":
                data.append({
                    "model": model_id,
                    "prompt": text or input("enter input"),
                    "size": size or None,
                })
            elif category == "video":
                data.append({
                    "model": model_id,
                    "prompt": text or input("enter input"),
                })
            elif category == "other":
                data.append({
                    "model": model_id,
                })

        self.data_prompt = data

        return data

    def generate_ai(self, data: dict):
        try:
            category = data.get("category")
            model = data.get("model")

            if category == "chat":
                messages = []
                if data.get("model_prompt"):
                    messages.append({"role": "system", "content": data["model_prompt"]})
                if data.get("user_prompt"):
                    messages.append({"role": "user", "content": data["user_prompt"]})

                return genai.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=data.get("temperature", 0.7),
                    max_tokens=data.get("max_tokens")
                )

            elif category == "tts":
                return genai.audio.speech.create(
                    model=model,
                    voice=data.get("voice", "alloy"),
                    input=data["input"]
                )

            elif category == "embeddings":
                return genai.embeddings.create(
                    model=model,
                    input=data["input"]
                )

            elif category == "speech_to_text":
                return genai.audio.transcriptions.create(
                    model=model,
                    file=data["audio_url"],
                    prompt=data.get("input")
                )

            elif category == "moderation":
                return genai.moderations.create(
                    model=model,
                    input=data["input"]
                )

            elif category == "image":
                return genai.images.generate(
                    model=model,
                    prompt=data["prompt"],
                    size=data.get("size", "1024x1024")
                )

            elif category == "video":
                return genai.videos.generate(
                    model=model,
                    prompt=data["prompt"],
                    size=data.get("size", "1024x1024")
                )
            else:
                raise ValueError(f"Unsupported category: {category}")

        except Exception as e:
            print(f"GoogleProvider Error: {e}")
            return None

class AISettings:
    def __init__(self, client: BaseProvider):
        self.data_prompt = {}
        self.client = client
        if isinstance(client, OpenAI):
            self.adapter = OpenAIProvider(client)
        elif isinstance(client, Groq):
            self.adapter = GroqProvider(client)
        elif isinstance(client, ModuleType):
            self.adapter = GoogleProvider(client)
    def get_models(self) -> List[Dict]:
        try:
            return self.adapter.get_models()
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve models for provider: {str(e)}")

    def get_model_info(self, model_id: str) -> Dict:
        try:
            return self.adapter.get_model_info(model_id)
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve model info for provider: {str(e)}")

    def exists_model(self, model_id: str) -> bool:
        try:
            return any(m["id"] == model_id for m in self.get_models())
        except Exception as e:
            raise RuntimeError(f"Error checking Groq model existence: {str(e)}")
        
    def print_models(self):
        try:
            self.adapter.print_models()
        except Exception as e:
            raise RuntimeError(f"Failed to print models for provider: {str(e)}")
    
    def create_data(self, **kwargs) -> list[dict]:
        try:
            return self.adapter.create_data(**kwargs)
        except Exception as e:
            raise RuntimeError(f"Failed to create data for provider: {str(e)}")
        
    def generate_ai(self, data: dict):
        try:
            return self.adapter.generate_ai(data)
        except Exception as e:
            raise RuntimeError(f"Failed to generate AI response for provider: {str(e)}")