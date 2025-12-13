"""Usage Resource
Track platform usage and API keys
"""

from typing import Dict, Any, List
import requests


class UsageResource:
    def __init__(self, session: requests.Session, base_url: str, timeout: int):
        self.session = session
        self.base_url = base_url
        self.timeout = timeout

    def get(self, range: str = "7d") -> Dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/usage",
            params={"range": range},
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()["usage"]

    def keys(self) -> List[Dict[str, Any]]:
        response = self.session.get(
            f"{self.base_url}/usage/key",
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()["keys"]
