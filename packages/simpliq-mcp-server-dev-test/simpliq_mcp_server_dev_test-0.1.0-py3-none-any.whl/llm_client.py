from abc import ABC, abstractmethod
import os
import logging
from typing import Optional
import requests


class LLMClient(ABC):
    """Abstract LLM client. Implementations must provide generate(prompt)->str."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        raise NotImplementedError()


class MockLLMClient(LLMClient):
    """Very small mock client used for tests. It returns responses based on substring matching.

    response_map: dict where key is a substring to look for in prompt and value is the response string.
    If no key matches, '__default__' entry is returned if present, otherwise 'UNABLE_TO_GENERATE'.
    """

    def __init__(self, response_map: dict | None = None):
        self.response_map = response_map or {}

    def generate(self, prompt: str) -> str:
        for k, v in self.response_map.items():
            if k == '__default__':
                continue
            if k in prompt:
                return v
        return self.response_map.get('__default__', 'UNABLE_TO_GENERATE')


class OpenAIClient(LLMClient):
    """OpenAI chat completions client (sem dependência do SDK oficial).

    Usa endpoint /v1/chat/completions. Configuração por env vars:
      - OPENAI_API_KEY (obrigatório)
      - SIMPLIQ_OPENAI_MODEL (opcional, padrão: gpt-4o-mini)
      - SIMPLIQ_OPENAI_BASE_URL (opcional, padrão: https://api.openai.com)
      - SIMPLIQ_OPENAI_TEMPERATURE (opcional, padrão: 0.1)
      - SIMPLIQ_OPENAI_MAX_TOKENS (opcional, padrão: 800)
    """

    def __init__(self,
                 api_key: Optional[str] = None,
                 model: Optional[str] = None,
                 base_url: Optional[str] = None,
                 temperature: Optional[float] = None,
                 max_tokens: Optional[int] = None):
        self.logger = logging.getLogger(__name__)
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY não definido")
        
        # Debug: Print which API key is being used
        print(f"🔑 DEBUG OpenAIClient: API Key = {self.api_key[:20]}...{self.api_key[-6:]}")
        print(f"🔑 DEBUG: OPENAI_API_KEY env var = {os.environ.get('OPENAI_API_KEY', 'NOT SET')[:20] if os.environ.get('OPENAI_API_KEY') else 'NOT SET'}...")
        
        self.model = model or os.environ.get("SIMPLIQ_OPENAI_MODEL", "gpt-4o-mini")
        self.base_url = (base_url or os.environ.get("SIMPLIQ_OPENAI_BASE_URL") or "https://api.openai.com").rstrip("/")
        self.temperature = float(os.environ.get("SIMPLIQ_OPENAI_TEMPERATURE", temperature if temperature is not None else 0.1))
        self.max_tokens = int(os.environ.get("SIMPLIQ_OPENAI_MAX_TOKENS", max_tokens if max_tokens is not None else 800))

    def generate(self, prompt: str) -> str:
        """Generate content with configurável retry/backoff e timeout.

        Env vars suportadas (opcionais):
          SIMPLIQ_LLM_FAIL_FAST -> "1"/true para tentar só uma vez
          SIMPLIQ_LLM_MAX_ATTEMPTS -> número máximo de tentativas (default 3)
          SIMPLIQ_LLM_HTTP_TIMEOUT -> timeout da requisição em segundos (default 30)
          SIMPLIQ_LLM_BACKOFF_BASE -> base para backoff linear/exponencial (default 2)
          SIMPLIQ_LLM_RETRY_ON_429 -> "0" para desabilitar retry quando 429 (default 1)

        Retorna 'UNABLE_TO_GENERATE' se todas as tentativas falharem.
        """
        url = f"{self.base_url}/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }

        def _truthy(v: Optional[str], default: bool = False) -> bool:
            if v is None:
                return default
            return str(v).strip().lower() in ("1", "true", "yes", "on")

        fail_fast = _truthy(os.environ.get("SIMPLIQ_LLM_FAIL_FAST"), False)
        max_attempts = int(os.environ.get("SIMPLIQ_LLM_MAX_ATTEMPTS", 3))
        if fail_fast:
            max_attempts = 1
        timeout_s = float(os.environ.get("SIMPLIQ_LLM_HTTP_TIMEOUT", 30))
        backoff_base = float(os.environ.get("SIMPLIQ_LLM_BACKOFF_BASE", 2))
        retry_on_429 = _truthy(os.environ.get("SIMPLIQ_LLM_RETRY_ON_429"), True)

        attempts = 0
        while attempts < max_attempts:
            attempts += 1
            try:
                resp = requests.post(url, json=payload, headers=headers, timeout=timeout_s)
                if resp.status_code == 429 and retry_on_429 and attempts < max_attempts:
                    self.logger.warning(f"OpenAI 429 rate/quota attempt={attempts}/{max_attempts}; backoff...")
                    import time as _t
                    _t.sleep(backoff_base * attempts)
                    continue
                resp.raise_for_status()
                data = resp.json()
                content = data.get("choices", [{}])[0].get("message", {}).get("content")
                return content or "UNABLE_TO_GENERATE"
            except Exception as e:
                self.logger.error(f"OpenAIClient error attempt={attempts}/{max_attempts}: {e}")
                if attempts < max_attempts:
                    import time as _t
                    _t.sleep(backoff_base * attempts)
                    continue
                return "UNABLE_TO_GENERATE"
        return "UNABLE_TO_GENERATE"


class AnthropicClient(LLMClient):
    """Anthropic Messages API client (sem dependência do SDK oficial).

    Usa endpoint /v1/messages. Configuração por env vars:
      - ANTHROPIC_API_KEY (obrigatório)
      - SIMPLIQ_ANTHROPIC_MODEL (opcional, padrão: claude-3-5-sonnet-latest)
      - SIMPLIQ_ANTHROPIC_BASE_URL (opcional, padrão: https://api.anthropic.com)
      - SIMPLIQ_ANTHROPIC_TEMPERATURE (opcional, padrão: 0.1)
      - SIMPLIQ_ANTHROPIC_MAX_TOKENS (opcional, padrão: 800)
    """

    def __init__(self,
                 api_key: Optional[str] = None,
                 model: Optional[str] = None,
                 base_url: Optional[str] = None,
                 temperature: Optional[float] = None,
                 max_tokens: Optional[int] = None):
        self.logger = logging.getLogger(__name__)
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise RuntimeError("ANTHROPIC_API_KEY não definido")
        self.model = model or os.environ.get("SIMPLIQ_ANTHROPIC_MODEL", "claude-3-5-sonnet-latest")
        self.base_url = (base_url or os.environ.get("SIMPLIQ_ANTHROPIC_BASE_URL") or "https://api.anthropic.com").rstrip("/")
        self.temperature = float(os.environ.get("SIMPLIQ_ANTHROPIC_TEMPERATURE", temperature if temperature is not None else 0.1))
        self.max_tokens = int(os.environ.get("SIMPLIQ_ANTHROPIC_MAX_TOKENS", max_tokens if max_tokens is not None else 800))

    def generate(self, prompt: str) -> str:
        """Anthropic generation com retry/backoff configurável.

        Variáveis mesmas da OpenAI (SIMPLIQ_LLM_FAIL_FAST, etc.).
        """
        url = f"{self.base_url}/v1/messages"
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        payload = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "messages": [{"role": "user", "content": prompt}]
        }

        def _truthy(v: Optional[str], default: bool = False) -> bool:
            if v is None:
                return default
            return str(v).strip().lower() in ("1", "true", "yes", "on")

        fail_fast = _truthy(os.environ.get("SIMPLIQ_LLM_FAIL_FAST"), False)
        max_attempts = int(os.environ.get("SIMPLIQ_LLM_MAX_ATTEMPTS", 3))
        if fail_fast:
            max_attempts = 1
        timeout_s = float(os.environ.get("SIMPLIQ_LLM_HTTP_TIMEOUT", 30))
        backoff_base = float(os.environ.get("SIMPLIQ_LLM_BACKOFF_BASE", 2))
        retry_on_429 = _truthy(os.environ.get("SIMPLIQ_LLM_RETRY_ON_429"), True)

        attempts = 0
        while attempts < max_attempts:
            attempts += 1
            try:
                resp = requests.post(url, json=payload, headers=headers, timeout=timeout_s)
                if resp.status_code == 429 and retry_on_429 and attempts < max_attempts:
                    self.logger.warning(f"Anthropic 429 rate/quota attempt={attempts}/{max_attempts}; backoff...")
                    import time as _t
                    _t.sleep(backoff_base * attempts)
                    continue
                resp.raise_for_status()
                data = resp.json()
                contents = data.get("content", [])
                if contents and isinstance(contents, list):
                    for block in contents:
                        if isinstance(block, dict) and block.get("type") == "text":
                            return block.get("text") or "UNABLE_TO_GENERATE"
                return "UNABLE_TO_GENERATE"
            except Exception as e:
                self.logger.error(f"AnthropicClient error attempt={attempts}/{max_attempts}: {e}")
                if attempts < max_attempts:
                    import time as _t
                    _t.sleep(backoff_base * attempts)
                    continue
                return "UNABLE_TO_GENERATE"
        return "UNABLE_TO_GENERATE"


class GeminiClient(LLMClient):
    """Google Gemini Generative Language API client (without official SDK).

    Default REST endpoint shape:
      POST {base_url}/v1beta/models/{model}:generateContent?key={api_key}

    Config via env vars (mirrors other providers):
      - GEMINI_API_KEY or GOOGLE_API_KEY (required)
      - SIMPLIQ_GEMINI_MODEL (optional, default: gemini-1.5-pro)
      - SIMPLIQ_GEMINI_BASE_URL (optional, default: https://generativelanguage.googleapis.com)
      - SIMPLIQ_GEMINI_TEMPERATURE (optional, default: 0.1)
      - SIMPLIQ_GEMINI_MAX_TOKENS (optional, default: 800)
      - Retry/backoff knobs same as OpenAI/Anthropic: SIMPLIQ_LLM_* envs
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ):
        self.logger = logging.getLogger(__name__)
        # Prefer GEMINI_API_KEY, fallback GOOGLE_API_KEY
        self.api_key = (
            api_key
            or os.environ.get("GEMINI_API_KEY")
            or os.environ.get("GOOGLE_API_KEY")
        )
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY/GOOGLE_API_KEY não definido")

        self.model = model or os.environ.get("SIMPLIQ_GEMINI_MODEL", "gemini-1.5-pro")
        self.base_url = (
            (base_url or os.environ.get("SIMPLIQ_GEMINI_BASE_URL") or "https://generativelanguage.googleapis.com").rstrip("/")
        )
        self.temperature = float(
            os.environ.get(
                "SIMPLIQ_GEMINI_TEMPERATURE", temperature if temperature is not None else 0.1
            )
        )
        self.max_tokens = int(
            os.environ.get(
                "SIMPLIQ_GEMINI_MAX_TOKENS", max_tokens if max_tokens is not None else 800
            )
        )

    def generate(self, prompt: str) -> str:
        """Generate text using Gemini with configurable retry/backoff.

        Uses the same SIMPLIQ_LLM_* environment variables as other providers.
        """
        # Endpoint for generateContent
        url = f"{self.base_url}/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt}],
                }
            ],
            "generationConfig": {
                "temperature": self.temperature,
                "maxOutputTokens": self.max_tokens,
            },
        }

        def _truthy(v: Optional[str], default: bool = False) -> bool:
            if v is None:
                return default
            return str(v).strip().lower() in ("1", "true", "yes", "on")

        fail_fast = _truthy(os.environ.get("SIMPLIQ_LLM_FAIL_FAST"), False)
        max_attempts = int(os.environ.get("SIMPLIQ_LLM_MAX_ATTEMPTS", 3))
        if fail_fast:
            max_attempts = 1
        timeout_s = float(os.environ.get("SIMPLIQ_LLM_HTTP_TIMEOUT", 30))
        backoff_base = float(os.environ.get("SIMPLIQ_LLM_BACKOFF_BASE", 2))
        retry_on_429 = _truthy(os.environ.get("SIMPLIQ_LLM_RETRY_ON_429"), True)

        attempts = 0
        while attempts < max_attempts:
            attempts += 1
            try:
                resp = requests.post(url, json=payload, headers=headers, timeout=timeout_s)
                # Gemini often returns 429 for rate; honor retry flag
                if resp.status_code == 429 and retry_on_429 and attempts < max_attempts:
                    self.logger.warning(
                        f"Gemini 429 rate/quota attempt={attempts}/{max_attempts}; backoff..."
                    )
                    import time as _t

                    _t.sleep(backoff_base * attempts)
                    continue
                resp.raise_for_status()
                data = resp.json()
                # Extract first candidate text
                # Response shape: { candidates: [ { content: { parts: [ { text } ] } } ] }
                candidates = data.get("candidates") or []
                if candidates:
                    content = candidates[0].get("content") or {}
                    parts = content.get("parts") or []
                    for p in parts:
                        if isinstance(p, dict) and "text" in p:
                            return p.get("text") or "UNABLE_TO_GENERATE"
                return "UNABLE_TO_GENERATE"
            except Exception as e:
                self.logger.error(f"GeminiClient error attempt={attempts}/{max_attempts}: {e}")
                if attempts < max_attempts:
                    import time as _t

                    _t.sleep(backoff_base * attempts)
                    continue
                return "UNABLE_TO_GENERATE"
        return "UNABLE_TO_GENERATE"
