from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group

# Create your models here.
roles = [
    ('Admin', 'Admin'),
    ('User', 'User'),
    ('Guest', 'Guest')
]

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if email is None:
            raise ValueError('The Email is required')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        group = Group.objects.get(name='Admin')
        if password:
            password = make_password(password)
            user.password = password
        user.groups.add(group)
        user.is_active = True
        user.role = 'User'
        user.save()
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        
        user = self.create_user(username, email, password, **extra_fields)
        user.role = 'Admin'
        user.is_staff = True
        user.is_superuser = True

        user.save()

        return user


class CustomUser(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, default='User', choices=roles)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser, blank=True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    githubUsername = models.CharField(max_length=50, blank=True)
    profilePic = models.ImageField(
        upload_to='images/', blank=True, default='images/default_avatar.jpeg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} Profile. created at {self.created_at}"

    @property
    def get_profilePic(self):
        return self.profilcPic


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

