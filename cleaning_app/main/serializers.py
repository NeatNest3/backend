from rest_framework import serializers 
from .models import *



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('__all__')


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'

    def create(self, validated_data):

        user = validated_data.get('user')
        if not user:
            raise serializers.ValidationError("User ID is required to create a customer.")
        
        return super().create(validated_data)

class SpecialtySerializer(serializers.ModelSerializer):

    class Meta:
        model = Specialty
        fields = ('__all__')


class Service_ProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service_Provider
        fields = ('__all__')

    def create(self, validated_data):
        user = validated_data.get('user')
        if not user:
            raise serializers.ValidationError("User ID is required to create a cleaner.")
        return Service_Provider.objects.create(**validated_data)


class HomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Home
        fields = ('__all__')


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ('__all__')


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('__all__')


class JobSerializer(serializers.ModelSerializer):

    rooms = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), many=True)
    tasks = TaskSerializer(many=True)

    class Meta:
        model = Job
        fields = [
            'customer', 'service_provider', 'home', 'status', 'date', 'start_time', 
            'end_time', 'total_cost', 'payment_made', 'special_requests', 'rooms', 'tasks'
        ]

    def create(self, validated_data):
        rooms_data = validated_data.pop('rooms')
        tasks_data = validated_data.pop('tasks')
        job = Job.objects.create(**validated_data)

        job.rooms.set(rooms_data)

        for task_data in tasks_data:
            Task.objects.create(job=job, **task_data)

        return job



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