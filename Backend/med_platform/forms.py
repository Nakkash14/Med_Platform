# med_platform/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'input100', 'placeholder': 'Email'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input100', 'placeholder': 'Username'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input100', 'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input100', 'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'firstname', 'lastname', 'age', 'dob', 'gender', 'email',
            'address', 'city', 'profile_photo', 'occupation', 'licence', 'speciality', 'terms_accepted'
        ]
        labels = {
            'firstname': 'Prénom',
            'lastname': 'Nom',
            'age': 'Âge',
            'dob': 'Date de naissance',
            'gender': 'Genre',
            'email': 'Email',
            'address': 'Adresse',
            'city': 'Ville',
            'profile_photo': 'Photo de Profil (facultatif)',
            'occupation': 'Êtes-vous patient ou docteur ?',
            'licence': 'Télécharger la licence (obligatoire si docteur)',
            'speciality': 'Spécialité médicale (obligatoire si docteur)',
            'terms_accepted': "J'accepte les conditions, termes et politiques",
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # Cache le champ de spécialité par défaut, il sera affiché avec JavaScript si "Docteur" est sélectionné
        self.fields['speciality'].widget = forms.TextInput(attrs={'placeholder': 'Sélectionnez votre spécialité'})
        self.fields['speciality'].required = False  # Spécialité non requise par défaut
