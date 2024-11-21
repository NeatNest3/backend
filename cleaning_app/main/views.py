import boto3
import logging
from .models import *
from .serializers import *
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Image
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
# from .firebase import db
from firebase_admin import auth, credentials as firebase_auth, firestore
from .models import DeviceToken
from cleaning_app.cleaning_app.local_settings import messaging
from .firebase_messaging import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from .utils import get_eligible_providers, get_nearby_providers
from botocore.exceptions import NoCredentialsError
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
import firebase_admin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


logger = logging.getLogger(__name__)

def homepage(request):
    return render(request, 'main/index.html')  # Use 'appname/filename.html'

if not firebase_admin._apps:
    cred = firebase_admin.credentials.Certificate(r'C:\Users\dilll\Backend\backend\cleaning_app\credentials\neatnest-308c4-firebase-adminsdk-8bt91-be2f5d5a1b.json')  # Path to your Firebase service account key
    firebase_admin.initialize_app(cred)

#---------------------------------------------------------------------------------------------------------
# Auth View

class VerifyFirebaseToken(APIView):

    permission_classes =[AllowAny]


    def post(self, request):
        # Retrieve the Firebase ID token from the Authorization header
        token = request.headers.get('Authorization')
        
        if token is None or not token.startswith('Bearer '):
            return Response({'error': 'Authorization token is missing or invalid.'}, status=status.HTTP_400_BAD_REQUEST)
        
        id_token = token.split(' ')[1]  # Get the actual token without "Bearer"
        
        try:
            # Verify the Firebase ID token
            decoded_token = firebase_auth.verify_id_token(id_token)
            firebase_uid = decoded_token['uid']
            
            # Get the user associated with the Firebase UID
            user = get_user_model().objects.filter(firebase_uid=firebase_uid).first()
            if user:
                return Response({
                    'message': 'User authenticated successfully',
                    'user': {'id': user.id, 'username': user.username, 'firebase_uid': user.firebase_uid},
                })
            else:
                return Response({'error': 'User does not exist in Django.'}, status=status.HTTP_404_NOT_FOUND)
        
        except firebase_auth.AuthError as e:
            return Response({'error': f'Invalid Firebase token: {str(e)}'}, status=status.HTTP_401_UNAUTHORIZED)


#---------------------------------------------------------------------------------------------------------
# User Views

class CreateUserFromFirebase(APIView):
    
    permission_classes =[AllowAny]

    def post(self, request):
        # Log incoming headers and metadata for debugging
        try:
            
            # Log the raw Authorization header from META for extra debugging
            raw_auth_header = request.META.get('HTTP_AUTHORIZATION', None)
            logger.debug("Raw Authorization Header from META: %s", raw_auth_header)
            message = "1. No header returned" if raw_auth_header is None else "SUCCESS"
            logger.debug(message)
            
            # Step 1: Extract the Firebase ID token from the Authorization header
            auth_header = request.headers.get('Authorization')
            logger.debug("Extracted Authorization Header: %s", auth_header)
            message = "2. No header returned" if auth_header is None else "SUCCESS"
            logger.debug(message)        

            if not auth_header or not auth_header.startswith('Bearer '):
                logger.debug("Authorization header missing or malformed")
                return Response({"error": "Authorization header missing or malformed"}, status=status.HTTP_400_BAD_REQUEST)

            id_token = auth_header.split('Bearer ')[1]
            logger.debug(f"Extracted ID Token: {id_token}")

            # Step 2: Verify the ID token with Firebase Admin SDK
            decoded_token = auth.verify_id_token(id_token)
            firebase_uid = decoded_token['uid']  # This is the Firebase UID of the user
            logger.debug(f"Decoded Firebase UID: {firebase_uid}")

        

            # Step 3: Check if the user already exists by Firebase UID
            if User.objects.filter(firebase_uid=firebase_uid).exists():
                logger.debug(f"User with Firebase UID {firebase_uid} already exists")
                return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

            # Step 4: Create a new user in Django based on the data in the request
            user_data = request.data
            logger.debug(f"User data received: {user_data}")
            
            user = User.objects.create_user(
                username=user_data['email'],  # Firebase UID is used as the username
                first_name=user_data.get('first_name', ''),
                last_name=user_data.get('last_name', ''),
                preferred_name=user_data.get('preferred_name', ''),
                phone=user_data['phone'],
                email=user_data['email'],
                password=user_data['password'],  # If you want, you can hash the password securely
                allergies=user_data.get('allergies', []),  # Default to empty list if not provided
                date_of_birth=user_data['date_of_birth'],
                role=user_data.get('role', 'customer'),  # Default to 'customer' if role is not provided
                firebase_uid=firebase_uid  # Store the Firebase UID to link this user with Firebase
            )

            logger.debug(f"User taken in: {user}")
            # Step 5: Serialize the user data to return in the response
            user_serializer = UserSerializer(user)
            logger.debug(f"User created successfully: {user_serializer.data}")

            return Response(user_serializer.data, status=status.HTTP_201_CREATED)

        except KeyError as e:
            # If any required field is missing from the request body
            logger.error(f"Missing field in request: {str(e)}")
            return Response({"error": f"Missing field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        except auth.InvalidIdTokenError as e:
            # If the Firebase ID token is invalid
            logger.error(f"Invalid Firebase ID token: {str(e)}")
            return Response({"error": "Invalid Firebase ID token"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Catch all other exceptions
            logger.error(f"An unexpected error occurred: {str(e)}")
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class UserDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

#---------------------------------------------------------------------------------------------------------
# Customer Views

class CustomerList(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Here, 'user' should be included in the validated data sent from the frontend.
        # Ensure that the user ID is provided in the request data.
        user = self.request.data.get('user')
        if user:
            serializer.save(user_id=user)  # This sets the user_id on the Customer instance being created.
        else:
            raise serializers.ValidationError({"user": "User ID is required to create a customer."})

class CustomerDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

#---------------------------------------------------------------------------------------------------------
# Specialty Views

class SpecialtyList(generics.ListCreateAPIView):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
    permission_classes = [IsAuthenticated]

class SpecialtyDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
    permission_classes = [IsAuthenticated]

#---------------------------------------------------------------------------------------------------------
# Service Provider Views

class Service_ProviderList(generics.ListCreateAPIView):
    queryset = Service_Provider.objects.all()
    serializer_class = Service_ProviderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Here, 'user' should be included in the validated data sent from the frontend.
        # Ensure that the user ID is provided in the request data.
        user = self.request.data.get('user')
        if user:
            serializer.save(user_id=user)  # This sets the user_id on the Service Provider instance being created.
        else:
            raise serializers.ValidationError({"user": "User ID is required to create a customer."})

class Service_ProviderDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service_Provider.objects.all()
    serializer_class = Service_ProviderSerializer
    permission_classes = [IsAuthenticated]


class JobHistoryList(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        service_provider_id = self.kwargs['pk']
        # Filter jobs by the cleaner id and order by date in descending order
        return Job.objects.filter(service_provider=service_provider_id).order_by('-date')

#---------------------------------------------------------------------------------------------------------
# Home Views

class HomeList(generics.ListCreateAPIView):
    queryset = Home.objects.all()
    serializer_class = HomeSerializer
    permission_classes = [IsAuthenticated]

class HomeDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Home.objects.all()
    serializer_class = HomeSerializer
    permission_classes = [IsAuthenticated]

class HomeHistoryList(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        home_id = self.kwargs['pk']
        return Job.objects.filter(home=home_id).order_by('-date')

#---------------------------------------------------------------------------------------------------------
# Room Views

class RoomList(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

class RoomDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

#---------------------------------------------------------------------------------------------------------
# Job Views

class JobList(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

class JobDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

#---------------------------------------------------------------------------------------------------------
# Availability Views

class AvailabilityList(generics.ListCreateAPIView):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    permission_classes = [IsAuthenticated]

class AvailabilityDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    permission_classes = [IsAuthenticated]

#---------------------------------------------------------------------------------------------------------
# Payment Views

class PaymentList(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

class PaymentDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

#---------------------------------------------------------------------------------------------------------
# Service Views

class ServiceList(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

class ServiceDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

#---------------------------------------------------------------------------------------------------------
# Task Views
class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

class TaskDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

#---------------------------------------------------------------------------------------------------------
# Review Views

class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

#---------------------------------------------------------------------------------------------------------
# Payment Method Views
class Payment_MethodList(generics.ListCreateAPIView):
    queryset = Payment_Method.objects.all()
    serializer_class = Payment_MethodSerializer
    permission_classes = [IsAuthenticated]

class Payment_MethodDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment_Method.objects.all()
    serializer_class = Payment_MethodSerializer
    permission_classes = [IsAuthenticated]

#---------------------------------------------------------------------------------------------------------
# Bank Account Views

class Bank_AccountList(generics.ListCreateAPIView):
    queryset = Bank_Account.objects.all()
    serializer_class = Bank_AccountSerializer
    permission_classes = [IsAuthenticated]

class Bank_AccountDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bank_Account.objects.all()
    serializer_class = Bank_AccountSerializer
    permission_classes = [IsAuthenticated]

#---------------------------------------------------------------------------------------------------------

class NearbyProvidersView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, home_id):
        # Retrieve the specific Home instance based on home_id
        customer_home = Home.objects.get(id=home_id)
        # Pass the Home instance to get eligible providers
        eligible_providers = get_eligible_providers(customer_home)
        api_key = settings.LOCATIONIQ_API_KEY
        # Pass only the customer_home ID and eligible providers to get_nearby_providers
        nearby_providers = get_nearby_providers(customer_home.customer_id, customer_home.id, eligible_providers, api_key)
        return Response(nearby_providers)
    
#---------------------------------------------------------------------------------------------------------

#@csrf_exempt  # For simplicity, you may want to implement CSRF protection properly
#def upload_image(request):
   #if request.method == 'POST':
        #file = request.FILES['image']
        # Get the Firebase storage bucket
   #     bucket = storage.bucket()
        # Create a blob for the uploaded file
    #    blob = bucket.blob(f'images/{file.name}')
     #   blob.upload_from_file(file, content_type=file.content_type)

        # Make the file publicly accessible
      #  blob.make_public()

        # Store the image URL in the database (optional)
       # image = Image.objects.create(image_url=blob.public_url)

       # return HttpResponse("Image Successfully Uploaded!")
#    return render(request, 'main/upload_image.html')

import requests
import base64

LAMBDA_URL = " https://cmfjyilffk.execute-api.us-west-2.amazonaws.com/default/s3LambdaFunction"

@csrf_exempt
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_image(request):
    if request.method == 'POST' and request.FILES['image']:
        image_file = request.FILES['image']
        
        # Read the image and encode it in base64
        image_data = image_file.read()
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        # Send the image to AWS Lambda for upload to S3
        response = requests.post(
            LAMBDA_URL,
            json={
                'image_base64': image_base64,
                'file_name': image_file.name,
                'content_type': image_file.content_type,
            }
        )

        if response.status_code == 200:
            # Get the URL of the uploaded image from the Lambda response
            response_data = response.json()
            s3_url = response_data.get('url')

            # Save the image metadata in your Django model
            Image.objects.create(
                file_name=image_file.name,
                s3_url=s3_url
            )

            # Return success response
            return JsonResponse({'message': 'Image uploaded successfully', 'url': s3_url}, status=200)
        else:
            return JsonResponse({'error': 'Failed to upload image to S3'}, status=500)

    return render(request, 'upload_image.html')
    
    if request.method == 'POST':
        file = request.FILES.get('file')
        if not file:
            return JsonResponse({'error': 'No file provided'}, status=400)

        # Set up data for the Lambda function
        url = 'https://yddlnybva9.execute-api.us-west-2.amazonaws.com/default/s3LambdaFunction'
        files = {'file': file.read()}
        headers = {'Content-Type': 'application/octet-stream'}

        # Make the request
        response = requests.post(url, files=files, headers=headers)
        
#         return HttpResponse("Image Successfully Uploaded!")

        return JsonResponse({'message': 'File uploaded successfully'}, status=200)
