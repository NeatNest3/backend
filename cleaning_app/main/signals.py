from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Home, Service_Provider
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


