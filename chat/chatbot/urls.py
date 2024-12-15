from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot_view, name='home'),  # Racine redirige en fonction de l'état d'authentification
    path('chatbot/', views.chatbot_page, name='chatbot_authenticated'),  # Page des utilisateurs connectés
    path('chatbot-anonymous/', views.chatbot_anonymous, name='chatbot_anonymous'),  # Page non connectée
    path('historique/', views.afficher_historique, name='afficher_historique'),
    path('historique/<int:session_id>/', views.afficher_detail_session, name='afficher_detail_session'),
]
