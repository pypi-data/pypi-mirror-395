# OKRouter Python Client

[![PyPI version](https://badge.fury.io/py/okrouter.svg)](https://badge.fury.io/py/okrouter)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

The official Python client for **[OKRouter](https://okrouter.com)**.

OKRouter allows you to integrate **OpenAI (GPT-5), Anthropic (Claude 4-5),  XAI (Grok 4),and Google (Gemini-3-pro)** APIs using a single standardized interface.

## 🚀 Why use OKRouter?

* **Unified API:** Switch between models without changing code.
* **Cost Saving:** Automatic routing to the most cost-effective provider.
* **High Availability:** Smart fallback to prevent downtime.
* 👉 **Get your API Key here:** [https://okrouter.com](https://okrouter.com)

## 📦 Installation

```bash
pip install okrouter
💡 Usage
Python

import okrouter

# Initialize the client with your API Key
client = okrouter.Client(api_key="YOUR_OKROUTER_KEY")

# Create a chat completion
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.choices[0].message.content)
🔗 Resources
Official Website

API Documentation
