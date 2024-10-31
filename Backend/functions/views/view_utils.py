# functions/views/view_utils.py
from django.shortcuts import render

def handle_admin_page(request):
    return render(request, 'Admin/admin.html')  # Chemin vers le template admin

def handle_doctor_page(request):
    return render(request, 'Doctor/doctor.html')  # Chemin vers le template doctor

def handle_patient_page(request):
    return render(request, 'Patient/patient.html')  # Chemin vers le template patient

def handle_index_page(request):
    return render(request, 'Formulaires_connection/index.html')

