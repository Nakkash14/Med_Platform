# med_platform/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from .forms import UserRegistrationForm
from functions.auth.auth_utils import handle_signup, handle_confirm_email, handle_create_profile
from functions.email.email_utils import send_confirmation_email, handle_confirm_page
from functions.views.view_utils import handle_admin_page, handle_doctor_page, handle_patient_page, handle_index_page
from django.contrib import messages
import random
from .models import UserProfile 
from . import views

def signup_page(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = handle_signup(request, form)
            
            # Génère un code de confirmation unique
            confirmation_code = random.randint(1000, 9999)
            
            # Envoie le code dans l'email
            send_confirmation_email(user.email, user.username, user.id, confirmation_code)
            
            # Passe le code dans le contexte pour le rendre accessible en JavaScript
            return render(request, 'Mail/mail_confirm.html', {'confirmation_code': confirmation_code})
    else:
        form = UserRegistrationForm()
    return render(request, 'Formulaires_connection/signup.html', {'form': form})

def confirm_email(request, uid, token):
    return handle_confirm_email(request, uid, token)


def create_profile(request):
    return handle_create_profile(request)

def admin_page(request):
    return handle_admin_page(request)

def doctor_page(request):
    return handle_doctor_page(request)

def patient_page(request):
    return handle_patient_page(request)

def index_page(request):
    return handle_index_page(request)

def succes_page(request) :
    return  render(request, 'create.Profile/succes.html')

@login_required
def mail_confirm_page(request):
    user_id = request.user.id

    if request.method == 'POST':
        # Récupère le code saisi dans le champ unique
        code = request.POST.get("confirmation_code", "")
        
        # Appel de la fonction de confirmation de code
        result = handle_confirm_page(request, user_id)
        
        if result['success']:
            return redirect('create_profile')  # Redirige vers la page de création de profil
        else:
            messages.error(request, result['message'])  # Affiche un message d'erreur si le code est incorrect

    return render(request, 'Mail/mail_confirm.html')

@login_required
def redirect_after_login(request):
    try:
        # Récupère le profil de l'utilisateur connecté
        user_profile = UserProfile.objects.get(user=request.user)

        # Redirection basée sur l'occupation de l'utilisateur
        if user_profile.occupation == 'docteur':
            return redirect('doctor_page')
        elif user_profile.occupation == 'patient':
            return redirect('patient_page')
        else:
            return redirect('index_page')  # Option de redirection par défaut si occupation inconnue
    except UserProfile.DoesNotExist:
        # Si le profil n'existe pas, redirige vers la page d'accueil
        return redirect('index_page')
    
