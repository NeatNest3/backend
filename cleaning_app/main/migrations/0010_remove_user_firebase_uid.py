# Generated by Django 5.1.2 on 2024-11-27 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_service_provider_pet_friendly'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='firebase_uid',
        ),
    ]