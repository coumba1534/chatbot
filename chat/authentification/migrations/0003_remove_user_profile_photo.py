# Generated by Django 5.1.2 on 2024-12-14 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0002_alter_user_first_name_alter_user_last_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='profile_photo',
        ),
    ]