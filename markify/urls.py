"""markify URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""








from django.contrib import admin
from django.urls import path,include,re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authentication import BasicAuthentication
from rest_framework import permissions
from django.views.generic.base import TemplateView





urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls', namespace='social')),
    path('visual/',include('visual.urls', namespace='visual')),
    path('global-search/',include('GlobalSearch.urls')),
    path('accounts/', include('allauth.urls')),

]


api_info = openapi.Info(
    title="Markify APIs.",
    default_version="v1",
    description="Apis documentation for Markify.",
)



schema_view = get_schema_view(
    api_info,
    public=True,
    authentication_classes=(BasicAuthentication,),
    permission_classes=(permissions.IsAuthenticated,),
)


admin.site.site_header = "Markify App"
admin.site.site_title = "Markify App Admin Portal"
admin.site.index_title = "Markify App Admin"


urlpatterns += [
    path("api-docs/", schema_view.with_ui("swagger", cache_timeout=0), name="api_docs"),
]



urlpatterns += [path("", TemplateView.as_view(template_name='index.html'))]
# urlpatterns += [re_path(r"^(?:.*)/?$",
#                 TemplateView.as_view(template_name='index.html'))]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
