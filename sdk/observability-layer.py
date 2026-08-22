import json
import os
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

from dotenv import load_dotenv


load_dotenv(Path(__file__).with_name(".env"))


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"{name} environment variable is not set")
    return value


BASE_URL = _required_env("BASE_URL")
OPENAI_RESPONSES_URL = _required_env("OPENAI_RESPONSES_URL")


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
