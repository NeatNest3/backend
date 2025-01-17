from rest_framework import serializers 
from .models import *
from django.contrib.auth import get_user_model



class UserSerializer(serializers.ModelSerializer):

    User = get_user_model()

    class Meta:
        model = User
        fields = [
             'id','first_name', 'last_name', 'password', 'phone', 'email', 'date_of_birth', 
             'allergies', 'role'
         ]


    def create(self, validated_data):
        # Create the user using the validated data
        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            username=validated_data['email'],
            email=validated_data['email'],
            date_of_birth=validated_data['date_of_birth'],
            phone=validated_data['phone']
        )

        # Assign optional fields with default values if not present
        user.role = validated_data.get('role', 'customer')  # Default to 'customer'
        user.allergies = validated_data.get('allergies', [])  # Default to empty list
        
        user.save()
        
        return user

    def validate_allergies(self, value):
        # Custom validation for allergies
        valid_allergies = User.ALLERGY_CHOICES
        for allergy in value:
            if allergy not in dict(valid_allergies).keys():
                raise serializers.ValidationError(f"{allergy} is not a valid allergy choice.")
        return value
    
class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ('__all__')



class SpecialtySerializer(serializers.ModelSerializer):

    class Meta:
        model = Specialty
        fields = ('__all__')


class Service_ProviderSerializer(serializers.ModelSerializer):
    specialties = serializers.PrimaryKeyRelatedField(
        queryset = Specialty.objects.all(), many=True
    )
    class Meta:
        model = Service_Provider
        fields = ('__all__')

    def create(self, validated_data):
        # Retrieve the user and specialties data from validated_data
        user = validated_data.get('user')
        specialties = validated_data.pop('specialties', [])

        # Check if the user is provided
        if not user:
            raise serializers.ValidationError("User ID is required to create a service provider.")

        # Create the Service_Provider instance without specialties
        service_provider = Service_Provider.objects.create(**validated_data)

        # Set the specialties using .set() method to establish the many-to-many relationship
        service_provider.specialties.set(specialties)
        
        return service_provider


class Service_Provider_DistanceSerializer(serializers.ModelSerializer):
    distance = serializers.FloatField()

    class Meta:
        model = Service_Provider
        fields = ['id', 'user', 'flexible_rate', 'pet_friendly', 'rating', 'background_check', 'bio_work_history', 'specialties', 'distance']

class HomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Home
        fields = ('__all__')


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ('__all__')


class TaskSerializer(serializers.ModelSerializer):

    job = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'

class JobSerializer(serializers.ModelSerializer):

    rooms = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), many=True)
    tasks = TaskSerializer(many=True)

    class Meta:
        model = Job
        fields = [
             'customer', 'service_provider', 'home', 'status', 'date', 'start_time', 
             'end_time', 'rooms', 'tasks'
         ]
    

    def create(self, validated_data):
        # Extract rooms and tasks from validated data
        rooms_data = validated_data.pop('rooms')
        tasks_data = validated_data.pop('tasks')

        # Create the Job instance
        job = Job.objects.create(**validated_data)

        # Assign the rooms
        job.rooms.set(rooms_data)

        # Create related tasks
        for task_data in tasks_data:
            Task.objects.create(job=job, **task_data)

        return job

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('__all__')

