from django.contrib.auth.backends import BaseBackend
from .models import User

class MyBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):        
        # check user using usrname and password
        # if user is exist then return user
        # else return user = None

        user_exists = User.objects.get(username=username,password=password)  #This line user by check user using usrname and password
        if  user_exists: 
            return user_exists 
        else:
            user_exists = None
            return user_exists
    

            
            

