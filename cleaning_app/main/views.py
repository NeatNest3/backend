import boto3
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
from firebase_admin import auth as firebase_auth, firestore
from .models import DeviceToken
from cleaning_app.cleaning_app.local_settings import messaging
from .firebase_messaging import *
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .utils import get_eligible_providers, get_nearby_providers

def homepage(request):
    return render(request, 'main/index.html')  # Use 'appname/filename.html'

#---------------------------------------------------------------------------------------------------------
# Auth View

class VerifyFirebaseToken(APIView):
    permission_classes = [IsAuthenticated]  # You can set this to allow public access if not using session authentication

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
            
            # Get the user associated with the Firebase UID (you can store it as `firebase_uid` field in your User model)
            user = get_user_model().objects.filter(firebase_uid=firebase_uid).first()
            if user:
                # Optionally, you could set the session or return the user data
                return Response({
                    'message': 'User authenticated successfully',
                    'user': {'id': user.id, 'username': user.username},
                })
            else:
                return Response({'error': 'User does not exist in Django.'}, status=status.HTTP_404_NOT_FOUND)
        
        except firebase_auth.AuthError as e:
            return Response({'error': f'Invalid Firebase token: {str(e)}'}, status=status.HTTP_401_UNAUTHORIZED)


#---------------------------------------------------------------------------------------------------------
# User Views

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class UserDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

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

def upload_image(request):
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
        
        if response.status_code != 200:
            raise Exception("Failed to upload to S3")
        
        return JsonResponse({'message': 'File uploaded successfully'}, status=200)
