"""Commande make:domaine pour générer des domaines Django."""

from pathlib import Path

import click

from pyfastcli.generators.domaine_generator import generate_domaine_structure


@click.command("make:domaine")
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
    "--include-services/--no-services",
    default=True,
    help="Inclure services.py (recommandé)",
)
@click.option(
    "--include-selectors/--no-selectors",
    default=True,
    help="Inclure selectors.py (recommandé)",
)
@click.option(
    "--description",
    "-d",
    default=None,
    help="Description du domaine",
)
def make_domaine(
    app_name,
    model_name,
    output_dir,
    include_services,
    include_selectors,
    description,
):
    """
    Génère une structure complète de domaine Django selon les best practices.

    Crée tous les fichiers recommandés pour un domaine Django :
    - models.py (modèles Pratique, SessionPratique, etc.)
    - views.py (vues liées à la pratique)
    - urls.py (routes de cette app)
    - forms.py (formulaires liés à la pratique)
    - services.py (logique métier réutilisable, optionnel)
    - selectors.py (requêtes complexes sur les modèles, optionnel)
    - templates/pratique/ (liste.html, detail.html, formulaire.html)

    Exemple d'utilisation:
        pyfastcli make:domaine --app-name pratique --model-name Pratique
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

        app_dir = generate_domaine_structure(
            app_name=app_name,
            model_name=model_name,
            output_dir=str(output_path),
            include_services=include_services,
            include_selectors=include_selectors,
            description=description,
        )

        click.echo(
            click.style(f"✅ Domaine créé avec succès dans : {app_dir}", fg="green")
        )
        click.echo("\n📁 Structure créée :")
        click.echo(f"  {app_dir}/")
        click.echo("    ├── __init__.py")
        click.echo("    ├── apps.py")
        click.echo("    ├── admin.py")
        click.echo("    ├── models.py")
        click.echo("    ├── views.py")
        click.echo("    ├── urls.py")
        click.echo("    ├── forms.py")
        if include_services:
            click.echo("    ├── services.py")
        if include_selectors:
            click.echo("    ├── selectors.py")
        click.echo("    └── templates/")
        click.echo(f"        └── {app_name}/")
        click.echo("            ├── liste.html")
        click.echo("            ├── detail.html")
        click.echo("            └── formulaire.html")

        click.echo(click.style("\n💡 Prochaines étapes :", fg="yellow"))
        click.echo(f"  1. Ajoutez '{app_name}' à INSTALLED_APPS dans settings.py")
        click.echo("  2. Incluez les URLs dans votre urls.py principal:")
        click.echo("     from django.urls import include, path")
        click.echo(f"     path('{app_name}/', include('{app_name}.urls')),")
        click.echo(
            f"  3. Exécutez les migrations: python manage.py makemigrations {app_name}"
        )
        click.echo("  4. Appliquez les migrations: python manage.py migrate")

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
