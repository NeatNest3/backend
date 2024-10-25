from django.db import models
from django.contrib.auth.models import AbstractUser # inherited by user model for baked in Django features
from django.conf import settings  # To reference the User model
from django.core.validators import MinValueValidator, MaxValueValidator # to set min and max values for ratings
from django.contrib.gis.db import models as gis_models #for tracking geo location data for our cleaners
from django.core.exceptions import ValidationError

#---------------------------------------------------------------------------------------------------------

class User(AbstractUser):
    # choices for role field. first part of tuple is what is stored in database, second is what the user or admin sees.
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('cleaner', 'Cleaner'),
        ('both', 'Both'),
    )

    #choices for allergies. uses list so we can store multiple if needed.
    ALLERGY_CHOICES = ['none', 'dogs', 'cats', 'dust', 'pollen', 'mold', 'fragrance', 'SLS', 'ammonia', 'bleach', 'other']

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
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

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

    #profile picture via image field, required for cleaner
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=False, null=False)

    # Link to Specialty model using a Many-to-Many relationship
    specialties = models.ManyToManyField(Specialty, blank=True, related_name='cleaners')

    # stores location data in cleaner data table
    location = gis_models.PointField(geography=True, null=True)

    def __str__(self):
        return f'Cleaner: {self.user.username}'

#---------------------------------------------------------------------------------------------------------

class Home(models.Model):

    HOME_TYPE_CHOICES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('condo', 'Condo'),
        ('townhouse', 'Townhouse'),
        ('duplex', 'Duplex'),
        ('loft', 'Loft'),
        ('studio', 'Studio'),
        ('cottage', 'Cottage'),
        ('cabin', 'Cabin'),
        ('mobile_home', 'Mobile Home'),
        ('bungalow', 'Bungalow'),
        ('villa', 'Villa'),
        ('mansion', 'Mansion'),
        ('farmhouse', 'Farmhouse'),
        ('other', 'Other'),
    ]

    PET_TYPE_CHOICES = ['dog', 'cat', 'bird', 'fish', 'reptile', 'other', 'none']

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

    # Outdoor picture, special instructions
    outdoor_image = models.ImageField(upload_to='home_images/', null=False, blank=False)
    special_instructions = models.TextField(max_length=1000, blank=True, null=True)

    

    def clean(self):
        super().clean()
        for pet, count in self.pets.items():
            if pet not in self.PET_TYPE_CHOICES:
                raise ValidationError(f"{pet} is not a recognized pet type.")
            if not isinstance(count, int) or count < 0:
                raise ValidationError(f"Count for {pet} should be a non-negative integer.")
            

#---------------------------------------------------------------------------------------------------------

# Model for storing indoor images of the home if customer would like to
class Indoor_Home_Image(models.Model):
    home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='home_images/')
    caption = models.CharField(max_length=100, blank=True, null=True)  # Optional caption

    def __str__(self):
        return f"Image for {self.home.address}"
    
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
    customer = models.ForeignKey(Customer, related_name='jobs')
    cleaner = models.ForeignKey(Cleaner, related_name='jobs')
    home = models.ForeignKey(Home, related_name='jobs')

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
    
#---------------------------------------------------------------------------------------------------------

