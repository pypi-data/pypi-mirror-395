"""Commande make:domaine-ddd pour générer des domaines Django DDD."""

from pathlib import Path

import click

from pyfastcli.generators.ddd_domaine_generator import (
    generate_ddd_domaine_structure,
)


@click.command("make:domaine-ddd")
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
    help="Nom du modèle principal (ex: Pratique)",
)
@click.option(
    "--output-dir",
    "-o",
    default=".",
    help="Dossier de sortie où créer l'app",
    prompt="Dossier de sortie",
)
@click.option(
    "--include-serializers/--no-serializers",
    default=True,
    help="Inclure serializers.py pour DRF (recommandé)",
)
@click.option(
    "--description",
    "-d",
    default=None,
    help="Description du domaine",
)
def make_domaine_ddd(
    app_name,
    model_name,
    output_dir,
    include_serializers,
    description,
):
    """
    Génère une structure complète de domaine Django selon les principes DDD
    (Domain-Driven Design) light.

    Crée tous les fichiers recommandés pour un domaine Django organisé en couches :
    - domain/models.py (entités métier, logique métier pure)
    - domain/services.py (règles métier complexes)
    - domain/value_objects.py (objets de valeur immutables)
    - infrastructure/repositories.py (accès DB, querysets personnalisés)
    - presentation/views.py (Django views)
    - presentation/forms.py (formulaires)
    - presentation/serializers.py (DRF serializers, optionnel)
    - presentation/urls.py (routes)
    - presentation/templates/pratique/ (templates HTML)
    - tests/ (test_models.py, test_services.py, test_views.py)

    Exemple d'utilisation:
        pyfastcli make:domaine-ddd --app-name pratique --model-name Pratique
    """
    try:
        # Validation du dossier de sortie
        output_path = Path(output_dir)
        if not output_path.is_absolute():
            output_path = Path.cwd() / output_path

        # Génération automatique du nom de modèle si non fourni
        if model_name is None:
            # Utilise l'app_name comme base et le convertit en PascalCase
            model_name = app_name.replace("_", " ").title().replace(" ", "")

        # Si description n'est pas fournie, on demande interactivement
        if description is None:
            description = click.prompt(
                "Description du domaine (optionnel, Entrée pour ignorer)",
                default="",
                show_default=False,
            )
            if not description.strip():
                description = None

        app_dir = generate_ddd_domaine_structure(
            app_name=app_name,
            model_name=model_name,
            output_dir=str(output_path),
            include_serializers=include_serializers,
            description=description,
        )

        click.echo(
            click.style(f"✅ Domaine DDD créé avec succès dans : {app_dir}", fg="green")
        )
        click.echo("\n📁 Structure créée :")
        click.echo(f"  {app_dir}/")
        click.echo("    ├── __init__.py")
        click.echo("    ├── apps.py")
        click.echo("    ├── admin.py")
        click.echo("    ├── domain/")
        click.echo("    │   ├── models.py")
        click.echo("    │   ├── services.py")
        click.echo("    │   └── value_objects.py")
        click.echo("    ├── infrastructure/")
        click.echo("    │   └── repositories.py")
        click.echo("    ├── presentation/")
        click.echo("    │   ├── views.py")
        click.echo("    │   ├── forms.py")
        if include_serializers:
            click.echo("    │   ├── serializers.py")
        click.echo("    │   └── urls.py")
        click.echo(f"    ├── templates/{app_name}/")
        click.echo("    │   ├── liste.html")
        click.echo("    │   ├── detail.html")
        click.echo("    │   └── formulaire.html")
        click.echo("    └── tests/")
        click.echo("        ├── test_models.py")
        click.echo("        ├── test_services.py")
        click.echo("        └── test_views.py")

        click.echo(click.style("\n💡 Prochaines étapes :", fg="yellow"))
        click.echo(f"  1. Ajoutez '{app_name}' à INSTALLED_APPS dans settings.py")
        click.echo("  2. Incluez les URLs dans votre urls.py principal:")
        click.echo("     from django.urls import include, path")
        click.echo(
            f"     path('{app_name}/', include('{app_name}.presentation.urls')),"
        )
        click.echo(
            f"  3. Exécutez les migrations: python manage.py makemigrations {app_name}"
        )
        click.echo("  4. Appliquez les migrations: python manage.py migrate")
        if include_serializers:
            click.echo(
                "  5. Assurez-vous d'avoir 'rest_framework' dans INSTALLED_APPS "
                "pour les serializers"
            )

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
