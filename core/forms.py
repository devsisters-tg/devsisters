from django import forms


class ContactForm(forms.Form):
    nom = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Votre nom / entreprise',
            'class': 'form-input'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'votre@email.com',
            'class': 'form-input'
        })
    )
    service = forms.ChoiceField(
        choices=[
            ('',                   '-- Quel service vous intéresse ?'),
            ('site_vitrine',       'Site vitrine'),
            ('site_ecommerce',     'Site e-commerce'),
            ('application_web',    'Application web'),
            ('application_mobile', 'Application mobile'),
            ('api_backend',        'API / Backend'),
            ('autre',              'Autre'),
        ],
        widget=forms.Select(attrs={'class': 'form-input'})
    )
    budget = forms.ChoiceField(
        choices=[
            ('',               '-- Budget approximatif'),
            ('moins_150k',     'Moins de 150 000 FCFA'),
            ('150k_300k',      '150 000 – 300 000 FCFA'),
            ('300k_600k',      '300 000 – 600 000 FCFA'),
            ('600k_1m',        '600 000 – 1 000 000 FCFA'),
            ('plus_1m',        'Plus de 1 000 000 FCFA'),
            ('a_discuter',     'À discuter'),
        ],
        widget=forms.Select(attrs={'class': 'form-input'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Décrivez votre projet, vos besoins, vos délais...',
            'class': 'form-input',
            'rows': 5
        })
    )