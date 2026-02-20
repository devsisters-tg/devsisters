from django.db import models
from django.utils import timezone


class ContactMessage(models.Model):

    class StatutChoices(models.TextChoices):
        NOUVEAU   = 'nouveau',   'Nouveau'
        EN_COURS  = 'en_cours',  'En cours de traitement'
        REPONDU   = 'repondu',   'Repondu'
        ARCHIVE   = 'archive',   'Archive'

    class ServiceChoices(models.TextChoices):
        SITE_VITRINE    = 'site_vitrine',       'Site vitrine'
        SITE_ECOMMERCE  = 'site_ecommerce',     'Site e-commerce'
        APPLICATION_WEB = 'application_web',    'Application web'
        APP_MOBILE      = 'application_mobile', 'Application mobile'
        API_BACKEND     = 'api_backend',        'API / Backend'
        AUTRE           = 'autre',              'Autre'

    class BudgetChoices(models.TextChoices):
        MOINS_150K  = 'moins_150k', 'Moins de 150 000 FCFA'
        ENTRE_150K  = '150k_300k',  '150 000 - 300 000 FCFA'
        ENTRE_300K  = '300k_600k',  '300 000 - 600 000 FCFA'
        ENTRE_600K  = '600k_1m',    '600 000 - 1 000 000 FCFA'
        PLUS_1M     = 'plus_1m',    'Plus de 1 000 000 FCFA'
        A_DISCUTER  = 'a_discuter', 'A discuter'

    nom          = models.CharField(max_length=150, verbose_name="Nom / Entreprise")
    email        = models.EmailField(verbose_name="Email")
    service      = models.CharField(max_length=50, choices=ServiceChoices.choices, verbose_name="Service demande")
    budget       = models.CharField(max_length=20, choices=BudgetChoices.choices, verbose_name="Budget")
    message      = models.TextField(verbose_name="Message / Description du projet")
    statut       = models.CharField(max_length=20, choices=StatutChoices.choices, default=StatutChoices.NOUVEAU, verbose_name="Statut")
    note_interne = models.TextField(blank=True, verbose_name="Note interne (visible seulement dans l'admin)")
    date_envoi   = models.DateTimeField(default=timezone.now, verbose_name="Recu le")

    class Meta:
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
        ordering = ['-date_envoi']

    def __str__(self):
        return f"{self.nom} - {self.get_service_display()} ({self.date_envoi.strftime('%d/%m/%Y')})"


class Project(models.Model):

    class CategorieChoices(models.TextChoices):
        SITE_WEB    = 'site_web',   'Site Web'
        ECOMMERCE   = 'ecommerce',  'E-commerce'
        APP_WEB     = 'app_web',    'Application Web'
        APP_MOBILE  = 'app_mobile', 'Application Mobile'
        API         = 'api',        'API / Backend'
        DESIGN      = 'design',     'UI/UX Design'

    titre            = models.CharField(max_length=200, verbose_name="Titre du projet")
    client           = models.CharField(max_length=200, verbose_name="Client")
    categorie        = models.CharField(max_length=30, choices=CategorieChoices.choices, verbose_name="Categorie")
    description      = models.TextField(verbose_name="Description courte")
    detail           = models.TextField(blank=True, verbose_name="Details complets")
    image_url        = models.URLField(blank=True, verbose_name="URL de l'image")
    url_live         = models.URLField(blank=True, verbose_name="URL du site en ligne")
    url_github       = models.URLField(blank=True, verbose_name="URL GitHub")
    technologies     = models.CharField(max_length=300, blank=True, verbose_name="Technologies (separees par des virgules)")
    est_en_avant     = models.BooleanField(default=False, verbose_name="Mettre en avant sur la page d'accueil")
    est_fictif       = models.BooleanField(default=False, verbose_name="Projet fictif / demonstration")
    ordre            = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")
    date_realisation = models.DateField(null=True, blank=True, verbose_name="Date de realisation")
    created_at       = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Projet portfolio"
        verbose_name_plural = "Projets portfolio"
        ordering = ['ordre', '-created_at']

    def __str__(self):
        tag = " [FICTIF]" if self.est_fictif else ""
        return f"{self.titre} - {self.client}{tag}"

    def get_technologies_list(self):
        if self.technologies:
            return [t.strip() for t in self.technologies.split(',') if t.strip()]
        return []


class TeamMember(models.Model):

    class RoleChoices(models.TextChoices):
        FULLSTACK = 'fullstack', 'Fullstack & Lead Dev'
        FRONTEND  = 'frontend',  'Frontend & UI/UX'
        BACKEND   = 'backend',   'Backend & API'
        MOBILE    = 'mobile',    'Mobile & DevOps'
        AUTRE     = 'autre',     'Autre'

    prenom         = models.CharField(max_length=100, verbose_name="Prenom")
    nom_de_famille = models.CharField(max_length=100, blank=True, verbose_name="Nom de famille (optionnel)")
    role           = models.CharField(max_length=30, choices=RoleChoices.choices, verbose_name="Role principal")
    bio            = models.TextField(verbose_name="Bio courte (1-2 phrases)")
    initiale       = models.CharField(max_length=2, verbose_name="Initiale sur l'avatar (ex: A)")
    email          = models.EmailField(blank=True, verbose_name="Email pro")
    linkedin_url   = models.URLField(blank=True, verbose_name="Profil LinkedIn")
    github_url     = models.URLField(blank=True, verbose_name="Profil GitHub")
    competences    = models.CharField(max_length=300, blank=True, verbose_name="Competences (separees par des virgules)")
    photo_url      = models.URLField(blank=True, verbose_name="URL photo de profil")
    ordre          = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")
    est_active     = models.BooleanField(default=True, verbose_name="Membre active")

    class Meta:
        verbose_name = "Membre de l'equipe"
        verbose_name_plural = "Membres de l'equipe"
        ordering = ['ordre', 'prenom']

    def __str__(self):
        return f"{self.prenom} - {self.get_role_display()}"

    def get_competences_list(self):
        if self.competences:
            return [c.strip() for c in self.competences.split(',') if c.strip()]
        return []


class Service(models.Model):

    titre        = models.CharField(max_length=200, verbose_name="Nom du service")
    emoji        = models.CharField(max_length=5, default='🚀', verbose_name="Emoji")
    description  = models.TextField(verbose_name="Description courte")
    prix_min     = models.PositiveIntegerField(verbose_name="Prix minimum (FCFA)")
    prix_max     = models.PositiveIntegerField(null=True, blank=True, verbose_name="Prix maximum (FCFA) - laisser vide si Sur devis")
    prix_label   = models.CharField(max_length=100, blank=True, verbose_name="Label tarif perso - remplace les prix si rempli")
    technologies = models.CharField(max_length=300, blank=True, verbose_name="Technologies (separees par des virgules)")
    ordre        = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")
    est_actif    = models.BooleanField(default=True, verbose_name="Afficher ce service")

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ['ordre']

    def __str__(self):
        return f"{self.emoji} {self.titre}"

    def get_prix_display(self):
        if self.prix_label:
            return self.prix_label
        if self.prix_max:
            return f"{self.prix_min:,} – {self.prix_max:,} FCFA".replace(',', ' ')
        return f"A partir de {self.prix_min:,} FCFA".replace(',', ' ')

    def get_technologies_list(self):
        if self.technologies:
            return [t.strip() for t in self.technologies.split(',') if t.strip()]
        return []