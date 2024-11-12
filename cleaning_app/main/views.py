
from .models import *
from .serializers import *
from django.http import HttpResponse
from rest_framework import generics
from .serializers import *
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Image
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .firebase import db
from firebase_admin import firestore
from .models import DeviceToken
from .firebase import messaging

def homepage(request):
    return render(request, 'main/index.html')  # Use 'appname/filename.html'

#---------------------------------------------------------------------------------------------------------
# User Views
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

#---------------------------------------------------------------------------------------------------------
# Customer Views
class CustomerList(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

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

#---------------------------------------------------------------------------------------------------------
# Specialty Views
class SpecialtyList(generics.ListCreateAPIView):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer

class SpecialtyDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer

#---------------------------------------------------------------------------------------------------------
# Service Provider Views

class Service_ProviderList(generics.ListCreateAPIView):
    queryset = Service_Provider.objects.all()
    serializer_class = Service_ProviderSerializer

    def perform_create(self, serializer):
        # Here, 'user' should be included in the validated data sent from the frontend.
        # Ensure that the user ID is provided in the request data.
        user = self.request.data.get('user')
        if user:
            serializer.save(user_id=user)  # This sets the user_id on the Customer instance being created.
        else:
            raise serializers.ValidationError({"user": "User ID is required to create a customer."})

class Service_ProviderDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service_Provider.objects.all()
    serializer_class = Service_ProviderSerializer


class JobHistoryList(generics.ListAPIView):
    serializer_class = JobSerializer

    def get_queryset(self):
        service_provider_id = self.kwargs['pk']
        # Filter jobs by the cleaner id and order by date in descending order
        return Job.objects.filter(service_provider=service_provider_id).order_by('-date')

#---------------------------------------------------------------------------------------------------------
# Home Views

class HomeList(generics.ListCreateAPIView):
    queryset = Home.objects.all()
    serializer_class = HomeSerializer

class HomeDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Home.objects.all()
    serializer_class = HomeSerializer

class HomeHistoryList(generics.ListAPIView):
    serializer_class = JobSerializer

    def get_queryset(self):
        home_id = self.kwargs['pk']
        return Job.objects.filter(home=home_id).order_by('-date')

#---------------------------------------------------------------------------------------------------------

class RoomList(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class RoomDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

#---------------------------------------------------------------------------------------------------------

# Job Views
class JobList(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

class JobDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

#---------------------------------------------------------------------------------------------------------
# Availability Views
class AvailabilityList(generics.ListCreateAPIView):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer

class AvailabilityDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer

#---------------------------------------------------------------------------------------------------------
# Payment Views
class PaymentList(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class PaymentDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

#---------------------------------------------------------------------------------------------------------
# Service Views
class ServiceList(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ServiceDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

#---------------------------------------------------------------------------------------------------------
# Task Views
class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

#---------------------------------------------------------------------------------------------------------
# Review Views
class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

#---------------------------------------------------------------------------------------------------------
# Payment Method Views
class Payment_MethodList(generics.ListCreateAPIView):
    queryset = Payment_Method.objects.all()
    serializer_class = Payment_MethodSerializer

class Payment_MethodDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment_Method.objects.all()
    serializer_class = Payment_MethodSerializer

#---------------------------------------------------------------------------------------------------------
# Bank Account Views
class Bank_AccountList(generics.ListCreateAPIView):
    queryset = Bank_Account.objects.all()
    serializer_class = Bank_AccountSerializer

class Bank_AccountDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bank_Account.objects.all()
    serializer_class = Bank_AccountSerializer

#---------------------------------------------------------------------------------------------------------
# Function to save a message in Firestore when a user sends one.
def send_message(request, sender_id, receiver_id):
    sender = get_object_or_404(User, id=sender_id)
    receiver = get_object_or_404(User, id=receiver_id)
    text = request.POST.get("text")
    
    # Firestore chat ID generation based on user IDs
    chat_id = f"{min(sender_id, receiver_id)}_{max(sender_id, receiver_id)}"
    
    # Save the message in Firestore
    message_data = {
        "senderId": sender_id,
        "receiverId": receiver_id,
        "text": text,
        "timestamp": firestore.SERVER_TIMESTAMP,
        "seen": False
    }
    
    db.collection("chats").document(chat_id).collection("messages").add(message_data)
    
    # Update the last message at the chat level for easy querying
    db.collection("chats").document(chat_id).set({
        "lastMessage": text,
        "timestamp": firestore.SERVER_TIMESTAMP
    }, merge=True)

    # Send a notification to the receiver
    send_fcm_notification(receiver_id, text)

    return JsonResponse({"status": "Message sent"})

#---------------------------------------------------------------------------------------------------------
# Function to send  notifications using FCM (Firebase Cloud Messaging)
def send_fcm_notification(receiver_id, message_text):
    try:
        # Retrieve the FCM token for the receiver
        token = DeviceToken.objects.get(user_id=receiver_id).token
        
        # Create a notification payload
        message = messaging.Message(
            notification=messaging.Notification(
                title="New Message",
                body=message_text
            ),
            token=token,
        )
        
        # Send the notification
        response = messaging.send(message)
        print(f"Notification sent successfully: {response}")
    except DeviceToken.DoesNotExist:
        print("No device token found for user.")
    except Exception as e:
        print(f"Error sending notification: {e}")
#------------------------------------------------------------------------------------------------------------
# Function when a user reads a message it marks it as seen in Firestore.
def mark_message_as_seen(request, chat_id, message_id):
    db.collection("chats").document(chat_id).collection("messages").document(message_id).update({
        "seen": True
    })
    return JsonResponse({"status": "Message marked as seen"})\
    






# @csrf_exempt  # For simplicity, you may want to implement CSRF protection properly
# def upload_image(request):
#     if request.method == 'POST':
#         file = request.FILES['image']
#         # Get the Firebase storage bucket
#         bucket = storage.bucket()
#         # Create a blob for the uploaded file
#         blob = bucket.blob(f'images/{file.name}')
#         blob.upload_from_file(file, content_type=file.content_type)

#         # Make the file publicly accessible
#         blob.make_public()

#         # Store the image URL in the database (optional)
#         image = Image.objects.create(image_url=blob.public_url)

#         return HttpResponse("Image Successfully Uploaded!")

#     return render(request, 'main/upload_image.html')
