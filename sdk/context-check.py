import json
import os
from typing import Any
from urllib.request import Request, urlopen


BASE_URL = "http://localhost:3000"
OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"


def send_json(data: Any) -> Any:
    """Send data to the local server as JSON and return its JSON response."""
    request = Request(
        BASE_URL,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urlopen(request) as response:
        return json.load(response)


def receive_json() -> Any:
    """Receive JSON data from the local server."""
    request = Request(
        BASE_URL,
        headers={"Accept": "application/json"},
        method="GET",
    )

    with urlopen(request) as response:
        return json.load(response)


def call_openai(prompt: str, model: str = "gpt-5.6") -> Any:
    """Send a prompt to the OpenAI Responses API and return its JSON response."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")

    request = Request(
        OPENAI_RESPONSES_URL,
        data=json.dumps({"model": model, "input": prompt}).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urlopen(request) as response:
        return json.load(response)
