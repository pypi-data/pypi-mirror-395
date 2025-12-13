"""Générateur de modèles Django avec champs interactifs."""

import re
from pathlib import Path
from typing import Dict, List, Tuple

from pyfastcli.generators.domaine_generator import (
    _sanitize_app_name,
    _sanitize_model_name,
)

# Types de champs Django disponibles
DJANGO_FIELD_TYPES = {
    "CharField": "models.CharField(max_length=255)",
    "TextField": "models.TextField()",
    "IntegerField": "models.IntegerField()",
    "BigIntegerField": "models.BigIntegerField()",
    "DecimalField": "models.DecimalField(max_digits=10, decimal_places=2)",
    "FloatField": "models.FloatField()",
    "BooleanField": "models.BooleanField(default=False)",
    "DateField": "models.DateField()",
    "DateTimeField": "models.DateTimeField()",
    "TimeField": "models.TimeField()",
    "EmailField": "models.EmailField()",
    "URLField": "models.URLField()",
    "SlugField": "models.SlugField()",
    "UUIDField": (
        "models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)"
    ),
    "ForeignKey": "models.ForeignKey('app.Model', on_delete=models.CASCADE)",
    "ManyToManyField": "models.ManyToManyField('app.Model')",
    "OneToOneField": "models.OneToOneField('app.Model', on_delete=models.CASCADE)",
    "FileField": "models.FileField(upload_to='uploads/')",
    "ImageField": "models.ImageField(upload_to='uploads/')",
    "JSONField": "models.JSONField()",
    "PositiveIntegerField": "models.PositiveIntegerField()",
    "PositiveSmallIntegerField": "models.PositiveSmallIntegerField()",
    "SmallIntegerField": "models.SmallIntegerField()",
    "DurationField": "models.DurationField()",
    "BinaryField": "models.BinaryField()",
    "IPAddressField": "models.GenericIPAddressField()",
}


def discover_existing_models(project_path: Path) -> List[Tuple[str, str]]:
    """
    Découvre les modèles Django existants dans le projet.

    Args:
        project_path: Chemin du projet Django

    Returns:
        Liste de tuples (app_name, model_name) des modèles trouvés
    """
    models_found = []
    project_path = Path(project_path).resolve()

    # Cherche les apps Django dans le projet
    for app_dir in project_path.iterdir():
        if not app_dir.is_dir() or app_dir.name.startswith("."):
            continue

        models_file = app_dir / "models.py"
        if not models_file.exists():
            continue

        try:
            content = models_file.read_text(encoding="utf-8")
            # Recherche les classes de modèles
            pattern = r"class\s+(\w+)\s*\([^)]*models\.Model"
            matches = re.findall(pattern, content)
            for model_name in matches:
                if model_name not in ["Model", "TimeStampedModel", "AbstractBaseUser"]:
                    models_found.append((app_dir.name, model_name))
        except Exception:
            # Ignore les erreurs de lecture
            continue

    return models_found


def generate_model_file(
    app_name: str,
    model_name: str,
    fields: List[Dict[str, str]],
    output_dir: str,
    add_timestamps: bool = True,
) -> str:
    """
    Génère un fichier models.py avec un modèle Django.

    Args:
        app_name: Nom de l'app Django
        model_name: Nom du modèle
        fields: Liste de dictionnaires avec les champs
                Format: [{"name": "nom", "type": "CharField",
                "options": "max_length=100"}]
        output_dir: Dossier de sortie
        add_timestamps: Ajouter created_at et updated_at

    Returns:
        Chemin du fichier models.py créé ou modifié
    """
    app_name = _sanitize_app_name(app_name)
    model_name = _sanitize_model_name(model_name)

    output_path = Path(output_dir)
    models_file = output_path / app_name / "models.py"

    # Si le fichier existe, on l'ajoute au fichier existant
    if models_file.exists():
        content = models_file.read_text(encoding="utf-8")
        # Vérifie si le modèle existe déjà (cherche le pattern exact)
        # On cherche à la fois le nom original et le nom sanitized
        import re

        pattern1 = rf"class\s+{re.escape(model_name)}\s*\("
        # Le nom peut être sanitized différemment, cherchons aussi le nom original
        # avant sanitization
        if re.search(pattern1, content):
            raise ValueError(f"Le modèle {model_name} existe déjà dans {models_file}")
        # Ajoute le nouveau modèle avant la dernière ligne
        model_code = _generate_model_code(model_name, fields, add_timestamps)
        # Ajoute deux lignes vides avant le nouveau modèle
        content = content.rstrip() + "\n\n" + model_code
        models_file.write_text(content, encoding="utf-8")
    else:
        # Crée le fichier models.py complet
        content = _generate_models_file_content(model_name, fields, add_timestamps)
        models_file.parent.mkdir(parents=True, exist_ok=True)
        models_file.write_text(content, encoding="utf-8")

    return str(models_file)


def _generate_model_code(
    model_name: str, fields: List[Dict[str, str]], add_timestamps: bool
) -> str:
    """Génère le code Python pour un modèle Django."""
    imports = set()
    field_lines = []

    # Génère les champs
    for field in fields:
        field_name = field["name"]
        field_type = field["type"]
        field_options = field.get("options", "")
        related_model = field.get("related_model", None)

        # Gère les imports nécessaires
        if field_type == "UUIDField":
            imports.add("import uuid")
        elif field_type in ["ForeignKey", "ManyToManyField", "OneToOneField"]:
            if related_model:
                app_name, model_name_ref = related_model.split(".")
                imports.add(f"from {app_name}.models import {model_name_ref}")

        # Construit la ligne du champ
        if field_type in ["ForeignKey", "ManyToManyField", "OneToOneField"]:
            if not related_model:
                raise ValueError(
                    f"Le champ de relation '{field_name}' (type: {field_type}) "
                    "nécessite un modèle lié (related_model). "
                    "Utilisez le format 'app.Model'."
                )
            app_name_ref, model_name_ref = related_model.split(".")
            field_line = f"    {field_name} = models.{field_type}("
            field_line += f"{model_name_ref}"
            if field_type == "ForeignKey":
                field_line += ", on_delete=models.CASCADE"
            elif field_type == "OneToOneField":
                field_line += ", on_delete=models.CASCADE"
            # ManyToManyField n'a pas besoin de on_delete
            if field_options:
                field_line += f", {field_options}"
            field_line += ")"
        else:
            field_def = DJANGO_FIELD_TYPES.get(field_type, f"models.{field_type}()")
            # Remplace les options par défaut si fournies
            if field_options:
                # Extrait le type de base
                base_type = field_type
                field_line = f"    {field_name} = models.{base_type}({field_options})"
            else:
                field_line = f"    {field_name} = {field_def}"

        field_lines.append(field_line)

    # Ajoute les timestamps si demandé
    if add_timestamps:
        field_lines.insert(
            0,
            "    id = models.AutoField(primary_key=True)",
        )
        field_lines.append(
            "    created_at = models.DateTimeField("
            'auto_now_add=True, verbose_name="Date de création"'
            ")"
        )
        field_lines.append(
            "    updated_at = models.DateTimeField("
            'auto_now=True, verbose_name="Date de modification"'
            ")"
        )

    # Génère le code complet
    imports_code = "\n".join(sorted(imports)) if imports else ""
    if imports_code and "from django.db import models" not in imports_code:
        imports_code = "from django.db import models\n" + imports_code

    # Détermine l'ordering
    ordering_value = '["-created_at"]' if add_timestamps else '["id"]'

    model_code = f'''class {model_name}(models.Model):
    """Modèle {model_name}."""

{chr(10).join(field_lines)}

    class Meta:
        verbose_name = "{model_name}"
        verbose_name_plural = "{model_name}s"
        ordering = {ordering_value}

    def __str__(self):
        return f"{model_name} #{{self.id}}"
'''

    if imports_code:
        return imports_code + "\n\n" + model_code
    return "from django.db import models\n\n" + model_code


def _generate_models_file_content(
    model_name: str, fields: List[Dict[str, str]], add_timestamps: bool
) -> str:
    """Génère le contenu complet d'un fichier models.py."""
    model_code = _generate_model_code(model_name, fields, add_timestamps)
    return model_code
