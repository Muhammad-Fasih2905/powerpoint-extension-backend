from rest_framework import serializers
from dj_rest_auth.registration.serializers import SocialLoginSerializer
import requests
from  rest_framework import serializers
from  .models import *



# user

# signup serilaizer

# class SignUpSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only = True)
    
#     class Meta:
#         model = User
#         fields = ('id','first_name','last_name','email','username','created_at','password', 'is_superuser', 'is_staff', 'is_active',)
#         # extra_kwargs = {'password':{'write_only':True}}
        
#     def create(self,validated_data):
#         password = validated_data.pop("password")
#         print("pswf",password)
#         user = User(**validated_data)
#         user.set_password(password)
#         user.is_superuser = True  # Assign a boolean value instead of a string
#         user.is_active = True  # Assign a boolean value instead of a string
#         user.is_staff = True
#         user.save()
#         return user
        

# # UserSerilaizer

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=User
#         fields = ['id', 'first_name', 'last_name', 'username', 'email', 'is_superuser', 'is_staff', 'is_active', 'created_at']
        



from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# import slugify
from django.utils.text import slugify


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # token['email'] = user.email
        return token



class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email','name')

class AllUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        exclude = ['password','groups','user_permissions']


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id','username', 'email', 'password','is_superuser','is_staff']
        extra_kwargs = {
            'name': {'required': False},
        }



    def create(self, validated_data):
        # Generate a username based on the user's email without checking for uniqueness
        email = validated_data.get('email')
        username = slugify(email.split('@')[0])

        user = User.objects.create(
            username=username,  # Assign the generated username
            name=validated_data.get('name'),
            email=validated_data['email'],
            is_superuser=validated_data['is_superuser'],
            is_staff=validated_data['is_staff'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
    
    
    
    
    


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        exclude = ['password','groups','user_permissions','first_name','last_name','last_login']


    







class GitHubLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)



class AccessTokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)



class CustomGitHubLoginSerializer(SocialLoginSerializer):
    def validate(self, attrs):
        attrs = super(CustomGitHubLoginSerializer, self).validate(attrs)

        # Get the user info from GitHub using the access token
        access_token = attrs['access_token']
        user_info_url = 'https://api.github.com/user'

        headers = {'Authorization': f'token {access_token}'}
        response = requests.get(user_info_url, headers=headers)

        if response.status_code == 200:
            extra_data = response.json()
            print(extra_data,"1111111111111111111111")

            # Set the response data explicitly only if the user is authenticated
            if self.context['request'].user.is_authenticated:
                attrs['user'] = self.context['request'].user
            attrs['extra_data'] = extra_data

        return attrs
    



    def to_representation(self, instance):
        ret = super(CustomGitHubLoginSerializer, self).to_representation(instance)
        ret['extra_data'] = self.extra_data
        return ret

    





# class CustomGitHubLoginSerializer(GitHubLoginSerializer):
#     def validate(self, attrs):
#         attrs = super(CustomGitHubLoginSerializer, self).validate(attrs)

#         # Get the user info from GitHub using the access token
#         access_token = attrs['access_token']
#         user_info_url = 'https://api.github.com/user'

#         headers = {'Authorization': f'token {access_token}'}
#         response = requests.get(user_info_url, headers=headers)

#         if response.status_code == 200:
#             extra_data = response.json()
#             print(extra_data, "1111111111111111111111")

#             # Set the response data explicitly only if the user is authenticated
#             if self.context['request'].user.is_authenticated:
#                 attrs['user'] = self.context['request'].user
#             attrs['extra_data'] = extra_data

#         return attrs

#     def to_representation(self, instance):
#         # Call the parent class's to_representation method to get the default representation
#         data = super().to_representation(instance)
#         print(data, '2222222222222222222222')

#         # Add the extra_data to the response
#         if 'extra_data' in data:
#             data.update(data['extra_data'])

#         return data