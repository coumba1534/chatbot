from django.db import models
from django.core.exceptions import ValidationError
from authentification.models import User


class Universite(models.Model):
    nom = models.CharField(max_length=255)
    localisation = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom
    

# Modèle Etablissement (Facultés, Instituts, Ecoles)
class Etablissement(models.Model):
    TYPES_CHOICES = [
        ('faculte', 'Faculté'),
        ('institut', 'Institut'),
        ('ecole', 'École'),
    ]

    nom = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=TYPES_CHOICES)
    description = models.TextField(blank=True, null=True)
    universite = models.ForeignKey(Universite, on_delete=models.CASCADE, blank=True, null=True, related_name='etablissements')
    est_independant = models.BooleanField(default=False)

    def clean(self):
        """
        Validation personnalisée pour s'assurer que les instituts indépendants n'ont pas d'université liée.
        """
        if self.type == 'institut' and self.est_independant and self.universite is not None:
            raise ValidationError("Un institut indépendant ne doit pas être rattaché à une université.")
        if self.type == 'institut' and not self.est_independant and self.universite is None:
            raise ValidationError("Un institut rattaché doit avoir une université associée.")

    def __str__(self):
        if self.type == 'faculte' and not self.universite:
            raise ValueError("Une faculté doit être rattachée à une université.")
        return f"{self.nom} ({self.get_type_display()})"



# Grandes écoles
class GrandeEcole(models.Model):
    nom = models.CharField(max_length=255, unique=True)
    localisation = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom

    
# Filières
class Filiere(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    duree = models.IntegerField(help_text="Durée en années", null=True, blank=True)
    
    # Une filière est liée soit à une composante (faculté/institut) ou à une grande école
    etablissement = models.ForeignKey(Etablissement, on_delete=models.CASCADE, related_name='filieres', null=True, blank=True)
    grande_ecole = models.ForeignKey(GrandeEcole, on_delete=models.CASCADE, related_name='filieres', null=True, blank=True)

    def __str__(self):
        return self.nom 

#Informations Supplementaires sur les filieres 
class InformationSupplementaire(models.Model):
    CATEGORIES = [
        ('inscription', 'Étapes d\'inscription'),
        ('frais', 'Frais de scolarité'),
        ('diplome', 'Diplômes délivrés'),
        ('diplome_requis', 'Diplômes requis pour l\'admission'),
        ('contact', 'Contact'),
    ]

    categorie = models.CharField(max_length=50, choices=CATEGORIES)
    contenu = models.TextField()
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, blank=True, null=True, related_name="informations")

    def __str__(self):
        return f"{self.get_categorie_display()} - {self.universite.nom if self.universite else 'Général'}"   

class SessionChat(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)  # L'utilisateur lié à la session
    date_debut = models.DateTimeField(auto_now_add=True)  # Date de début de la session
    date_fin = models.DateTimeField(null=True, blank=True)  # Date de fin (optionnelle pour l'instant)
    
    def __str__(self):
        return f"Session {self.id} de {self.utilisateur.username} - {self.date_debut}"

class MessageChat(models.Model):
    session_chat = models.ForeignKey(SessionChat, related_name='messages', on_delete=models.CASCADE)  # Lien vers la session
    message_utilisateur = models.TextField()  # Le message de l'utilisateur
    message_chatbot = models.TextField()  # La réponse du chatbot
    date_message = models.DateTimeField(auto_now_add=True)  # Date et heure du message
    
    def __str__(self):
        return f"Message {self.id} - Session {self.session_chat.id}"

