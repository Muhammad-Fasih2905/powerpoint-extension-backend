from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics
import requests
from urllib.parse import parse_qs
from urllib.parse import urlencode
from .serializers import AccessTokenSerializer,CustomGitHubLoginSerializer
from allauth.socialaccount.models import SocialAccount
from rest_framework.views import APIView
from rest_framework import status,viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import redirect



# User Authentications APIS Starts Here.

class SignupView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            response_data = {
                "user": serializer.data,
                "access_token": access_token,
                "refresh_token": refresh_token
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        if 'username' not in request.data:
            return Response({"username": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        token = serializer.validated_data.get('access')
        refresh = serializer.validated_data.get('refresh')
        response = {
            'access_token': token,
            'refresh_token': refresh,
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'is_superuser': user.is_superuser,
                'is_staff': user.is_staff,
            }
        }
        return Response(response, status=status.HTTP_200_OK)
    
class AllUsersViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AllUserProfileSerializer
    http_method_names = ["get"]

    # permission_classes = [IsAuthenticated]

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    model = User
    
    
    def get_object(self):
        print(self.request.user)
        return self.request.user


# GitHUb Login APIS Starts Here.

class GitHubLoginView(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    client_class = OAuth2Client
    serializer_class = CustomGitHubLoginSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

class GitHubUserDataView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            github_account = request.user.socialaccount_set.get(provider='github')
        except SocialAccount.DoesNotExist:
            return Response({"detail": "User does not have a connected GitHub account."}, status=status.HTTP_404_NOT_FOUND)
        access_token = github_account.socialtoken_set.get(account=github_account).token
        github_user_url = 'https://api.github.com/user'
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(github_user_url, headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            return Response(user_data, status=status.HTTP_200_OK)
        else:
            error_message = response.json().get('message', 'Failed to retrieve GitHub user data.')
            return Response({"detail": error_message}, status=response.status_code)

class GitHubAccessTokenView(APIView):
    def get(self, request):
        authorization_code = request.query_params.get('code')
        if not authorization_code:
            return Response({'error': 'Authorization code not provided'}, status=status.HTTP_400_BAD_REQUEST)
        params = {
            'client_id': settings.GITHUB_CLIENT_ID,
            'client_secret': settings.GITHUB_CLIENT_SECRET,
            'code': authorization_code,
        }
        response = requests.post('https://github.com/login/oauth/access_token', params=params, headers={'Accept': 'application/json'})
        if response.status_code == 200:
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Failed to exchange authorization code for access token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GenerateTokenView(APIView):
    GITHUB_API_URL = "https://github.com/login/oauth/access_token"
    CLIENT_ID = "4adade2a7a76ad7c2c9d"
    CLIENT_SECRET = "d347f29a7e2bb850682ce29f83ce56633136a324"
    REDIRECT_URI = "https://markify-5b6a5.web.app"
    # REDIRECT_URI = "https://master--reliable-paprenjak-5997fa.netlify.app/"

    def post(self, request, *args, **kwargs):
        authorization_code = request.query_params.get('code')
        if not authorization_code:
            return Response(
                {"error": "Authorization code is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        token_request_data = {
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET,
            "code": authorization_code,
            "redirect_uri": self.REDIRECT_URI,
        }
        response = requests.post(self.GITHUB_API_URL, data=token_request_data)
        if response.status_code == 200:
            response_data = parse_qs(response.text)
            token_value = response_data.get("access_token", [None])[0]
            if token_value:
                serializer = AccessTokenSerializer(data={"token": token_value})
                if serializer.is_valid():
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(
                        {"error": "Failed to serialize token."},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
            else:
                return Response(
                    {"error": "Failed to extract access token from GitHub response."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            return Response(
                {"error": "Failed to obtain GitHub access token."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class GenerateAuthorizationURL(APIView):
    GITHUB_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
    CLIENT_ID = "4adade2a7a76ad7c2c9d"
    REDIRECT_URI = "https://markify-5b6a5.web.app/"
    # REDIRECT_URI = "https://master--reliable-paprenjak-5997fa.netlify.app/"
    SCOPE = "gist"

    def get(self, request, *args, **kwargs):
        authorization_url = "{}?{}".format(
            self.GITHUB_AUTHORIZE_URL,
            urlencode({
                'client_id': self.CLIENT_ID,
                # 'redirect_uri': self.REDIRECT_URI,
                'scope': self.SCOPE,
            })
        )
        return Response({"authorization_url": authorization_url}, status=status.HTTP_200_OK)

# Microsoft Login Apis

class MicrosoftLoginView(APIView):
    def get(self, request):
        onedrive_auth_url = (
            # 'https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize'
            'https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
            f'?client_id={settings.ONEDRIVE_CLIENT_ID}'
            # '&redirect_uri=http://localhost:8000/getAToken'
            f'&redirect_uri={settings.ONEDRIVE_REDIRECT_URI}'
            '&response_type=code'
            '&scope=User.Read Files.ReadWrite'
        )
        print("one drive ", onedrive_auth_url)
        return redirect(onedrive_auth_url)


class MicrosoftCallbackView(APIView):
    def get(self, request):

        
        # Ensure 'code' is in the query parameters
        if 'code' in request.query_params:
            code = request.query_params['code']
            print("code", code)

            token_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
            # token_url = 'https://login.microsoftonline.com/consumers/oauth2/v2.0/token'
            
            token_data = {
                'client_id': settings.ONEDRIVE_CLIENT_ID,
                'client_secret': settings.ONEDRIVE_CLIENT_SECRET,
                'redirect_uri': settings.ONEDRIVE_REDIRECT_URI,
                'code': code,
                'grant_type': 'authorization_code',
                'scope': 'User.Read',
            }

            response = requests.post(token_url, data=token_data)

            if response.status_code == 200:
                access_token = response.json().get('access_token')
                 # Use the access token to make a request to Microsoft Graph API
                graph_url = 'https://graph.microsoft.com/v1.0/me'  # This endpoint retrieves user details
                headers = {'Authorization': f'Bearer {access_token}'}

                graph_response = requests.get(graph_url, headers=headers)

                if graph_response.status_code == 200:
                    user_details = graph_response.json()
                    print("User Details:", user_details)
                # Store or use the access token as needed
                # Example: You may want to associate the access token with the user in your system
                # Update the following line with your logic for storing the access token
                # user = request.user  # Assuming you have a user object
                # user.onedrive_access_token = access_token
                # user.save()

                return Response({'message': 'Authentication successful','access_token':access_token}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Failed to authenticate with OneDrive'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'No code parameter in the callback URL'}, status=status.HTTP_400_BAD_REQUEST)


# onedrive userdetails\


class OneDriveUserDetails(APIView):

    def get(self, request):
        access_token = request.query_params.get('access_token')

        # Use the access token to get user details
        graph_url = 'https://graph.microsoft.com/v1.0/me'
        headers = {'Authorization': f'Bearer {access_token}'}
        graph_response = requests.get(graph_url, headers=headers)

        if graph_response.status_code == 200:
            user_details = graph_response.json()
            print("user details",user_details)
            save_data = "test one drive"

            # Upload data to OneDrive
            upload_url = 'https://graph.microsoft.com/v1.0/me/drive/root:/test.txt:/content'
            upload_headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'text/plain'}

            # Use bytes for the content
            upload_data = save_data.encode('utf-8')

            upload_response = requests.put(upload_url, headers=upload_headers, data=upload_data)
            print("upload resp",upload_response)

            if upload_response.status_code == 201:
                return Response({'message': 'Data saved to OneDrive successfully', 'User Details': user_details},
                                status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Error uploading data to OneDrive'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)


# work for user details 
# class OneDriveUserDetails(APIView):
#     def get(self,request):
#                 access_token =request.query_params.get ('access_token')
#                 print("access_token",access_token)
#                  # Use the access token to make a request to Microsoft Graph API
#                 graph_url = 'https://graph.microsoft.com/v1.0/me'  # This endpoint retrieves user details
#                 headers = {'Authorization': f'Bearer {access_token}'}

#                 graph_response = requests.get(graph_url, headers=headers)

#                 if graph_response.status_code == 200:
#                     user_details = graph_response.json()
#                     save_data = "test one drive "
#                 # Store or use the access token as needed
#                 # Example: You may want to associate the access token with the user in your system
#                 # Update the following line with your logic for storing the access token
#                 # user = request.user  # Assuming you have a user object
#                 # user.onedrive_access_token = access_token
#                 # user.save()

#                     return Response({'message': 'Authentication successful','User Details':user_details}, status=status.HTTP_200_OK)
#                 return Response({'eror':"err"})
    