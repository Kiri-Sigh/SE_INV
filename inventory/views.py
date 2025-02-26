import calendar
from django.shortcuts import render

from datetime import date
from django.utils.safestring import mark_safe
from django.views import View
from inventory.models import CheapItem, ExpensiveItem
from user.utils import get_google_profile

from django.contrib.auth.decorators import login_required
from .serializers import CheapItemListSerializer, ExpensiveItemListSerializer,CombinedItemSerializer,CheapItemDetailSerializer,UserCartSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authentication import SessionAuthentication
from rest_framework import mixins, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import CheapItem, ExpensiveItem, UserCart
from rest_framework.pagination import PageNumberPagination



def handler404(request, exception=None):
    """Custom 404 handler"""
    template = loader.get_template('404.html')
    return TemplateResponse(request, template, {'error_message': str(exception)}, status=404)

class MainPage(View):
    template_name = 'item_list.html'

    def get(self, request, *args, **kwargs):
        google_data = ""
        if request.user.is_authenticated:
            user = request.user
            google_data = get_google_profile(user)

        query = request.GET.get('q', '')
        cheap_items = CheapItem.objects.all()
        expensive_items = ExpensiveItem.objects.all()

        if query:
            cheap_items = cheap_items.filter(name__icontains=query)
            expensive_items = expensive_items.filter(name__icontains=query)

        context = {
            'cheap_items': cheap_items,
            'expensive_items': expensive_items,
            'query': query,
            'google_data': google_data
        }
        
        return render(request, self.template_name, context)

    def load_items(self):
        """Load all items"""
        query = self.request.GET.get('q', '')
        cheap_items = CheapItem.objects.all()
        expensive_items = ExpensiveItem.objects.all()
        
        if query:
            cheap_items = cheap_items.filter(name__icontains=query)
            expensive_items = expensive_items.filter(name__icontains=query)
            
        return {
            'cheap_items': cheap_items,
            'expensive_items': expensive_items,
            'query': query
        }

class DetailPage(View):
    template_name = 'item_detail.html'

    def get(self, request, item_id, *args, **kwargs):
        item = CheapItem.objects.filter(component_id=item_id).first() or ExpensiveItem.objects.filter(component_id=item_id).first()
        
        if not item:
            return render(request, '404.html', status=404)
        
        today = date.today()
        
        year = request.GET.get("year")
        month = request.GET.get("month")

        if not year or not year.isdigit():
            year = today.year
        else:
            year = int(year)

        if not month or not month.isdigit():
            month = today.month
        else:
            month = int(month)

        prev_month = 12 if month == 1 else month - 1
        prev_year = year - 1 if month == 1 else year

        next_month = 1 if month == 12 else month + 1
        next_year = year + 1 if month == 12 else year

        html_calendar = calendar.HTMLCalendar().formatmonth(year, month)

        context = {
            'item': item,
            'calendar': mark_safe(html_calendar),
            'prev_month': prev_month,
            'prev_year': prev_year,
            'next_month': next_month,
            'next_year': next_year,
        }
        
        return render(request, self.template_name, context)

# from rest_framework import viewsets
# from .models import Product
# from .serializers import ProductSerializer

# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

# View for CheapItem
class CheapItemListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = CheapItem.objects.all()
    serializer_class = CheapItemListSerializer
    permission_classes = [AllowAny]  # No authentication required

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

# View for ExpensiveItem
class ExpensiveItemListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = ExpensiveItem.objects.all()
    serializer_class = ExpensiveItemListSerializer
    permission_classes = [AllowAny]  # No authentication required

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
class CheapItemDetailView(generics.RetrieveAPIView):
    queryset = CheapItem.objects.all()
    serializer_class = CheapItemDetailSerializer
    lookup_field = "component_id"
    permission_classes = [AllowAny]  # Public access


# Custom Pagination
class CustomPagination(PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 'pagination'  # Allow frontend to control page size
    max_page_size = 100

# Mixin-based view for Cheap Items Pagination
class CheapItemPaginationListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = CheapItem.objects.all()
    serializer_class = CheapItemListSerializer
    pagination_class = CustomPagination
    permission_classes = [AllowAny]  # Anyone can access

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)  # Calls the ListModelMixin's list() method

# Mixin-based view for Expensive Items Pagination
class ExpensiveItemPaginationListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = ExpensiveItem.objects.all()
    serializer_class = ExpensiveItemListSerializer
    pagination_class = CustomPagination
    permission_classes = [AllowAny]  # Anyone can access

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)  # Calls the ListModelMixin's list() method




class CombinedItemPaginationListView(generics.GenericAPIView):
    serializer_class = CombinedItemSerializer  # You need a serializer that handles both models
    pagination_class = CustomPagination
    permission_classes = [AllowAny]  # Public access

    def get_queryset(self):
        cheap_items = CheapItem.objects.all()
        expensive_items = ExpensiveItem.objects.all()
        combined_items = list(cheap_items) + list(expensive_items)  # Merge both QuerySets
        return combined_items  # This will cause issues, see next step

    #combines and cheap new filed of cheap or exp item
    # def get(self, request, *args, **kwargs):
    #     page = self.paginate_queryset(self.get_queryset())  # Paginate the merged data
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #     return Response(serializer.data)
    #seperate to different key ,1 key is cheap,another is exp
    def get(self, request, *args, **kwargs):
        cheap_items = CheapItem.objects.all()
        expensive_items = ExpensiveItem.objects.all()

        cheap_serialized = CheapItemListSerializer(cheap_items, many=True).data
        expensive_serialized = ExpensiveItemListSerializer(expensive_items, many=True).data

        return Response({
            "cheap_items": cheap_serialized,
            "expensive_items": expensive_serialized
        })


class UserCartView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view

    def get(self, request, id):
        print("running")

        # Fetch the cart for the given cart_id
        try:
            # Fetch the cart using the cart_id
            cart = UserCart.objects.get(user__user_id=id)
            print("cart",cart)
            # Compare the user_id from the CustomUser (FK) to the authenticated user ID
            if str(cart.user.user_id) != str(request.session._auth_user_id):
                # If the IDs don't match, return a 403 Forbidden response
                return Response({"detail": "You are not allowed to access this cart."}, status=status.HTTP_403_FORBIDDEN)

            # Serialize the cart data
            serializer = UserCartSerializer(cart)

            # Return the serialized data
            return Response(serializer.data)

        except UserCart.DoesNotExist:
            raise Http404
        


class CartItemsView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view

    def get(self, request, cart_id):
        print("running")

        # Fetch the cart for the given cart_id
        try:
            # Fetch the cart using the cart_id
            cart = UserCart.objects.get(cart_id=cart_id)

            # Compare the user_id from the CustomUser (FK) to the authenticated user ID
            if str(cart.user.id) != str(request.user.id):
                # If the IDs don't match, return a 403 Forbidden response
                return Response({"detail": "You are not allowed to access this cart."}, status=status.HTTP_403_FORBIDDEN)

            # Serialize the cart data
            serializer = UserCartSerializer(cart)

            # Return the serialized data
            return Response(serializer.data)

        except UserCart.DoesNotExist:
            raise Http404
from rest_framework.generics import ListAPIView


    
class CheapItemListView(ListAPIView):
    queryset = CheapItem.objects.all()
    serializer_class = CheapItemListSerializer
    permission_classes = [AllowAny]  # No authentication required

# View for ExpensiveItem
class ExpensiveItemListView(ListAPIView):
    queryset = ExpensiveItem.objects.all()
    serializer_class = ExpensiveItemListSerializer
    permission_classes = [AllowAny]  # No authentication required
