from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import exchange_google_token
from .views import issue_jwt_token,custom_refresh_token,protected_view
from .views import custom_logout

urlpatterns = [
    #path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login
    #path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh expired token
    path('token/', issue_jwt_token, name='issue-jwt-token'),  # This path issues the JWT token
    path('token/refresh/', custom_refresh_token, name='custom_token_refresh'),
    path('logout/', custom_logout, name='logout'),
    #path('auth/google/login/', exchange_google_token, name="google_login"),
    path('auth/refresh/', custom_refresh_token, name="token_refresh"),
    path('auth/protected/', protected_view, name="protected_view"),
    path('auth/logout/', custom_logout, name="logout"),
]
