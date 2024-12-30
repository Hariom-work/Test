# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db.models.functions import Now
from datetime import datetime
from django.db import models
import uuid
from django.utils import timezone
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        try:
            user = self.model(username=username,**extra_fields)
            if password:
                user.set_password(password)
            user.save(using=self._db)
            return user
        except Exception as e:
            raise ValueError(str(e))

    def create_admin(self,username, password=None, **extra_fields):
        user = self.model(username=username,user_type=CustomUser.UserType.ADMIN, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', CustomUser.UserType.SUPER_ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_staff(mobile, password, **extra_fields)
    
    def get_customers(self):
        return super().get_queryset().filter(user_type=CustomUser.UserType.USER, is_active=True)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    class UserType(models.TextChoices):
        SUPER_ADMIN = "super_admin", _("Super Admin")
        ADMIN = "admin", _("Admin")
        STAFF = "staff", _("Staff")
        USER = "user", _("User")

    def get_current_date():
        return timezone.now().date()

    id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, primary_key=True)
    username = models.CharField(max_length=50, null=False, blank=False, unique=True)
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(unique=True, null=True, blank=False,)
    password = models.CharField(max_length=255, null=True, blank=False)
    date_joined = models.DateField(default=get_current_date)  
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    user_type = models.CharField(max_length=50,choices=UserType.choices, default=UserType.USER)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', "last_name"]

    class Meta:
        db_table = 'users'

    def __str__(self) -> str:
        return self.username

    def last_updated(self):
        return self.modified_at.strftime("%d %b %y %I:%M %p")

