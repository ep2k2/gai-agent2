# Reference: Based on engine/openai.py structure

try:
    import google.generativeai as genai
except ImportError:
    raise ImportError("If you'd like to use Gemini models, please install the google-generativeai package by running `pip install google-generativeai`, and add 'GOOGLE_GEMINI_API_KEY' to your environment variables.")

import os
import json
import platformdirs
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)
from typing import List, Union

from .base import EngineLM, CachedEngine
from dotenv import load_dotenv
load_dotenv()

from pydantic import BaseModel

class DefaultFormat(BaseModel):
    response: str

class ChatGemini(EngineLM, CachedEngine):
    DEFAULT_SYSTEM_PROMPT = "You are a helpful, creative, and smart assistant."

    def __init__(
        self,
        model_string="gemini-flash-2.0",
        system_prompt=DEFAULT_SYSTEM_PROMPT,
        is_multimodal: bool=False,
        enable_cache: bool=True,
        **kwargs):
        """
        :param model_string: gemini-flash-2.0
        :param system_prompt:
        :param is_multimodal:
        """
        if enable_cache:
            root = platformdirs.user_cache_dir("octotools")
            cache_path = os.path.join(root, f"cache_gemini_{model_string}.db")
            
            self.image_cache_dir = os.path.join(root, "image_cache")
            os.makedirs(self.image_cache_dir, exist_ok=True)

            super().__init__(cache_path=cache_path)

        self.system_prompt = system_prompt
        if os.getenv("GOOGLE_GEMINI_API_KEY") is None:
            raise ValueError("Please set the GOOGLE_GEMINI_API_KEY environment variable if you'd like to use Gemini models.")
        
        genai.configure(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))
        self.model = genai.GenerativeModel(model_string)
        self.model_string = model_string
        self.is_multimodal = is_multimodal
        self.enable_cache = enable_cache

        if enable_cache:
            print(f"!! Cache enabled for model: {self.model_string}")
        else:
            print(f"!! Cache disabled for model: {self.model_string}")

    @retry(wait=wait_random_exponential(min=1, max=5), stop=stop_after_attempt(5))
    def generate(self, content: Union[str, List[Union[str, bytes]]], system_prompt=None, **kwargs):
        try:
            # Print retry attempt information
            attempt_number = self.generate.retry.statistics.get('attempt_number', 0) + 1
            if attempt_number > 1:
                print(f"Attempt {attempt_number} of 5")

            if isinstance(content, str):
                return self._generate_text(content, system_prompt=system_prompt, **kwargs)
            
            elif isinstance(content, list):
                if (not self.is_multimodal):
                    raise NotImplementedError("Multimodal generation is only supported for vision models.")
                
                return self._generate_multimodal(content, system_prompt=system_prompt, **kwargs)

        except Exception as e:
            print(f"Error in generate method: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            print(f"Error details: {e.args}")
            return {
                "error": type(e).__name__,
                "message": str(e),
                "details": getattr(e, 'args', None)
            }
        
    def _generate_text(
        self, prompt, system_prompt=None, temperature=0, max_tokens=4000, top_p=0.99, response_format=None
    ):
        sys_prompt_arg = system_prompt if system_prompt else self.system_prompt

        if self.enable_cache:
            cache_key = sys_prompt_arg + prompt
            cache_or_none = self._check_cache(cache_key)
            if cache_or_none is not None:
                return cache_or_none

        # Combine system prompt and user prompt
        full_prompt = f"{sys_prompt_arg}\n\n{prompt}"

        response = self.model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                top_p=top_p,
                max_output_tokens=max_tokens,
            )
        )

        response_text = response.text

        if self.enable_cache:
            self._save_cache(cache_key, response_text)
        return response_text

    def __call__(self, prompt, **kwargs):
        return self.generate(prompt, **kwargs)

    def _generate_multimodal(
        self, content: List[Union[str, bytes]], system_prompt=None, temperature=0, max_tokens=4000, top_p=0.99, response_format=None
    ):
        if not self.is_multimodal:
            raise ValueError("This model does not support multimodal inputs. Use gemini-pro-vision instead.")

        sys_prompt_arg = system_prompt if system_prompt else self.system_prompt

        if self.enable_cache:
            # Create a cache key from the content
            cache_key = sys_prompt_arg + json.dumps([
                str(item) if isinstance(item, str) else f"<binary_{len(item)}_bytes>"
                for item in content
            ])
            cache_or_none = self._check_cache(cache_key)
            if cache_or_none is not None:
                return cache_or_none

        # Process multimodal content
        processed_content = []
        for item in content:
            if isinstance(item, str):
                processed_content.append(item)
            elif isinstance(item, bytes):
                processed_content.append(genai.types.Image.from_bytes(item))
            else:
                raise ValueError(f"Unsupported content type: {type(item)}")

        response = self.model.generate_content(
            processed_content,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                top_p=top_p,
                max_output_tokens=max_tokens,
            )
        )

        response_text = response.text

        if self.enable_cache:
            self._save_cache(cache_key, response_text)
        return response_text 