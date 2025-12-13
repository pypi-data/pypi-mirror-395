"""Commande make:model pour générer des modèles Django interactivement."""

from pathlib import Path
from typing import Dict, List, Optional

import click

from pyfastcli.generators.model_generator import (
    DJANGO_FIELD_TYPES,
    discover_existing_models,
    generate_model_file,
)


def _prompt_field_type() -> str:
    """Demande le type de champ à l'utilisateur."""
    field_types = list(DJANGO_FIELD_TYPES.keys())
    click.echo("\nTypes de champs disponibles :")
    for i, field_type in enumerate(field_types, 1):
        click.echo(f"  {i}. {field_type}")

    while True:
        choice = click.prompt(
            "\nChoisissez le type de champ (numéro ou nom)",
            type=str,
        )
        # Essaie de convertir en numéro
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(field_types):
                return field_types[idx]
        except ValueError:
            pass

        # Essaie de trouver par nom
        choice_upper = choice.strip()
        for field_type in field_types:
            if field_type.lower() == choice_upper.lower():
                return field_type

        click.echo(click.style(f"❌ Type invalide : {choice}", fg="red"))


def _prompt_relation_type() -> str:
    """Demande le type de relation."""
    relations = ["ForeignKey", "ManyToManyField", "OneToOneField"]
    click.echo("\nTypes de relations disponibles :")
    for i, rel in enumerate(relations, 1):
        click.echo(f"  {i}. {rel}")

    while True:
        choice = click.prompt(
            "\nChoisissez le type de relation (numéro ou nom)",
            type=str,
        )
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(relations):
                return relations[idx]
        except ValueError:
            pass

        choice_upper = choice.strip()
        for rel in relations:
            if rel.lower() == choice_upper.lower():
                return rel

        click.echo(click.style(f"❌ Type invalide : {choice}", fg="red"))


def _prompt_related_model(existing_models: List[tuple]) -> Optional[str]:
    """Demande le modèle lié à l'utilisateur."""
    if not existing_models:
        click.echo(
            click.style(
                "⚠️  Aucun modèle existant trouvé. "
                "Vous devrez spécifier manuellement.",
                fg="yellow",
            )
        )
        app_name: str = click.prompt("Nom de l'app du modèle lié", type=str)
        model_name: str = click.prompt("Nom du modèle lié", type=str)
        return f"{app_name}.{model_name}"

    click.echo("\nModèles existants disponibles :")
    for i, (app_name, model_name) in enumerate(existing_models, 1):
        click.echo(f"  {i}. {app_name}.{model_name}")

    while True:
        choice = click.prompt(
            "\nChoisissez le modèle lié (numéro ou app.Model)",
            type=str,
        )
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(existing_models):
                app_name, model_name = existing_models[idx]
                return f"{app_name}.{model_name}"
        except ValueError:
            pass

        # Format app.Model
        if "." in choice:
            parts = choice.split(".")
            if len(parts) == 2:
                return str(choice)

        click.echo(click.style(f"❌ Choix invalide : {choice}", fg="red"))
        return None


def _prompt_field_options(field_type: str) -> str:
    """Demande les options supplémentaires pour un champ."""
    options = []
    click.echo("\nOptions disponibles (laissez vide pour terminer) :")

    # Options communes
    if field_type in ["CharField", "TextField", "EmailField", "URLField"]:
        if click.confirm("Ajouter max_length ?", default=False):
            max_length = click.prompt("max_length", default=255, type=int)
            options.append(f"max_length={max_length}")

    if field_type not in ["BooleanField", "ManyToManyField"]:
        if click.confirm("Le champ peut être vide (blank=True) ?", default=False):
            options.append("blank=True")

        if click.confirm("Le champ peut être null (null=True) ?", default=False):
            options.append("null=True")

    if field_type in ["CharField", "TextField", "EmailField"]:
        if click.confirm("Ajouter un verbose_name ?", default=False):
            verbose_name = click.prompt("verbose_name", type=str)
            options.append(f'verbose_name="{verbose_name}"')

    if field_type in ["IntegerField", "DecimalField", "FloatField"]:
        if click.confirm("Ajouter une valeur par défaut ?", default=False):
            default_value = click.prompt("Valeur par défaut", type=str)
            try:
                # Essaie de convertir en nombre
                float(default_value)
                options.append(f"default={default_value}")
            except ValueError:
                options.append(f'default="{default_value}"')

    if field_type == "ForeignKey":
        if click.confirm("Ajouter related_name ?", default=False):
            related_name = click.prompt("related_name", type=str)
            options.append(f'related_name="{related_name}"')

    return ", ".join(options)


@click.command("make:model")
@click.option(
    "--app-name",
    "-a",
    default=None,
    help="Nom de l'app Django (ex: pratique)",
    prompt="Nom de l'app Django (ex: pratique)",
)
@click.option(
    "--model-name",
    "-m",
    default=None,
    help="Nom du modèle (ex: Pratique)",
    prompt="Nom du modèle (ex: Pratique)",
)
@click.option(
    "--output-dir",
    "-o",
    default=".",
    help="Dossier de sortie (chemin du projet Django)",
    prompt="Dossier de sortie (chemin du projet Django)",
)
@click.option(
    "--no-timestamps",
    is_flag=True,
    default=False,
    help="Ne pas ajouter created_at et updated_at",
)
def make_model(app_name: str, model_name: str, output_dir: str, no_timestamps: bool):
    """
    Génère un modèle Django avec des champs définis interactivement.

    Cette commande fonctionne comme make:entity de Symfony :
    - Pose des questions pour chaque champ
    - Propose des types de champs Django
    - Détecte les modèles existants pour les relations
    - Génère le code du modèle

    Exemple d'utilisation:
        pyfastcli make:model --app-name pratique --model-name Pratique
    """
    try:
        output_path = Path(output_dir).resolve()

        # Découvre les modèles existants
        click.echo(click.style("🔍 Recherche des modèles existants...", fg="cyan"))
        existing_models = discover_existing_models(output_path)
        if existing_models:
            click.echo(
                click.style(
                    f"✅ {len(existing_models)} modèle(s) trouvé(s)", fg="green"
                )
            )
        else:
            click.echo(click.style("ℹ️  Aucun modèle existant trouvé", fg="yellow"))

        # Collecte les champs
        fields: List[Dict[str, str]] = []
        click.echo(click.style("\n📝 Définition des champs du modèle", fg="cyan"))

        while True:
            click.echo(f"\n--- Champ {len(fields) + 1} ---")
            field_name = click.prompt("Nom du champ (ou 'fin' pour terminer)", type=str)

            if field_name.lower() in ["fin", "end", "stop", "q", "quit"]:
                break

            if not field_name.strip():
                click.echo(
                    click.style("❌ Le nom du champ ne peut pas être vide", fg="red")
                )
                continue

            # Demande si c'est une relation
            is_relation = click.confirm(
                "Est-ce une relation vers un autre modèle ?", default=False
            )

            if is_relation:
                field_type = _prompt_relation_type()
                related_model = _prompt_related_model(existing_models)
                field_options = _prompt_field_options(field_type)
                field_dict: Dict[str, str] = {
                    "name": field_name,
                    "type": field_type,
                    "options": field_options,
                }
                if related_model:
                    field_dict["related_model"] = related_model
                fields.append(field_dict)
            else:
                field_type = _prompt_field_type()
                field_options = _prompt_field_options(field_type)
                fields.append(
                    {
                        "name": field_name,
                        "type": field_type,
                        "options": field_options,
                    }
                )

        if not fields:
            click.echo(click.style("❌ Aucun champ défini. Abandon.", fg="red"))
            raise click.Abort()

        # Génère le modèle
        click.echo(click.style("\n⚙️  Génération du modèle...", fg="cyan"))
        models_file = generate_model_file(
            app_name=app_name,
            model_name=model_name,
            fields=fields,
            output_dir=str(output_path),
            add_timestamps=not no_timestamps,
        )

        click.echo(
            click.style(f"✅ Modèle généré avec succès : {models_file}", fg="green")
        )
        click.echo(click.style("\n💡 Prochaines étapes :", fg="yellow"))
        click.echo(f"  1. Vérifiez le modèle dans {models_file}")
        click.echo(f"  2. Exécutez: python manage.py makemigrations {app_name}")
        click.echo("  3. Appliquez: python manage.py migrate")

    except ValueError as e:
        click.echo(click.style(f"❌ Erreur de validation : {e}", fg="red"), err=True)
        raise click.Abort()
    except FileExistsError as e:
        click.echo(click.style(f"❌ Erreur : {e}", fg="red"), err=True)
        raise click.Abort()
    except OSError as e:
        click.echo(click.style(f"❌ Erreur d'écriture : {e}", fg="red"), err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(click.style(f"❌ Erreur inattendue : {e}", fg="red"), err=True)
        raise click.Abort()
