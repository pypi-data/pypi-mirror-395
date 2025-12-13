"""OSE SDK Client
Main entry point for programmatic access to the OSE platform
"""

import requests
from typing import Optional
from .resources.sandboxes import SandboxesResource
from .resources.deployments import DeploymentsResource
from .resources.chats import ChatsResource
from .resources.usage import UsageResource


class OSE:
    def __init__(self, api_key: str, base_url: Optional[str] = None, timeout: int = 60):
        if not api_key:
            raise ValueError("API key is required")

        self.base_url = base_url or "http://213.136.81.77:8000/api/v1"
        self.timeout = timeout

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "@ose/sdk-python/1.0.0",
        })

        self.sandboxes = SandboxesResource(self.session, self.base_url, self.timeout)
        self.deployments = DeploymentsResource(self.session, self.base_url, self.timeout)
        self.chats = ChatsResource(self.session, self.base_url, self.timeout)
        self.usage = UsageResource(self.session, self.base_url, self.timeout)
