from django.urls import path
from apiapp.views import UserRegistationView
from apiapp.views import UserLoginView
from apiapp.views import UserProfileView
from apiapp.views import ProductView
from apiapp.views import OrderView
from apiapp.views import ChangePasswordView
from apiapp.views import ResetPassword
from apiapp.views import SentEmail,HomeView
# from apiapp import views
from .views import GeneratePdf





urlpatterns = [
    path('register/', UserRegistationView.as_view(),name= 'register'),
    path('login/', UserLoginView.as_view(),name= 'login'),
    path('profile/',UserProfileView.as_view(),name = 'profile'),
    path('product/',ProductView.as_view(),name= 'product'),
    path('product/<int:pk>',ProductView.as_view(),name='product'),
    path('order/',OrderView.as_view(),name='order'),
    path('order/<int:pk>',OrderView.as_view(),name='order'),
    path('changepassword/', ChangePasswordView.as_view(), name='changepassword'),
    path('resetpassword/', ResetPassword.as_view(),name='resetpassword'),
    path('sendemail/',SentEmail.as_view(),name='sendemail'),
    path('pdf/', GeneratePdf.as_view(),name='pdf'), 
    path('home/',HomeView.as_view(),name="home"),
    
    
]




# class ProductView(APIView):
#     def post(self, request, format=None):
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
#         else:
            # return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# Serilizer
#  name =  serializers.CharField(max_length=20)
#     stock = serializers.IntegerField(required=False,default=1)
#     price = serializers.FloatField()
#     description = serializers.CharField(max_length=50)
#     image = serializers.ImageField()
#     class Meta:
#         model = Product
#         fields =('__all__')            


# check the email is not None
        #     user = User.objects.get(email=str(request.query_params['email']))       # validate user by email
        #     order = Order.objects.get(order = order.id)                                # get order = by user id
        #                                                                             # for x in order
        #                                                                             # x.product
        #                                                                             # get product by x.product
        #     return Response({"status":True, "massage":"Successfully"})              # response success
        # else:                                                                       # not valid     
# 

 


        # user_id=user.id 