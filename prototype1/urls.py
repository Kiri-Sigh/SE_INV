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
from prototype1.views import home_view,home_view2,my_view
from qr_app.views import generate_qr
from prototype1.views import login_view
from api.views import custom_logout
from inventory.views import handler404, MainPage, borrow_list_view, add_to_borrow_list, remove_from_borrow_list

urlpatterns = [
    path('inventory/', include('inventory.urls')),  # app_name is already set in inventory/urls.py
    
    # not refactored yet
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('auth/', include('social_django.urls', namespace='social')),
    path("social-profile/", social_profile, name="social_profile"),
    path('login/', login_view, name='login'),
    path('qr-request/', generate_qr, name='qr-request'),
    path('social/', include('user.urls')),  # Include your app's URLs
    path('api/', include('api.urls')),  # Include the auth API URLs
    path('auth/logout/', custom_logout, name="logout"),
    path('cmd_info/', my_view, name="cmd_info"),
    path('items/', MainPage.as_view()),
    path("borrow-list/", borrow_list_view, name="borrow_list_view"),
    path("borrow-list/add/<uuid:item_id>/", add_to_borrow_list, name="add_to_borrow_list"),
    path("borrow-list/remove/<uuid:booking_id>/", remove_from_borrow_list, name="remove_from_borrow_list"),
]

handler404 = handler404  # Register custom 404 handler
