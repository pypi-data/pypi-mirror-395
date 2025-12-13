import re
from pathlib import Path
from typing import Optional


def _sanitize_func_name(name: str) -> str:
    """Nettoie et valide un nom de fonction Python."""
    # Supprime les caractères non valides et remplace par underscore
    name = name.strip()
    # Remplace les caractères non alphanumériques (sauf underscore) par underscore
    name = re.sub(r"[^a-zA-Z0-9_]", "_", name)
    # S'assure que le nom commence par une lettre ou underscore
    if name and name[0].isdigit():
        name = f"_{name}"
    # S'assure que le nom n'est pas vide
    if not name:
        name = "endpoint"
    return name


def _validate_http_method(method: str) -> str:
    """Valide et normalise la méthode HTTP."""
    method = method.lower().strip()
    valid_methods = {"get", "post", "put", "delete", "patch", "head", "options"}
    if method not in valid_methods:
        raise ValueError(
            f"Méthode HTTP invalide: {method}. "
            f"Méthodes valides: {', '.join(sorted(valid_methods))}"
        )
    return method


def _validate_url_path(path: str) -> str:
    """Valide et normalise le chemin d'URL."""
    path = path.strip()
    # S'assure que le chemin commence par /
    if not path.startswith("/"):
        path = f"/{path}"
    return path


def _escape_string(s: str) -> str:
    """Échappe les guillemets dans une chaîne pour le template."""
    return s.replace('"', '\\"').replace("'", "\\'")


def generate_ninja_route_file(
    module_name: str,
    function_name: str,
    url_path: str,
    http_method: str,
    tag: str,
    output_dir: str,
    description: Optional[str] = None,
) -> str:
    """
    Génère un fichier Python contenant une route Django Ninja.

    Args:
        module_name: Nom du module/app (non utilisé actuellement mais
            conservé pour compatibilité)
        function_name: Nom de la fonction à générer
        url_path: Chemin d'URL (ex: /orders)
        http_method: Méthode HTTP (get, post, put, delete, etc.)
        tag: Tag Ninja pour la documentation
        output_dir: Dossier de sortie
        description: Description optionnelle de l'endpoint

    Returns:
        Chemin du fichier généré

    Raises:
        ValueError: Si les paramètres sont invalides
        OSError: Si le fichier ne peut pas être écrit
    """
    # Validation et nettoyage des entrées
    func_name = _sanitize_func_name(function_name)
    http_method = _validate_http_method(http_method)
    url_path = _validate_url_path(url_path)
    tag = tag.strip() or "Default"

    if description:
        description = description.strip()
    else:
        description = f"Endpoint {func_name}"

    # Nom du fichier = fonction, par exemple get_orders.py
    file_name = f"{func_name}.py"
    out_dir = Path(output_dir)

    # Création du dossier si nécessaire
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise OSError(f"Impossible de créer le dossier {output_dir}: {e}") from e

    file_path = out_dir / file_name

    # Vérification si le fichier existe déjà
    if file_path.exists():
        raise FileExistsError(
            f"Le fichier {file_path} existe déjà. "
            "Supprimez-le ou choisissez un autre nom de fonction."
        )

    # Mapping des méthodes HTTP vers les décorateurs Django Ninja
    method_decorator_map = {
        "get": "router.get",
        "post": "router.post",
        "put": "router.put",
        "delete": "router.delete",
        "patch": "router.patch",
        "head": "router.head",
        "options": "router.options",
    }

    decorator = method_decorator_map[http_method]
    escaped_url = _escape_string(url_path)
    escaped_tag = _escape_string(tag)
    escaped_description = _escape_string(description)

    # Template de route Django Ninja amélioré
    template = f'''from ninja import Router

router = Router(tags=["{escaped_tag}"])


@{decorator}("{escaped_url}")
def {func_name}(request):
    """
    {escaped_description}
    """
    return {{"message": "Hello from {func_name}!"}}
'''

    # Écriture du fichier
    try:
        file_path.write_text(template, encoding="utf-8")
    except OSError as e:
        raise OSError(f"Impossible d'écrire le fichier {file_path}: {e}") from e

    return str(file_path)
