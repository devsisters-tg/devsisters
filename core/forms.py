from django import forms

ATTRS_INPUT = {'class': 'form-field'}
ATTRS_SELECT = {'class': 'form-field'}
ATTRS_TEXTAREA = {'class': 'form-field', 'rows': 5}

class ContactForm(forms.Form):
    nom = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={**ATTRS_INPUT, 'placeholder': 'Votre nom / entreprise'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={**ATTRS_INPUT, 'placeholder': 'votre@email.com'})
    )
    service = forms.ChoiceField(
        choices=[
            ('', '-- Quel service vous intéresse ?'),
            ('site_vitrine', 'Site vitrine'),
            ('site_ecommerce', 'Site e-commerce'),
            ('application_web', 'Application web'),
            ('application_mobile', 'Application mobile'),
            ('api_backend', 'API / Backend'),
            ('autre', 'Autre'),
        ],
        widget=forms.Select(attrs=ATTRS_SELECT)
    )
    budget = forms.ChoiceField(
        choices=[
            ('', '-- Budget approximatif'),
            ('moins_150k', 'Moins de 150 000 FCFA'),
            ('150k_300k', '150 000 – 300 000 FCFA'),
            ('300k_600k', '300 000 – 600 000 FCFA'),
            ('600k_1m', '600 000 – 1 000 000 FCFA'),
            ('plus_1m', 'Plus de 1 000 000 FCFA'),
            ('a_discuter', 'À discuter'),
        ],
        widget=forms.Select(attrs=ATTRS_SELECT)
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={**ATTRS_TEXTAREA, 'placeholder': 'Décrivez votre projet, vos besoins, vos délais...'})
    )