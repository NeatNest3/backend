# Generated by Django 5.1.2 on 2024-11-18 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_devicetoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='firebase_uid',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
