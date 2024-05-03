from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models

# Create your models here.

class TodoItem(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] #added

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="custom_user_groups",  # Unique related_name to avoid clashes
        related_query_name="custom_users",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="custom_user_permissions",  # Unique related_name to avoid clashes
        related_query_name="custom_users",
    )
    

    # Define the Meta class correctly without the invalid attributes
    class Meta(AbstractUser.Meta):
        # You can define other Meta options here, but not 'groups' or 'user_permissions'
        pass

    #new backend implementation//////////////////////////
from django.db import models
from cryptography.fernet import Fernet

class CreditCard(models.Model):
    card_number_encrypted = models.TextField()
    card_expiry = models.CharField(max_length=5)
    user_id = models.IntegerField()
    card_type = models.CharField(max_length=100)
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2)
    card_name = models.CharField(max_length=100)
    credit_apr = models.DecimalField(max_digits=5, decimal_places=2)
    rewards = models.CharField(max_length=100)

    @staticmethod
    def generate_cipher_suite():
        key = Fernet.generate_key()
        return Fernet(key)

    def encrypt_card_number(self, card_number):
        cipher_suite = self.generate_cipher_suite()
        return cipher_suite.encrypt(card_number.encode()).decode()

    def decrypt_card_number(self, encrypted_card_number):
        cipher_suite = self.generate_cipher_suite()
        return cipher_suite.decrypt(encrypted_card_number.encode()).decode()

    def save(self, *args, **kwargs):
        self.card_number_encrypted = self.encrypt_card_number(self.card_number)
        super().save(*args, **kwargs)

    def get_card_number(self):
        return self.decrypt_card_number(self.card_number_encrypted)
    
    #/////////////NOT USING ABOVE

    # models.py

from django.contrib.auth.models import User
from django.db import models

class CreditCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    expiry_date = models.CharField(max_length=5)
    cvv = models.CharField(max_length=3)

class Transaction(models.Model):
    card = models.ForeignKey(CreditCard, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
