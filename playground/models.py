from django.db import models
from django.utils import timezone
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save





class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, first_name='DefaultFirst', last_name='DefaultLast', **extra_fields):
        if not username:
            raise ValueError('The Username field is required')
        if not email:
            raise ValueError('The Email field is required')

        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            date_joined=timezone.now(),  # Set the date_joined to the current time
            **extra_fields
        )
        # user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class MyUser(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=128)
    class Meta:
        db_table = 'table1'
        managed = False
    
    def __str__(self):
        return self.username
    


class User(AbstractBaseUser):
    # profile_picture = models.ImageField(upload_to='profile_images', default='profile_images/default.png', blank=False, null=True)
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=30, default='DefaultFirst')
    last_name = models.CharField(max_length=30, default='DefaultLast')
    password = models.CharField(max_length=128)  # Django expects hashed password here
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    # date_birth = models.DateTimeField(null=True, blank=True)
      # Add date_joined with default
    # picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def update_last_login(self):
        self.last_login = timezone.now()
        self.save(update_fields=['last_login'])

    class Meta:
        db_table = 'auth_user'
        managed = False

    def __str__(self):
        return self.username




class myProfile(models.Model):
    # id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile', primary_key=True)
    profile_picture = models.ImageField(upload_to='profile_images', default='profile_images/default.png', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)  # You can add other fields like bio or social media links
    first_name = models.CharField(max_length=30, default='DefaultFirst')
    last_name = models.CharField(max_length=30, default='DefaultLast')
    
    def __str__(self):
        return f"Profile of {self.user.username}"




# class User(models.Model):
#     id = models.AutoField(primary_key=True)
#     username = models.CharField(max_length=50)
#     email = models.EmailField(max_length=254, blank=True)
#     # matches = models.IntegerField()
#     password = models.CharField(max_length=50)
#     last_login = models.DateTimeField(null=True, blank=True)  # Add this field

#     def update_last_login(self):
#         self.last_login = timezone.now()  # Update last_login to the current time
#         self.save(update_fields=['last_login'])
#     REQUIRED_FIELDS = ['email']
#     USERNAME_FIELD = ['email']
#     class Meta:
#         db_table = 'auth_user'  # Specify the name of the table if it doesn't follow Django's naming conventions
#         managed = False  # This tells Django not to manage the table (no migrations, etc.)
        
#     def __str__(self):
        # return self.name

class Team(models.Model):
    name = models.CharField(max_length=50, primary_key=1)
    email = models.EmailField(blank=True, max_length=254)
    phoneNumber = models.IntegerField()

    class Meta:
        db_table = 'Team'
    
    def __str__(self):
        return self.name
    

