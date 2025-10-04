from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

class MyAccountManager(BaseUserManager): # kế thừa từ base user manager
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')
       
        if not username:
            raise ValueError('User must have an username')

        user = self.model( #tạo 1 user mới
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password) #lưu password theo dạng hash, không phải raw password
        user.save(using=self._db) # lưu vào database
        return user
    
    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    first_name          = models.CharField(max_length=50)
    last_name           = models.CharField(max_length=50)
    username            = models.CharField(max_length=50, unique= True)
    email               = models.CharField(max_length=150, unique= True)
    phone_number        = models.CharField(max_length=50)

    date_joined         = models.DateTimeField(auto_now=True)
    last_login          = models.DateTimeField(auto_now=True)
    is_admin            = models.BooleanField(default=False)
    is_staff            = models.BooleanField(default=False)
    is_active            = models.BooleanField(default=False)
    is_superadmin            = models.BooleanField(default=False)

    USERNAME_FIELD = 'email' # dùng email để login

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager() #Gắn custom manager (MyAccountManager) để tạo user/superuser đúng cách.
    def __str__(self): 
        return self.email
     #Override 2 hàm này
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True