import requests
import logging
from typing import Optional, Dict, Any

class VLLMClient:
    """
    vllm server API 客户端，支持OpenAI兼容接口
    """
    def __init__(self, base_url: str = "http://localhost:9001/v1/completions", timeout: int = 60):
        self.base_url = base_url
        self.timeout = timeout
        self.logger = logging.getLogger(self.__class__.__name__)

    def chat_completion(self, prompt: str, max_tokens: int = 1024, temperature: float = 0.2, stop: Optional[list] = None) -> Optional[str]:
        """
        调用vllm server生成文本
        """
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": "Qwen3-8B",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        if stop:
            payload["stop"] = stop
        try:
            resp = requests.post(self.base_url, json=payload, headers=headers, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
            # OpenAI格式兼容
            if "choices" in data and data["choices"]:
                return data["choices"][0]["message"]["content"]
            else:
                self.logger.error(f"vllm返回格式异常: {data}")
                return None
        except Exception as e:
            self.logger.error(f"vllm请求失败: {e}")
            return None 