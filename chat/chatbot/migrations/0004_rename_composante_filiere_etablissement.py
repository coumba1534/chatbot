# Generated by Django 5.1.2 on 2024-12-06 23:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0003_filiere'),
    ]

    operations = [
        migrations.RenameField(
            model_name='filiere',
            old_name='composante',
            new_name='etablissement',
        ),
    ]