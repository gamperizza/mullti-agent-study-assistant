"""LLM configuration"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

class LLMConfig:
    """LLM configuration for your server"""
    
    @staticmethod
    def get_llm():
        """Creates LLM with your settings"""
        llm = ChatOpenAI(
            openai_api_base=os.getenv("LITELLM_BASE_URL", "http://your_base_url"),
            openai_api_key=os.getenv("LITELLM_API_KEY", "key"),
            model_name=os.getenv("MODEL_NAME", "qwen3-32b"),
            temperature=0.3
        )
        print(f"LLM created: {llm.model_name}")
        print(f" Base URL: {llm.openai_api_base}")
        print(f" Temperature: {llm.temperature}")
        return llm