from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username ,email ,password, first_name, last_name):
        if username is None:
            raise TypeError("Users should have a username")
        if email is None:
            raise TypeError("Users should have an email")
        if first_name is None:
            raise TypeError("Users should have a first name")
        if last_name is None:
            raise TypeError("User should have a last name")
        
        user = self.model(username = username,
                          email = self.normalize_email(email),
                          first_name = first_name,
                          last_name = last_name)
        user.set_password(password)
        user.save()
        return user
        
    def create_superuser(self, username,email,password = None, first_name = ' ', last_name = ' '):
        if password is None:
            raise TypeError("Email should not be none")
        
        user = self.create_user(username, email, password, first_name, last_name)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
    
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique = True)
    email = models.EmailField(max_length=255, unique = True)
    first_name = models.CharField(max_length = 255, null= True)
    last_name = models.CharField(max_length = 255, null = True)
    is_current = models.BooleanField(default = False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True, editable = False)
    updated_at = models.DateTimeField(auto_now=True)
    avatar_url = models.URLField(max_length=255, default = '')
    cover_url = models.URLField(max_length = 255, default = '')
    about = models.TextField(null = True, blank = True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = ['username']
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        
        
class UserFollow(models.Model):
    user = models.ForeignKey(to = User, on_delete= models.CASCADE)
    follower = models.ForeignKey(to = User, on_delete = models.CASCADE, related_name='followers')
    create_at = models.DateTimeField(auto_now_add = True)
    