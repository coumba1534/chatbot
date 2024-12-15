from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User  # Assure-toi que tu as importé ton modèle personnalisé User

class CustomUserCreationForm(UserCreationForm):
    # Retirer le champ 'username' et ajouter des champs personnalisés
    first_name = forms.CharField(
        max_length=150, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=150, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User  # Utilise ton modèle User personnalisé
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']  # Enlève le champ 'username'

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        
        # Validation personnalisée : au moins 4 caractères
        if len(password) < 4:
            raise forms.ValidationError("Le mot de passe doit contenir au moins 4 caractères.")
        
        # Suppression de la validation sur les mots de passe trop courants ou numériques
        return password

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        # Validation pour vérifier que les deux mots de passe correspondent
        if password1 != password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        
        return password2


class LoginForm(forms.Form):
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'email': 'Adresse e-mail'
        }

class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe actuel")
    new_password = forms.CharField(widget=forms.PasswordInput, label="Nouveau mot de passe")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirmer le mot de passe")

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user  # Stocke l'utilisateur pour la validation

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise forms.ValidationError("Les nouveaux mots de passe ne correspondent pas.")

        return cleaned_data

