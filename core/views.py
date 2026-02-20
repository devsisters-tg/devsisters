from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from .models import ContactMessage, Project, TeamMember, Service


def index(request):
    # On charge les donnees depuis la base de donnees
    projets_en_avant = Project.objects.filter(est_en_avant=True).order_by('ordre')[:6]
    membres          = TeamMember.objects.filter(est_active=True)
    services         = Service.objects.filter(est_actif=True)

    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # 1. Sauvegarder le message en base de donnees
            message_obj = ContactMessage.objects.create(
                nom     = data['nom'],
                email   = data['email'],
                service = data['service'],
                budget  = data['budget'],
                message = data['message'],
            )

            # 2. Envoyer l'email de notification
            subject = f"Nouveau projet de {data['nom']} - {message_obj.get_service_display()}"
            body = f"""
Nouveau message depuis le site DevSisters !

Nom / Entreprise : {data['nom']}
Email            : {data['email']}
Service          : {message_obj.get_service_display()}
Budget           : {message_obj.get_budget_display()}

Message :
{data['message']}

---
Repondre depuis l'admin : {settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'localhost'}/admin/core/contactmessage/{message_obj.pk}/change/
            """
            try:
                send_mail(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
            except Exception:
                pass  # Le message est quand meme sauvegarde en base

            return redirect('success')

    context = {
        'form':             form,
        'projets_en_avant': projets_en_avant,
        'membres':          membres,
        'services':         services,
    }
    return render(request, 'core/index.html', context)


def success(request):
    return render(request, 'core/success.html')

# Create your views here.
