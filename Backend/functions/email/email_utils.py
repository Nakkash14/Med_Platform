# functions/email/email_utils.py

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.core.cache import cache
import random
import datetime
def send_confirmation_email(user_email, username, user_id, confirmation_code):
    subject = "Confirmation de votre inscription"
    message = ""
    html_message = f"""
    <p>Bonjour <strong>{username}</strong>,</p>
    <p>Merci pour votre inscription. Utilisez le code ci-dessous pour confirmer votre adresse e-mail :</p>
    <p><strong style="color: blue;">Code de confirmation : {confirmation_code}</strong></p>
    <p>Ce code est valide pendant 5 minutes.</p>
    <p>Merci !</p>
    """
    
    # Envoie de l'e-mail avec le code de confirmation
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
        html_message=html_message
    )
    # Génère un code de confirmation à 4 chiffres
    confirmation_code = random.randint(1000, 9999)
    # Définit le délai d'expiration pour le code
    expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=5)

    # Stocke le code et l'expiration dans le cache
    cache.set(f'confirmation_code_{user_id}', confirmation_code, timeout=300)
    cache.set(f'confirmation_expiration_{user_id}', expiration_time, timeout=300)

    subject = "Confirmation de votre inscription"
    message = ""
    html_message = f"""
    <p>Bonjour <strong>{username}</strong>,</p>
    <p>Merci pour votre inscription. Utilisez le code ci-dessous pour confirmer votre adresse e-mail :</p>
    <p><strong style="color: blue;">Code de confirmation : {confirmation_code}</strong></p>
    <p>Ce code est valide pendant 5 minutes.</p>
    <p>Merci !</p>
    """
    
    
# La fonction handle_confirm_page a été modifiée pour ne pas rendre de template
def handle_confirm_page(request, user_id):
    if request.method == "POST":
        code_saisi = request.POST.get("confirmation_code", "")
        
        stored_code = cache.get(f'confirmation_code_{user_id}')
        expiration_time = cache.get(f'confirmation_expiration_{user_id}')
        
        if stored_code and expiration_time:
            if str(stored_code) == code_saisi and datetime.datetime.now() < expiration_time:
                cache.delete(f'confirmation_code_{user_id}')
                cache.delete(f'confirmation_expiration_{user_id}')
                return {'success': True, 'message': "Le code est valide."}
            else:
                return {'success': False, 'message': "Le code est incorrect ou a expiré."}
        else:
            return {'success': False, 'message': "Le code n'est plus valide."}

    return {'success': False, 'message': "Veuillez entrer le code de confirmation."}