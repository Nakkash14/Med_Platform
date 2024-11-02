from django.db import models
from django.core.exceptions import ValidationError

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Homme'),
        ('female', 'Femme'),
        ('other', 'Autre'),
    ]
    OCCUPATION_CHOICES = [
        ('patient', 'Patient'),
        ('docteur', 'Docteur'),
    ]
    
    # Champs du modèle
    firstname = models.CharField("Prénom", max_length=50)
    lastname = models.CharField("Nom", max_length=50)
    age = models.PositiveIntegerField("Âge")
    dob = models.DateField("Date de naissance")
    gender = models.CharField("Genre", max_length=10, choices=GENDER_CHOICES)
    email = models.EmailField("Email", unique=True)
    address = models.CharField("Adresse", max_length=255)
    city = models.CharField("Ville", max_length=100)
    profile_photo = models.ImageField("Photo de Profil", upload_to='profile_photos/', blank=True, null=True)
    occupation = models.CharField("Occupation", max_length=10, choices=OCCUPATION_CHOICES)
    licence = models.FileField("Licence (si docteur)", upload_to='licences/', blank=True, null=True)  # Licence pour docteurs
    speciality = models.CharField("Spécialité médicale", max_length=100, blank=True, null=True)  # Ajoute le champ spécialité
    terms_accepted = models.BooleanField("Conditions acceptées", default=False)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    def clean(self):
        """
        Validation pour s'assurer que le champ 'licence' et 'speciality' sont remplis
        si l'utilisateur est un docteur.
        """
        if self.occupation == 'docteur':
            if not self.licence:
                raise ValidationError("La licence est obligatoire pour les docteurs.")
            if not self.speciality:
                raise ValidationError("La spécialité est obligatoire pour les docteurs.")
