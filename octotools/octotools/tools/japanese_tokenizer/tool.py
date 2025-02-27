import requests
import os
from octotools.tools.base import BaseTool

class Japanese_Tokenizer_Tool(BaseTool):
    require_llm_engine = False

    def __init__(self):
        super().__init__(
            tool_name="JapaneseTokenizerTool",
            tool_description="A tool that tokenizes Japanese text and performs morphological analysis to return parts of speech in a structured JSON response.",
            tool_version="0.0.1",
            input_types={
                "text": "str - The Japanese text to be tokenized.",
                "mode": "str - Optional mode of output (normal, spaced, okurigana, or furigana).",
                "to": "str - Optional conversion to writing system (hiragana, katakana, or romaji).",
                "romaji_system": "str - Optional romanization system (hepburn, kunrei)."
            },
            output_type="dict - A dictionary containing the tokenized text and additional information.",
            demo_commands=[
                {
                    "command": 'execution = tool.execute(text="日本は美しい国だ")',
                    "description": "Tokenize the Japanese sentence '日本は美しい国だ'."
                },
                {
                    "command": 'execution = tool.execute(text="私はレミです", mode="okurigana", to="hiragana")',
                    "description": "Tokenize with okurigana and convert to hiragana."
                }
            ]
        )

    def execute(self, text, mode=None, to=None, romaji_system=None):
        url = "https://yomi.onrender.com/analyze"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = f"text={text}"
        
        if mode:
            data += f"&mode={mode}"
        if to:
            data += f"&to={to}"
        if romaji_system:
            data += f"&romaji_system={romaji_system}"

        response = requests.post(url, headers=headers, data=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to tokenize text", "details": response.text}

if __name__ == "__main__":
    # Example usage of the JapaneseTokenizerTool
    tool = Japanese_Tokenizer_Tool()
    # text = "日本は美しい国だ"
    text = "天使の投げキッス 捕まえて!(you can try!)"
    execution = tool.execute(text=text)
    print(execution) 