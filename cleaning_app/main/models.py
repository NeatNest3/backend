from django.db import models
from django.contrib.auth.models import AbstractUser # inherited by user model for baked in Django features
from django.conf import settings  # To reference the User model
from django.core.validators import MinValueValidator, MaxValueValidator # to set min and max values for ratings
from django.core.exceptions import ValidationError
# import uuid

#---------------------------------------------------------------------------------------------------------

class User(AbstractUser):
    # choices for role field. first part of tuple is what is stored in database, second is what the user or admin sees.
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('cleaner', 'Cleaner'),
    )

    #choices for allergies
    ALLERGY_CHOICES = [
        ('none', 'None'), ('dogs', 'Dogs'), ('cats', 'Cats'), 
        ('dust', 'Dust'), ('pollen', 'Pollen'), ('mold', 'Mold'), 
        ('fragrance', 'Fragrance'), ('SLS', 'SLS'), ('ammonia', 'Ammonia'), 
        ('bleach', 'Bleach'), ('other', 'Other')
    ]

    #preffered name field for nicknames/preferences 
    preferred_name = models.CharField(max_length=25, blank=True, null=True)

    # role of the user
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')

    # required unique phone and email fields
    phone = models.CharField(max_length=25, blank=False, null=False, unique=True)
    email = models.EmailField(blank=False, null=False, unique=True)

    #Verification status fields
    is_phone_verified = models.BooleanField(default=False) # to check if phone is verified
    is_email_verified = models.BooleanField(default=False) # to check if email is verified

    date_of_birth = models.DateField(null=False, blank=False)

    # JSONField to store multiple allergy selections
    allergies = models.JSONField(default=list, blank=False, null=False)

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

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permission_set', # Custom related_name
        blank=True,
    )
    

#---------------------------------------------------------------------------------------------------------

class Customer(models.Model):

    # Link to the User model via a One-to-One field, automatically sets the PK of User to FK of Customer
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # One-to-many relationship: A customer can have multiple homes. 
    default_home = models.ForeignKey('Home', on_delete=models.SET_NULL, blank=True, null=True, related_name='default_for_customers')

    rating = models.FloatField(validators=[MinValueValidator(1.0), MaxValueValidator(5.0)], blank=True, null=True) #customer rating 1-5
    bio = models.TextField(max_length=750, blank=True) # bio with max length of 750 characters

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

    def __str__(self):
        return self.name
    
#---------------------------------------------------------------------------------------------------------

class Cleaner(models.Model):

    # Link to the User model via a One-to-One field, automatically sets the PK of User to FK of Cleaner
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Flexible rate: a numeric field with 6 total digits and 2 decimal places (1000.00)
    flexible_rate = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    # Pet friendly: Boolean field indicating if the cleaner is comfortable with pets
    pet_friendly = models.BooleanField(default=False)

    # Rating: Float rating with values from 1.0 to 5.0
    rating = models.FloatField(validators=[MinValueValidator(1.0), MaxValueValidator(5.0)], blank=True, null=True)

    # Background check status: Boolean field indicating if the cleaner passed a background check
    background_check = models.BooleanField(default=False)

    # TextField to describe cleaner and work experience
    bio_work_history = models.TextField(max_length=1000, blank=True)

    # Link to Specialty model using a Many-to-Many relationship
    specialties = models.ManyToManyField(Specialty, blank=True, related_name='cleaners')

    def __str__(self):
        return f'Cleaner: {self.user.username}'

#---------------------------------------------------------------------------------------------------------

class Home(models.Model):

    HOME_TYPE_CHOICES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('townhouse', 'Townhouse'),
        ('other', 'Other'),
    ]

    PET_TYPE_CHOICES = [
        ('dog', 'Dog'), ('cat', 'Cat'), ('bird', 'Bird'), 
        ('fish', 'Fish'), ('reptile', 'Reptile'), ('other', 'Other'), ('none', 'None')
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

    # Home Info
    size = models.CharField(max_length=50, blank=False, null=False)
    home_type = models.CharField(max_length=50, choices=HOME_TYPE_CHOICES, blank=False, null=False)
    bedrooms = models.CharField(max_length=2, blank=False, null=False)
    bathrooms = models.FloatField(max_length=3, blank=False, null=False)
    pets = models.JSONField(default=dict, blank=False, null=False)
    kids = models.CharField(max_length=2, blank=False, null=False)

    special_instructions = models.TextField(max_length=1000, blank=True, null=True)

    

    def clean(self):
        super().clean()
        for pet, count in self.pets.items():
            if pet not in self.PET_TYPE_CHOICES:
                raise ValidationError(f"{pet} is not a recognized pet type.")
            if not isinstance(count, int) or count < 0:
                raise ValidationError(f"Count for {pet} should be a non-negative integer.")
            

#---------------------------------------------------------------------------------------------------------

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
    cleaner = models.ForeignKey(Cleaner, related_name='jobs', on_delete=models.SET_NULL, null=True)
    home = models.ForeignKey(Home, related_name='jobs', on_delete=models.CASCADE)

    # Status and schedule fields
    status = models.CharField(max_length=20, choices=STATUS_TYPE_CHOICES, blank=False, null=False)
    date = models.DateField(blank=False, null=False)
    start_time = models.TimeField(blank=False, null=False)
    end_time = models.TimeField(blank=False, null=False)

    # Cost, Payment, Special Requests
    total_cost = models.DecimalField(max_digits=6, decimal_places=2, blank=False, null=False)
    payment_made = models.BooleanField(default=False)
    special_requests = models.TextField(max_length=500, null=True, blank=True)

    # Need Service and Task models before activating these
    # services = models.ManyToManyField(Service, related_name='jobs')  # Many-to-many with Service
    # tasks = models.ManyToManyField(Task, related_name='jobs')  # Many-to-many with Task

    def __str__(self):
        return f"Job for {self.customer} on {self.date} at {self.start_time}, Cleaner: {self.cleaner}"
    
#------------------------------------------------------------------------------------------------------    

class Availability(models.Model):
    DAYS_OF_WEEK = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]

    id = models.AutoField(primary_key=True)
    cleaner_id = models.ForeignKey(Cleaner, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.cleaner_id} available on {self.day_of_week} from {self.start_time} to {self.end_time}"

#---------------------------------------------------------------------------------------------------------

class Payment(models.Model):
    # Foreign key fields assuming `Job` and `Customer` models exist
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='payments')
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='payments')
    
    # Payment fields/ amount made decimal field which allows control over the number of digits and decimal places.
    method = models.CharField(max_length=25)
    status = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"Payment(id={self.id}, service_id={self.service.id}, customer_id={self.customer.id}, " \
               f"method='{self.method}', status='{self.status}', amount={self.amount}, date={self.date})"
    
#------------------------------------------------------------------------------------------------------------

class Service(models.Model):
    # Service fields
    name = models.CharField(max_length=50)
    description = models.TextField()
    price_range = models.DecimalField(max_digits=6, decimal_places=2)
    estimated_duration = models.DurationField()

    def __str__(self):
        return f"{self.name} - ${self.price_range} ({self.estimated_duration})"

#------------------------------------------------------------------------------------------------------------

class Task(models.Model):
    # Foreign key to a Job model (assuming Job model exists)
    job = models.ForeignKey('Job', on_delete=models.CASCADE, related_name='tasks')

    # Basic fields
    name = models.CharField(max_length=50)
    description = models.TextField()
    status = models.CharField(max_length=15)
    
    # Optional fields
    duration = models.DurationField(null=True, blank=True)  # Duration field for time intervals
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Notes fields
    cleaner_notes = models.TextField()
    customer_notes = models.TextField()

    # Optional pictures field using ManyToMany with an Image model
    # pictures = models.ManyToManyField('Image', blank=True, related_name='tasks')  # Optional field

    def __str__(self):
        return f"{self.name} - Status: {self.status} (${self.price or 'N/A'})"
    
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

    # PaymentMethod model
class PaymentMethod(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payment_methods")
    type = models.CharField(max_length=50)
    card_number = models.CharField(max_length=255)  # Store hashed
    last_four = models.CharField(max_length=4)
    exp_month = models.IntegerField()
    exp_year = models.IntegerField()
    provider = models.CharField(max_length=50)
    default = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.type} ending in {self.last_four} for {self.customer.username}"

    def is_expired(self):
        """Check if the payment method is expired."""
        from datetime import datetime
        return (self.exp_year < datetime.now().year) or (self.exp_year == datetime.now().year and self.exp_month < datetime.now().month)

#---------------------------------------------------------------------------------------------------------

    # BankAccount model
class BankAccount(models.Model):
    cleaner = models.ForeignKey(Cleaner, on_delete=models.CASCADE, related_name="bank_accounts")
    bank = models.CharField(max_length=100)
    account_last_four = models.CharField(max_length=4)
    account_type = models.CharField(max_length=50)
    account_number = models.CharField(max_length=255)  # Store hashed
    routing_number = models.CharField(max_length=255)  # Store hashed
    default = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Bank Account ({self.bank}) for {self.cleaner.username}"

    def is_default(self):
        """Check if this bank account is the default one."""
        return self.default
    
#---------------------------------------------------------------------------------------------------------

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
