from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('items/', views.list_items, name='list_items'),
    path('items/<uuid:item_id>/', views.item_detail, name='item_detail'),
] 