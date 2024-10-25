from django.db import models
from django.contrib.auth.models import AbstractUser # inherited by user model for baked in Django features
from django.conf import settings  # To reference the User model
from django.core.validators import MinValueValidator, MaxValueValidator 
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