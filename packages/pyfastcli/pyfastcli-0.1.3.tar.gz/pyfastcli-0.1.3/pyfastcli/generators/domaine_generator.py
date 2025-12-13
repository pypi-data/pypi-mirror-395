"""Générateur de structure de domaine Django selon les best practices."""

import re
from pathlib import Path
from typing import Optional


def _sanitize_app_name(name: str) -> str:
    """
    Nettoie et valide un nom d'app Django.

    Args:
        name: Nom de l'app à nettoyer

    Returns:
        Nom d'app valide avec underscores
    """
    # Remplace les tirets et espaces par des underscores
    name = re.sub(r"[- ]+", "_", name.strip())
    # Supprime les caractères non valides
    name = re.sub(r"[^a-zA-Z0-9_]", "", name)
    # S'assure que le nom commence par une lettre ou underscore
    if name and name[0].isdigit():
        name = f"_{name}"
    # S'assure que le nom n'est pas vide
    if not name:
        name = "my_app"
    # Convertit en minuscules
    return name.lower()


def _sanitize_model_name(name: str) -> str:
    """
    Nettoie et valide un nom de modèle Django.

    Args:
        name: Nom du modèle à nettoyer

    Returns:
        Nom de modèle valide en PascalCase
    """
    name = name.strip()
    if not name:
        return "Model"
    # Divise par les séparateurs (underscores, espaces, tirets, et caractères spéciaux)
    # Utilise une regex qui divise sur tout caractère non alphanumérique
    parts = re.split(r"[^a-zA-Z0-9]+", name)
    # Nettoie chaque partie et capitalise
    cleaned_parts = []
    for part in parts:
        if part:
            cleaned_parts.append(part.capitalize())
    # Si aucune partie valide, retourne Model
    if not cleaned_parts:
        return "Model"
    return "".join(cleaned_parts)


def generate_domaine_structure(
    app_name: str,
    model_name: str,
    output_dir: str,
    include_services: bool = True,
    include_selectors: bool = True,
    description: Optional[str] = None,
) -> str:
    """
    Génère une structure complète de domaine Django selon les best practices.

    Args:
        app_name: Nom de l'app Django (ex: pratique)
        model_name: Nom du modèle principal (ex: Pratique)
        output_dir: Dossier de sortie où créer l'app
        include_services: Inclure services.py
        include_selectors: Inclure selectors.py
        description: Description optionnelle du domaine

    Returns:
        Chemin du dossier de l'app créé

    Raises:
        ValueError: Si les paramètres sont invalides
        OSError: Si les fichiers ne peuvent pas être créés
    """
    # Validation et nettoyage
    app_name = _sanitize_app_name(app_name)
    model_name = _sanitize_model_name(model_name)

    if not description:
        description = f"Domaine {app_name}"

    # Création du dossier de sortie
    output_path = Path(output_dir)
    app_dir = output_path / app_name

    if app_dir.exists():
        raise FileExistsError(
            f"Le dossier {app_dir} existe déjà. "
            "Supprimez-le ou choisissez un autre nom d'app."
        )

    try:
        app_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise OSError(f"Impossible de créer le dossier {app_dir}: {e}") from e

    # Génération des fichiers
    _generate_app_init(app_dir, app_name)
    _generate_apps_py(app_dir, app_name)
    _generate_admin_py(app_dir, app_name, model_name)
    _generate_models_py(app_dir, app_name, model_name)
    _generate_views_py(app_dir, app_name, model_name)
    _generate_urls_py(app_dir, app_name, model_name)
    _generate_forms_py(app_dir, app_name, model_name)

    if include_services:
        _generate_services_py(app_dir, app_name, model_name)

    if include_selectors:
        _generate_selectors_py(app_dir, app_name, model_name)

    # Génération des templates
    _generate_templates(app_dir, app_name, model_name)

    return str(app_dir)


def _generate_app_init(app_dir: Path, app_name: str):
    """Génère le fichier __init__.py de l'app."""
    content = f'''"""
Application Django : {app_name}
"""
'''
    (app_dir / "__init__.py").write_text(content, encoding="utf-8")


def _generate_apps_py(app_dir: Path, app_name: str):
    """Génère le fichier apps.py."""
    app_name_capitalized = app_name.capitalize()
    content = f'''from django.apps import AppConfig


class {app_name_capitalized}Config(AppConfig):
    """Configuration de l'application {app_name}."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "{app_name}"
    verbose_name = "{app_name_capitalized}"
'''
    (app_dir / "apps.py").write_text(content, encoding="utf-8")


def _generate_admin_py(app_dir: Path, app_name: str, model_name: str):
    """Génère le fichier admin.py."""
    content = f'''from django.contrib import admin

from {app_name}.models import {model_name}


@admin.register({model_name})
class {model_name}Admin(admin.ModelAdmin):
    """Administration pour le modèle {model_name}."""

    list_display = ["id", "__str__"]
    list_filter = []
    search_fields = []
    readonly_fields = ["id", "created_at", "updated_at"]
'''
    (app_dir / "admin.py").write_text(content, encoding="utf-8")


def _generate_models_py(app_dir: Path, app_name: str, model_name: str):
    """Génère le fichier models.py."""
    session_model_name = f"Session{model_name}"
    content = f'''from django.db import models
from django.utils import timezone


class {model_name}(models.Model):
    """Modèle {model_name}."""

    # Champs de base
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Date de modification"
    )

    # Ajoutez vos champs spécifiques ici
    # nom = models.CharField(max_length=255, verbose_name="Nom")
    # description = models.TextField(blank=True, verbose_name="Description")

    class Meta:
        verbose_name = "{model_name}"
        verbose_name_plural = "{model_name}s"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{model_name} #{{self.id}}"


class {session_model_name}(models.Model):
    """Modèle {session_model_name}."""

    # Relation avec {model_name}
    {app_name.lower()} = models.ForeignKey(
        {model_name},
        on_delete=models.CASCADE,
        related_name="sessions",
        verbose_name="{model_name}",
    )

    # Champs de base
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Date de modification"
    )

    # Ajoutez vos champs spécifiques ici
    # date_debut = models.DateTimeField(verbose_name="Date de début")
    # date_fin = models.DateTimeField(verbose_name="Date de fin", null=True, blank=True)

    class Meta:
        verbose_name = "{session_model_name}"
        verbose_name_plural = "{session_model_name}s"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{session_model_name} #{{self.id}} - {{self.{app_name.lower()}}}"
'''
    (app_dir / "models.py").write_text(content, encoding="utf-8")


def _generate_views_py(app_dir: Path, app_name: str, model_name: str):
    """Génère le fichier views.py."""
    content = f'''from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy

from {app_name}.models import {model_name}
from {app_name}.forms import {model_name}Form


class {model_name}ListView(ListView):
    """Vue pour lister les {model_name}s."""

    model = {model_name}
    template_name = "{app_name}/liste.html"
    context_object_name = "{app_name}_list"
    paginate_by = 20


class {model_name}DetailView(DetailView):
    """Vue pour afficher les détails d'un {model_name}."""

    model = {model_name}
    template_name = "{app_name}/detail.html"
    context_object_name = "{app_name}"


class {model_name}CreateView(CreateView):
    """Vue pour créer un nouveau {model_name}."""

    model = {model_name}
    form_class = {model_name}Form
    template_name = "{app_name}/formulaire.html"
    success_url = reverse_lazy("{app_name}:liste")

    def form_valid(self, form):
        messages.success(self.request, "{model_name} créé avec succès.")
        return super().form_valid(form)


class {model_name}UpdateView(UpdateView):
    """Vue pour modifier un {model_name}."""

    model = {model_name}
    form_class = {model_name}Form
    template_name = "{app_name}/formulaire.html"
    success_url = reverse_lazy("{app_name}:liste")

    def form_valid(self, form):
        messages.success(self.request, "{model_name} modifié avec succès.")
        return super().form_valid(form)


class {model_name}DeleteView(DeleteView):
    """Vue pour supprimer un {model_name}."""

    model = {model_name}
    template_name = "{app_name}/confirmation_suppression.html"
    success_url = reverse_lazy("{app_name}:liste")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "{model_name} supprimé avec succès.")
        return super().delete(request, *args, **kwargs)
'''
    (app_dir / "views.py").write_text(content, encoding="utf-8")


def _generate_urls_py(app_dir: Path, app_name: str, model_name: str):
    """Génère le fichier urls.py."""
    content = f"""from django.urls import path

from {app_name}.views import (
    {model_name}ListView,
    {model_name}DetailView,
    {model_name}CreateView,
    {model_name}UpdateView,
    {model_name}DeleteView,
)

app_name = "{app_name}"

urlpatterns = [
    path("", {model_name}ListView.as_view(), name="liste"),
    path("<int:pk>/", {model_name}DetailView.as_view(), name="detail"),
    path("nouveau/", {model_name}CreateView.as_view(), name="creer"),
    path("<int:pk>/modifier/", {model_name}UpdateView.as_view(), name="modifier"),
    path("<int:pk>/supprimer/", {model_name}DeleteView.as_view(), name="supprimer"),
]
"""
    (app_dir / "urls.py").write_text(content, encoding="utf-8")


def _generate_forms_py(app_dir: Path, app_name: str, model_name: str):
    """Génère le fichier forms.py."""
    content = f'''from django import forms

from {app_name}.models import {model_name}


class {model_name}Form(forms.ModelForm):
    """Formulaire pour le modèle {model_name}."""

    class Meta:
        model = {model_name}
        fields = "__all__"
        # Exclure les champs automatiques si nécessaire
        # exclude = ["created_at", "updated_at"]

        # Personnaliser les widgets si nécessaire
        # widgets = {{
        #     "description": forms.Textarea(attrs={{"rows": 4, "cols": 40}}),
        # }}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajoutez vos personnalisations de formulaire ici
'''
    (app_dir / "forms.py").write_text(content, encoding="utf-8")


def _generate_services_py(app_dir: Path, app_name: str, model_name: str):
    """Génère le fichier services.py."""
    content = f'''"""
Services pour le domaine {app_name}.

Ce module contient la logique métier réutilisable pour {app_name}.
"""

from typing import Optional
from django.db import transaction

from {app_name}.models import {model_name}


def creer_{app_name.lower()}(**kwargs) -> {model_name}:
    """
    Crée un nouveau {model_name}.

    Args:
        **kwargs: Arguments pour créer le {model_name}

    Returns:
        Instance de {model_name} créée
    """
    with transaction.atomic():
        {app_name.lower()} = {model_name}.objects.create(**kwargs)
    return {app_name.lower()}


def modifier_{app_name.lower()}(
    {app_name.lower()}_id: int, **kwargs
) -> Optional[{model_name}]:
    """
    Modifie un {model_name} existant.

    Args:
        {app_name.lower()}_id: ID du {model_name} à modifier
        **kwargs: Arguments à mettre à jour

    Returns:
        Instance de {model_name} modifiée ou None si non trouvée
    """
    try:
        {app_name.lower()} = {model_name}.objects.get(id={app_name.lower()}_id)
        with transaction.atomic():
            for key, value in kwargs.items():
                setattr({app_name.lower()}, key, value)
            {app_name.lower()}.save()
        return {app_name.lower()}
    except {model_name}.DoesNotExist:
        return None


def supprimer_{app_name.lower()}({app_name.lower()}_id: int) -> bool:
    """
    Supprime un {model_name}.

    Args:
        {app_name.lower()}_id: ID du {model_name} à supprimer

    Returns:
        True si supprimé, False sinon
    """
    try:
        {app_name.lower()} = {model_name}.objects.get(id={app_name.lower()}_id)
        with transaction.atomic():
            {app_name.lower()}.delete()
        return True
    except {model_name}.DoesNotExist:
        return False
'''
    (app_dir / "services.py").write_text(content, encoding="utf-8")


def _generate_selectors_py(app_dir: Path, app_name: str, model_name: str):
    """Génère le fichier selectors.py."""
    content = f'''"""
Selectors pour le domaine {app_name}.

Ce module contient les requêtes complexes sur les modèles {app_name}.
"""

from typing import Optional, List
from django.db.models import QuerySet

from {app_name}.models import {model_name}


def obtenir_{app_name.lower()}_par_id(
    {app_name.lower()}_id: int
) -> Optional[{model_name}]:
    """
    Obtient un {model_name} par son ID.

    Args:
        {app_name.lower()}_id: ID du {model_name}

    Returns:
        Instance de {model_name} ou None si non trouvé
    """
    try:
        return {model_name}.objects.get(id={app_name.lower()}_id)
    except {model_name}.DoesNotExist:
        return None


def lister_{app_name.lower()}s() -> QuerySet[{model_name}]:
    """
    Liste tous les {model_name}s.

    Returns:
        QuerySet de {model_name}s
    """
    return {model_name}.objects.all()


def filtrer_{app_name.lower()}s(**filtres) -> QuerySet[{model_name}]:
    """
    Filtre les {model_name}s selon les critères donnés.

    Args:
        **filtres: Critères de filtrage

    Returns:
        QuerySet filtré de {model_name}s
    """
    return {model_name}.objects.filter(**filtres)
'''
    (app_dir / "selectors.py").write_text(content, encoding="utf-8")


def _generate_templates(app_dir: Path, app_name: str, model_name: str):
    """Génère les templates HTML."""
    templates_dir = app_dir / "templates" / app_name
    templates_dir.mkdir(parents=True, exist_ok=True)

    # Template liste.html
    liste_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Liste des {model_name}s</title>
</head>
<body>
    <h1>Liste des {model_name}s</h1>

    <a href="{{% url '{app_name}:creer' %}}">Créer un nouveau {model_name}</a>

    <ul>
        {{% for {app_name} in {app_name}_list %}}
        <li>
            <a href="{{% url '{app_name}:detail' {app_name}.pk %}}">
                {{{{ {app_name} }}}}
            </a>
            <a href="{{% url '{app_name}:modifier' {app_name}.pk %}}">Modifier</a>
            <a href="{{% url '{app_name}:supprimer' {app_name}.pk %}}">Supprimer</a>
        </li>
        {{% empty %}}
        <li>Aucun {model_name} trouvé.</li>
        {{% endfor %}}
    </ul>

    {{% if is_paginated %}}
    <div class="pagination">
        {{% if page_obj.has_previous %}}
        <a href="?page={{{{ page_obj.previous_page_number }}}}">Précédent</a>
        {{% endif %}}
        <span>
            Page {{{{ page_obj.number }}}} sur {{{{ page_obj.paginator.num_pages }}}}
        </span>
        {{% if page_obj.has_next %}}
        <a href="?page={{{{ page_obj.next_page_number }}}}">Suivant</a>
        {{% endif %}}
    </div>
    {{% endif %}}
</body>
</html>
"""
    (templates_dir / "liste.html").write_text(liste_content, encoding="utf-8")

    # Template detail.html
    detail_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Détails de {{{{ {app_name} }}}}</title>
</head>
<body>
    <h1>Détails du {model_name}</h1>

    <dl>
        <dt>ID</dt>
        <dd>{{{{ {app_name}.id }}}}</dd>
        <dt>Créé le</dt>
        <dd>{{{{ {app_name}.created_at }}}}</dd>
        <dt>Modifié le</dt>
        <dd>{{{{ {app_name}.updated_at }}}}</dd>
    </dl>

    <a href="{{% url '{app_name}:liste' %}}">Retour à la liste</a>
    <a href="{{% url '{app_name}:modifier' {app_name}.pk %}}">Modifier</a>
    <a href="{{% url '{app_name}:supprimer' {app_name}.pk %}}">Supprimer</a>
</body>
</html>
"""
    (templates_dir / "detail.html").write_text(detail_content, encoding="utf-8")

    # Template formulaire.html
    formulaire_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>
        {{% if object %}}Modifier{{% else %}}Créer{{% endif %}} un {model_name}
    </title>
</head>
<body>
    <h1>{{% if object %}}Modifier{{% else %}}Créer{{% endif %}} un {model_name}</h1>

    <form method="post">
        {{% csrf_token %}}
        {{{{ form.as_p }}}}
        <button type="submit">Enregistrer</button>
    </form>

    <a href="{{% url '{app_name}:liste' %}}">Annuler</a>
</body>
</html>
"""
    (templates_dir / "formulaire.html").write_text(formulaire_content, encoding="utf-8")
