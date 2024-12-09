import boto3
import logging
from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Image
from django.contrib.auth.models import User
from .utils import get_eligible_providers, get_nearby_providers
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404





logger = logging.getLogger(__name__)

def homepage(request):
    return render(request, 'main/index.html')  # Use 'appname/filename.html'
#---------------------------------------------------------------------------------------------------------
# User Views

User = get_user_model()

class UserList(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    
    def create(self, request, *args, **kwargs):
        # First, we handle the creation of the User
        user_serializer = self.get_serializer(data=request.data)
        if user_serializer.is_valid():
            # Save the user
            user = user_serializer.save()

            # If the role is 'customer', create a related Customer instance
            if user.role == 'customer':
                # Create a customer linked to the user
                customer = Customer.objects.create(user=user)
                customer.save()

            return Response(user_serializer.data, status=status.HTTP_201_CREATED)

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

#---------------------------------------------------------------------------------------------------------
# Customer Views

class CustomerList(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Here, 'user' should be included in the validated data sent from the frontend.
        # Ensure that the user ID is provided in the request data.
        user = self.request.data.get('user')
        if user:
            serializer.save(user_id=user)  # This sets the user_id on the Customer instance being created.
        else:
            raise serializers.ValidationError({"user": "User ID is required to create a customer."})

#---------------------------------------------------------------------------------------------------------
# Specialty Views

class SpecialtyList(viewsets.ModelViewSet):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
    # permission_classes = [IsAuthenticated]

#---------------------------------------------------------------------------------------------------------
# Service Provider Views

class Service_ProviderList(viewsets.ModelViewSet):
    queryset = Service_Provider.objects.all()
    serializer_class = Service_ProviderSerializer
    permission_classes = []

    def perform_create(self, serializer):
        # Here, 'user' should be included in the validated data sent from the frontend.
        # Ensure that the user ID is provided in the request data.
        user = self.request.data.get('user')
        if user:
            serializer.save(user_id=user)  # This sets the user_id on the Service Provider instance being created.
        else:
            raise serializers.ValidationError({"user": "User ID is required to create a customer."})

class JobHistoryList(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = []

    def get_queryset(self):
        service_provider_id = self.kwargs['pk']
        # Filter jobs by the cleaner id and order by date in descending order
        return Job.objects.filter(service_provider=service_provider_id).order_by('-date')

#---------------------------------------------------------------------------------------------------------
# Home Views

class HomeList(viewsets.ModelViewSet):
    queryset = Home.objects.all()
    serializer_class = HomeSerializer
    permission_classes = []

    def get_queryset(self):
        customer = self.request.query_params.get('customer')
        if customer:
            return self.queryset.filter(customer=customer)
        return self.queryset

class HomeHistoryList(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = []


    def get_queryset(self):
        home_id = self.kwargs['pk']
        return Job.objects.filter(home=home_id).order_by('-date')

#---------------------------------------------------------------------------------------------------------
# Room Views

class RoomList(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = []

#---------------------------------------------------------------------------------------------------------
# Job Views

class JobList(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = []

#---------------------------------------------------------------------------------------------------------
# Task Views
class TaskList(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # permission_classes = [IsAuthenticated]

#---------------------------------------------------------------------------------------------------------
# Review Views

class ReviewList(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]

#---------------------------------------------------------------------------------------------------------

class NearbyProvidersView(APIView):
    # permission_classes = [IsAuthenticated]
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



