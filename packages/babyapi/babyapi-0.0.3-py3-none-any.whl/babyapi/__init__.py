# babyapi/__init__.py
from .client import BabyAPI, BabyAPIError

# Optional sugar: functional style, like your "callLlm" but pythonic
def call_llm(model: str, prompt: str, **options):
    """
    Functional wrapper:

        from babyapi import call_llm
        text = call_llm("mistral", "Hello")

    Uses BABYAPI_API_KEY env var by default.
    """
    client = BabyAPI()
    opts = options.get("options") or options  # allow both styles
    return client.call_llm(model=model, prompt=prompt, options=opts)


__all__ = ["BabyAPI", "BabyAPIError", "call_llm"]
