"""Point d'entrée principal de la CLI pyfastcli."""

import click

from pyfastcli.commands import (
    make_domaine,
    make_domaine_ddd,
    make_model,
    make_package,
    make_url,
)


@click.group()
def cli():
    """CLI de génération de code (type make:xxx)."""
    pass


# Enregistrement des commandes modulaires
cli.add_command(make_url)
cli.add_command(make_package)
cli.add_command(make_domaine)
cli.add_command(make_domaine_ddd)
cli.add_command(make_model)
