# functions/auth/auth_utils.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

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

def handle_create_profile(request):
    return render(request, 'create.Profile/create_profile.html')
