# babyapi (Python)

Official Python client for [BabyAPI.org](https://babyapi.org).

```python
from babyapi import BabyAPI

client = BabyAPI(api_key="YOUR_KEY")  # or set BABYAPI_API_KEY

text = client.call_llm(
    model="mistral",
    prompt="Explain BabyAPI in one line."
)
print(text)
```