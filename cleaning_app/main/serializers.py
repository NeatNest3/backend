from rest_framework import serializers 
from .models import *



class UserSerializer(serializers.ModelSerializer):
    # Required fields from the model
    phone = serializers.CharField(required=True, max_length=25)
    date_of_birth = serializers.DateField(required=True)
    allergies = serializers.ListField(child=serializers.CharField(), required=False)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, default='customer', required=False)
    preferred_name = serializers.CharField(max_length=25, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'phone', 'date_of_birth', 
                  'role', 'allergies', 'preferred_name')


    def create(self, validated_data):

        # Create the user using the validated data
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            date_of_birth=validated_data['date_of_birth'],
        )
        
        user.phone = validated_data['phone']
        user.role = validated_data['role',  'customer']
        user.allergies = validated_data['allergies', []]
        user.preferred_name = validated_data['preffered_name', '']
        
        user.save()
        
        return user

    def validate_allergies(self, value):
        #Custom validation for allergies
        
        valid_allergies = User.ALLERGY_CHOICES
        for allergy in value:
            if allergy not in dict(valid_allergies).keys():
                raise serializers.ValidationError(f"{allergy} is not a valid allergy choice.")
        return value
    
class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'



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
             'end_time', 'total_cost', 'payment_made', 'special_requests', 'rooms', 'tasks'
         ]
    

    def create(self, validated_data):
        rooms_data = validated_data.pop('rooms')
        tasks_data = validated_data.pop('tasks', [])
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