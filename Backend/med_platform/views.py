# med_platform/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from functions.auth.auth_utils import handle_signup, handle_confirm_email, handle_create_profile
from functions.email.email_utils import send_confirmation_email, handle_confirm_page
from functions.views.view_utils import handle_admin_page, handle_doctor_page, handle_patient_page, handle_index_page

def signup_page(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = handle_signup(request, form)
            send_confirmation_email(user.email, user.username, user.id)  # Appel avec les bons arguments
            return redirect('mail_confirm')  # Redirige vers la page de confirmation par code
    else:
        form = UserRegistrationForm()
    return render(request, 'Formulaires_connection/signup.html', {'form': form})

def confirm_email(request, uid, token):
    return handle_confirm_email(request, uid, token)

@login_required
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

def mail_confirm_page(request):
    user_id = request.user.id
    result = handle_confirm_page(request, user_id)  # Appel de handle_confirm_page pour valider le code

    if result['success']:
        return render(request, 'Mail/mail_confirm.html', {'success': True})
    else:
        return render(request, 'Mail/mail_confirm.html', {'error_message': result['message']})