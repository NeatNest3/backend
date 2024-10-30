from rest_framework import serializers 
from .models import *



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('__all__')


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ('__all__')


class SpecialtySerializer(serializers.ModelSerializer):

    class Meta:
        model = Specialty
        fields = ('__all__')


class Service_ProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service_Provider
        fields = ('__all__')


class HomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Home
        fields = ('__all__')


class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = ('__all__')


class AvailabilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Availability
        fields = ('__all__')


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ('__all__')


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = ('__all__')


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('__all__')


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('__all__')


class Payment_MethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment_Method
        fields = ('__all__')


class Bank_AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bank_Account
        fields = ('__all__')