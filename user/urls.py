from django.urls import path, include
from django.contrib.auth import views as auth_views
from user.views import social_profile
    

urlpatterns = [
    #login URL = http://127.0.0.1:8000/auth/login/google-oauth2/
    #after login visit = http://127.0.0.1:8000/social-profile/
    #logouot = http://127.0.0.1:8000/logout/
    path('auth/', include('social_django.urls', namespace='social')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout URL
    #test when login get gmail user data
    path("social-profile/", social_profile, name="social_profile"),

]