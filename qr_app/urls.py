from django.urls import path
from . import views

app_name = 'qr_app'

urlpatterns = [
    path('generate/', views.generate_qr, name='generate_qr'),
    path('log/', views.log_data, name='log_data'),
] 