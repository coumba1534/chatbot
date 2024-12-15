import os
import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from dotenv import load_dotenv
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from chatbot.models import SessionChat, MessageChat

import logging
logger = logging.getLogger(__name__)

# Vue de redirection générale pour la racine
def chatbot_view(request):
    logger.info(f"User authenticated: {request.user.is_authenticated}")
    if request.user.is_authenticated:
        logger.info("Redirection vers la page utilisateur connecté.")
        return redirect('chatbot_authenticated')  # Redirection si l'utilisateur est connecté
    logger.info("Redirection vers la page anonyme.")
    return redirect('chatbot_anonymous')  # Redirection si l'utilisateur n'est pas connecté

# Vue pour la page utilisateur connecté
@login_required
def chatbot_page(request):
    logger.info(f"Accès à la page utilisateur connecté pour {request.user.username}")
    return render(request, 'chatbot.html')  # Affiche la page pour les utilisateurs connectés

# Vue pour la page anonyme
def chatbot_anonymous(request):
    logger.info("Accès à la page anonyme.")
    return render(request, 'chatbot1.html')  # Affiche la page pour les utilisateurs non connectés

@login_required
def afficher_historique(request):
    """
    Affiche toutes les sessions de chat avec un résumé.
    """
    # Récupérer toutes les sessions de l'utilisateur
    sessions = SessionChat.objects.filter(utilisateur=request.user).order_by("-date_debut")

    # Préparer un résumé pour chaque session
    historique = []
    for session in sessions:
        # Récupérer le premier message de la session pour le titre
        premier_message = MessageChat.objects.filter(session_chat=session).order_by("date_message").first()
        titre = premier_message.message_utilisateur[:50] + "..." if premier_message else "Session sans titre"

        historique.append({
            "id": session.id,
            "titre": titre,
            "date": session.date_debut,
        })

    return render(request, "historique.html", {"historique": historique})

@login_required
def afficher_detail_session(request, session_id):
    """
    Affiche les messages d'une session de chat.
    """
    try:
        # Vérifier si la session appartient à l'utilisateur connecté
        session = SessionChat.objects.get(id=session_id, utilisateur=request.user)
        messages = MessageChat.objects.filter(session_chat=session).order_by("date_message")
        
        return render(request, "detail_session.html", {
            "session": session,
            "messages": messages,
        })
    except SessionChat.DoesNotExist:
        return render(request, "404.html", status=404)











