"""Commande make:package pour générer des packages Python."""

from pathlib import Path

import click

from pyfastcli.generators.package_generator import generate_package_structure


@click.command("make:package")
@click.option(
    "--project-name",
    "-p",
    default=None,
    help="Nom du projet (avec tirets, ex: my-package)",
    prompt="Nom du projet (avec tirets, ex: my-package)",
)
@click.option(
    "--package-name",
    "-n",
    default=None,
    help="Nom du package Python (avec underscores, ex: my_package)",
)
@click.option(
    "--version",
    "-v",
    default="0.1.0",
    help="Version initiale du package",
    prompt="Version initiale (ex: 0.1.0)",
)
@click.option(
    "--description",
    "-d",
    default=None,
    help="Description du package",
    prompt="Description du package",
)
@click.option(
    "--author-name",
    "-a",
    default=None,
    help="Nom de l'auteur",
    prompt="Nom de l'auteur",
)
@click.option(
    "--author-email",
    "-e",
    default=None,
    help="Email de l'auteur",
    prompt="Email de l'auteur",
)
@click.option(
    "--python-version",
    default="3.8",
    help="Version Python minimale requise (ex: 3.8)",
    prompt="Version Python minimale (ex: 3.8)",
)
@click.option(
    "--license",
    "-l",
    "license_type",
    default="MIT",
    type=click.Choice(
        ["MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause"], case_sensitive=False
    ),
    help="Type de licence",
    prompt="Type de licence",
)
@click.option(
    "--output-dir",
    "-o",
    default=".",
    help="Dossier de sortie où créer le package",
    prompt="Dossier de sortie",
)
@click.option(
    "--include-makefile/--no-makefile",
    default=True,
    help="Inclure un Makefile avec des commandes utiles",
)
@click.option(
    "--include-manifest/--no-manifest",
    default=True,
    help="Inclure un fichier MANIFEST.in",
)
@click.option(
    "--include-setup-py/--no-setup-py",
    default=False,
    help="Inclure setup.py (optionnel, pyproject.toml suffit)",
)
@click.option(
    "--dependencies",
    default=None,
    help="Dépendances séparées par des virgules (ex: requests>=2.0.0,click>=8.0.0)",
)
@click.option(
    "--dev-dependencies",
    default=None,
    help=(
        "Dépendances de développement séparées par des virgules "
        "(ex: pytest>=7.0.0,black>=23.0.0)"
    ),
)
@click.option(
    "--github-username",
    default=None,
    help="Nom d'utilisateur GitHub (optionnel)",
)
@click.option(
    "--homepage-url",
    default=None,
    help="URL de la page d'accueil (optionnel)",
)
def make_package(
    project_name,
    package_name,
    version,
    description,
    author_name,
    author_email,
    python_version,
    license_type,
    output_dir,
    include_makefile,
    include_manifest,
    include_setup_py,
    dependencies,
    dev_dependencies,
    github_username,
    homepage_url,
):
    """
    Génère une structure complète de package Python selon les best practices.

    Crée tous les fichiers recommandés pour un package Python moderne :
    - pyproject.toml (configuration complète)
    - README.md (template)
    - LICENSE (selon le type choisi)
    - .gitignore (standard Python)
    - Structure du package avec __init__.py
    - Structure de tests
    - MANIFEST.in (optionnel)
    - Makefile (optionnel)

    Exemple d'utilisation:
        pyfastcli make:package --project-name my-package --package-name my_package
    """
    try:
        # Validation du dossier de sortie
        output_path = Path(output_dir)
        if not output_path.is_absolute():
            output_path = Path.cwd() / output_path

        # Génération automatique du nom de package si non fourni
        if package_name is None:
            # Utilise le project_name comme base
            package_name = project_name.replace("-", "_").lower()

        # Parsing des dépendances si fournies
        deps_list = None
        if dependencies:
            deps_list = [dep.strip() for dep in dependencies.split(",") if dep.strip()]

        dev_deps_list = None
        if dev_dependencies:
            dev_deps_list = [
                dep.strip() for dep in dev_dependencies.split(",") if dep.strip()
            ]

        package_dir = generate_package_structure(
            project_name=project_name,
            package_name=package_name,
            version=version,
            description=description,
            author_name=author_name,
            author_email=author_email,
            python_version=python_version,
            license_type=license_type,
            output_dir=str(output_path),
            include_makefile=include_makefile,
            include_manifest=include_manifest,
            include_setup_py=include_setup_py,
            dependencies=deps_list,
            dev_dependencies=dev_deps_list,
            github_username=github_username,
            homepage_url=homepage_url,
        )

        click.echo(
            click.style(f"✅ Package créé avec succès dans : {package_dir}", fg="green")
        )
        click.echo("\n📁 Structure créée :")
        click.echo(f"  {package_dir}/")
        click.echo("    ├── pyproject.toml")
        click.echo("    ├── README.md")
        click.echo("    ├── LICENSE")
        click.echo("    ├── .gitignore")
        if include_manifest:
            click.echo("    ├── MANIFEST.in")
        if include_makefile:
            click.echo("    ├── Makefile")
        click.echo(f"    ├── {package_name}/")
        click.echo("    │   └── __init__.py")
        click.echo("    └── tests/")
        click.echo("        ├── __init__.py")
        click.echo(f"        └── test_{package_name}.py")

        click.echo(click.style("\n💡 Prochaines étapes :", fg="yellow"))
        click.echo(f"  1. cd {package_dir}")
        click.echo("  2. git init")
        click.echo("  3. git add .")
        click.echo("  4. git commit -m 'Initial commit'")
        click.echo("  5. pip install -e '.[dev]'  # Installer en mode développement")

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
