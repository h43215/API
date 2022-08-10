from rest_framework import serializers
from apiapp.models import Product
from apiapp.models import User
from apiapp.models import Order


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=['email','name','password']
        extra_kwargs={
            'password':{'write_only':True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)    

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email','password']   
        # extra_kwargs = {
        #     'password':{"write_only":True}, 
        # }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User         
        fields = ['id','name']

class UserProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','stock','price','description','image']  
        extract_kwargs={
            "id":{"read_only":True},
            "product":{'write_only':True}
        }     

    def create(self, validated_data):
        product = Product.objects.create(
            name = validated_data['name'],
            stock = validated_data['stock'],
            price = validated_data ['price'],
            description = validated_data ['description'],
            image = validated_data ['image']
        )

        product.save()
        return product 


class UserOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','name','product','quantity','price', 'user']
        extract_kwargs={
            "id":{"read_only":True},
            "order":{'write_only':True},
        }
    
    def create(self,validate_data): 
        order = Order.objects.create(
            name = validate_data['name'],
            product = validate_data['product'],
            quantity = validate_data['quantity'],
            price = validate_data['price'],
            user = validate_data["user"]
        )
        order.save()
        return order

# User Change Password Serializer Code Start #
class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=255, write_only=True, style={'input_type':'password'})
    new_password2 = serializers.CharField(max_length=255, write_only=True, style={'input_type':'password'})

    class Meta:
        fields = ['new_password', 'new_password2']

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        new_password2 = attrs.get('new_password2')
        user = self.context.get('user')
        
        if new_password != new_password2:
            raise serializers.ValidationError("Password and Confirm Password Doesn't Match")
        user.set_password(new_password)
        user.save()
        return user
# User Change Password Serializer Code End #

    

