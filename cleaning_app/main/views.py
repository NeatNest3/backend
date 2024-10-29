from rest_framework import generics
from .models import *
from .serializers import *

from rest_framework import generics
from .models import User, Customer, Specialty, Service_Provider, Home, Job, Availability, Payment, Service, Task, Review, Payment_Method, Bank_Account
from .serializers import (
    UserSerializer, CustomerSerializer, SpecialtySerializer, ServiceProviderSerializer,
    HomeSerializer, JobSerializer, AvailabilitySerializer, PaymentSerializer,
    ServiceSerializer, TaskSerializer, ReviewSerializer, PaymentMethodSerializer,
    BankAccountSerializer
)

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
class ServiceProviderList(generics.ListCreateAPIView):
    queryset = Service_Provider.objects.all()
    serializer_class = ServiceProviderSerializer

class ServiceProviderDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service_Provider.objects.all()
    serializer_class = ServiceProviderSerializer

#---------------------------------------------------------------------------------------------------------
# Home Views
class HomeList(generics.ListCreateAPIView):
    queryset = Home.objects.all()
    serializer_class = HomeSerializer

class HomeDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Home.objects.all()
    serializer_class = HomeSerializer

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
class PaymentMethodList(generics.ListCreateAPIView):
    queryset = Payment_Method.objects.all()
    serializer_class = PaymentMethodSerializer

class PaymentMethodDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment_Method.objects.all()
    serializer_class = PaymentMethodSerializer

#---------------------------------------------------------------------------------------------------------
# Bank Account Views
class BankAccountList(generics.ListCreateAPIView):
    queryset = Bank_Account.objects.all()
    serializer_class = BankAccountSerializer

class BankAccountDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bank_Account.objects.all()
    serializer_class = BankAccountSerializer
