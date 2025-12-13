"""Générateur de structure de domaine Django selon les principes DDD light."""

from pathlib import Path
from typing import Optional

from pyfastcli.generators.domaine_generator import (
    _sanitize_app_name,
    _sanitize_model_name,
)


def generate_ddd_domaine_structure(
    app_name: str,
    model_name: str,
    output_dir: str,
    include_serializers: bool = True,
    description: Optional[str] = None,
) -> str:
    """
    Génère une structure complète de domaine Django selon les principes DDD light.

    Args:
        app_name: Nom de l'app Django (ex: pratique)
        model_name: Nom du modèle principal (ex: Pratique)
        output_dir: Dossier de sortie où créer l'app
        include_serializers: Inclure serializers.py (pour DRF)
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
        description = f"Domaine {app_name} (DDD)"

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

    # Génération des fichiers selon la structure DDD
    _generate_app_init(app_dir, app_name)
    _generate_apps_py(app_dir, app_name)
    _generate_admin_py(app_dir, app_name, model_name)

    # Domain layer
    _generate_domain_models(app_dir, app_name, model_name)
    _generate_domain_services(app_dir, app_name, model_name)
    _generate_value_objects(app_dir, app_name, model_name)

    # Infrastructure layer
    _generate_repositories(app_dir, app_name, model_name)

    # Presentation layer
    _generate_presentation_views(app_dir, app_name, model_name)
    _generate_presentation_forms(app_dir, app_name, model_name)
    if include_serializers:
        _generate_presentation_serializers(app_dir, app_name, model_name)
    _generate_presentation_urls(app_dir, app_name, model_name)
    _generate_templates(app_dir, app_name, model_name)

    # Tests
    _generate_tests_structure(app_dir, app_name, model_name)

    return str(app_dir)


def _generate_app_init(app_dir: Path, app_name: str):
    """Génère le fichier __init__.py de l'app."""
    content = f'''"""
Application Django : {app_name} (DDD)
"""
'''
    (app_dir / "__init__.py").write_text(content, encoding="utf-8")


def _generate_apps_py(app_dir: Path, app_name: str):
    """Génère le fichier apps.py."""
    app_name_capitalized = app_name.capitalize()
    content = f'''from django.apps import AppConfig


class {app_name_capitalized}Config(AppConfig):
    """Configuration de l'application {app_name} (DDD)."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "{app_name}"
    verbose_name = "{app_name_capitalized} (DDD)"
'''
    (app_dir / "apps.py").write_text(content, encoding="utf-8")


def _generate_admin_py(app_dir: Path, app_name: str, model_name: str):
    """Génère le fichier admin.py."""
    content = f'''from django.contrib import admin

from {app_name}.domain.models import {model_name}


@admin.register({model_name})
class {model_name}Admin(admin.ModelAdmin):
    """Administration pour le modèle {model_name}."""

    list_display = ["id", "__str__"]
    list_filter = []
    search_fields = []
    readonly_fields = ["id", "created_at", "updated_at"]
'''
    (app_dir / "admin.py").write_text(content, encoding="utf-8")


def _generate_domain_models(app_dir: Path, app_name: str, model_name: str):
    """Génère les modèles du domaine (domain/models.py)."""
    domain_dir = app_dir / "domain"
    domain_dir.mkdir(exist_ok=True)
    (domain_dir / "__init__.py").write_text("", encoding="utf-8")

    session_model_name = f"Session{model_name}"
    content = f'''"""
Modèles du domaine {app_name}.

Ce module contient les entités métier et la logique métier pure.
"""

from django.db import models
from django.utils import timezone


class {model_name}(models.Model):
    """
    Entité métier {model_name}.

    Cette classe représente une entité du domaine avec sa logique métier.
    """

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

    # Méthodes métier (logique métier pure)
    def est_valide(self) -> bool:
        """
        Vérifie si l'entité est valide selon les règles métier.

        Returns:
            True si l'entité est valide, False sinon
        """
        # Implémentez vos règles de validation métier ici
        return True

    def peut_etre_modifiee(self) -> bool:
        """
        Vérifie si l'entité peut être modifiée selon les règles métier.

        Returns:
            True si l'entité peut être modifiée, False sinon
        """
        # Implémentez vos règles métier ici
        return True


class {session_model_name}(models.Model):
    """
    Entité métier {session_model_name}.

    Cette classe représente une session liée à {model_name}.
    """

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
    (domain_dir / "models.py").write_text(content, encoding="utf-8")


def _generate_domain_services(app_dir: Path, app_name: str, model_name: str):
    """Génère les services du domaine (domain/services.py)."""
    domain_dir = app_dir / "domain"
    content = f'''"""
Services du domaine {app_name}.

Ce module contient les règles métier complexes et les opérations métier.
"""

from typing import Optional
from django.db import transaction

from {app_name}.domain.models import {model_name}


class {model_name}Service:
    """
    Service métier pour {model_name}.

    Contient la logique métier complexe qui ne peut pas être dans les modèles.
    """

    @staticmethod
    def creer_{app_name.lower()}(**kwargs) -> {model_name}:
        """
        Crée un nouveau {model_name} selon les règles métier.

        Args:
            **kwargs: Arguments pour créer le {model_name}

        Returns:
            Instance de {model_name} créée

        Raises:
            ValueError: Si les règles métier ne sont pas respectées
        """
        # Validation métier avant création
        # if not condition_metier:
        #     raise ValueError("Règle métier non respectée")

        with transaction.atomic():
            {app_name.lower()} = {model_name}.objects.create(**kwargs)
        return {app_name.lower()}

    @staticmethod
    def modifier_{app_name.lower()}(
        {app_name.lower()}_id: int, **kwargs
    ) -> Optional[{model_name}]:
        """
        Modifie un {model_name} existant selon les règles métier.

        Args:
            {app_name.lower()}_id: ID du {model_name} à modifier
            **kwargs: Arguments à mettre à jour

        Returns:
            Instance de {model_name} modifiée ou None si non trouvée

        Raises:
            ValueError: Si les règles métier ne sont pas respectées
        """
        try:
            {app_name.lower()} = {model_name}.objects.get(id={app_name.lower()}_id)

            # Validation métier avant modification
            if not {app_name.lower()}.peut_etre_modifiee():
                raise ValueError(
                    "L'entité ne peut pas être modifiée selon les règles métier"
                )

            with transaction.atomic():
                for key, value in kwargs.items():
                    setattr({app_name.lower()}, key, value)
                {app_name.lower()}.save()
            return {app_name.lower()}
        except {model_name}.DoesNotExist:
            return None

    @staticmethod
    def supprimer_{app_name.lower()}({app_name.lower()}_id: int) -> bool:
        """
        Supprime un {model_name} selon les règles métier.

        Args:
            {app_name.lower()}_id: ID du {model_name} à supprimer

        Returns:
            True si supprimé, False sinon

        Raises:
            ValueError: Si les règles métier ne sont pas respectées
        """
        try:
            {app_name.lower()} = {model_name}.objects.get(id={app_name.lower()}_id)

            # Validation métier avant suppression
            # if not {app_name.lower()}.peut_etre_supprimee():
            #     raise ValueError("L'entité ne peut pas être supprimée")

            with transaction.atomic():
                {app_name.lower()}.delete()
            return True
        except {model_name}.DoesNotExist:
            return False
'''
    (domain_dir / "services.py").write_text(content, encoding="utf-8")


def _generate_value_objects(app_dir: Path, app_name: str, model_name: str):
    """Génère les value objects (domain/value_objects.py)."""
    domain_dir = app_dir / "domain"
    content = f'''"""
Value Objects pour le domaine {app_name}.

Les Value Objects sont des objets immutables qui représentent des concepts métier.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class {model_name}Id:
    """
    Value Object représentant l'identifiant d'un {model_name}.

    Les Value Objects sont immutables et comparables par valeur.
    """
    value: int

    def __post_init__(self):
        """Valide la valeur de l'identifiant."""
        if self.value <= 0:
            raise ValueError("L'identifiant doit être positif")


# Exemple d'autres Value Objects possibles
# @dataclass(frozen=True)
# class NomPratique:
#     """Value Object pour le nom d'une pratique."""
#     value: str
#
#     def __post_init__(self):
#         if not self.value or len(self.value.strip()) == 0:
#             raise ValueError("Le nom ne peut pas être vide")
#         if len(self.value) > 255:
#             raise ValueError("Le nom ne peut pas dépasser 255 caractères")
'''
    (domain_dir / "value_objects.py").write_text(content, encoding="utf-8")


def _generate_repositories(app_dir: Path, app_name: str, model_name: str):
    """Génère les repositories (infrastructure/repositories.py)."""
    infra_dir = app_dir / "infrastructure"
    infra_dir.mkdir(exist_ok=True)
    (infra_dir / "__init__.py").write_text("", encoding="utf-8")

    content = f'''"""
Repositories pour le domaine {app_name}.

Ce module contient l'accès aux données et les querysets personnalisés.
"""

from typing import Optional, List
from django.db.models import QuerySet, Q

from {app_name}.domain.models import {model_name}


class {model_name}Repository:
    """
    Repository pour {model_name}.

    Encapsule l'accès aux données et fournit des méthodes de requête métier.
    """

    @staticmethod
    def obtenir_par_id({app_name.lower()}_id: int) -> Optional[{model_name}]:
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

    @staticmethod
    def lister_tous() -> QuerySet[{model_name}]:
        """
        Liste tous les {model_name}s.

        Returns:
            QuerySet de {model_name}s
        """
        return {model_name}.objects.all()

    @staticmethod
    def filtrer(**filtres) -> QuerySet[{model_name}]:
        """
        Filtre les {model_name}s selon les critères donnés.

        Args:
            **filtres: Critères de filtrage

        Returns:
            QuerySet filtré de {model_name}s
        """
        return {model_name}.objects.filter(**filtres)

    @staticmethod
    def rechercher(terme: str) -> QuerySet[{model_name}]:
        """
        Recherche des {model_name}s selon un terme.

        Args:
            terme: Terme de recherche

        Returns:
            QuerySet de {model_name}s correspondants
        """
        # Exemple de recherche personnalisée
        # return {model_name}.objects.filter(
        #     Q(nom__icontains=terme) | Q(description__icontains=terme)
        # )
        return {model_name}.objects.all()

    @staticmethod
    def creer(**kwargs) -> {model_name}:
        """
        Crée un nouveau {model_name}.

        Args:
            **kwargs: Arguments pour créer le {model_name}

        Returns:
            Instance de {model_name} créée
        """
        return {model_name}.objects.create(**kwargs)

    @staticmethod
    def supprimer({app_name.lower()}_id: int) -> bool:
        """
        Supprime un {model_name}.

        Args:
            {app_name.lower()}_id: ID du {model_name} à supprimer

        Returns:
            True si supprimé, False sinon
        """
        try:
            {app_name.lower()} = {model_name}.objects.get(id={app_name.lower()}_id)
            {app_name.lower()}.delete()
            return True
        except {model_name}.DoesNotExist:
            return False
'''
    (infra_dir / "repositories.py").write_text(content, encoding="utf-8")


def _generate_presentation_views(app_dir: Path, app_name: str, model_name: str):
    """Génère les vues de présentation (presentation/views.py)."""
    presentation_dir = app_dir / "presentation"
    presentation_dir.mkdir(exist_ok=True)
    (presentation_dir / "__init__.py").write_text("", encoding="utf-8")

    content = f'''"""
Vues de présentation pour le domaine {app_name}.

Ce module contient les vues Django (ou DRF viewsets).
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy

from {app_name}.domain.models import {model_name}
from {app_name}.domain.services import {model_name}Service
from {app_name}.infrastructure.repositories import {model_name}Repository
from {app_name}.presentation.forms import {model_name}Form


class {model_name}ListView(ListView):
    """Vue pour lister les {model_name}s."""

    model = {model_name}
    template_name = "{app_name}/liste.html"
    context_object_name = "{app_name}_list"
    paginate_by = 20

    def get_queryset(self):
        """Récupère le queryset via le repository."""
        return {model_name}Repository.lister_tous()


class {model_name}DetailView(DetailView):
    """Vue pour afficher les détails d'un {model_name}."""

    model = {model_name}
    template_name = "{app_name}/detail.html"
    context_object_name = "{app_name}"

    def get_object(self, queryset=None):
        """Récupère l'objet via le repository."""
        return get_object_or_404(
            {model_name}Repository.obtenir_par_id(self.kwargs["pk"])
        )


class {model_name}CreateView(CreateView):
    """Vue pour créer un nouveau {model_name}."""

    model = {model_name}
    form_class = {model_name}Form
    template_name = "{app_name}/formulaire.html"
    success_url = reverse_lazy("{app_name}:liste")

    def form_valid(self, form):
        """Valide le formulaire et crée via le service métier."""
        try:
            {model_name}Service.creer_{app_name.lower()}(**form.cleaned_data)
            messages.success(self.request, "{model_name} créé avec succès.")
            return super().form_valid(form)
        except ValueError as e:
            messages.error(self.request, f"Erreur: {{e}}")
            return self.form_invalid(form)


class {model_name}UpdateView(UpdateView):
    """Vue pour modifier un {model_name}."""

    model = {model_name}
    form_class = {model_name}Form
    template_name = "{app_name}/formulaire.html"
    success_url = reverse_lazy("{app_name}:liste")

    def get_object(self, queryset=None):
        """Récupère l'objet via le repository."""
        return get_object_or_404(
            {model_name}Repository.obtenir_par_id(self.kwargs["pk"])
        )

    def form_valid(self, form):
        """Valide le formulaire et modifie via le service métier."""
        try:
            {model_name}Service.modifier_{app_name.lower()}(
                self.object.id, **form.cleaned_data
            )
            messages.success(self.request, "{model_name} modifié avec succès.")
            return super().form_valid(form)
        except ValueError as e:
            messages.error(self.request, f"Erreur: {{e}}")
            return self.form_invalid(form)


class {model_name}DeleteView(DeleteView):
    """Vue pour supprimer un {model_name}."""

    model = {model_name}
    template_name = "{app_name}/confirmation_suppression.html"
    success_url = reverse_lazy("{app_name}:liste")

    def get_object(self, queryset=None):
        """Récupère l'objet via le repository."""
        return get_object_or_404(
            {model_name}Repository.obtenir_par_id(self.kwargs["pk"])
        )

    def delete(self, request, *args, **kwargs):
        """Supprime via le service métier."""
        try:
            {model_name}Service.supprimer_{app_name.lower()}(self.object.id)
            messages.success(self.request, "{model_name} supprimé avec succès.")
            return super().delete(request, *args, **kwargs)
        except ValueError as e:
            messages.error(self.request, f"Erreur: {{e}}")
            return redirect(self.success_url)
'''
    (presentation_dir / "views.py").write_text(content, encoding="utf-8")


def _generate_presentation_forms(app_dir: Path, app_name: str, model_name: str):
    """Génère les formulaires (presentation/forms.py)."""
    presentation_dir = app_dir / "presentation"
    content = f'''"""
Formulaires pour le domaine {app_name}.
"""

from django import forms

from {app_name}.domain.models import {model_name}


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

    def clean(self):
        """Validation personnalisée du formulaire."""
        cleaned_data = super().clean()
        # Ajoutez vos validations ici
        return cleaned_data
'''
    (presentation_dir / "forms.py").write_text(content, encoding="utf-8")


def _generate_presentation_serializers(app_dir: Path, app_name: str, model_name: str):
    """Génère les serializers DRF (presentation/serializers.py)."""
    presentation_dir = app_dir / "presentation"
    content = f'''"""
Serializers DRF pour le domaine {app_name}.
"""

from rest_framework import serializers

from {app_name}.domain.models import {model_name}


class {model_name}Serializer(serializers.ModelSerializer):
    """Serializer pour {model_name}."""

    class Meta:
        model = {model_name}
        fields = "__all__"
        # fields = ["id", "nom", "description", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, data):
        """Validation personnalisée."""
        # Ajoutez vos validations ici
        return data


class {model_name}ListSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour la liste de {model_name}s."""

    class Meta:
        model = {model_name}
        fields = ["id", "__str__", "created_at"]
        read_only_fields = ["id", "created_at"]
'''
    (presentation_dir / "serializers.py").write_text(content, encoding="utf-8")


def _generate_presentation_urls(app_dir: Path, app_name: str, model_name: str):
    """Génère les URLs (presentation/urls.py)."""
    presentation_dir = app_dir / "presentation"
    content = f'''"""
URLs pour le domaine {app_name}.
"""

from django.urls import path

from {app_name}.presentation.views import (
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
'''
    (presentation_dir / "urls.py").write_text(content, encoding="utf-8")


def _generate_templates(app_dir: Path, app_name: str, model_name: str):
    """Génère les templates HTML."""
    # Django cherche les templates dans templates/ à la racine de l'app
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


def _generate_tests_structure(app_dir: Path, app_name: str, model_name: str):
    """Génère la structure de tests."""
    tests_dir = app_dir / "tests"
    tests_dir.mkdir(exist_ok=True)
    (tests_dir / "__init__.py").write_text("", encoding="utf-8")

    # test_models.py
    models_test_content = f'''"""
Tests pour les modèles du domaine {app_name}.
"""

import pytest
from django.test import TestCase

from {app_name}.domain.models import {model_name}


class {model_name}ModelTest(TestCase):
    """Tests pour le modèle {model_name}."""

    def test_creation(self):
        """Test de création d'un {model_name}."""
        {app_name.lower()} = {model_name}.objects.create()
        self.assertIsNotNone({app_name.lower()}.id)
        self.assertIsNotNone({app_name.lower()}.created_at)

    def test_str(self):
        """Test de la méthode __str__."""
        {app_name.lower()} = {model_name}.objects.create()
        self.assertIn(str({app_name.lower()}.id), str({app_name.lower()}))
'''
    (tests_dir / "test_models.py").write_text(models_test_content, encoding="utf-8")

    # test_services.py
    services_test_content = f'''"""
Tests pour les services du domaine {app_name}.
"""

import pytest
from django.test import TestCase

from {app_name}.domain.models import {model_name}
from {app_name}.domain.services import {model_name}Service


class {model_name}ServiceTest(TestCase):
    """Tests pour le service {model_name}Service."""

    def test_creer_{app_name.lower()}(self):
        """Test de création via le service."""
        {app_name.lower()} = {model_name}Service.creer_{app_name.lower()}()
        self.assertIsNotNone({app_name.lower()})
        self.assertIsNotNone({app_name.lower()}.id)

    def test_modifier_{app_name.lower()}(self):
        """Test de modification via le service."""
        {app_name.lower()} = {model_name}Service.creer_{app_name.lower()}()
        modifie = {model_name}Service.modifier_{app_name.lower()}({app_name.lower()}.id)
        self.assertIsNotNone(modifie)
        self.assertEqual(modifie.id, {app_name.lower()}.id)

    def test_supprimer_{app_name.lower()}(self):
        """Test de suppression via le service."""
        {app_name.lower()} = {model_name}Service.creer_{app_name.lower()}()
        result = {model_name}Service.supprimer_{app_name.lower()}({app_name.lower()}.id)
        self.assertTrue(result)
        self.assertFalse({model_name}.objects.filter(id={app_name.lower()}.id).exists())
'''
    (tests_dir / "test_services.py").write_text(services_test_content, encoding="utf-8")

    # test_views.py
    views_test_content = f'''"""
Tests pour les vues de présentation {app_name}.
"""

import pytest
from django.test import TestCase
from django.urls import reverse

from {app_name}.domain.models import {model_name}


class {model_name}ViewsTest(TestCase):
    """Tests pour les vues {model_name}."""

    def setUp(self):
        """Configuration avant chaque test."""
        self.{app_name.lower()} = {model_name}.objects.create()

    def test_liste_view(self):
        """Test de la vue liste."""
        url = reverse("{app_name}:liste")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view(self):
        """Test de la vue détail."""
        url = reverse("{app_name}:detail", args=[self.{app_name.lower()}.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_creer_view_get(self):
        """Test de la vue création (GET)."""
        url = reverse("{app_name}:creer")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
'''
    (tests_dir / "test_views.py").write_text(views_test_content, encoding="utf-8")
