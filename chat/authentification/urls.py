
from django.urls import path
from . import views  
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('login/', views.login_page, name='login'),  
    path('logout/', LogoutView.as_view(), name='logout'),  
    path('register/', views.signup, name='register'), 
    path('edit-profile/', views.edit_profile, name='edit_profile'),


     # Réinitialisation du mot de passe
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    #path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
]

    



