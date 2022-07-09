"""
Database models
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


# i think the extra_field here is for additional params if available
# like name? guess you dont have to pass in name as a req
class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user"""
        if not email:
            raise ValueError('User must have an email address')
        # added in a self (remember this is the class so
        # BaseUserManage.normalize_email
        # (this is the function) - normalize email makes sure email is all
        # lower case (gmail)
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # hashes password
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


# You can use two classes for inherticance apparently
class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # references user manager class above
    objects = UserManager()

    USERNAME_FIELD = 'email'
