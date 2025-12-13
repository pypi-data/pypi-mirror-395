"""Commande make:url pour générer des routes Django Ninja."""

from pathlib import Path

import click

from pyfastcli.generators.ninja_routes import generate_ninja_route_file


@click.command("make:url")
@click.option(
    "--module-name",
    "-m",
    default="api",
    help="Nom du module / app (ex: orders)",
    prompt="Nom du module / app (ex: orders)",
    prompt_required=False,
)
@click.option(
    "--function-name",
    "-f",
    default="hello",
    help="Nom de la fonction (ex: get_orders)",
    prompt="Nom de la fonction (ex: get_orders)",
    prompt_required=False,
)
@click.option(
    "--url-path",
    "-u",
    default="/hello",
    help="Chemin d'URL (ex: /orders)",
    prompt="Chemin d'URL (ex: /orders)",
    prompt_required=False,
)
@click.option(
    "--http-method",
    "-M",
    default="get",
    type=click.Choice(
        ["get", "post", "put", "delete", "patch", "head", "options"],
        case_sensitive=False,
    ),
    help="Méthode HTTP",
    prompt="Méthode HTTP",
    prompt_required=False,
)
@click.option(
    "--tag",
    "-t",
    default="Default",
    help="Tag Ninja (ex: Orders)",
    prompt="Tag Ninja (ex: Orders)",
    prompt_required=False,
)
@click.option(
    "--output-dir",
    "-o",
    default="app/api/routes",
    help="Dossier de sortie (relatif au projet Django)",
    prompt="Dossier de sortie (relatif au projet Django)",
    prompt_required=False,
)
@click.option(
    "--description",
    "-d",
    default=None,
    help="Description de l'endpoint",
)
def make_url(
    module_name, function_name, url_path, http_method, tag, output_dir, description
):
    """
    Génère un fichier .py contenant une route Django Ninja.

    Exemple d'utilisation:
        pyfastcli make:url --function-name get_orders \\
            --url-path /orders --http-method get
    """
    try:
        # Validation du dossier de sortie
        output_path = Path(output_dir)
        if not output_path.is_absolute():
            # Si c'est un chemin relatif, on le convertit en absolu
            # depuis le répertoire courant
            output_path = Path.cwd() / output_path

        # Si description n'est pas fournie, on demande interactivement
        if description is None:
            description = click.prompt(
                "Description de l'endpoint (optionnel, Entrée pour ignorer)",
                default="",
                show_default=False,
            )
            if not description.strip():
                description = None

        file_path = generate_ninja_route_file(
            module_name=module_name,
            function_name=function_name,
            url_path=url_path,
            http_method=http_method,
            tag=tag,
            output_dir=str(output_path),
            description=description,
        )

        click.echo(
            click.style(f"✅ Fichier généré avec succès : {file_path}", fg="green")
        )
        click.echo(
            click.style(
                "💡 N'oublie pas d'inclure ce router dans tes urls Ninja.", fg="yellow"
            )
        )
        click.echo("\nExemple d'utilisation dans votre fichier urls.py:")
        click.echo(
            f"  from {Path(file_path).parent.name}.{Path(file_path).stem} import router"
        )
        click.echo("  api.add_router(router)")

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
