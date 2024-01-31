from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

# Create your models here.

# class User(AbstractUser):
#     first_name = models.CharField(max_length=200)
#     last_name = models.CharField(max_length=200)
#     username = models.CharField(unique=True,max_length=50)
#     email = models.EmailField(unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name','last_name','username']
    
#     # class Meta:
#     #     verbose_name='Use'
    
#     def __str__(self):
#         return self.username






class User(AbstractUser):
    # WARNING!
    """
    Some officially supported features of Crowdbotics Dashboard depend on the initial
    state of this User model (Such as the creation of superusers using the CLI
    or password reset in the dashboard). Changing, extending, or modifying this model
    may lead to unexpected bugs and or behaviors in the automated flows provided
    by Crowdbotics. Change it at your own risk.


    This model represents the User instance of the system, login system and
    everything that relates with an `User` is represented by this model.
    """

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(("Name of User"), blank=True, null=True, max_length=255,default="")
    username = models.CharField(unique=True,blank=True,null=True,max_length=100)
    email = models.EmailField(default='email',unique=True,max_length=255)

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})