# babyapi/client.py
import os
from typing import Any, Dict, Optional

import requests

DEFAULT_BASE_URL = "https://api.babyapi.org"
DEFAULT_TIMEOUT_SECONDS = 30  # npm uses 30000 ms → 30 seconds here


class BabyAPIError(Exception):
    def __init__(
        self,
        message: str,
        *,
        status: Optional[int] = None,
        code: Optional[str] = None,
        details: Any = None,
    ) -> None:
        super().__init__(message)
        self.name = "BabyAPIError"
        self.status = status
        self.code = code
        self.details = details

    def __str__(self) -> str:
        base = super().__str__()
        if self.status:
            return f"{base} (status={self.status})"
        return base


class BabyAPI:
    """
    Python client for BabyAPI.org

    Mirrors the npm client:

      - Reads api_key from arg or env BABYAPI_API_KEY
      - Uses base_url (default https://api.babyapi.org)
      - Exposes .infer(...) and .call_llm(...)
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    ) -> None:
        api_key = api_key or os.getenv("BABYAPI_API_KEY")
        if not api_key:
            raise BabyAPIError(
                "Missing BabyAPI api_key. Pass it to BabyAPI(api_key=...) "
                "or set BABYAPI_API_KEY env var."
            )

        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

        self._default_headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "User-Agent": "babyapi-py/0.0.1",
        }

    def _request(self, method: str, path: str, json: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"

        try:
            resp = requests.request(
                method=method.upper(),
                url=url,
                json=json,
                headers=self._default_headers,
                timeout=self.timeout_seconds,
            )
        except requests.RequestException as e:
            # Network / timeout / etc.
            raise BabyAPIError(
                "No response received from BabyAPI",
                details=str(e),
            ) from e

        if not resp.ok:
            # Try to parse error body as JSON, fallback to text
            try:
                details = resp.json()
            except ValueError:
                details = resp.text

            raise BabyAPIError(
                f"BabyAPI request failed with status {resp.status_code}",
                status=resp.status_code,
                details=details,
            )

        # Successful response
        try:
            return resp.json()
        except ValueError as e:
            raise BabyAPIError(
                "Invalid JSON response from BabyAPI",
                details=resp.text,
            ) from e

    def infer(
        self,
        *,
        model: str,
        prompt: str,
        options: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Low-level infer call.

        Mirrors JS:
          client.infer({ model, prompt, options })

        POST /infer/:model
        """
        if not model:
            raise BabyAPIError(
                "model is required in infer(model=..., prompt=..., options=...)"
            )
        if not prompt:
            raise BabyAPIError(
                "prompt is required in infer(model=..., prompt=..., options=...)"
            )

        path = f"/infer/{requests.utils.quote(model, safe='')}"
        payload = {
            "prompt": prompt,
            "options": options or {},
        }

        return self._request("POST", path, payload)

    def call_llm(
        self,
        *,
        model: str,
        prompt: str,
        options: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        High-level helper: returns just the text/completion string.

        Mirrors JS callLlm:
          client.callLlm({ model, prompt, options })

        It tries common fields: output, text, completion, choices[0].message.content, etc.
        """
        data = self.infer(model=model, prompt=prompt, options=options)

        # Same heuristics as your JS client
        if isinstance(data.get("output"), str):
            return data["output"]
        if isinstance(data.get("text"), str):
            return data["text"]
        if isinstance(data.get("completion"), str):
            return data["completion"]

        choices = data.get("choices")
        if isinstance(choices, list) and choices:
            choice = choices[0]
            message = choice.get("message") if isinstance(choice, dict) else None
            if message and isinstance(message.get("content"), str):
                return message["content"]
            if isinstance(choice.get("text"), str):
                return choice["text"]

        # Fallback: stringify everything
        return str(data)
