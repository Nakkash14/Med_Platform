from django.shortcuts import render , redirect
from .forms import UserRegistrationForm
from django.contrib.auth import login


# Vue pour la page admin
def admin_page(request):
    return render(request, 'Admin/admin.html')  # Chemin vers le template admin

# Vue pour la page doctor
def doctor_page(request):
    return render(request, 'Doctor/doctor.html')  # Chemin vers le template doctor

# Vue pour la page patient
def patient_page(request):
    return render(request, 'Patient/patient.html')  # Chemin vers le template patient

def index_page(request):
    return render(request, 'Formulaires_connection/index.html')  

def signup_page(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Enregistre l'utilisateur dans la base de données
            login(request, user)  # Connecte automatiquement l'utilisateur après l'inscription
            return redirect('doctor_page')  # Redirige vers la page des docteurs
    else:
        form = UserRegistrationForm()

    return render(request, 'Formulaires_connection/signup.html', {'form': form})