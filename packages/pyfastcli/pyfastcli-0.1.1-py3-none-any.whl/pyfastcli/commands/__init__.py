"""Commandes CLI modulaires pour pyfastcli."""

from pyfastcli.commands.domaine_command import make_domaine
from pyfastcli.commands.domaine_ddd_command import make_domaine_ddd
from pyfastcli.commands.model_command import make_model
from pyfastcli.commands.package_command import make_package
from pyfastcli.commands.url_command import make_url

__all__ = [
    "make_url",
    "make_package",
    "make_domaine",
    "make_domaine_ddd",
    "make_model",
]
