# functions/auth/auth_utils.py
import requests
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, login
from django.contrib import messages

def handle_signup(request, form):
    user = form.save(commit=False)
    user.is_active = False  # Désactiver l'utilisateur jusqu'à la confirmation
    user.save()
    return user  # Retourner l'utilisateur pour l'utiliser dans le processus d'envoi d'email

def handle_confirm_email(request, uid, token):
    try:
        uid = urlsafe_base64_decode(uid).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True  # Activer le compte
        user.save()
        login(request, user)
        return redirect('create_profile')
    else:
        return render(request, 'med_platform/invalid_link.html')  # Page d'erreur en cas de lien invalide

from med_platform.forms import UserProfileForm  # Assurez-vous que UserProfileForm est bien importé


from med_platform.forms import UserProfileForm

def handle_create_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        
        # Vérification pour s'assurer que le champ licence est rempli si l'utilisateur est docteur
        if request.POST.get('occupation') == 'docteur' and not request.FILES.get('licence'):
            form.add_error('licence', "La licence est obligatoire pour les docteurs.")
        
        if form.is_valid():
            form.save()
            return redirect('succes_page')  
    else:
        form = UserProfileForm()

    return render(request, 'create.Profile/create_profile.html', {'form': form})

def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('redirect_after_login')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
            return redirect('index_page')  # Recharge le formulaire avec un message d'erreur

    return redirect('index_page') 