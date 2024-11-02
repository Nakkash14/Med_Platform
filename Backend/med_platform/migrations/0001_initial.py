# Generated by Django 5.1.2 on 2024-11-01 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50, verbose_name='Prénom')),
                ('lastname', models.CharField(max_length=50, verbose_name='Nom')),
                ('age', models.PositiveIntegerField(verbose_name='Âge')),
                ('dob', models.DateField(verbose_name='Date de naissance')),
                ('gender', models.CharField(choices=[('male', 'Homme'), ('female', 'Femme'), ('other', 'Autre')], max_length=10, verbose_name='Genre')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('address', models.CharField(max_length=255, verbose_name='Adresse')),
                ('city', models.CharField(max_length=100, verbose_name='Ville')),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to='profile_photos/', verbose_name='Photo de Profil')),
                ('occupation', models.CharField(choices=[('patient', 'Patient'), ('docteur', 'Docteur')], max_length=10, verbose_name='Occupation')),
                ('terms_accepted', models.BooleanField(default=False, verbose_name='Conditions acceptées')),
            ],
        ),
    ]