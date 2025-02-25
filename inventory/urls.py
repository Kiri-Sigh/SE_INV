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
    UserCartView,
    CombinedItemPaginationListView,
    CheapItemDetailView
)
urlpatterns = [
    path('cheap-items/', CheapItemListView.as_view(), name='cheap-items-list'),  # View for Cheap Items
    path('expensive-items/', ExpensiveItemListView.as_view(), name='expensive-items-list'),  # View for Expensive Items

    # Pagination Views for Cheap and Expensive Items
    path('cheap-items-pagination/', CheapItemPaginationListView.as_view(), name='cheap-items-pagination'),
    path('expensive-items-pagination/', ExpensiveItemPaginationListView.as_view(), name='expensive-items-pagination'),
    path('main-items/', CombinedItemPaginationListView.as_view(), name='main-items'),
    path("cp-item/<uuid:component_id>/", CheapItemDetailView.as_view(), name="cheap-item-detail"),

    # UserCart view
    path('user-cart/<int:id>/', UserCartView.as_view(), name='user-cart-view'),
]