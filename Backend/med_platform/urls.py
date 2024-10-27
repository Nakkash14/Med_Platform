from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name='index_page'),  # Route pour la page d'accueil
    path('signup/', views.signup_page, name='signup'),
    path('admin/', views.admin_page, name='admin_page'),
    path('doctor/', views.doctor_page, name='doctor_page'),
    path('patient/', views.patient_page, name='patient_page'),
]
