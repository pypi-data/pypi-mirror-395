"""Chats Resource
Interact with AI chat sessions
"""

from typing import Dict, Any, List, Optional
import requests


class ChatsResource:
    def __init__(self, session: requests.Session, base_url: str, timeout: int):
        self.session = session
        self.base_url = base_url
        self.timeout = timeout

    def create(self, title: str = "New Chat", visibility: str = "private") -> 'ChatInstance':
        response = self.session.post(
            f"{self.base_url}/chats",
            json={"title": title, "visibility": visibility},
            timeout=self.timeout
        )
        response.raise_for_status()
        data = response.json()
        return ChatInstance(self.session, self.base_url, self.timeout, data["chat"]["id"])

    def list(self) -> List[Dict[str, Any]]:
        response = self.session.get(
            f"{self.base_url}/chats",
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()["chats"]

    def connect(self, chat_id: str) -> 'ChatInstance':
        return ChatInstance(self.session, self.base_url, self.timeout, chat_id)


class ChatInstance:
    def __init__(self, session: requests.Session, base_url: str, timeout: int, chat_id: str):
        self.session = session
        self.base_url = base_url
        self.timeout = timeout
        self.id = chat_id

    def get_info(self) -> Dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/chats/{self.id}",
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()["chat"]

    def delete(self) -> None:
        response = self.session.delete(
            f"{self.base_url}/chats/{self.id}",
            timeout=self.timeout
        )
        response.raise_for_status()

    def messages(self) -> List[Dict[str, Any]]:
        response = self.session.get(
            f"{self.base_url}/chats/{self.id}/messages",
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()["messages"]

    def send(self, content: str) -> Dict[str, Any]:
        response = self.session.post(
            f"{self.base_url}/chats/{self.id}/messages",
            json={"content": content},
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()["message"]
