from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass
class ClientConfig:
    api_key: str
    base_url: str = "https://api.sportsdatabase.io/v1"
    timeout: float = 10.0
    max_retries: int = 2
    user_agent_suffix: str = ""

    def __post_init__(self) -> None:
        parsed = urlparse(self.base_url)
        if parsed.scheme not in {"http", "https"}:
            raise ValueError("base_url must include http or https scheme")
