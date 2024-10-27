# med_platform/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name='index_page'),  # Page d'accueil
    path('signup/', views.signup_page, name='signup'),  # Page d'inscription
    path('confirm-email/<uid>/<token>/', views.confirm_email, name='confirm_email'),  # Confirmation par lien si nécessaire
    path('create-profile/', views.create_profile, name='create_profile'),  # Création de profil
    path('admin/', views.admin_page, name='admin_page'),
    path('doctor/', views.doctor_page, name='doctor_page'),
    path('patient/', views.patient_page, name='patient_page'),
    path('mail-confirm/', views.mail_confirm_page, name='mail_confirm'),  # Route pour la confirmation par code
]
