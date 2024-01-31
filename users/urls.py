from django.urls import path,include
# from django.conf.urls import url
from .views import *
from rest_framework import routers
from users import views

router = routers.DefaultRouter()
router.register('',AllUsersViewset,basename='all-users')

app_name = 'users'


urlpatterns = [
    # user
    path('all-users/', include(router.urls)),
    path("user/api/profile/", UserProfileView.as_view(), name="api-users-profile"),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('github-login/', GitHubLoginView.as_view(), name='github-login'),
    path('api/generate-access-token/', GenerateTokenView.as_view(), name='generate-access-token'),
    path('api/authorize-access-token/', GenerateAuthorizationURL.as_view(), name='authorize-access-token'),
    path('github-user-data/', GitHubUserDataView.as_view(), name='github-user-data'),
    path('microsoft/login/', MicrosoftLoginView.as_view(), name='onedrive-login'),
    # path('onedrive_auth', MicrosoftCallbackView.as_view(), name='onedrive-callback'),
    path('onedrive_auth', MicrosoftCallbackView.as_view(), name='onedrive-callback'),
    path('onedrive/userdetails/',OneDriveUserDetails.as_view())
    

]