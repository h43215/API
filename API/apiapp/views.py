from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from apiapp.serializers import UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializer,UserProductSerializer,UserOrderSerializer
from django.contrib.auth import authenticate
from apiapp.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import Product, User, Order
from .serializers import ChangePasswordSerializer
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.generic import View
from .utils import render_to_pdf
from datetime import timedelta


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh_token = refresh
    access_token = refresh.access_token

    refresh_token.set_exp(lifetime=timedelta(days=60))
    access_token.set_exp(lifetime=timedelta(days=15))
    return {
        'refresh': str(refresh_token),
        'access': str(access_token),
    } 


class UserRegistationView(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({"status":True, "massage":"Registration Successfully", "data":serializer.data, 'token':token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self,request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email= email, password = password)
            if user is not None:    
                token = get_tokens_for_user(user)
                data_dict = {
                    "email":serializer.data.get("email")

                }
                return Response({"status":True, "massage":"Login Successfully", "data":data_dict,'token':token}, status=status.HTTP_200_OK)
            else:
               return Response({'error':{'non_field_errors':['Email or password is not valid']}},status=status.HTTP_404_NOT_FOUND)   
        return Response({'error':{'non_field_errors':['Email or password is not valid']}},status=status.HTTP_404_NOT_FOUND)           

class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
  

    def get(self,request,format=None):
        if request.user.isanonymous:
            return Response({"Message":"you dont have access"})
        serializer = UserProfileSerializer(request.user,)        
        return Response({"status":True, "massage":"Successfully", "data":serializer.data}, status=status.HTTP_200_OK)

    def put(self,request,format=None):
        print(request.user)
        try:
            user = User.objects.get(email=request.user)
        except User.DoesNotExist:
            return Response({'Error':"fail"})
        serializer = UserProfileSerializer(user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
        
            return Response({"status":True, "massage":"Update Successfully", "data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request):
        try:
            user = User.objects.get(email=request.user)
        except User.DoesNotExist:
            return Response({"status":'Error'})

        user.delete()    
        return Response({"massage":"Deleted Successfully"})


class ProductView(APIView):
    def post(self, request, format=None):
        serializer = UserProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'status':True, 'massage':'Product successful', 'data':serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'error':{'non_field_errors':['Product Details is not Valid']}},status=status.HTTP_404_NOT_FOUND)
       
    def get(self,request,pk=None,format=None):
        products = ""
        if pk is None:
            products = Product.objects.all()
        else:
            products = Product.objects.filter(id=pk) 
        serializer = UserProductSerializer(products, many=True)
        return Response({"status":True ,"massage":"successfull Completed",'data':serializer.data},status=status.HTTP_200_OK)

    def put(self,request,pk,format=None):
        product = ""
        
        product = Product.objects.get(id=str(pk)) 
        serializer = UserProductSerializer(product, data=request.data)
        if serializer.is_valid(raise_exception=True):
            product = serializer.save()
            return Response({"status":True, "massage":"Update Successfully", "data":serializer.data}, status=status.HTTP_201_CREATED)
        else:   
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)   
    
    def delete(self,request,pk=None):
        try:
            product = Product.objects.filter(id=pk)
        except Product.DoesNotExist:
            return Response({"status":"error"})
    
        product.delete()    
        return Response({"massage":"Deleted Successfully"})


class OrderView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        print(request.user)
   
        # validate user by request.user and get user id
        user = User.objects.get(email = request.user) # email=pragnesh@gmail.com # 1=pragnesh@gmail.com
        print(user.id)    # get user id

        # validate product by request.data["product"] and get product id
        try:
            product = Product.objects.get(name=request.data["product"])
        except Product.DoesNotExist:
            return Response({"message":"Product Detail Not Found"}, status=status.HTTP_404_NOT_FOUND)
        
        print(product)
        
        request.data["user"] = user.id
        request.data["product"] = product.id
        
        serializer = UserOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':True, 'massage':'Order successful', 'data':serializer.data}, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response({'error':{'non_field_errors':['Order Details is not Valid']}},status=status.HTTP_404_NOT_FOUND)
        

    def get(self,request,pk=None,format=None):
        order =""
        if pk is None:
            order = Order.objects.all()
        else:
           order = Order.objects.filter(id=pk)
        serializer =  UserOrderSerializer(order, many=True)  
        return Response({"status":True ,"massage":"Order successfull Completed",'data':serializer.data},status=status.HTTP_200_OK)
    
    


    def put(self,request,pk=None,format=None):
        order = ""
         
        order = Order.objects.get(id=str(pk))  #chack user
        serializer = UserOrderSerializer(order, data=request.data)
        if serializer.is_valid(raise_exception=True):
            order = serializer.save()
            return Response({"status":True, "massage":"Update Successfully", "data":serializer.data}, status=status.HTTP_201_CREATED)
        else:    
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request,pk=None):
        try:
            order = Order.objects.filter(id=pk)    
        except Order.DoesNotExist:
            return Response({"status":"Error"})
            
        order.delete()  
        return Response({"massage":"Deleted Successfully"}) 
    
    # request.user is always use to only for user(means only for login person) 


class ChangePasswordView(APIView):
    def put(self,request,format=None):
        email = request.data.pop("email")
        password = request.data.pop("password")
        user = authenticate(email=email, password=password)

        if user is not None:
            serializer = ChangePasswordSerializer(data=request.data, context={'user':user})
            if serializer.is_valid(raise_exception=True):
                # serializer.save() 
                return Response({"status":True,"massage":"password change successfull"},status=status.HTTP_200_OK)
            else:
                return Response({"Error":{'non_field_errors':["password is not valid"]}},status=status.HTTP_404_NOT_FOUND)
        return Response({"Error":{'non_field_errors':["password is not valid"]}},status=status.HTTP_404_NOT_FOUND)

class SentEmail(APIView): 
    
    def post(self,request,format=None):
        print(request.data)
        email = request.data.pop("email")
        base64_encoded_id = urlsafe_base64_encode(force_bytes(email))
        link = "http://127.0.0.1:8000/api/user/resetpassword/?uid=%s"%(base64_encoded_id)
        email_subject = 'test'
        to = email
        print(to)
        subject, from_email, to = email_subject, settings.EMAIL_HOST_USER, to
        print(subject ,from_email,to)
        message = "django based test email"
        mssg = EmailMessage(subject, message, from_email, [to],)
        mssg.send(fail_silently=False)
        print(mssg)
        

        return Response({"link":link})
       
class ResetPassword(APIView):
    def post(self, request):
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        print(request.POST.get('email'), "hello")
        if password1 == password2:
            user = User.objects.filter(email=str(request.POST.get('email')))   # chack user     
            password = make_password(password1)
            user.update(password=password)
            return HttpResponse("password updated")
        else:
            return HttpResponse("password doesn't match")


     
    def get(self, request):
        email = urlsafe_base64_decode(request.query_params.get('uid')).decode('UTF-8')
        print(email)
        # decode uid
        # return render(request, "resetpassword.html", {"email":email})
        return render(request,"password.html",{"email":email})

class GeneratePdf(View):
     def get(self, request, *args, **kwargs):
        
        #getting the template
        pdf = render_to_pdf('invoice.html')
         
         #rendering the template
        return HttpResponse(pdf, content_type='application/pdf')


class HomeView(APIView):
    permission_classes = (IsAuthenticated,)                    # user authanticate(user are not register so it can't access the api(data))
    
    def get(self,request,format=None):
        data_dict = dict()
        data_list = []
        user = request.user                                                     # user check      
        if user is not None:      
            user = User.objects.get(email=str(user))                                # validate user by email
            order = Order.objects.filter(user_id = user.id)                          # get order = by user id 
            for x in order:                                                         # for x in order
                product = Product.objects.get(id = x.product.id)                    # Filter product id
                # print(product) 
                product_data = {                                                # product dict
                    "name": product.name, 
                    "description":product.description,
                    "price":product.price
                }

                order_data={                                                #order Dic        
                    "name": x.name,
                    "quantity": x.quantity,
                    "price": x.price,
                    "product": product_data
                }
                data_list.append(order_data)                                # data_list append                                               
            data_dict["orders"] = data_list                                 # dic into list        
            print(data_dict)                                                                                                              # x.product                                                                          # get product by x.product
            return Response({"status":True, "massage":"Successfully" ,"data":data_dict})              # response success
        else:                                                                                          # not valid
           return Response({"massage":"fail"})







