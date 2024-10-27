from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('med_platform.urls')),  # Inclure les URLs de l'application med_platform
]
