from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from firebase_admin import auth as firebase_auth
from .models import Home, Service_Provider, User
from .utils import geocode_address
from django.conf import settings
from .utils import verify_firebase_uid


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


@receiver(user_logged_in)
def update_firebase_uid(sender, request, user, **kwargs):
    """
    Signal handler to update firebase_uid when the user logs in via Firebase.
    """
    if not user.firebase_uid:  # Only update if firebase_uid is not set yet
        firebase_uid = request.META.get('HTTP_X_FIREBASE_UID')  # Assuming UID is passed in headers
        
        if firebase_uid and verify_firebase_uid(firebase_uid):
            user.firebase_uid = firebase_uid
            user.save()  # Save the updated firebase_uid