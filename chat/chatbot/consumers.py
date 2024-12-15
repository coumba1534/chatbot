
import os
import json
from datetime import datetime, timezone
import google.generativeai as genai
from dotenv import load_dotenv
from chatbot.models import SessionChat, MessageChat, Universite, Filiere, GrandeEcole
from django.contrib.auth.models import AnonymousUser
from channels.generic.websocket import SyncConsumer
import logging

# Configurer le logger
logger = logging.getLogger(__name__)

# Charger la clé API
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Erreur : GEMINI_API_KEY manquant dans le fichier .env")
genai.configure(api_key=api_key)

class ChatbotConsumer(SyncConsumer):
    def websocket_connect(self, event):
        """
        Initialisation de la connexion WebSocket et de la session.
        """
        logger.info("Connexion WebSocket établie.")
        self.send({"type": "websocket.accept"})

        user = self.scope.get("user", AnonymousUser())
        self.user = user  # Garde la référence pour les autres méthodes

        # Gestion des utilisateurs connectés
        if user.is_authenticated:
            # Créer une nouvelle session de chat dans la base
            self.session_chat = SessionChat.objects.create(
                utilisateur=user,
                date_debut=datetime.now()
            )
            logger.info(f"Nouvelle session créée pour {user.username}.")
        else:
            self.session_chat = None
            logger.info("Utilisateur non authentifié. Session anonyme.")

        # Configuration initiale du chatbot
        self.chat_session = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 8192,
            }
        ).start_chat()

        # Envoi de l'instruction système
        system_instruction = """
            Tu es un chatbot spécialisé dans l’orientation universitaire et professionnelle pour les jeunes maliens.
            Tu es informé sur les universités, écoles et instituts publics au Mali, ainsi que sur leurs programmes,
            frais de scolarité et conditions d'admission. Tu dois répondre de manière claire et précise.
        """
        self.chat_session.send_message(system_instruction)

        # Envoyer un message de bienvenue
        welcome_message = f"Bonjour {user.first_name} ! Posez vos questions." if user.is_authenticated else \
                          "Bonjour ! Veuillez vous connecter pour bénéficier de fonctionnalités complètes."
        self._send_message_to_client(welcome_message)

    def websocket_receive(self, event):
        """
        Traitement des messages WebSocket entrants.
        """
        try:
            # Vérifier les données reçues
            text_data = event.get("text", None)
            if not text_data:
                self._send_message_to_client("Message vide reçu.")
                return

            # Charger le JSON
            data = json.loads(text_data)
            action = data.get("action", "message")
            user_message = data.get("message", "").strip()

            if action == "consulter_historique":
                reply = self._retrieve_history(self.user)
            elif user_message:
                reply = self._process_user_message(user_message)
            else:
                reply = "Veuillez entrer un message valide."

            # Envoyer la réponse au client
            self._send_message_to_client(reply)

        except json.JSONDecodeError:
            logger.error("JSON mal formé reçu.")
            self._send_message_to_client("Erreur : format JSON invalide.")
        except Exception as e:
            logger.error(f"Erreur dans websocket_receive : {e}")
            self._send_message_to_client("Une erreur est survenue. Veuillez réessayer.")

    def websocket_disconnect(self, event):
        """
        Gestion de la déconnexion WebSocket.
        """
        logger.info("Déconnexion WebSocket.")
        if self.user.is_authenticated and self.session_chat:
            # Marquer la session comme terminée
            self.session_chat.date_fin = datetime.now()
            self.session_chat.save()
            logger.info(f"Session terminée pour {self.user.username}.")

    def _process_user_message(self, message):
        """
        Traite le message utilisateur avec l'IA et sauvegarde les données.
        """
        try:
            # Ignorer les messages vides
            if not message.strip():
                return "Veuillez entrer un message valide."

            # Requête au chatbot avec contexte
            db_context = self._query_database(message)
            response = self.chat_session.send_message(f"{message}\n\n{db_context}")
            chatbot_reply = response.candidates[0].content.parts[0].text if response.candidates else \
                            "Je n'ai pas pu répondre pour le moment."

            # Sauvegarder le message dans la base si connecté
            if self.user.is_authenticated:
                if not hasattr(self, 'session_chat') or self.session_chat is None:
                    self.session_chat = SessionChat.objects.create(
                        utilisateur=self.user,
                        date_debut=timezone.now()
                )
                MessageChat.objects.create(
                    session_chat=self.session_chat,
                    message_utilisateur=message,
                    message_chatbot=chatbot_reply
                )
            return chatbot_reply

        except Exception as e:
            logger.error(f"Erreur dans _process_user_message : {e}")
            return "Je rencontre un problème technique. Veuillez réessayer plus tard."

    def _retrieve_history(self, user):
        """
        Retourne l'historique des sessions terminées.
        """
        if not user.is_authenticated:
            return "Connectez-vous pour consulter votre historique."

        sessions = SessionChat.objects.filter(
            utilisateur=user, 
            date_fin__isnull=False,
            messages__isnull=False  # Vérifie s'il y a des messages associés
            ).distinct().order_by('-date_debut')[:5]
        if not sessions.exists():
            return "Aucun historique trouvé."

        historique = []
        for session in sessions:
            messages = MessageChat.objects.filter(session_chat=session).order_by('date_message')
            session_data = "\n".join(f"User: {m.message_utilisateur}\nBot: {m.message_chatbot}" for m in messages)
            historique.append(f"Session du {session.date_debut}:\n{session_data}")
        return "\n\n".join(historique)

    def _query_database(self, query):
        """
        Interroge la base pour des informations pertinentes.
        """
        try:
            # Exemple simple d'interrogation contextuelle
            if "universite" in query.lower():
                return "\n".join(f"- {u.nom} : {u.description}" for u in Universite.objects.all()[:5])
            elif "filiere" in query.lower():
                return "\n".join(f"- {f.nom} ({f.duree} ans)" for f in Filiere.objects.all()[:5])
            elif "grande ecole" in query.lower():
                return "\n".join(f"- {e.nom} : {e.description}" for e in GrandeEcole.objects.all()[:5])
            else:
                return "Aucune information spécifique trouvée."
        except Exception as e:
            logger.error(f"Erreur dans _query_database : {e}")
            return "Erreur lors de la recherche d'informations."

    def _send_message_to_client(self, message):
        """
        Envoie un message au client.
        """
        try:
            self.send({"type": "websocket.send", "text": json.dumps({"reply": message})})
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi au client : {e}")



# import os
# import json
# import google.generativeai as genai
# from dotenv import load_dotenv
# import django
# django.setup()
# from chatbot.models import Filiere, Universite, GrandeEcole, InformationSupplementaire, Historique
# from authentification.models import User
# from channels.generic.websocket import SyncConsumer

# # Charger la clé API depuis .env
# load_dotenv()

# # Initialiser Django avant toute interaction avec les modèles


# api_key = os.getenv("GEMINI_API_KEY")
# if api_key:
#     genai.configure(api_key=api_key)
#     model = genai.GenerativeModel(
#         model_name="gemini-1.5-flash",
#         generation_config={
#             "temperature": 1,
#             "top_p": 0.95,
#             "top_k": 64,
#             "max_output_tokens": 8192,
#         }
#     )
#     chat_session = model.start_chat()
# else:
#     raise ValueError("Erreur : GEMINI_API_KEY manquant dans le fichier .env")

# class ChatbotConsumer(SyncConsumer):
#     def websocket_connect(self, event):
#         self.send({
#             "type": "websocket.accept"
#         })

#         # Initialiser la session de chat
#         self.chat_session = chat_session

#         # Envoi de l'instruction système comme message initial
#         system_instruction = """
#             Tu es un chatbot spécialisé dans l’orientation universitaire et professionnelle pour les jeunes maliens.
#             Tu es informé sur les universités, écoles et instituts publics au Mali, ainsi que sur leurs programmes,
#             frais de scolarité et conditions d'admission. 
#              Tu dois répondre de manière claire et précise.
#         """
#         self.chat_session.send_message(system_instruction)

#          # Message de bienvenue
#         user = self.scope.get('user')
#         if user:
#             welcome_message = f"Bonjour {user.first_name} ! Je suis ici pour vous aider. Vous pouvez consulter votre historique ou poser une nouvelle question."
#         else:
#             welcome_message = "Bonjour ! Je suis un chatbot spécialisé dans l'orientation universitaire et professionnelle pour les jeunes maliens. Comment puis-je vous aider ?"


#         # Envoyer une réponse initiale
#         self.send({
#             "type": "websocket.send",
#             "text": json.dumps({
#                 'reply': welcome_message
#             })
#         })

#     def websocket_receive(self, event):
#         # Récupérer le message utilisateur
#         text_data = event.get('text', None)
#         if not text_data:
#             return

#         try:
#             text_data_json = json.loads(text_data)
#             user = self.scope.get('user')
#             if text_data_json.get('action') == 'consulter_historique':
#                 # Logique de consultation d'historique pour les utilisateurs connectés
#                 if user and user.is_authenticated:
#                     historique = Historique.objects.filter(utilisateur=user).order_by('-date')[:5]
#                     historique_messages = [
#                         f"User: {h.message_utilisateur}\nBot: {h.message_chatbot}" for h in historique
#                     ]
#                     chatbot_reply = "\n\n".join(historique_messages) if historique_messages else \
#                         "Vous n'avez pas d'historique de conversation."
#                 else:
#                     chatbot_reply = "Vous devez être connecté pour consulter votre historique."
#             else:
#                 # Logique normale de réponse du chatbot
#                 user_message = text_data_json.get('message', '')
#                 chatbot_reply = self.handle_user_message(user_message, user)
#         except Exception as e:
#             chatbot_reply = f"Erreur lors de la réponse du chatbot : {e}"
#         self.send({
#             "type": "websocket.send",
#             "text": json.dumps({'reply': chatbot_reply})
#         })

#     def handle_user_message(self, message, user):
#         """
#         Logique principale pour traiter les messages utilisateurs, 
#         avec ou sans enregistrement d'historique selon l'état de connexion.
#         """    
#             # Interroger la base de données
#         db_response = self.query_database(message)

#             # Combiner la réponse de la base de données avec la question de l'utilisateur
#         full_message = f"{message}\n\nInformations disponibles : {db_response}"
#         response = self.chat_session.send_message(full_message)

#             # Extraction de la réponse du modèle
#         if hasattr(response, 'candidates') and len(response.candidates) > 0:
#             chatbot_reply = response.candidates[0].content.parts[0].text
#         else:
#             chatbot_reply = "Je n'ai pas de réponse pour le moment."

#              # Sauvegarder l'historique dans la base de données
#         if user and user.is_authenticated:  # Vérifier si l'utilisateur est connecté et authentifié
#             Historique.objects.create(
#                 utilisateur=user,
#                 message_utilisateur=message ,
#                 message_chatbot=chatbot_reply
#             )   
        
#             # Envoyer la réponse au client
#         return chatbot_reply


#     def websocket_disconnect(self, event):
#         # Déconnexion du WebSocket
#             print("Déconnexion WebSocket...")

#     def query_database(self, query):
#         """
#         Interroge la base de données pour des informations pertinentes basées sur la requête utilisateur.
#         """
#         query = query.lower()
#         result = []

#         # Interroger les universités
#         if "universite" in query:
#             universites = Universite.objects.all()
#             result.append("Voici les universités disponibles :")
#             for uni in universites:
#                 result.append(f"- {uni.nom} ({uni.localisation}) : {uni.description}")

#         # Interroger les filières
#         elif "filiere" in query or "programme" in query:
#             filieres = Filiere.objects.all()
#             result.append("Voici les filières disponibles :")
#             for filiere in filieres:
#                 result.append(f"- {filiere.nom} ({filiere.duree} ans)")

#         # Interroger les grandes écoles
#         elif "grande ecole" in query or "ecole" in query:
#             ecoles = GrandeEcole.objects.all()
#             result.append("Voici les grandes écoles disponibles :")
#             for ecole in ecoles:
#                 result.append(f"- {ecole.nom} ({ecole.localisation}) : {ecole.description}")

#         # Informations générales sur l'inscription
#         elif "inscription" in query:
#             result.append(""" 
#                 Étapes générales d'inscription :
#                 1. Remplir un formulaire d'inscription.
#                 2. Soumettre les documents requis.
#                 3. Payer les frais d'inscription si nécessaire.
#                 4. Attendre la confirmation ou passer un concours.
#             """)

#         return "\n".join(result) if result else "Désolé, je n'ai pas trouvé d'informations pertinentes."


# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# import google.generativeai as genai
# import os
# from dotenv import load_dotenv


# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")
# if api_key:
#     genai.configure(api_key=api_key)
#     model = genai.GenerativeModel(
#         model_name="gemini-1.5-flash",
#         generation_config={
#             "temperature": 1,
#             "top_p": 0.95,
#             "top_k": 64,
#             "max_output_tokens": 8192,
#         }
#     )
#     chat_session = model.start_chat()
# else:
#     print("Erreur : GEMINI_API_KEY manquant dans le fichier .env")    

# class ChatbotConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         # Initialisation de la session sans instruction système
#         self.chat_session = model.start_chat()

#         # Envoi de l'instruction système comme message initial
#         system_instruction = """

#                 Tu es un chatbot spécialisé dans l’orientation universitaire et professionnelle pour les jeunes maliens. 
#                 Tu es informé sur les universités, écoles et instituts publics au Mali, ainsi que sur leurs programmes, 
#                 frais de scolarité et conditions d'admission. 
#                 Voici des informations importantes que tu dois connaître et utiliser 
#                 pour répondre aux questions des utilisateurs :
#                 Universités au Mali :

#                 Université des Sciences des Techniques et des Technologies de Bamako (USTTB) : comprend la FST (Faculté des Sciences et Techniques), l'ISA (Institut des Sciences Appliquées), la FAPH (Faculté de Pharmacie), et la FMOS (Faculté de Médecine et d’Onto-stomatologie).
#                 Université des Lettres et des Sciences Humaines de Bamako (ULSHB) : comprend la FLSL (Faculté des Lettres et des Sciences de Langage), la FSHSE (Faculté des Sciences Humaines et de l’Éducation), et l'IUT (Institut Universitaire de Technologie).
#                 Université des Sciences Sociales et de Gestion de Bamako (USSGB) : comprend la FSEG (Faculté des Sciences Économiques et de Gestion), la FSH (Faculté des Sciences Humaines), l'IUG (Institut Universitaire de Gestion), l'IUDT (Institut Universitaire de Développement Territorial), et la FHG (Faculté d’Histoire et de Géographie).
#                 Université des Sciences Juridiques et Politiques de Bamako (USJPB) : comprend la FDPU (Faculté des Droits Publics), la FDPRI (Faculté des Droits Privés), et la FSAP (Faculté des Sciences d’Administration et Politique).
#                 Université de Ségou : comprend la FAMA (Faculté d’Agronomie et de Médecine Animale), la FASSO (Faculté des Sciences Sociales), la FAGES (Faculté du Génie et des Sciences), et l'IUFP (Institut Universitaire de Formation Professionnelle).
#                 Grandes Écoles :

#                 ENI (École Nationale d’Ingénierie)
#                 ENETP (École Normale d’Enseignement Technique et Professionnel)
#                 Instituts :

#                 INFTS (Institut National de Formation des Travailleurs Sociaux)
#                 INFSS (Institut National de Formation en Sciences de la Santé)
#                 IFM (Institut de Formation de Maîtres)
#                 IPER (Institut Polytechnique Rural de Formation et de Recherche Appliquée)
#                 ENA (École Nationale d’Administration)
#                 INA (Institut National des Arts)
#                 Réponds de manière concise et professionnelle. Ne donne que les informations présentes ici, sans émettre de suppositions. Si un utilisateur demande une information non spécifiée dans cette base, indique poliment que tu ne disposes pas de cette information.
                    

#                 Étapes d'inscription dans les universités maliennes :
#                 - Remplir un formulaire d'inscription en ligne ou en présentiel.
#                 - Soumettre les pièces justificatives requises.
#                 - Payer les frais d'inscription (si applicables).
#                 - Attendre la confirmation d'admission ou passer un concours (si requis).

#                 Pièces exigées pour l'inscription :
#                 - Photocopie de la pièce d'identité ou passeport valide.
#                 - Relevé de notes du Baccalauréat.
#                 - Diplôme ou attestation de réussite.
#                 - Certificat de résidence (si nécessaire).
#                 - Deux photos d'identité récentes.

#                 Tu dois répondre de manière claire et précise aux utilisateurs en te basant sur ces informations.
#                 """
#         response = self.chat_session.send_message(system_instruction)

#         # Optionnel : envoyer la réponse du modèle (ou une confirmation) au client pour montrer que l'instruction a été définie
#         await self.send(text_data=json.dumps({
#             'reply': "Bonjour ! Je suis un chatbot spécialisé dans l'orientation universitaire et professionnelle pour les jeunes maliens. Comment puis-je vous aider ?"
#         }))

#     async def disconnect(self, close_code):
#         # Nettoyage des ressources si nécessaire
#         pass

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         user_message = text_data_json['message']

#         try:
#             # Envoi du message utilisateur à la session de chat
#             response = self.chat_session.send_message(user_message)

#             # Extraction de la réponse du modèle
#             if hasattr(response, 'candidates') and len(response.candidates) > 0:
#                 chatbot_reply = response.candidates[0].content.parts[0].text
#             else:
#                 chatbot_reply = "Je n'ai pas de réponse pour le moment."

#         except Exception as e:
#             chatbot_reply = f"Erreur lors de la réponse du chatbot : {e}"

#         # Envoi de la réponse au client
#         await self.send(text_data=json.dumps({
#             'reply': chatbot_reply
#         }))