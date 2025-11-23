from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser


class ScheduleUserManager(BaseUserManager):
    # Creates a default user. Has no extra permissions
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("*** ERROR: You must input an Email! ***")
        
        email = self.normalize_email(email) # Get the email address

        #is_superuser and is_staff are always false
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_staff", False)

        #Store information
        student_user = self.model(email=email, **extra_fields)
        student_user.set_password(password)
        student_user.save(using=self._db)

        return student_user
    
    #Creates a superuser instead of a normal user
    def create_superuser(self, email, password=None, **extra_fields):
        #is_staff and is_superuser are both set to True
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        
        return self.create_user(email, password, **extra_fields)


# Custom model that stores the information of all users
# Fields: email, password, full_name, is_staff, is_superuser (need both is_staff and is_superuser to create a superuser. You'd think it would just be is_superuser)
#
class ScheduleUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True) # When an account is made with 1 email then another account may never use that email

    USERNAME_FIELD = "email" # User's email acts like username
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    full_name=models.CharField(max_length=200) # Default model only contains fields for first name or last name, not the full name.
    REQUIRED_FIELDS = ["password"]

    # Store associated schedule IDs for quick lookup and association.
    # Uses a JSON list of integers so SQLite (default dev DB) works without Postgres-specific fields.
    # Named `schedule_ids` to avoid colliding with the reverse related-name `schedules` on Schedule.user
    schedule_ids = models.JSONField(default=list, blank=True, help_text="List of schedule IDs owned by this user")

    objects = ScheduleUserManager()

