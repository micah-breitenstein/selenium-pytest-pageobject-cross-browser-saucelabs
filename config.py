import os
from dataclasses import dataclass

# Defaults (safe fallbacks)
BASE_URL = os.getenv("BASE_URL", "https://the-internet.herokuapp.com").rstrip("/")
TIMEOUT = int(os.getenv("TIMEOUT", "10"))

@dataclass(frozen=True)
class Config:
    base_url: str
