from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager): 
     def create_user(self, first_name, last_name, username, email, password=None): # Creating regular user and it extends the base user manager
        if not email: #to make sure the user provides email address
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("user must have a username") #to make sure the user provides username 
        
        user = self.model(
            email = self.normalize_email(email),# normalizing email address. if yo uuse small, caps or both it would normalise it
            username = username,
            first_name = first_name,
            last_name = last_name,
            
            
            )
        user.set_password(password) #set_password is a method that would take the password and encode it before storing in db
        user.save(using=self._db)# This determines the database you want to use for this operation if you have more than one db. but in our case we are using one db
        #it would take the default db we have configured in the settings.py file
        #user.save(using='db2') if i have multiple db and wants to use db2
        return user
     
     def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(  # to create a super user you first need to create a user
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
            
              
         )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db) #this would save it in the default database which is in the settings.py
        #However we can have multiple db and choose the one to save it to
        return user
     

     
class User(AbstractBaseUser): #there us another called AbstractUser class only allows you to add extra fields to your models
    #we would extend it in the user class and we would take full control of the editing user model including the authetication functionality

    VENDOR = 1
    CUSTOMER = 2

    ROLE_CHOICE = (
        (VENDOR, 'Vendor'),
        (CUSTOMER, 'Customer'),


    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=80, unique=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)

    #REQUIRED FIELD
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)


    USERNAME_FIELD = 'email' #this would allow you use email as the login field if not it would use the username
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']#email is not added as required field becouse user name is already a required field so by default email becomes required

    objects = UserManager() #tells the user class which user manager to use on this model. we creared the UserManager class up

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin  #it would return true if the user is an admin. has permision if the user is an admin or superuser
    
    def has_module_perms(self, app_label): ##it would return true if the user is an admin. has permision if the user is an admin or superuser
        return True 


    def get_role(self):
        if self.role == 1:
            user_role = 'vendor'
        elif self.role == 2:
            user_role ='Customer'
        return user_role

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank = True, null = True )# to make user have only one profile. 
    #if you want one user to have multiple profiles then you can use foreign key ForeignKey()
    profile_picture = models.ImageField(upload_to="users/profile_pictures", blank=True, null=True)
    cover_photo = models.ImageField(upload_to="users/cover_photo", blank=True, null=True)
    primaryAddress= models.CharField(max_length=250, blank=True, null=True)
    address_line_1 = models.CharField(max_length=50, blank=True, null=True)
    address_line_2 = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)
    latitude = models.CharField(max_length=50, blank=True, null=True)
    longitude = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    def full_address(self):
        return f'{self.address_line_1}, {self.address_line_2}'#We used this on the cover.html

    def full_address1(self):#We used this on the cover.html called from context_processor
        address_parts = [self.address_line_1, self.address_line_2, self.city, self.state, self.country, self.pin_code]
        non_empty_parts = [str(part) for part in address_parts if part]
        return ', '.join(non_empty_parts)#This modification ensures that each part of the address is converted to a string before joining. If any part is None, it will be skipped

    def __str__(self):
        return self.user.email
    

