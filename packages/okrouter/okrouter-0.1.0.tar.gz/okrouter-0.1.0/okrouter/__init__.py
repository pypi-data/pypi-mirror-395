import requests
import json
import os

class OkRouterError(Exception):
    """Base exception for OkRouter"""
    pass

class Objectifier:
    """
    Helper class to convert a dictionary into an object, 
    allowing access via dot notation (e.g., response.choices[0].message).
    """
    def __init__(self, data):
        for key, value in data.items():
            if isinstance(value, (list, tuple)):
                setattr(self, key, [Objectifier(x) if isinstance(x, dict) else x for x in value])
            else:
                setattr(self, key, Objectifier(value) if isinstance(value, dict) else value)

class Completions:
    def __init__(self, client):
        self.client = client

    def create(self, model, messages, temperature=0.7, max_tokens=None, **kwargs):
        """
        Send a chat completion request to OKRouter API.
        """
        url = f"{self.client.base_url}/chat/completions"
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            **kwargs
        }
        
        if max_tokens:
            payload["max_tokens"] = max_tokens

        headers = {
            "Authorization": f"Bearer {self.client.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "okrouter-python-sdk/0.1.0"
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            # Convert JSON response to an object so README example works
            return Objectifier(response.json())
            
        except requests.exceptions.RequestException as e:
            raise OkRouterError(f"Request failed: {e}")

class Chat:
    def __init__(self, client):
        self.completions = Completions(client)

class Client:
    def __init__(self, api_key=None, base_url="https://okrouter.com/api/v1"):
        """
        Initialize the OKRouter Client.
        
        Args:
            api_key (str): Your OKRouter API Key.
            base_url (str): The API endpoint (default: https://okrouter.com/api/v1).
        """
        self.api_key = api_key or os.environ.get("OKROUTER_API_KEY")
        
        if not self.api_key:
            raise OkRouterError("API Key is required. Pass it to Client() or set OKROUTER_API_KEY env var.")
            
        # Ensure base_url doesn't end with slash
        self.base_url = base_url.rstrip("/")
        
        # Initialize namespaces
        self.chat = Chat(self)

# Expose the Client directly
__all__ = ["Client", "OkRouterError"]
