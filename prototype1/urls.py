"""
URL configuration for prototype1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from user.views import social_profile
from prototype1.views import login_view#google_login


# urlpatterns = [
#     path('admin/', admin.site.urls),
#         #login URL = http://127.0.0.1:8000/auth/login/google-oauth2/
#     #after login visit = http://127.0.0.1:8000/social-profile/
#     #logouot = http://127.0.0.1:8000/logout/
#     path('auth/', include('social_django.urls', namespace='social')),
#     path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout URL
#     #test when login get gmail user data
#     path("social-profile/", social_profile, name="social_profile"),
#     path('login/', login_view, name='login'),
#    # path('login/google/', google_login, name='google_login'),


# ]


urlpatterns = [
    path('admin/', admin.site.urls),
    # Ensure this line is present for social authentication
    path('auth/', include('social_django.urls', namespace='social')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("social-profile/", social_profile, name="social_profile"),
    path('login/', login_view, name='login'),
]