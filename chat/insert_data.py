import os
import django

# Définir le chemin du projet Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat.settings')

# Initialiser Django
django.setup()


from chatbot.models import Universite, Etablissement, GrandeEcole, InformationSupplementaire, Filiere

# # Insertion des Universités
# usttb = Universite.objects.create(
#     nom="Université des Sciences des Techniques et des Technologies de Bamako",
#     localisation="Bamako",
#     description="Grande université publique dédiée aux sciences et technologies."
# )

# ulshb = Universite.objects.create(
#     nom="Université des Lettres et des Sciences Humaines de Bamako",
#     localisation="Bamako",
#     description="Université spécialisée dans les lettres et sciences humaines."
# )

# ussgb = Universite.objects.create(
#     nom="Université des Sciences Sociales et de Gestion de Bamako",
#     localisation="Bamako",
#     description="Université dédiée aux sciences sociales et à la gestion."
# )

# usjpb = Universite.objects.create(
#     nom="Université des Sciences Juridiques et Politiques de Bamako",
#     localisation="Bamako",
#     description="Université spécialisée dans les sciences juridiques et politiques."
# )

# univ_segou = Universite.objects.create(
#     nom="Université de Ségou",
#     localisation="Ségou",
#     description="Université publique située à Ségou, offrant des formations diverses."
# )

# Insertion des Etablissements (Facultés, Instituts)

# Université des Sciences des Techniques et des Technologies de Bamako (USTTB)
# Etablissement.objects.create(
#     nom="Faculté des Sciences et Techniques de Bamako",
#     type="faculte",
#     description="Faculté dédiée aux sciences fondamentales et appliquées.",
#     universite=usttb
# )

# Etablissement.objects.create(
#     nom="Institut des Sciences Appliquées",
#     type="institut",
#     description="Institut spécialisé dans les sciences appliquées.",
#     universite=usttb
# )

# Etablissement.objects.create(
#     nom="Faculté de Pharmacie",
#     type="faculte",
#     description="Faculté offrant des formations en pharmacie.",
#     universite=usttb
# )

# Etablissement.objects.create(
#     nom="Faculté de Médecine et d'Onto-stomatologie",
#     type="faculte",
#     description="Faculté dédiée à la médecine et à l'odontostomatologie.",
#     universite=usttb
# )

# Université des Lettres et des Sciences Humaines de Bamako (ULSHB)
# Etablissement.objects.create(
#     nom="Faculté des Lettres et des Sciences de Langage",
#     type="faculte",
#     description="Faculté dédiée aux lettres et aux sciences du langage.",
#     universite=ulshb
# )

# Etablissement.objects.create(
#     nom="Faculté des Sciences Humaines et des Sciences de l’Éducation",
#     type="faculte",
#     description="Faculté dédiée aux sciences humaines et à l'éducation.",
#     universite=ulshb
# )

# Etablissement.objects.create(
#     nom="Institut Universitaire de Technologie",
#     type="institut",
#     description="Institut dédié aux formations en technologie.",
#     universite=ulshb
# )

# Université des Sciences Sociales et de Gestion de Bamako (USSGB)
# Etablissement.objects.create(
#     nom="Faculté des Sciences Économiques et de Gestion",
#     type="faculte",
#     description="Faculté spécialisée en sciences économiques et gestion.",
#     universite=ussgb
# )

# Etablissement.objects.create(
#     nom="Faculté des Sciences Humaines",
#     type="faculte",
#     description="Faculté dédiée aux sciences humaines.",
#     universite=ussgb
# )

# Etablissement.objects.create(
#     nom="Institut Universitaire de Gestion",
#     type="institut",
#     description="Institut de formation en gestion.",
#     universite=ussgb
# )

# Etablissement.objects.create(
#     nom="Institut Universitaire de Développement Territorial",
#     type="institut",
#     description="Institut de formation en développement territorial.",
#     universite=ussgb
# )

# Etablissement.objects.create(
#     nom="Faculté d’Histoire et de Géographie",
#     type="faculte",
#     description="Faculté dédiée aux études d'histoire et de géographie.",
#     universite=ussgb
# )

# Université des Sciences Juridiques et Politiques de Bamako (USJPB)
# Etablissement.objects.create(
#     nom="Faculté des Droits Publics",
#     type="faculte",
#     description="Faculté spécialisée en droit public.",
#     universite=usjpb
# )

# Etablissement.objects.create(
#     nom="Faculté des Droits Privés",
#     type="faculte",
#     description="Faculté spécialisée en droit privé.",
#     universite=usjpb
# )

# Etablissement.objects.create(
#     nom="Faculté des Sciences d'Administration et Politique",
#     type="faculte",
#     description="Faculté dédiée aux sciences administratives et politiques.",
#     universite=usjpb
# )

# Université de Ségou
# Etablissement.objects.create(
#     nom="Faculté d'Agronomie et de Médecine Animale",
#     type="faculte",
#     description="Faculté dédiée à l'agronomie et à la médecine animale.",
#     universite=univ_segou
# )

# Etablissement.objects.create(
#     nom="Faculté des Sciences Sociales",
#     type="faculte",
#     description="Faculté dédiée aux sciences sociales.",
#     universite=univ_segou
# )

# Etablissement.objects.create(
#     nom="Faculté du Génie et des Sciences",
#     type="faculte",
#     description="Faculté dédiée au génie et aux sciences appliquées.",
#     universite=univ_segou
# )

# Etablissement.objects.create(
#     nom="Institut Universitaire de Formation Professionnelle",
#     type="institut",
#     description="Institut de formation professionnelle.",
#     universite=univ_segou
# )

# Insertion des Grandes Écoles
# eni = GrandeEcole.objects.create(
#     nom="École Nationale d'Ingénierie",
#     localisation="Bamako",
#     description="Grande école formant des ingénieurs de haut niveau."
# )

# enetp = GrandeEcole.objects.create(
#     nom="École Normale d’Enseignement Technique et Professionnel",
#     localisation="Bamako",
#     description="École spécialisée dans la formation des enseignants techniques."
# )

# Insertion des Instituts (non rattachés à une Université)
# Etablissement.objects.create(
#     nom="Institut National de Formation des Travailleurs Sociaux",
#     type="institut",
#     description="Institut pour la formation des travailleurs sociaux.",
#     universite=None  # Non rattaché à une université
# )

# Etablissement.objects.create(
#     nom="Institut National de Formation en Sciences de Santé",
#     type="institut",
#     description="Institut pour la formation en sciences de santé.",
#     universite=None  # Non rattaché à une université
# )

# Etablissement.objects.create(
#     nom="Institut de Formation de Maîtres",
#     type="institut",
#     description="Institut dédié à la formation des enseignants.",
#     universite=None  # Non rattaché à une université
# )

# Etablissement.objects.create(
#     nom="Institut Polytechnique Rural de Formation et de Recherche Appliquée",
#     type="institut",
#     description="Institut spécialisé dans la formation polytechnique rurale.",
#     universite=None  # Non rattaché à une université
# )

# Etablissement.objects.create(
#     nom="École Nationale d’Administration",
#     type="ecole",
#     description="École formant des administrateurs publics.",
#     universite=None  # Non rattaché à une université
# )

# Etablissement.objects.create(
#     nom="Institut National des Arts",
#     type="institut",
#     description="Institut dédié aux formations en arts.",
#     universite=None  # Non rattaché à une université
# )


# Données des filières
filieres_data = [
    {
        "nom": "LICENCE PROFESSIONNELLE AGROECONOMIE ",
        "description": 
        """ 
            L’objectif de cette licence est de former des assistants en agroéconomie. Les assistants en 
            agroéconomie pourront intervenir au niveau de l’assistance dans le suivi, le contrôle de qualité, 
            la réalisation et la maintenance des projets d’agriculture. Ils peuvent également intervenir 
            comme agents technico-commerciaux.
        """, 
        "duree": 3,
        "etablissement_nom": "Faculté d'Agronomie et de Médecine Animale"
    },
]

# Insérer les filières dans la base de données
for filiere in filieres_data:
    try:
        duree = filiere.get("duree", None)  # Récupère la durée ou None si elle est absente
        if duree is None:
            print(f"Durée manquante pour la filière '{filiere['nom']}'")
            continue  # Ignore cette filière

        etablissement = Etablissement.objects.get(nom=filiere["etablissement_nom"].strip())
        Filiere.objects.create(
            nom=filiere["nom"],
            description=filiere["description"],
            duree=duree,
            etablissement=etablissement
        )
        print(f"Filière '{filiere['nom']}' ajoutée à l'établissement '{etablissement.nom}' avec succès.")
    except Etablissement.DoesNotExist:
        print(f"Erreur : L'établissement '{filiere['etablissement_nom']}' n'existe pas.")
