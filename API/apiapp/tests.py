from django.test import TestCase

# Create your tests here.


# request.user is always use to only for user(means only for login person) 


# only for the not user a password

# view.py
# class UserLoginView(APIView):
#     def post(self,request, format=None):
#         serializer = UserLoginSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             email = serializer.data.get('email')
#             password = serializer.data.get('password')
#             user = authenticate(email=email)
#             if user is not None:
#                 token = get_tokens_for_user(user)
#                 return Response({"status":True, "massage":"Login Successfully", "data":serializer.data,'token':token}, status=status.HTTP_200_OK)
#             else:
#                return Response({'error':{'non_field_errors':['Email or password is not valid']}},status=status.HTTP_404_NOT_FOUND)   
#         return Response({'error':{'non_field_errors':['Email or password is not valid']}},status=status.HTTP_404_NOT_FOUND)           

# backends.py

# from django.contrib.auth.backends import BaseBackend
# from .models import User

# class MyBackend(BaseBackend):
#     def authenticate(self, request, email=None):        
#         # check user using usrname and password
#         # if user is exist then return user
#         # else return user = None

#         user_exists = User.objects.get(email=email)
#         if  user_exists: 
#             return user_exists 
#         else:
#             user_exists = None
#             return user_exists

