from django.db import models
import jwt
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager 
from datetime import datetime, timedelta
from django.contrib.postgres.fields import JSONField

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(blank=True, max_length=100) 
    username = models.CharField(db_index=True, max_length=100, unique=True)
    phone = models.CharField(unique=True, max_length=15)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=True)
    USER_CHOICES = (
        ('student', 'Student')
        ('school', 'School'),
        ('teacher', 'Teacher'),
        ('government', 'Government Official')
    )
    user_type = models.CharField(blank=False, choices=USER_CHOICES, max_length=40)
    data = JSONField()

    objects = UserManager()
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone', 'email', 'user_type']

    def __str__(self):
        return self.username
    
    @property
    def token(self):
        return self._generate_jwt_token()
    
    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%S'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

