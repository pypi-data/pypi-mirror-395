"""Sandboxes Resource
Manage cloud sandboxes for code execution
"""

from typing import Dict, Any, Optional, List
import requests


class SandboxesResource:
    def __init__(self, session: requests.Session, base_url: str, timeout: int):
        self.session = session
        self.base_url = base_url
        self.timeout = timeout

    def create(self, **options) -> 'SandboxInstance':
        response = self.session.post(
            f"{self.base_url}/sandboxes",
            json={
                "name": options.get("name"),
                "template": options.get("template", "nextjs"),
                "metadata": options.get("metadata"),
                "envs": options.get("envs"),
                "timeoutMS": options.get("timeout_ms"),
                "exposePort": options.get("port"),
            },
            timeout=self.timeout
        )
        response.raise_for_status()
        data = response.json()
        return SandboxInstance(self.session, self.base_url, self.timeout, data["sandbox"]["id"])

    def list(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        params = {"status": status} if status else {}
        response = self.session.get(
            f"{self.base_url}/sandboxes",
            params=params,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()["sandboxes"]

    def connect(self, sandbox_id: str) -> 'SandboxInstance':
        return SandboxInstance(self.session, self.base_url, self.timeout, sandbox_id)


class SandboxInstance:
    def __init__(self, session: requests.Session, base_url: str, timeout: int, sandbox_id: str):
        self.session = session
        self.base_url = base_url
        self.timeout = timeout
        self.id = sandbox_id
        self.files = FilesAPI(session, base_url, timeout, sandbox_id)
        self.commands = CommandsAPI(session, base_url, timeout, sandbox_id)

    def get_info(self) -> Dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/sandboxes/{self.id}",
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()["sandbox"]

    def delete(self) -> None:
        response = self.session.delete(
            f"{self.base_url}/sandboxes/{self.id}",
            timeout=self.timeout
        )
        response.raise_for_status()


class FilesAPI:
    def __init__(self, session: requests.Session, base_url: str, timeout: int, sandbox_id: str):
        self.session = session
        self.base_url = base_url
        self.timeout = timeout
        self.sandbox_id = sandbox_id

    def list(self, path: str = "/workspace") -> List[Dict[str, Any]]:
        response = self.session.get(
            f"{self.base_url}/sandboxes/{self.sandbox_id}/files",
            params={"path": path},
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()["files"]

    def read(self, path: str) -> str:
        response = self.session.get(
            f"{self.base_url}/sandboxes/{self.sandbox_id}/files/content",
            params={"path": path},
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()["content"]

    def write(self, path: str, content: str) -> None:
        response = self.session.post(
            f"{self.base_url}/sandboxes/{self.sandbox_id}/files",
            json={"files": [{"path": path, "content": content}]},
            timeout=self.timeout
        )
        response.raise_for_status()

    def write_multiple(self, files: List[Dict[str, str]]) -> None:
        response = self.session.post(
            f"{self.base_url}/sandboxes/{self.sandbox_id}/files",
            json={"files": files},
            timeout=self.timeout
        )
        response.raise_for_status()

    def delete(self, path: str) -> None:
        response = self.session.delete(
            f"{self.base_url}/sandboxes/{self.sandbox_id}/files",
            params={"path": path},
            timeout=self.timeout
        )
        response.raise_for_status()

    def glob(self, pattern: str, path: str = "/workspace") -> Dict[str, Any]:
        response = self.session.post(
            f"{self.base_url}/sandboxes/{self.sandbox_id}/files/search",
            json={"type": "glob", "query": pattern, "path": path},
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def grep(self, pattern: str, path: str = "/workspace", **options) -> Dict[str, Any]:
        response = self.session.post(
            f"{self.base_url}/sandboxes/{self.sandbox_id}/files/search",
            json={"type": "grep", "query": pattern, "path": path, "options": options},
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()


class CommandsAPI:
    def __init__(self, session: requests.Session, base_url: str, timeout: int, sandbox_id: str):
        self.session = session
        self.base_url = base_url
        self.timeout = timeout
        self.sandbox_id = sandbox_id

    def run(self, command: str, workdir: str = "/workspace", envs: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        response = self.session.post(
            f"{self.base_url}/sandboxes/{self.sandbox_id}/execute",
            json={"command": command, "workdir": workdir, "envs": envs},
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()["execution"]
