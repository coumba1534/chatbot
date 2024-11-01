import os
import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from dotenv import load_dotenv
from django.shortcuts import render

# Chargement des variables d'environnement pour recuperer la cle 
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Erreur : GEMINI_API_KEY est manquant dans le fichier .env")
else:
    print("Clé API trouvée :", api_key)

# Configuration du modele de chatbot
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config={
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        },
        system_instruction="Tu es un chatbot spécialisé dans l’orientation universitaire et professionnelle pour les jeunes maliens..."
    )
    # Initialisation d'une session de chat pour maintenir le contexte
    chat_session = model.start_chat()
    print("Session de chat initialisee avec succes")
except Exception as e:# Permet de vérifier plus tard si l'initialisation a echoue
    print("Erreur d'initialisation du modele ou de la session :", e)

# Vue pour la page du chatbot 
def chatbot_page(request):
    return render(request, 'chatbot.html')

# Vue pour gerer les requetes de l'API 
@csrf_exempt
def chatbot_view(request):
    print("Méthode de requete :", request.method)
    if request.method == "POST":
        try:
            print("Début de la requete POST reçue")
            # Chargement du corps de la requete JSON
            data = json.loads(request.body)
            user_input = data.get("message", "")

            # Verification si le message est vide
            if not user_input:
                print("Message vide reçu")
                return JsonResponse({"error": "Message vide"}, status=400)

            print("Message utilisateur :", user_input)

            # Envoi du message utilisateur a l'API du modele
            response = chat_session.send_message(user_input)
            print("Reponse brute de l'API :", response)

            # Verification que la reponse contient des candidats
            if hasattr(response, 'candidates') and isinstance(response.candidates, list) and len(response.candidates) > 0:
                # Extraction du texte brut de la reponse
                json_text = response.candidates[0].content.parts[0].text
                message_response = json.loads(json_text)
                # Tentative de decodage de la reponse en JSON
                try:
                    message_response = json.loads(json_text)  #
                    print("Reponse decodee :", message_response)
                    return JsonResponse({"reply": message_response.get("message", "Aucune reponse disponible.")})
                except json.JSONDecodeError:
                    # Gestion de l'erreur si la réponse n'est pas un JSON valide
                    print("Erreur de decodage JSON dans la reponse :", json_text)
                    return JsonResponse({"error": "Erreur de decodage de la reponse du chatbot"}, status=500)
            else:
                # Gestion du cas ou aucune reponse n'est reçue du modele
                return JsonResponse({"error": "Aucune reponse du chatbot"}, status=500)

        except json.JSONDecodeError:
            # Gestion des erreurs si la requete reçue n'est pas un JSON valide
            print("Erreur de decodage JSON dans la requete")
            return JsonResponse({"error": "Requete JSON invalide"}, status=400)
        except Exception as e:
            # Gestion de toute autre exception inattendue
            print(f"Erreur lors du traitement de la requete : {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    # Gestion des requetes non-POST avec un message d'erreur
    return JsonResponse({"error": "Invalid request"}, status=400)










