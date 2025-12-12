from datetime import datetime
import uuid
import json
from pathlib import Path
from typing import Dict, Any, Optional

from terratest.core.docker_manager import DockerManager
from terratest.core.validation import validate_module_path, validate_terraform_files, ValidationError
from terratest.utils.filesystem import (
    ensure_base_dirs,
    get_job_workspace_dir,
    get_job_output_dir,
    copy_tree,
)
from terratest.utils.logging import get_job_logger
from terratest.utils.config_store import get_config_store
from terratest.constants import DEFAULT_TERRAFORM_IMAGE


class JobExecutor:
    """FASE 1–4: Docker + Terraform real + Parser con SSH integrado."""

    def __init__(self) -> None:
        ensure_base_dirs()
        
        # Obtener imagen seleccionada del config store
        config_store = get_config_store()
        selected_image = config_store.get('selected_docker_image', DEFAULT_TERRAFORM_IMAGE)
        
        self.docker = DockerManager(image=selected_image)

    def _generate_job_id(self) -> str:
        return f"job-{uuid.uuid4().hex[:8]}"

    def _stream_and_log(self, logger, container, cmd: list, log_file: Path):
        with log_file.open("a", encoding="utf-8") as f:
            for line in self.docker.stream_exec(container, cmd):
                clean = line.rstrip()
                logger.info(clean)
                f.write(clean + "\n")

    def _parse_outputs_from_plan(self, plan_data: dict) -> dict:
        outputs = {}
        output_changes = plan_data.get("output_changes", {})
        for key, item in output_changes.items():
            outputs[key] = item.get("after")
        return outputs

    def _parse_plan_json(self, plan_path: Path) -> Dict[str, Any]:
        if not plan_path.exists():
            return {"summary": None, "resources": []}

        raw = plan_path.read_text(encoding="utf-8").strip()
        if not raw:
            return {"summary": None, "resources": []}

        data = json.loads(raw)
        changes = data.get("resource_changes", [])

        summary = {"add": 0, "change": 0, "destroy": 0}
        resources = []

        for rc in changes:
            actions = rc.get("change", {}).get("actions", [])
            if "create" in actions:
                summary["add"] += 1
            if "update" in actions:
                summary["change"] += 1
            if "delete" in actions:
                summary["destroy"] += 1

            resources.append({
                "type": rc.get("type"),
                "name": rc.get("name"),
                "actions": actions,
            })

        return {"summary": summary, "resources": resources}

    def execute_job(
        self,
        module_path: str | Path,
        secrets: Optional[Dict[str, str]] = None,
        run_init: bool = True,
        run_plan: bool = True,
        run_apply: bool = False,
        timeout: int = 600,
        enable_ssh: bool = False,
        ssh_key_path: Optional[str] = None,
        tf_cloud_token: Optional[str] = None,
        tf_cloud_org: Optional[str] = None,
        tf_cloud_workspace: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_session_token: Optional[str] = None,
    ) -> Dict[str, Any]:

        started_at = datetime.utcnow()
        job_id = self._generate_job_id()
        logger = get_job_logger(job_id)

        container = None

        try:
            # --------------------- FASE 1 ---------------------
            module_path = validate_module_path(module_path)
            validate_terraform_files(module_path)

            job_workspace = get_job_workspace_dir(job_id)
            job_output = get_job_output_dir(job_id)
            copy_tree(module_path, job_workspace)

            job_work = job_output / "work"
            job_work.mkdir(parents=True, exist_ok=True)

            log_file = job_output / "terraform.log"

            # Configuración SSH
            env = {}
            ssh_home = None
            
            if enable_ssh:
                if ssh_key_path:
                    ssh_home = Path(ssh_key_path).parent
                else:
                    ssh_home = Path.home() / ".ssh"
                
                if ssh_home.exists():
                    logger.info(f"SSH habilitado: {ssh_home}")
                    env["GIT_SSH_COMMAND"] = (
                        "ssh -i /ssh-home/id_rsa "
                        "-o StrictHostKeyChecking=no "
                        "-o UserKnownHostsFile=/ssh-home/known_hosts"
                    )
                else:
                    logger.warning(f"SSH habilitado pero directorio no existe: {ssh_home}")
                    ssh_home = None
            else:
                logger.info("SSH deshabilitado")
            
            # Configuración Terraform Cloud
            if tf_cloud_token:
                logger.info("Terraform Cloud habilitado")
                env["TF_TOKEN_app_terraform_io"] = tf_cloud_token
                
                if tf_cloud_org and tf_cloud_workspace:
                    logger.info(f"Workspace Cloud: {tf_cloud_org}/{tf_cloud_workspace}")
            
            # Configuración AWS
            if aws_access_key_id:
                logger.info("AWS credentials configuradas")
                env["AWS_ACCESS_KEY_ID"] = aws_access_key_id
                
                if aws_secret_access_key:
                    env["AWS_SECRET_ACCESS_KEY"] = aws_secret_access_key
                
                if aws_session_token:
                    env["AWS_SESSION_TOKEN"] = aws_session_token
                    logger.info("AWS session token incluido")

            # --------------------- FASE 2 ---------------------
            container = self.docker.create_container(
                job_id=job_id,
                workspace=job_workspace,
                output=job_output,
                work=job_work,
                ssh_home=ssh_home,
                enable_ssh=enable_ssh,
                env=env,
                tf_cloud_token=tf_cloud_token,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                aws_session_token=aws_session_token,
            )
            self.docker.start_container(container)

            # Fix de permisos SSH — solo si está habilitado
            if enable_ssh and ssh_home:
                logger.info("Configurando permisos SSH en container...")
                self.docker.exec(container, ["/bin/sh", "-c", "chmod 600 /ssh-home/id_rsa || true"])
                self.docker.exec(container, ["/bin/sh", "-c", "chmod 644 /ssh-home/id_rsa.pub || true"])
                self.docker.exec(container, ["/bin/sh", "-c", "touch /ssh-home/known_hosts"])
                self.docker.exec(container, ["/bin/sh", "-c", "chmod 644 /ssh-home/known_hosts"])

            tf_version = self.docker.exec(container, ["terraform", "--version"])

            # --------------------- FASE 3 ---------------------
            if run_init:
                self._stream_and_log(
                    logger, container,
                    ["/bin/sh", "-c",
                     "cd /work && terraform init -input=false -no-color -lock=false -from-module=/workspace"],
                    log_file,
                )

            if run_plan:
                self._stream_and_log(
                    logger, container,
                    ["/bin/sh", "-c",
                     "cd /work && terraform plan -input=false -no-color -lock=false -out=/work/tfplan"],
                    log_file,
                )

                self._stream_and_log(
                    logger, container,
                    ["/bin/sh", "-c",
                     "cd /work && terraform show -json /work/tfplan | tee /output/plan.json"],
                    log_file,
                )

            # --------------------- OUTPUTS ---------------------
            outputs_raw = self.docker.exec(
                container,
                ["/bin/sh", "-c", "cd /work && (terraform output -json || echo '{}')"]
            )
            (job_output / "outputs.json").write_text(outputs_raw, encoding="utf-8")

            outputs = json.loads(outputs_raw.strip() or "{}")

            if not outputs:
                try:
                    plan_data = json.loads((job_output / "plan.json").read_text(encoding="utf-8"))
                    outputs = self._parse_outputs_from_plan(plan_data)
                except:
                    outputs = {}

            # --------------------- FASE 4 ---------------------
            parsed = self._parse_plan_json(job_output / "plan.json")

            finished_at = datetime.utcnow()

            return {
                "job_id": job_id,
                "status": "terraform_complete",
                "workspace_dir": str(job_workspace),
                "output_dir": str(job_output),
                "terraform_version": tf_version.strip(),
                "started_at": started_at.isoformat() + "Z",
                "finished_at": finished_at.isoformat() + "Z",
                "duration_seconds": (finished_at - started_at).total_seconds(),
                "plan_summary": parsed["summary"],
                "resources": parsed["resources"],
                "outputs": outputs,
            }

        except Exception as ex:
            return {"job_id": job_id, "status": "error", "error": str(ex)}

        finally:
            if container:
                try: self.docker.stop_container(container)
                except: pass
                try: self.docker.cleanup_container(container)
                except: pass
