import json
from pathlib import Path


class TerraformPlanParser:
    """Convierte plan.json en datos estructurados útiles."""

    def load_plan(self, plan_path: Path) -> dict:
        if not plan_path.exists():
            raise FileNotFoundError(f"El archivo {plan_path} no existe")

        with plan_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        return data

    def get_summary(self, plan: dict) -> dict:
        """Retorna:
        - recursos a crear
        - actualizar
        - eliminar
        """

        resource_changes = plan.get("resource_changes", [])
        summary = {"add": 0, "change": 0, "destroy": 0}

        for rc in resource_changes:
            action = rc.get("change", {}).get("actions", [])
            if "create" in action:
                summary["add"] += 1
            if "update" in action:
                summary["change"] += 1
            if "delete" in action:
                summary["destroy"] += 1

        return summary

    def get_resources(self, plan: dict) -> list:
        """Retorna lista de recursos con tipo, nombre y acciones."""
        result = []
        for rc in plan.get("resource_changes", []):
            result.append({
                "type": rc.get("type"),
                "name": rc.get("name"),
                "actions": rc.get("change", {}).get("actions", []),
            })
        return result
