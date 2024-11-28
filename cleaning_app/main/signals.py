from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from firebase_admin import auth as firebase_auth
from .models import Home, Service_Provider, User
from .utils import geocode_address
from django.conf import settings


api_key = settings.LOCATIONIQ_API_KEY

@receiver(post_save, sender=Home)
def geocode_home(sender, instance, created, **kwargs):
    if created:
        instance.longitude, instance.latitude = geocode_address(instance.address_line_one, instance.state, instance.city, api_key)
        instance.save()


@receiver(post_save, sender=Service_Provider)
def geocode_service_provider(sender, instance, created, **kwargs):
    if created:
        instance.longitude, instance.latitude = geocode_address(instance.address_line_one, instance.state, instance.city, api_key)
        instance.save()


