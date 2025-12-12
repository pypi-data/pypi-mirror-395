import docker
from docker.models.containers import Container
from pathlib import Path
from typing import List, Dict, Optional

from terratest.constants import DEFAULT_TERRAFORM_IMAGE


class DockerManager:
    """
    Manejo de contenedores Terraform con soporte SSH real.
    """

    def __init__(self, image: str = DEFAULT_TERRAFORM_IMAGE):
        self.client = docker.from_env()
        self.image = image

    def create_container(
        self,
        job_id: str,
        workspace: Path,
        output: Path,
        work: Path,
        ssh_home: Optional[Path] = None,
        enable_ssh: bool = False,
        env: Optional[Dict[str, str]] = None,
        tf_cloud_token: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_session_token: Optional[str] = None,
    ) -> Container:

        volumes = {
            str(workspace): {"bind": "/workspace", "mode": "ro"},
            str(output):    {"bind": "/output", "mode": "rw"},
            str(work):      {"bind": "/work", "mode": "rw"},
        }

        # Variables de entorno
        env = env or {}

        # ← SSH support (solo si está habilitado)
        if enable_ssh and ssh_home and ssh_home.exists():
            volumes[str(ssh_home)] = {"bind": "/ssh-home", "mode": "rw"}
            env["GIT_SSH_COMMAND"] = "ssh -i /ssh-home/id_rsa -o StrictHostKeyChecking=no"
        
        # ← Terraform Cloud support
        if tf_cloud_token:
            env["TF_TOKEN_app_terraform_io"] = tf_cloud_token
        
        # ← AWS Credentials support
        if aws_access_key_id:
            env["AWS_ACCESS_KEY_ID"] = aws_access_key_id
        if aws_secret_access_key:
            env["AWS_SECRET_ACCESS_KEY"] = aws_secret_access_key
        if aws_session_token:
            env["AWS_SESSION_TOKEN"] = aws_session_token

        container = self.client.containers.create(
            image=self.image,
            name=f"terratest-{job_id}",
            entrypoint=["/bin/sh", "-c", "tail -f /dev/null"],
            volumes=volumes,
            environment=env,
            network_mode="bridge",
            tty=True,
            stdin_open=True,
            auto_remove=True,
        )

        return container

    def start_container(self, container: Container):
        container.start()

    def exec(self, container: Container, cmd: List[str]) -> str:
        exec_id = self.client.api.exec_create(container.id, cmd)
        output = self.client.api.exec_start(exec_id).decode("utf-8")
        return output

    def stream_exec(self, container, cmd: list):
        exec_id = self.client.api.exec_create(container.id, cmd, tty=True)
        stream = self.client.api.exec_start(exec_id, stream=True)
        for chunk in stream:
            yield chunk.decode("utf-8", errors="ignore")

    def stop_container(self, container: Container):
        try:
            container.stop()
        except Exception:
            pass

    def cleanup_container(self, container: Container):
        try:
            container.remove(force=True)
        except Exception:
            pass
