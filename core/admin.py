from django.contrib import admin
from django.utils.html import format_html
from .models import ContactMessage, Project, TeamMember, Service


# ─────────────────────────────────────────────
#  ADMIN : MESSAGES DE CONTACT
# ─────────────────────────────────────────────
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):

    # Colonnes affichees dans la liste
    list_display  = ('nom', 'email', 'service_badge', 'budget', 'statut_badge', 'date_envoi')
    list_filter   = ('statut', 'service', 'budget')
    search_fields = ('nom', 'email', 'message')
    readonly_fields = ('nom', 'email', 'service', 'budget', 'message', 'date_envoi')

    # Champs modifiables (pour le suivi interne)
    fields = ('nom', 'email', 'service', 'budget', 'message', 'date_envoi', 'statut', 'note_interne')

    # Nombre de messages par page
    list_per_page = 25

    def statut_badge(self, obj):
        couleurs = {
            'nouveau':   '#7cffcb',
            'en_cours':  '#fbbf24',
            'repondu':   '#6b8fff',
            'archive':   '#555566',
        }
        couleur = couleurs.get(obj.statut, '#888')
        return format_html(
            '<span style="background:{};color:#000;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:700">{}</span>',
            couleur,
            obj.get_statut_display()
        )
    statut_badge.short_description = "Statut"

    def service_badge(self, obj):
        return obj.get_service_display()
    service_badge.short_description = "Service"


# ─────────────────────────────────────────────
#  ADMIN : PROJETS PORTFOLIO
# ─────────────────────────────────────────────
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    list_display  = ('titre', 'client', 'categorie', 'fictif_badge', 'en_avant_badge', 'ordre', 'date_realisation')
    list_filter   = ('categorie', 'est_fictif', 'est_en_avant')
    search_fields = ('titre', 'client', 'description', 'technologies')
    list_editable = ('ordre',)

    fieldsets = (
        ('Informations principales', {
            'fields': ('titre', 'client', 'categorie', 'description', 'detail')
        }),
        ('Visuels et liens', {
            'fields': ('image_url', 'url_live', 'url_github')
        }),
        ('Technologies', {
            'fields': ('technologies',),
            'description': 'Separez les technos par des virgules. Ex: Django, PostgreSQL, React'
        }),
        ('Parametres d affichage', {
            'fields': ('est_en_avant', 'est_fictif', 'ordre', 'date_realisation')
        }),
    )

    def fictif_badge(self, obj):
        if obj.est_fictif:
            return format_html('<span style="color:#fbbf24;font-size:11px">FICTIF</span>')
        return format_html('<span style="color:#7cffcb;font-size:11px">REEL</span>')
    fictif_badge.short_description = "Type"

    def en_avant_badge(self, obj):
        if obj.est_en_avant:
            return format_html('<span style="color:#7cffcb">⭐</span>')
        return ''
    en_avant_badge.short_description = "A la une"


# ─────────────────────────────────────────────
#  ADMIN : MEMBRES DE L'EQUIPE
# ─────────────────────────────────────────────
@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):

    list_display  = ('prenom', 'role_display', 'email', 'active_badge', 'ordre')
    list_filter   = ('role', 'est_active')
    search_fields = ('prenom', 'nom_de_famille', 'email', 'competences')
    list_editable = ('ordre',)

    fieldsets = (
        ('Identite', {
            'fields': ('prenom', 'nom_de_famille', 'initiale', 'role', 'bio')
        }),
        ('Contact et reseaux', {
            'fields': ('email', 'linkedin_url', 'github_url')
        }),
        ('Profil', {
            'fields': ('photo_url', 'competences'),
            'description': 'Separez les competences par des virgules. Ex: Django, React, PostgreSQL'
        }),
        ('Affichage', {
            'fields': ('ordre', 'est_active')
        }),
    )

    def role_display(self, obj):
        return obj.get_role_display()
    role_display.short_description = "Role"

    def active_badge(self, obj):
        if obj.est_active:
            return format_html('<span style="color:#7cffcb">Active</span>')
        return format_html('<span style="color:#ff6b6b">Inactive</span>')
    active_badge.short_description = "Statut"


# ─────────────────────────────────────────────
#  ADMIN : SERVICES & TARIFS
# ─────────────────────────────────────────────
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):

    list_display  = ('emoji', 'titre', 'tarif_display', 'actif_badge', 'ordre')
    list_filter   = ('est_actif',)
    search_fields = ('titre', 'description', 'technologies')
    list_editable = ('ordre',)

    fieldsets = (
        ('Service', {
            'fields': ('emoji', 'titre', 'description')
        }),
        ('Tarifs', {
            'fields': ('prix_min', 'prix_max', 'prix_label'),
            'description': 'Si "Label tarif perso" est rempli, il remplace les champs prix min/max.'
        }),
        ('Technologies', {
            'fields': ('technologies',),
            'description': 'Separez les technos par des virgules. Ex: Django, React, Stripe'
        }),
        ('Affichage', {
            'fields': ('ordre', 'est_actif')
        }),
    )

    def tarif_display(self, obj):
        return obj.get_prix_display()
    tarif_display.short_description = "Tarif"

    def actif_badge(self, obj):
        if obj.est_actif:
            return format_html('<span style="color:#7cffcb">Affiche</span>')
        return format_html('<span style="color:#555566">Cache</span>')
    actif_badge.short_description = "Statut"


# Personnalisation du titre de l'admin
admin.site.site_header  = "DevSisters — Administration"
admin.site.site_title   = "DevSisters Admin"
admin.site.index_title  = "Tableau de bord"

# Register your models here.
