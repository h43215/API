from pyexpat import model
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, name and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name = name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser with the given email, name and password.
        """
        user = self.create_user(
            email,
            password=password,
            name =name
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

        

class Product(models.Model):
 
    name = models.CharField(max_length=50)
    stock = models.CharField(max_length=50,default=None,blank=True,null= True)
    price = models.CharField(max_length=200 ,default=None,blank=True,null= True)
    description = models.CharField(max_length=50)
    image = models.ImageField(upload_to='API/media/',default=None,blank=True,null= True)

    def __str__(self):
        return self.name

class Order(models.Model):

    name = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default="")
    quantity = models.CharField(max_length=50)
    price = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=True)


    def __str__(self):
        return self.name      