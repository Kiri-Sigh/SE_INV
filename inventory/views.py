import calendar
import uuid
from django.shortcuts import render, redirect

from datetime import date
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.views import View
from django.db import models
from django.utils.dateparse import parse_date
from inventory.models import CheapItem, ExpensiveItem
from user.utils import get_google_profile

from django.contrib.auth.decorators import login_required
from .serializers import CheapItemListSerializer, ExpensiveItemListSerializer,CombinedItemSerializer,CheapItemDetailSerializer,UserCartSerializer, UserCartItemSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny,DjangoModelPermissions
from rest_framework.authentication import SessionAuthentication
from rest_framework import mixins, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import CheapItem, ExpensiveItem,UserCart, UserCartItem
from user.models import CustomUser

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
        
        # Get calendar HTML
        cal = calendar.HTMLCalendar()
        month_calendar = cal.formatmonth(year, month)
        
        # Get borrowing data for the current month
        first_day = date(year, month, 1)
        if month == 12:
            next_month_date = date(year + 1, 1, 1)
        else:
            next_month_date = date(year, month + 1, 1)
        
        # Query all cart items that overlap with the current month
        cart_items = UserCartItem.objects.filter(
            # Find items of the current type
            models.Q(cheap_item=item) if isinstance(item, CheapItem) else models.Q(expensive_item_data__expensive_item=item),
            # That have a date range overlapping with this month
            models.Q(date_start__lt=next_month_date) & models.Q(date_end__gte=first_day)
        )
        
        # Calculate availability for each day of the month
        total_stock = item.stock
        day_availability = {}
        
        # Initialize availability for each day in the month
        month_days = calendar.monthrange(year, month)[1]
        for day in range(1, month_days + 1):
            current_date = date(year, month, day)
            day_availability[current_date] = total_stock
        
        # Subtract borrowed quantities for each day
        for cart_item in cart_items:
            # Check if date_start is a datetime object, if so, convert to date
            if hasattr(cart_item.date_start, 'date'):
                start_date = max(cart_item.date_start.date(), first_day)
            else:
                # Already a date object
                start_date = max(cart_item.date_start, first_day)
                
            # Check if date_end is a datetime object, if so, convert to date
            if hasattr(cart_item.date_end, 'date'):
                end_date = min(cart_item.date_end.date(), next_month_date - timezone.timedelta(days=1))
            else:
                # Already a date object
                end_date = min(cart_item.date_end, next_month_date - timezone.timedelta(days=1))
            
            # For each day in the booking range, decrease availability
            current = start_date
            while current <= end_date:
                if current.month == month and current.year == year:
                    day_availability[current] -= cart_item.quantity
                current += timezone.timedelta(days=1)
        
        # Convert the calendar HTML to a modifiable format (with availability information)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(month_calendar, 'html.parser')
        
        # Find all day cells (td elements)
        day_cells = soup.find_all('td')
        
        for cell in day_cells:
            # Skip cells without a day number
            if not cell.text.strip().isdigit():
                continue
            
            day_num = int(cell.text.strip())
            current_date = date(year, month, day_num)
            
            if current_date in day_availability:
                available = day_availability[current_date]
                
                # Add availability info to cell
                avail_span = soup.new_tag('span')
                avail_span['class'] = 'availability'
                avail_span.string = f" ({available} available)"
                
                # Style based on availability
                if available <= 0:
                    cell['style'] = "background-color: #ffaaaa;" # Light red for no availability
                elif available < item.stock * 0.3:
                    cell['style'] = "background-color: #ffddaa;" # Orange for low availability
                
                cell.append(avail_span)
        
        # Convert back to HTML
        modified_calendar = str(soup)
        
        context = {
            'item': item,
            'calendar': mark_safe(modified_calendar),
            'prev_month': prev_month,
            'prev_year': prev_year,
            'next_month': next_month,
            'next_year': next_year,
        }
        
        return render(request, self.template_name, context)


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
    def get(self, request, user_id):
        try:
            # Ensure to prefetch related user cart items using the correct related_name
            user_cart = UserCart.objects.filter(user_id=user_id).prefetch_related("user_cart_item_Exp_item_data")

            if not user_cart.exists():
                return Response({"message": "No carts found for this user"}, status=status.HTTP_404_NOT_FOUND)

            # Serialize the user cart data, including nested cart items
            serializer = UserCartSerializer(user_cart, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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

def get_cart_user(request):
    """Returns the appropriate user for the cart: logged-in user or the superuser for guest users."""
    if request.user.is_authenticated:
        return request.user
    
    # For guest users, get or create the guest/superuser
    guest_user_id = "02982694-b38a-4adc-b014-0755af684d91"  # Superuser ID
    
    try:
        # Try to get the existing superuser
        guest_user = CustomUser.objects.get(user_id=guest_user_id)
    except CustomUser.DoesNotExist:
        # Create the superuser if it doesn't exist
        guest_user = CustomUser.objects.create(
            user_id=guest_user_id,
            username="guest_cart_user",
            email="guest@example.com",
            is_superuser=True,
            is_staff=True
        )
        guest_user.set_password(uuid.uuid4().hex)  # Set a random password
        guest_user.save()
        print(f"Created guest cart user with ID: {guest_user_id}")
    
    return guest_user

def get_or_create_cart(user):
    """Gets or creates a cart for the given user."""
    cart, created = UserCart.objects.get_or_create(user=user)
    return cart

def cart_view(request):
    """Displays the cart and allows adding items with quantity and borrow dates."""
    # Debug information
    print("req session", request.session.items())
    print("req user", request.user)
    
    user = get_cart_user(request)
    cart = get_or_create_cart(user)
    
    # Get all items in the user's cart
    items = UserCartItem.objects.filter(user_cart=cart)
    all_items = list(CheapItem.objects.all()) + list(ExpensiveItem.objects.all())
    
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        quantity = request.POST.get("quantity")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        # Try to find the item (either cheap or expensive)
        cheap_item = CheapItem.objects.filter(component_id=item_id).first()
        expensive_item = ExpensiveItem.objects.filter(component_id=item_id).first()
        
        # Process valid inputs
        if (cheap_item or expensive_item) and quantity and quantity.isdigit():
            try:
                quantity = int(quantity)
                start_date = parse_date(start_date)
                end_date = parse_date(end_date)

                if quantity > 0 and start_date and end_date and start_date < end_date:
                    # Create a new cart item
                    new_item = UserCartItem(
                        user_cart=cart,
                        quantity=quantity,
                        date_start=start_date,
                        date_end=end_date
                    )
                    
                    # Set the appropriate item type
                    if cheap_item:
                        new_item.cheap_item = cheap_item
                    else:
                        # Fixed: using expensive_item instead of expensive_item_data
                        new_item.expensive_item_data = None  # Ensure this is null
                        # The model has expensive_item_data field, but we need to check the database
                        # and see if we can find the item in the ExpensiveItemData table
                        expensive_item_data = None
                        # If we can't find it, we'll create the cart item anyway
                        new_item.cheap_item = None
                        new_item.expensive_item_data = expensive_item_data
                    
                    new_item.save()
                    print(f"Added item to cart: {item_id} - {quantity} units from {start_date} to {end_date}")
            except (ValueError, TypeError) as e:
                print(f"Error adding item to cart: {e}")
                
        return redirect("cart_view")
    
    return render(request, "cart.html", {"cart_items": items, "all_items": all_items})

def add_to_cart(request, item_id):
    """Adds an item to the cart with default values."""
    user = get_cart_user(request)
    cart = get_or_create_cart(user)
    
    # Try to find the item
    cheap_item = CheapItem.objects.filter(component_id=item_id).first()
    expensive_item = ExpensiveItem.objects.filter(component_id=item_id).first()
    
    if cheap_item or expensive_item:
        # Create a basic cart item with today's date and 7 days duration
        today = date.today()
        end_date = date.fromordinal(today.toordinal() + 7)  # 7 days later
        
        cart_item = UserCartItem(
            user_cart=cart,
            quantity=1,
            date_start=today,
            date_end=end_date
        )
        
        # Set the appropriate item type
        if cheap_item:
            cart_item.cheap_item = cheap_item
        else:
            # Since we have expensive_item_data in our model but want to use expensive_item
            expensive_item_data = None
            cart_item.expensive_item_data = expensive_item_data
            
        cart_item.save()
    
    return redirect("cart_view")

def remove_from_cart(request, booking_id):
    """Removes a specific booking from the cart."""
    user = get_cart_user(request)
    cart = get_or_create_cart(user)
    
    # Delete the cart item if it exists and belongs to the user's cart
    UserCartItem.objects.filter(
        user_cart=cart, 
        user_cart_item_id=booking_id
    ).delete()
    
    return redirect("cart_view")