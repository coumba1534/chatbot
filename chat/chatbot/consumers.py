import json
from channels.generic.websocket import AsyncWebsocketConsumer
import google.generativeai as genai
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config={
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
        }
    )
    chat_session = model.start_chat()
else:
    print("Erreur : GEMINI_API_KEY manquant dans le fichier .env")    

class ChatbotConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        # Initialisation de la session sans instruction système
        self.chat_session = model.start_chat()

        # Envoi de l'instruction système comme message initial
        system_instruction = "Tu es un chatbot spécialisé dans l’orientation universitaire et professionnelle pour les jeunes maliens..."
        response = self.chat_session.send_message(system_instruction)

        # Optionnel : envoyer la réponse du modèle (ou une confirmation) au client pour montrer que l'instruction a été définie
        await self.send(text_data=json.dumps({
            'reply': "Bonjour ! Je suis un chatbot spécialisé dans l'orientation universitaire et professionnelle pour les jeunes maliens. Comment puis-je vous aider ?"
        }))

    async def disconnect(self, close_code):
        # Nettoyage des ressources si nécessaire
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user_message = text_data_json['message']

        try:
            # Envoi du message utilisateur à la session de chat
            response = self.chat_session.send_message(user_message)

            # Extraction de la réponse du modèle
            if hasattr(response, 'candidates') and len(response.candidates) > 0:
                chatbot_reply = response.candidates[0].content.parts[0].text
            else:
                chatbot_reply = "Je n'ai pas de réponse pour le moment."

        except Exception as e:
            chatbot_reply = f"Erreur lors de la réponse du chatbot : {e}"

        # Envoi de la réponse au client
        await self.send(text_data=json.dumps({
            'reply': chatbot_reply
        }))