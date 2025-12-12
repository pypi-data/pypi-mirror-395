# summrai

`summrai` is a lightweight and secure Python library for interacting with AI text-generation models.  
It is designed for use in Flask applications or any Python project that needs AI processing.

✔ **No API keys stored inside the library**  
✔ **Supports free Google Gemini API (OpenAI-compatible)**  
✔ **Provides helper utilities for summarizing and formatting text**

---

## 🚀 Installation




---

## 📌 Usage Example

```python
from summrai import AIClient, summarize_text

# Create the AI client (API key must be provided manually)
client = AIClient(api_key="YOUR_GEMINI_API_KEY")

# Basic response
print(client.get_response("Explain machine learning."))

# Summarization
text = "Artificial Intelligence is transforming industries..."
summary = summarize_text(text, client)
print(summary)
