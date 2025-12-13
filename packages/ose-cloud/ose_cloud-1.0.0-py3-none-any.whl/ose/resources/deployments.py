"""Deployments Resource
Deploy applications to OSE Cloud
"""

from typing import Dict, Any, Optional, List
import requests


class DeploymentsResource:
    def __init__(self, session: requests.Session, base_url: str, timeout: int):
        self.session = session
        self.base_url = base_url
        self.timeout = timeout

    def create(self, name: str, sandbox_id: str, **options) -> 'DeploymentInstance':
        response = self.session.post(
            f"{self.base_url}/deployments",
            json={
                "name": name,
                "projectType": options.get("project_type", "nextjs"),
                "sandboxId": sandbox_id,
                "port": options.get("port", 3000),
                "customDomain": options.get("custom_domain"),
                "buildCommand": options.get("build_command"),
                "installCommand": options.get("install_command"),
                "startCommand": options.get("start_command"),
                "environmentVariables": options.get("environment_variables"),
            },
            timeout=self.timeout
        )
        response.raise_for_status()
        data = response.json()
        return DeploymentInstance(self.session, self.base_url, self.timeout, data["deployment"]["id"])

    def list(self) -> List[Dict[str, Any]]:
        response = self.session.get(
            f"{self.base_url}/deployments",
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()["deployments"]

    def connect(self, deployment_id: str) -> 'DeploymentInstance':
        return DeploymentInstance(self.session, self.base_url, self.timeout, deployment_id)


class DeploymentInstance:
    def __init__(self, session: requests.Session, base_url: str, timeout: int, deployment_id: str):
        self.session = session
        self.base_url = base_url
        self.timeout = timeout
        self.id = deployment_id
        self.logs = LogsAPI(session, base_url, timeout, deployment_id)

    def get_info(self) -> Dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/deployments/{self.id}",
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()["deployment"]

    def delete(self) -> None:
        response = self.session.delete(
            f"{self.base_url}/deployments/{self.id}",
            timeout=self.timeout
        )
        response.raise_for_status()

    def restart(self) -> None:
        response = self.session.post(
            f"{self.base_url}/deployments/{self.id}/restart",
            timeout=self.timeout
        )
        response.raise_for_status()

    def stop(self) -> None:
        response = self.session.post(
            f"{self.base_url}/deployments/{self.id}/stop",
            timeout=self.timeout
        )
        response.raise_for_status()


class LogsAPI:
    def __init__(self, session: requests.Session, base_url: str, timeout: int, deployment_id: str):
        self.session = session
        self.base_url = base_url
        self.timeout = timeout
        self.deployment_id = deployment_id

    def get(self, lines: int = 100) -> str:
        response = self.session.get(
            f"{self.base_url}/deployments/{self.deployment_id}/logs",
            params={"lines": lines},
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()["logs"]
