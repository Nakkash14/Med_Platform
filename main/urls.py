
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login_page'),
    path('signup/', views.signup_view, name='signup_page'),
    path('verify/', views.verify_code_view, name='verify_code'),
    path('create-profile/', views.create_profile_view, name='create_profile'),
    path('success/', views.success_view, name='succes_page'),
    path('dashboard/patient/', views.patient_dashboard, name='patient_dashboard'),
    path('dashboard/docteur/', views.docteur_dashboard, name='docteur_dashboard'),
]
