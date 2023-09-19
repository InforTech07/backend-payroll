"""
This file contains the User model.
roles: 
    - superadmin : can do anything
    - admin : can do anything except create superadmin
    - user : can do anything except create superadmin and admin
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    """Custom User model.
    extendes from django's abrastract user,
    changes the username field to email.
    and add some extra fields.
    """
    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'A user with that email already exists.'
        }
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    role = models.CharField(max_length=255, default='user')
    picture = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(
        'active status',
        default=True,
        help_text=(
            'help eshteht to show if the user is active'
        )
    )
    is_dafault_password = models.BooleanField(
        'default password status',
        default=True,
        help_text=(
            'help eshteht to show if the user is active'
        )
    )

    def __str__(self):
        """Return username."""
        return self.username

    def get_short_name(self) -> str:
        """Return username."""
        return self.username



































# class UserAccountManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('Users must have an email address')
        
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)

#         user.set_password(password)
#         user.save()

#         return user
#     def create_admin(self, email, password, **extra_fields):
#         user = self.create_user(email, password, **extra_fields)
#         user.role = 'admin'
#         user.is_staff = True
#         user.save()

#         return user
    
    
#     def create_superuser(self, email, password, **extra_fields):
#         user = self.create_user(email, password, **extra_fields)

#         user.role = 'superadmin'
#         user.is_superuser = True
#         user.is_staff = True
#         user.save()

        

#         return user


# class UserAccount(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(max_length=255, unique=True)
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#     role = models.CharField(max_length=255, default='user')
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)

#     objects = UserAccountManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'last_name']

#     def get_full_name(self):
#         return self.first_name + ' ' + self.last_name

#     def get_short_name(self):
#         return self.first_name

#     def __str__(self):
#         return self.email