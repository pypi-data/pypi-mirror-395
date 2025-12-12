from pathlib import Path

import yaml
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from shared_auth.conf import get_setting

DEFAULT_ACTIONS = [
    ("add", "Adicionar"),
    ("view", "Visualizar"),
    ("change", "Editar"),
    ("delete", "Excluir"),
]


class Command(BaseCommand):
    help = "Generate permissions from permissions.yml"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            default="permissions.yml",
            help="Path to permissions YAML file (default: permissions.yml)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be done without making changes",
        )

    def handle(self, *args, **options):
        from shared_auth.utils import get_permission_model, get_system_model

        system_id = get_setting("SYSTEM_ID", None)
        if not system_id:
            raise CommandError("SYSTEM_ID not configured in settings.")

        System = get_system_model()
        try:
            system = System.objects.using("auth_db").get(id=system_id)
        except System.DoesNotExist:
            raise CommandError(f"System with ID {system_id} not found.")

        self.stdout.write(f"System: {system.name} (ID: {system_id})")

        # Find and parse YAML
        yaml_path = self._find_yaml(options["file"])
        if not yaml_path:
            raise CommandError(f"File not found: {options['file']}")

        with open(yaml_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)

        scopes = data.get("scopes", {})
        if not scopes:
            raise CommandError("No scopes found in YAML file.")

        Permission = get_permission_model()
        dry_run = options["dry_run"]
        created, updated = 0, 0

        for scope_key, scope_data in scopes.items():
            scope_name = scope_data.get("name", scope_key)
            models = scope_data.get("models", [])

            self.stdout.write(f"\n[{scope_key}] {scope_name}")

            for model_config in models:
                model_name = model_config.get("model")
                model_display_name = model_config.get("name", model_name)

                if not model_name:
                    continue

                # Create default CRUD permissions
                for action, action_name in DEFAULT_ACTIONS:
                    codename = f"{action}_{model_name}"
                    name = f"{action_name} {model_display_name}"

                    c, u = self._create_permission(
                        Permission,
                        codename=codename,
                        name=name,
                        scope=scope_key,
                        scope_label=scope_name,
                        model=model_name,
                        model_label=model_display_name,
                        system_id=system_id,
                        dry_run=dry_run,
                    )
                    created += c
                    updated += u

                # Create custom permissions
                custom_permissions = model_config.get("custom_permissions", [])
                for custom_perm in custom_permissions:
                    action = custom_perm.get("action")
                    perm_name = custom_perm.get("name")

                    if not action and not custom_perm.get("codename"):
                        continue

                    codename = custom_perm.get("codename", f"{action}_{model_name}")

                    name = perm_name or f"{action} {model_display_name}"

                    c, u = self._create_permission(
                        Permission,
                        codename=codename,
                        name=name,
                        scope=scope_key,
                        scope_label=scope_name,
                        model=model_name,
                        model_label=model_display_name,
                        system_id=system_id,
                        dry_run=dry_run,
                    )
                    created += c
                    updated += u

        self.stdout.write(f"\nCreated: {created} | Updated: {updated}")

    def _create_permission(
        self,
        Permission,
        codename,
        name,
        scope,
        scope_label,
        model,
        model_label,
        system_id,
        dry_run,
    ) -> tuple[int, int]:
        """Create or update a permission. Returns (created_count, updated_count)."""
        defaults = {
            "name": name,
            "scope": scope,
            "scope_label": scope_label,
            "model": model,
            "model_label": model_label,
        }

        if dry_run:
            exists = (
                Permission.objects.using("auth_db")
                .filter(codename=codename, system_id=system_id)
                .exists()
            )
            status = "exists" if exists else "new"
            self.stdout.write(f"  [{status}] {codename}")
            return (0, 0)

        obj, is_new = Permission.objects.using("auth_db").update_or_create(
            codename=codename,
            system_id=system_id,
            defaults=defaults,
        )

        if is_new:
            self.stdout.write(self.style.SUCCESS(f"  + {codename}"))
            return (1, 0)

        self.stdout.write(f"  ~ {codename}")
        return (0, 1)

    def _find_yaml(self, file_path: str) -> Path | None:
        paths = [
            Path(file_path),
            Path(settings.BASE_DIR) / file_path
            if hasattr(settings, "BASE_DIR")
            else None,
            Path.cwd() / file_path,
        ]
        for p in paths:
            if p and p.exists():
                return p
        return None
