from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.http import HttpResponse
import random
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserProfileForm


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Vérifiez si un UserProfile existe pour cet utilisateur
            try:
                profile = user.userprofile
                if profile.occupation == 'patient':
                    return redirect('patient_dashboard')
                elif profile.occupation == 'docteur':
                    return redirect('docteur_dashboard')
                else:
                    messages.warning(request, "Occupation non spécifiée.")
                    return redirect('profile_setup')  # Redirection pour compléter le profil si nécessaire
            except UserProfile.DoesNotExist:
                messages.error(request, "Profil utilisateur introuvable. Veuillez contacter l'administrateur.")
                return redirect('login')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
            return redirect('login')
    
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            
            # Créer un profil vide lié à l'utilisateur
            UserProfile.objects.create(user=user)
            
            request.session['username'] = username
            request.session['verification_code'] = str(random.randint(1000, 9999))
            
            send_mail(
                'Votre code de vérification',
                f'Votre code de vérification est {request.session["verification_code"]}.',
                'medi.plateforme@gmail.com',
                [email],
            )
            return redirect('verify_code')
        else:
            return render(request, 'signup.html', {'error': 'Les mots de passe ne correspondent pas'})
    return render(request, 'signup.html')

def verify_code_view(request):
    
    if request.method == 'POST':
        entered_code = request.POST['verification_code']
        if entered_code == request.session.get('verification_code'):
            user = User.objects.get(username=request.session.get('username'))
            login(request, user)  # Connexion automatique
            return redirect('create_profile')  # Rediriger vers création de profil
        else:
            return render(request, 'verify_code.html', {'error': 'Code de vérification invalide'})
    return render(request, 'verify_code.html')

@login_required
def create_profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile.firstname = request.POST.get('firstname', '').strip()
        profile.lastname = request.POST.get('lastname', '').strip()
        profile.age = request.POST.get('age', None)
        profile.dob = request.POST.get('dob', None)
        profile.gender = request.POST.get('gender', None)
        profile.email = request.POST.get('email', '').strip()
        profile.address = request.POST.get('address', '').strip()
        profile.occupation = request.POST.get('occupation', None)

        if request.FILES.get('licence'):
            profile.licence = request.FILES.get('licence')

        profile.speciality = request.POST.get('speciality', '').strip()
        profile.terms_accepted = request.POST.get('terms_accepted') == 'on'

        try:
            profile.save()
            messages.success(request, "Votre profil a été mis à jour avec succès.")
            return redirect('succes_page')
        except Exception as e:
            messages.error(request, f"Erreur lors de la mise à jour du profil : {e}")

    context = {
        'profile': profile,  # Passer les données existantes pour pré-remplir le formulaire
    }

    return render(request, 'create_profile.html', context)


def success_view(request):
    logout(request)
    return render(request, 'succes.html')

@login_required
def patient_dashboard(request):
    return render(request, 'patient_dashboard.html')  # Template pour patient

@login_required
def docteur_dashboard(request):
    return render(request, 'docteur_dashboard.html')  # Template pour docteur


def react_dashboard(request):
    return render(request, "index.html")