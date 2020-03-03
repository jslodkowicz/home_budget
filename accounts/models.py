from django.db import models
from django.contrib.auth.models import AbstractBaseUser,\
                                       PermissionsMixin,\
                                       BaseUserManager

from transactions.models import Wallet, Transaction


class UserProfileManager(BaseUserManager):
    """Helps Django work with our custom user model"""

    def create_user(self, email, first_name, last_name, password):
        """Create a new user profile object"""

        if not email:
            raise ValueError('Users must have an email address.')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          first_name=first_name,
                          last_name=last_name)

        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """Creates and saves a new superuser with given details"""

        user = self.create_user(email, first_name, last_name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self.db)
        return user

    def get_by_natural_key(self, email_):
        print(email_)
        return self.get(email=email_)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Represent a user profile"""

    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    wallet = models.ManyToManyField(Wallet,
                                    related_name='user')
    transaction = models.ManyToManyField(Transaction,
                                         related_name='user')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        """Used to get a users full name"""
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        """Used to get a users short name"""
        return self.first_name

    def natural_key(self):
        """Used to get a users natural key"""
        return self.email

    def __str__(self):
        """Django uses this when it needs to
        convert the object to a string"""
        return self.email
