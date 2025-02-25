from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('items/', views.MainPage.as_view(), name='list_items'),
    path('items/<uuid:item_id>/', views.DetailPage.as_view(), name='item_detail'),
] 