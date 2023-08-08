from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserDetails(AbstractUser):

    username = models.CharField(max_length=150, unique=True, null=False)
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(null=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    is_staff = None
    is_active = None
    date_joined = None
    groups = None
    user_permissions = None
    last_login = None
    is_superuser = None
    first_name = None
    last_name = None

    def __str__(self):
        return self.username
