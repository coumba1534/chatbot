from django.conf import settings
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site

from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .forms import UserProfileForm, PasswordChangeForm



def logout_user(request):
    logout(request)
    return redirect('login')


def login_page(request):
    #if request.user.is_authenticated:
        #return redirect('home')  # Remplacez 'home' par la page d'accueil ou de tableau de bord appropriée

    form = forms.LoginForm()
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                messages.success(request, "Connexion réussie.")
                
                # Redirection vers la page précédente ou par défaut
                next_url = request.GET.get('next', 'chatbot_page') 
                return redirect(next_url)
            else:
                messages.error(request, 'Identifiants invalides.')

    return render(
        request, 'login.html', context={'form': form}
    )



def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Sauvegarde l'utilisateur
            messages.success(request, "Votre compte a été créé avec succès !")
            return redirect('login')  # Redirige vers la page de connexion
    else:
        form = CustomUserCreationForm()  # Crée un formulaire vide

    return render(request, 'signup.html', {'form': form})




class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'

    def form_valid(self, form):
        response = super().form_valid(form)
        # Personnaliser l'email ici si besoin
        return response


@login_required
def edit_profile(request):
    user = request.user

    if request.method == "POST":
        # Si l'utilisateur modifie ses informations personnelles
        profile_form = UserProfileForm(request.POST, instance=user)
        password_form = PasswordChangeForm(user, request.POST)

        if "update_profile" in request.POST and profile_form.is_valid():  # Mise à jour du profil
                profile_form.save()
                messages.success(request, "Votre profil a été mis à jour avec succès.")
                return redirect('edit_profile')

        elif "change_password" in request.POST and password_form.is_valid():  # Changement du mot de passe
                current_password = password_form.cleaned_data["current_password"]
                if not user.check_password(current_password):
                    password_form.add_error("current_password", "Le mot de passe actuel est incorrect.")
                else:
                    new_password = password_form.cleaned_data["new_password"]
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)  # Maintient l'utilisateur connecté
                    messages.success(request, "Votre mot de passe a été changé avec succès.")
                    return redirect('edit_profile')

    else:
        profile_form = UserProfileForm(instance=user)
        password_form = PasswordChangeForm(user)

    return render(request, 'edit_profile.html', {
        'profile_form': profile_form,
        'password_form': password_form
    })
