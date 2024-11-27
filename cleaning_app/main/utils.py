import requests
from django.conf import settings
from django.db.models import Q
from .models import Service_Provider, Home, Customer, User
from .serializers import Service_Provider_DistanceSerializer
from firebase_admin import auth as firebase_auth
from rest_framework import authentication, exceptions
import logging
import jwt
from jwt import PyJWKClient
from datetime import datetime
from ..cleaning_app.settings import FIREBASE_PROJECT_ID
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)


#---------------------------------------------------------------------------------------------------------

FIREBASE_PUBLIC_KEYS_URL = "https://www.googleapis.com/service_accounts/v1/metadata/x509/securetoken@system.gserviceaccount.com"


class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Extract the Authorization header
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return None  # No token provided, let other authentication methods handle it
        
        try:
            # Split the header to get the token
            token = auth_header.split(" ")[1]
            
            # Verify the Firebase ID token manually
            decoded_token = verify_firebase_id_token(token)
            firebase_uid = decoded_token['uid']
            
            # Try to retrieve the user based on the Firebase UID
            user = self.get_or_create_user(firebase_uid)

            return (user, None)  # Return the authenticated user and None for the auth token

        except Exception as e:
            # Raise an authentication error if the token is invalid or any other error occurs
            raise exceptions.AuthenticationFailed(f"Token authentication failed: {str(e)}")

    def get_or_create_user(self, firebase_uid):
        """
        Retrieve an existing user or create a new one based on the Firebase UID.
        This assumes that you've extended the Django User model or added a custom field for the Firebase UID.
        """
        try:
            # Check if a user already exists with the Firebase UID
            user = get_user_model().objects.get(firebase_uid=firebase_uid)
        except get_user_model().DoesNotExist:
            # If no user exists, create a new one
            user = get_user_model().objects.create_user(
                username=firebase_uid, 
                email=f"{firebase_uid}@firebase.com",  # Create a default email, adjust as needed
                firebase_uid=firebase_uid
            )
            user.save()

        return user

#---------------------------------------------------------------------------------------------------------

def verify_firebase_id_token(id_token):
    """
    Verify Firebase ID Token using Firebase's public keys.
    :param id_token: The Firebase ID token to verify
    :return: The decoded payload if the token is valid
    :raises: jwt.ExpiredSignatureError or jwt.PyJWTError on failure
    """
    try:
        # Get Firebase public keys
        response = requests.get(FIREBASE_PUBLIC_KEYS_URL)
        response.raise_for_status()
        keys = response.json()

        # Decode the token header to get the kid (key ID)
        unverified_header = jwt.get_unverified_header(id_token)
        if unverified_header is None or 'kid' not in unverified_header:
            raise ValueError('Invalid token: Missing kid in header')

        kid = unverified_header['kid']

        # Find the corresponding public key for the kid
        if kid not in keys:
            raise ValueError('Invalid token: Invalid kid')

        # Get the public key
        public_key = keys[kid]

        # Decode and verify the token
        decoded_token = jwt.decode(
            id_token,
            public_key,
            algorithms=["RS256"],
            audience=FIREBASE_PROJECT_ID,  
            issuer=f"https://securetoken.google.com/{FIREBASE_PROJECT_ID}",  # Firebase token issuer
        )

        # Check if the token is expired
        if decoded_token['exp'] < datetime.now().timestamp():
            raise jwt.ExpiredSignatureError('Token has expired')

        return decoded_token

    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.PyJWTError as e:
        raise ValueError(f"Invalid token: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error verifying token: {str(e)}")

#---------------------------------------------------------------------------------------------------------

def geocode_address(address, state, city, api_key=settings.LOCATIONIQ_API_KEY):
    """Retrieve coordinates for a given address using LocationIQ's forward geocoding API."""

    url = 'https://us1.locationiq.com/v1/search'
    params = {
        "key": api_key,
        "q": f"{address} {state}, {city}",
        "format": "json",
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    location = response.json()[0]
    return float(location["lon"]), float(location["lat"])

#---------------------------------------------------------------------------------------------------------

def get_eligible_providers(home, min_rating=3.0):
    """Filter service providers by rating and exclude providers with allergies to the pets in the home."""

    logger.debug("Entering get_eligible_providers") 

    pets_list = list(home.pets.keys()) if isinstance(home.pets, dict) else home.pets

    logger.debug(f"Pets List for Filtering: {pets_list}")

    providers = Service_Provider.objects.filter(
        rating__gte=min_rating
    )

    # ignore_allergies = ["none", "other", "pollen", "mold", "dust", "fragrance", 'ammonia', "bleach", "bleach"]

    # providers = providers.exclude(
    #     Q(user__allergies__overlap=pets_list) &
    #     ~Q(user__allergies__contained=ignore_allergies)
    # )

    logger.debug(print("Eligible Providers:", providers))  # Debugging line
    return providers

#---------------------------------------------------------------------------------------------------------

def get_nearby_providers(customer_id, home_id, eligible_providers, api_key=settings.LOCATIONIQ_API_KEY, max_results=10):
    """Retrieve nearby service providers based on proximity to the customer's home, using LocationIQ's Distance Matrix API."""

    # Retrieve customer home and format coordinates
    customer_home = Home.objects.get(id=home_id)
    customer_coords = f"{customer_home.longitude},{customer_home.latitude}"
    logger.debug(f"Customer Coordinates: {customer_coords}")

    # Collect all coordinates in the format for the API
    provider_coords = [
        f"{provider.longitude},{provider.latitude}" for provider in eligible_providers if provider.longitude and provider.latitude
    ]
    all_coords = f"{customer_coords};" + ";".join(provider_coords)
    logger.debug(f"All Coordinates for Matrix API: {all_coords}")

    # Set sources and destinations as indexes (0 is customer, 1+ are providers)
    sources_indices = ";".join(str(i+1) for i in range(len(eligible_providers)))  # Providers as sources
    destination_index = "0"  # Customer as the destination
    logger.debug(f"Sources (Providers): {sources_indices}")
    logger.debug(f"Destination (Customer): {destination_index}")

    # Define the URL and parameters
    url = f"https://us1.locationiq.com/v1/matrix/driving/{all_coords}"
    params = {
        'key': api_key,
        'sources': sources_indices,
        'destinations': destination_index,
        'annotations': 'distance'  # Use 'distance,duration' if both are needed
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        response_data = response.json()

        # Debugging the entire response
        logger.debug("Matrix API Response Data: %s", response_data)

        # Get distances data and check if it is valid
        distances_data = response_data.get("distances")
        if not distances_data or not isinstance(distances_data, list):
            logger.error("No valid distances returned from API.")
            return []

        distances = []
        if 'distances' in response_data and response_data['distances']:
            for row in response_data['distances']:
                distances.append(row[0])  # First item should be the distance to the destination (customer)


    except (requests.RequestException, IndexError, KeyError) as e:
        logger.error("Error fetching distances from LocationIQ API: %s", e)
        return []

    # Combine distances with provider info and sort by proximity
    proximity_info = [
        {"provider": provider, "distance": distances[i]}
        for i, provider in enumerate(eligible_providers) if i < len(distances)
    ]
    proximity_info = sorted(proximity_info, key=lambda x: x["distance"])[:max_results]
    logger.debug("Proximity Info (Sorted): %s", proximity_info)

    # Serialize the data with the custom distance included
    serialized_data = Service_Provider_DistanceSerializer(
        [{"id": item["provider"].id, "user": item["provider"].user, "flexible_rate": item["provider"].flexible_rate,
          "pet_friendly": item["provider"].pet_friendly, "rating": item["provider"].rating,
          "background_check": item["provider"].background_check, "bio_work_history": item["provider"].bio_work_history,
          "specialties": item["provider"].specialties, "distance": item["distance"]} 
         for item in proximity_info], many=True
    ).data

    return serialized_data

#---------------------------------------------------------------------------------------------------------



# def get_customer_home(customer_id, home_id):
#     """Retrieve the specific Home instance ID associated with a Customer, based on provided IDs."""
#     try:
#         # Ensure customer_id corresponds to a valid Customer instance
#         customer = Customer.objects.get(id=customer_id)
#         # Retrieve the specific Home instance ID associated with this Customer
#         customer_home = Home.objects.get(id=home_id, customer=customer)
#         return customer_home.id  # Only return the ID
#     except (Home.DoesNotExist, Customer.DoesNotExist):
#         # Return None if the Home or Customer does not exist
#         return None
