
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import ProductViewSet
# from django.contrib.auth.decorators import login_required

# router = DefaultRouter()
# router.register(r'products', ProductViewSet)  # Generates full CRUD routes

# urlpatterns = [
#     path('', include(router.urls)),
# ]
from django.urls import path
#from .views import CartView
from .views import (
    CheapItemListView,
    ExpensiveItemListView,
    CheapItemPaginationListView,
    ExpensiveItemPaginationListView,
    UserCartView,CartItemsView,
    CombinedItemPaginationListView,
    CheapItemDetailView
)
from . import views

app_name = 'inventory'

urlpatterns = [
    path('items/', views.MainPage.as_view(), name='list_items'),
    path('items/<uuid:item_id>/', views.DetailPage.as_view(), name='item_detail'),
    path('cheap-items/', CheapItemListView.as_view(), name='cheap-items-list'),  # View for Cheap Items
    path('expensive-items/', ExpensiveItemListView.as_view(), name='expensive-items-list'),  # View for Expensive Items

    path('cheap-items-pagination/', CheapItemPaginationListView.as_view(), name='cheap-items-pagination'),
    path('expensive-items-pagination/', ExpensiveItemPaginationListView.as_view(), name='expensive-items-pagination'),
    #for now to show every item both cp and exp
    path('main-items/', CombinedItemPaginationListView.as_view(), name='main-items'),
    #detail page for the cheap item
    path("cp-item/<uuid:component_id>/", CheapItemDetailView.as_view(), name="cheap-item-detail"),
    #cart items for that cart (user)

    #path('cart-items/<uuid:cart_id>/', CartItemsView.as_view(), name='cart-items'),
    #path('user-cart/<uuid:user_id>/', UserCartView.as_view(), name='user-cart')
    path('cart-items/<uuid:cart_id>/', CartItemsView.as_view(), name='user-cart-view'),
    path('user-cart/<uuid:id>/',UserCartView.as_view(),name='user-cart-view')
]