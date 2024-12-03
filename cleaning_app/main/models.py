from django.db import models
from django.contrib.auth.models import AbstractUser # inherited by user model for baked in Django features
from django.conf import settings  # To reference the User model
from django.core.validators import MinValueValidator, MaxValueValidator # to set min and max values for ratings
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


#---------------------------------------------------------------------------------------------------------
 
class User(AbstractUser):
    # choices for role field. first part of tuple is what is stored in database, second is what the user or admin sees.
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('cleaner', 'Cleaner'),
    ]

    #choices for allergies
    ALLERGY_CHOICES = [
        ('none', 'None'), ('dogs', 'Dogs'), ('cats', 'Cats'), 
        ('dust', 'Dust'), ('pollen', 'Pollen'), ('mold', 'Mold'), 
        ('fragrance', 'Fragrance'), ('SLS', 'SLS'), ('ammonia', 'Ammonia'), 
        ('bleach', 'Bleach'), ('other', 'Other')
    ]
    first_name = models.CharField(max_length=25, blank=False, null=False, unique=False)
    last_name = models.CharField(max_length=25, blank=False, null=False, unique=False)
    
    password = models.CharField(max_length=128, blank=True, null=True)
    phone = models.CharField(max_length=25, blank=False, null=False, unique=True)
    email = models.EmailField(blank=False, null=False, unique=True)

    date_of_birth = models.DateField(null=False, blank=False)
    allergies = models.JSONField(blank=True, null=True, choices=ALLERGY_CHOICES,  default='none')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')

    def allergy_validation(self):
        """Custom method to validate allergies."""
        for allergy in self.allergies:
            if allergy not in self.ALLERGY_CHOICES:
                raise ValidationError(f'{allergy} is not a valid allergy choice')
        
    def clean(self):
        # Call parent class's clean method to retain other validations
        super().clean()

        # Call specific allergy validation
        self.allergy_validation()

    def __str__(self):
        return self.username
    
    
    # Add related_name to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set', # Custom related_name
        blank=True,
    )

    # user_permissions = models.ManyToManyField(
    #     'auth.Permission',
    #     related_name='custom_user_permission_set', # Custom related_name
    #     blank=True,
    # )
    

#---------------------------------------------------------------------------------------------------------

class Customer(models.Model):

    # Link to the User model via a One-to-One field, automatically sets the PK of User to FK of Customer
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # One-to-many relationship: A customer can have multiple homes. 
    # default_home = models.ForeignKey('Home', on_delete=models.SET_NULL, blank=True, null=True, related_name='default_for_customers')

    rating = models.FloatField(validators=[MinValueValidator(1.0), MaxValueValidator(5.0)], blank=True, null=True) #customer rating 1-5
    bio = models.TextField(max_length=750, blank=True) # bio with max length of 750 characters

    # profile_pic!!! ASK DARE MONDAY

    def __str__(self):
        return f"Customer: {self.user.username}"
    
    def clean(self):
        super().clean()
        # Validate that if a default home is set, it belongs to the customer's homes
        if self.default_home and self.default_home.customer != self:
            raise ValidationError("The default home must belong to this customer")
        
#---------------------------------------------------------------------------------------------------------

class Specialty(models.Model):

    # The name of the specialty, e.g., "Deep Cleaning"
    name = models.CharField(max_length=50)

    # brief description of what the specialty entails
    description = models.TextField()

    # Optional fields if needed
    # For example, could add a price modifier or a level of expertise requirement
    # price_modifier = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    # experience_level = models.CharField(max_length=50, blank=True, null=True)

    # rooms_list = list(job.rooms.all())

    def __str__(self):
        return self.name
    
#---------------------------------------------------------------------------------------------------------

class Service_Provider(models.Model):

    # Link to the User model via a One-to-One field, automatically sets the PK of User to FK of Cleaner
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    flexible_rate = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    pet_friendly = models.BooleanField(default=True)
    rating = models.FloatField(validators=[MinValueValidator(1.0), MaxValueValidator(5.0)], blank=True, null=True)

    background_check = models.BooleanField(default=False)

    bio_work_history = models.TextField(max_length=1000, blank=True)

    specialties = models.ManyToManyField(Specialty, blank=True, related_name='service_providers')

    country = models.CharField(max_length=50, blank=False, null=False)
    address_line_one = models.CharField(max_length=255, blank=False, null=False)
    address_line_two = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=50, blank=False, null=False)
    state = models.CharField(max_length=50, blank=False, null=False)
    zipcode = models.CharField(max_length=10, blank=False, null=False)

    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f'Service Provider: {self.user.username}, Rating: {self.rating}'
    
#---------------------------------------------------------------------------------------------------------

class Home(models.Model):

    HOME_TYPE_CHOICES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('townhouse', 'Townhouse'),
        ('other', 'Other'),
    ]

    PET_TYPE_CHOICES = [
        ('dogs', 'Dogs'), ('cats', 'Cats'), ('birds', 'Birds'), 
        ('fish', 'Fish'), ('reptiles', 'Reptiles')
    ]

    #Foreign key to cusomter_id
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='homes')
    home_name = models.CharField(max_length=50, blank=False, null=False)
    
    # Address info, we will use an API for auto suggestions
    country = models.CharField(max_length=50, blank=False, null=False)
    address_line_one = models.CharField(max_length=255, blank=False, null=False)
    address_line_two = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=50, blank=False, null=False)
    state = models.CharField(max_length=50, blank=False, null=False)
    zipcode = models.CharField(max_length=10, blank=False, null=False)

    #geolocation fields for filtering results by proximity
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # Home Info
    size = models.CharField(max_length=50, blank=True, null=True)
    home_type = models.CharField(max_length=50, choices=HOME_TYPE_CHOICES, blank=False, null=False)
    bedrooms = models.CharField(max_length=2, blank=True, null=True)
    bathrooms = models.FloatField(max_length=3, blank=True, null=True)
    pets = models.JSONField(default=dict, blank=False, null=False)
    kids = models.CharField(max_length=2, blank=False, null=False)

    special_instructions = models.TextField(max_length=1000, blank=True, null=True)
    #House picture MONDAY WITH DARE
    
    def __str__(self):
        return f"{self.customer.user.first_name} {self.customer.user.last_name}: {self.home_name} - {self.address_line_one}, {self.city}"

    def clean(self):
        super().clean()
        for pet, count in self.pets.items():
            if pet not in self.PET_TYPE_CHOICES:
                raise ValidationError(f"{pet} is not a recognized pet type.")
            if not isinstance(count, int) or count < 0:
                raise ValidationError(f"Count for {pet} should be a non-negative integer.")
            
#------------------------------------------------------------------------------------------------------------

class Room(models.Model):

    home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name='rooms')
    type = models.CharField(max_length=50, blank=False, null=False)
    name = models.CharField(max_length=50, null=False, blank=False)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.home.home_name} - {self.type} - {self.name}"

#------------------------------------------------------------------------------------------------------------

class Service(models.Model):
    # Service fields
    name = models.CharField(max_length=50)
    description = models.TextField()
    # price_range = models.DecimalField(max_digits=6, decimal_places=2)
    # estimated_duration = models.DurationField()

    def __str__(self):
        return f"{self.name})"
    # ${self.price_range} ({self.estimated_duration}

#------------------------------------------------------------------------------------------------------------

class Job(models.Model):

    STATUS_TYPE_CHOICES = [
        ('pending', 'Pending'),
        ('booked', 'Booked'),
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed')
    ]

    # Foreign key relationships with related name 'jobs'
    customer = models.ForeignKey(Customer, related_name='jobs', on_delete=models.CASCADE)
    service_provider = models.ForeignKey(Service_Provider, related_name='jobs', on_delete=models.SET_NULL, null=True)
    home = models.ForeignKey(Home, related_name='jobs', on_delete=models.CASCADE)

    rooms  = models.ManyToManyField(Room, related_name="jobs")
    services = models.ManyToManyField(Service, related_name='jobs')  # Many-to-many with Service
    #tasks = models.ManyToManyField('Task', related_name='job_tasks') # Many-to-many with Task

    # Status and schedule fields
    status = models.CharField(max_length=20, choices=STATUS_TYPE_CHOICES, blank=False, null=False, default='pending')
    date = models.DateField(blank=False, null=False )
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)

    # Cost, Payment, Special Requests
    # total_cost = models.DecimalField(max_digits=6, decimal_places=2, blank=False, null=False)
    # payment_made = models.BooleanField(default=False)
    # special_requests = models.TextField(max_length=500, null=True, blank=True)


    def __str__(self):
        return f"Job for {self.customer} on {self.date} at {self.start_time}, Cleaner: {self.service_provider}"
    
#---------------------------------------------------------------------------------------------------------

# class Task(models.Model):
#     # Foreign key to a Job model 
#     job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='task_jobs')
#     room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='tasks', default='General')

#     # Basic fields
#     name = models.CharField(max_length=50)
#     description = models.TextField()
#     status = models.CharField(max_length=15)
    
#     # Optional fields
#     duration = models.DurationField(null=True, blank=True)  # Duration field for time intervals
#     price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
#     # Notes fields
#     service_provider_notes = models.TextField(blank=True, null=True)
#     customer_notes = models.TextField(blank=True, null=True)



#     def __str__(self):
#         return f"{self.name} - Status: {self.status} (${self.price or 'N/A'})"

    
#------------------------------------------------------------------------------------------------------    

# class Availability(models.Model):
#     DAYS_OF_WEEK = [
#         ('monday', 'Monday'),
#         ('tuesday', 'Tuesday'),
#         ('wednesday', 'Wednesday'),
#         ('thursday', 'Thursday'),
#         ('friday', 'Friday'),
#         ('saturday', 'Saturday'),
#         ('sunday', 'Sunday'),
#     ]

#     service_provider_id = models.ForeignKey(Service_Provider, on_delete=models.CASCADE)
#     day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
#     start_time = models.TimeField()
#     end_time = models.TimeField()

#     def __str__(self):
#         return f"{self.service_provider_id} available on {self.day_of_week} from {self.start_time} to {self.end_time}"

#---------------------------------------------------------------------------------------------------------


class Image(models.Model):
    image_name = models.CharField(max_length=255)  # Original file name
    s3_url = models.URLField(max_length=500, blank=True, null=True)  # URL of the image in S3
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp of upload

    def __str__(self):
        return self.image_name
    
    
#---------------------------------------------------------------------------------------------------------

# class Payment(models.Model):
#     # Foreign key fields assuming `Job` and `Customer` models exist
#     job = models.ForeignKey('Job', on_delete=models.CASCADE, null=True, related_name='payments')
#     customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='payments')
    
#     # Payment fields/ amount made decimal field which allows control over the number of digits and decimal places.
#     method = models.CharField(max_length=25)
#     status = models.CharField(max_length=20)
#     amount = models.DecimalField(max_digits=6, decimal_places=2)
#     date = models.DateField()

#     def __str__(self):
#         return f"Payment(id={self.id}, job_id={self.job.id}, customer_id={self.customer.id}, " \
#                f"method='{self.method}', status='{self.status}', amount={self.amount}, date={self.date})"
    

    
#---------------------------------------------------------------------------------------------------------

# Review model
class Review(models.Model):
    job = models.ForeignKey('Job', on_delete=models.CASCADE, related_name="reviews")
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="given_reviews")
    reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_reviews")
    reviewer_role = models.CharField(max_length=10)
    reviewee_role = models.CharField(max_length=10)
    review_text = models.TextField()
    review_date = models.DateField()
    rating = models.FloatField([MinValueValidator(1.0), MaxValueValidator(5.0)], blank=False, null=False)

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.reviewee.username} - Rating: {self.rating}"

    def is_positive(self):
        """Check if the review rating is positive (4 or 5)."""
        return self.rating >= 4

#---------------------------------------------------------------------------------------------------------

#     # PaymentMethod model
# class Payment_Method(models.Model):
#     customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payment_methods")
#     type = models.CharField(max_length=50)
#     card_number = models.CharField(max_length=255)  # Store hashed
#     last_four = models.CharField(max_length=4)
#     exp_month = models.IntegerField()
#     exp_year = models.IntegerField()
#     provider = models.CharField(max_length=50)
#     default = models.BooleanField(default=False)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.type} ending in {self.last_four} for {self.customer.username}"

#     def is_expired(self):
#         """Check if the payment method is expired."""
#         from datetime import datetime
#         return (self.exp_year < datetime.now().year) or (self.exp_year == datetime.now().year and self.exp_month < datetime.now().month)

#---------------------------------------------------------------------------------------------------------

#     # BankAccount model
# class Bank_Account(models.Model):
    
#     service_provider = models.ForeignKey(Service_Provider, on_delete=models.CASCADE, related_name="bank_accounts")
#     bank = models.CharField(max_length=100)
#     account_last_four = models.CharField(max_length=4)
#     account_type = models.CharField(max_length=50)
#     account_number = models.CharField(max_length=255)  # Store hashed
#     routing_number = models.CharField(max_length=255)  # Store hashed
#     default = models.BooleanField(default=False)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Bank Account ({self.bank}) for {self.service_provider.username}"

#     def is_default(self):
#         """Check if this bank account is the default one."""
#         return self.default
    
#---------------------------------------------------------------------------------------------------------

#class Image(models.Model):
 #   image_url = models.URLField(max_length=200)
  #  created_at = models.DateTimeField(auto_now_add=True)

   # def __str__(self):
    #    return f'Image {self.id}'
    


# model to save FCM (Firebase Cloud Messaging). Needed to be able to send notifications.
# class DeviceToken(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     token = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.username} - Token"

# class Ticket(models.Model):

#     customer = Customer
#     cleaner = Cleaner
     
#     ROLE_CHOICES = (
#         ('customer', 'Customer'),
#         ('cleaner', 'Cleaner'),
#     )

#     # id creates a universal unique identifier that guarantees a unique ID for each ticket.
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
#     # Account_id as an integer field
#     account_id = models.ForeignKey(Account, on_delete=models.CASCADE) 

#     # Role as an integer field
#     role = models.IntegerField(choices=ROLE_CHOICES)

#     # Ticket content as a text field
#     ticket_content = models.TextField()

#     # Date and time fields
#     date = models.DateField()
#     time = models.TimeField()

#     # Status as a character field with max length of 10
#     status = models.CharField(max_length=10)

    
#     def __str__(self):
#         return f"Ticket {self.id} - Role: {self.ROLE_CHOICES()} - Status: {self.status}"


#     #---------------------------------------------------------------------------------------------------------
#     # Chat model
# class Chat(models.Model):
#     customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer_chats")
#     cleaner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cleaner_chats")

#     def __str__(self):
#         return f"Chat between {self.customer.username} and {self.cleaner.username}"

#     #---------------------------------------------------------------------------------------------------------
#     # Message model
# class Message(models.Model):
#     chat = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name="messages")
#     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
#     receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
#     message = models.TextField()
#     date = models.DateField()
#     time = models.TimeField()

#     def __str__(self):
#         return f"Message from {self.sender.username} to {self.receiver.username} on {self.date} at {self.time}"

#     def is_sent_by(self, user):
#         """Check if the message was sent by a specific user."""
# <<<<<<< HEAD
#         return self.sender == user
# >>>>>>> 009b9e8f951ccc9ebb55473aadcafd1bb40d394d
# =======
#         return self.sender == user
# >>>>>>> 009b9e8f951ccc9ebb55473aadcafd1bb40d394d
