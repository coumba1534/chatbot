from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = None  # Supprime le champ 'username' de AbstractUser

    first_name = models.CharField(max_length=150, blank=False)  # Prénom
    last_name = models.CharField(max_length=150, blank=False)   # Nom
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Mot de passe
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"