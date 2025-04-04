import calendar
import qrcode
import base64
import requests
from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.views import View
from django.db import models
from django.utils.dateparse import parse_date
from inventory.models import CheapItem, ExpensiveItem, ExpensiveItemData, BorrowItemList
from user.utils import get_google_profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .serializers import CheapItemListSerializer, ExpensiveItemListSerializer, CombinedItemSerializer, CheapItemDetailSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, DjangoModelPermissions
from rest_framework.authentication import SessionAuthentication
from rest_framework import mixins, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import CheapItem, ExpensiveItem, ExpensiveItemData, BorrowItemList
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
        print("PATH",request.path)

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
        
        # Get month name for display
        month_name = calendar.month_name[month]
        
        # Get calendar HTML
        cal = calendar.HTMLCalendar()
        month_calendar = cal.formatmonth(year, month)
        
        # Get borrowing data for the current month
        first_day = date(year, month, 1)
        if month == 12:
            next_month_date = date(year + 1, 1, 1)
        else:
            next_month_date = date(year, month + 1, 1)
        
        # Query all borrow items that overlap with the current month
        borrow_items = BorrowItemList.objects.filter(
            # Find items of the current type
            models.Q(cheap_item=item) if isinstance(item, CheapItem) else models.Q(expensive_item_data__expensive_item=item),
            # That have a date range overlapping with this month
            models.Q(date_start__lt=next_month_date) & models.Q(date_end__gte=first_day)
        )
        
        # Calculate availability for each day of the month
        available_stock = item.stock - item.amount_reserve  # Using amount_reserve instead of amount_reserved_rn
        day_availability = {}
        
        # Initialize availability for each day in the month
        month_days = calendar.monthrange(year, month)[1]
        for day in range(1, month_days + 1):
            current_date = date(year, month, day)
            day_availability[current_date] = available_stock
        
        # Subtract borrowed quantities for each day
        for borrow_item in borrow_items:
            # Check if date_start is a datetime object, if so, convert to date
            if hasattr(borrow_item.date_start, 'date'):
                start_date = max(borrow_item.date_start.date(), first_day)
            else:
                # Already a date object
                start_date = max(borrow_item.date_start, first_day)
                
            # Check if date_end is a datetime object, if so, convert to date
            if hasattr(borrow_item.date_end, 'date'):
                end_date = min(borrow_item.date_end.date(), next_month_date - timezone.timedelta(days=1))
            else:
                # Already a date object
                end_date = min(borrow_item.date_end, next_month_date - timezone.timedelta(days=1))
            
            # For each day in the booking range, decrease availability
            current = start_date
            while current <= end_date:
                if current.month == month and current.year == year:
                    day_availability[current] -= borrow_item.quantity
                current += timezone.timedelta(days=1)

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(month_calendar, 'html.parser')
        
        table = soup.find('table')
        if table:
            table['class'] = 'calendar-table'
        
        # day cells in td
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
                    cell['class'] = "no-availability"
                elif available < (item.stock - item.amount_reserve) * 0.3:
                    cell['class'] = "low-availability"
                
                cell.append(avail_span)
        
        # Convert back to HTML
        modified_calendar = str(soup)
        
        # Set default dates for the form (today and a week from today)
        default_start_date = today
        default_end_date = date.fromordinal(today.toordinal() + 7)  # 7 days later
        
        context = {
            'item': item,
            'calendar': mark_safe(modified_calendar),
            'prev_month': prev_month,
            'prev_year': prev_year,
            'next_month': next_month,
            'next_year': next_year,
            'default_start_date': default_start_date,
            'default_end_date': default_end_date,
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request, item_id, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")  # Redirect to login if not authenticated
        
        item = CheapItem.objects.filter(component_id=item_id).first() or ExpensiveItem.objects.filter(component_id=item_id).first()
        
        if not item:
            return render(request, '404.html', status=404)
        
        # Get form data
        quantity = request.POST.get("quantity")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        
        # Process valid inputs
        if quantity and quantity.isdigit():
            try:
                quantity = int(quantity)
                start_date_obj = parse_date(start_date)
                end_date_obj = parse_date(end_date)

                if quantity > 0 and start_date_obj and end_date_obj and start_date_obj < end_date_obj:
                    # Check if borrowing this quantity would make availability negative on any day
                    available_stock = item.stock - item.amount_reserve
                    
                    # Get all existing bookings that overlap with the requested date range
                    overlapping_bookings = BorrowItemList.objects.filter(
                        models.Q(cheap_item=item) if isinstance(item, CheapItem) else models.Q(expensive_item_data__expensive_item=item),
                        models.Q(date_start__lte=end_date_obj) & models.Q(date_end__gte=start_date_obj)
                    )
                    
                    # Check availability for each day in the requested range
                    current_date = start_date_obj
                    can_borrow = True
                    
                    while current_date <= end_date_obj:
                        # Start with the available stock
                        daily_available = available_stock
                        
                        # Subtract quantities from existing bookings for this day
                        for booking in overlapping_bookings:
                            if booking.date_start <= current_date and booking.date_end >= current_date:
                                daily_available -= booking.quantity
                        
                        # Now check if we can accommodate the new request
                        if daily_available - quantity < 0:
                            can_borrow = False
                            break
                        
                        current_date += timezone.timedelta(days=1)
                    
                    if can_borrow:
                        # Create a new borrow item
                        new_item = BorrowItemList(
                            user=request.user,
                            quantity=quantity,
                            date_start=start_date_obj,
                            date_end=end_date_obj
                        )
                        
                        # Set the appropriate item type
                        if isinstance(item, CheapItem):
                            new_item.cheap_item = item
                            new_item.quantity_specified = False
                        else:
                            # For expensive items
                            expensive_item_data = None
                            # Try to find an available ExpensiveItemData object
                            available_data = ExpensiveItemData.objects.filter(
                                expensive_item=item,
                                item_status='A'  # Available status
                            ).first()
                            
                            if available_data:
                                expensive_item_data = available_data
                            
                            new_item.expensive_item_data = expensive_item_data
                            new_item.quantity_specified = True
                        
                        new_item.date_specified = True
                        new_item.save()
                        print(f"Added item to borrow list: {item_id} - {quantity} units from {start_date_obj} to {end_date_obj}")
                        
                        # Redirect to borrow list view after successful addition
                        return redirect("borrow_list_view")
                    else:
                        # If borrowing would make availability negative, redirect back with an error
                        # In a real application, you'd add an error message here
                        print(f"Cannot borrow: Not enough availability for the requested dates")
                        messages.error(request, "Not enough items left to borrow.")
                        return self.get(request, item_id, *args, **kwargs)  
            except (ValueError, TypeError) as e:
                print(f"Error adding item to borrow list: {e}")
        
        # If something went wrong, redirect back to the item detail page
        return redirect("detail", item_id=item_id)


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

class UserBorrowItemsView(APIView):
    def get(self, request, user_id):
        try:
            # Get all borrow items for the user
            borrow_items = BorrowItemList.objects.filter(user_id=user_id)

            if not borrow_items.exists():
                return Response({"message": "No borrowed items found for this user"}, status=status.HTTP_404_NOT_FOUND)

            # You'll need to create a BorrowItemListSerializer
            # For now, returning a basic response
            result = []
            for item in borrow_items:
                item_data = {
                    "borrow_id": item.borrow_id,
                    "user": item.user.username,
                    "quantity": item.quantity,
                    "date_start": item.date_start,
                    "date_end": item.date_end,
                }
                
                if item.expensive_item_data:
                    item_data["item_name"] = item.expensive_item_data.expensive_item.name
                    item_data["item_type"] = "expensive"
                elif item.cheap_item:
                    item_data["item_name"] = item.cheap_item.name
                    item_data["item_type"] = "cheap"
                
                result.append(item_data)
                
            return Response(result, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BorrowItemsView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view

    def get(self, request):
        try:
            # Fetch all borrowed items for the authenticated user
            borrow_items = BorrowItemList.objects.filter(user=request.user)
            
            # You'll need to create a BorrowItemListSerializer
            # For now, returning a basic response
            result = []
            for item in borrow_items:
                item_data = {
                    "borrow_id": item.borrow_id,
                    "quantity": item.quantity,
                    "date_start": item.date_start,
                    "date_end": item.date_end,
                }
                
                if item.expensive_item_data:
                    item_data["item_name"] = item.expensive_item_data.expensive_item.name
                    item_data["item_type"] = "expensive"
                elif item.cheap_item:
                    item_data["item_name"] = item.cheap_item.name
                    item_data["item_type"] = "cheap"
                
                result.append(item_data)
                
            return Response(result, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from rest_framework.generics import ListAPIView

class CheapItemAPIListView(ListAPIView):
    queryset = CheapItem.objects.all()
    serializer_class = CheapItemListSerializer
    permission_classes = [AllowAny]  # No authentication required

# View for ExpensiveItem
class ExpensiveItemAPIListView(ListAPIView):
    queryset = ExpensiveItem.objects.all()
    serializer_class = ExpensiveItemListSerializer
    permission_classes = [AllowAny]  # No authentication required

# def borrow_list_view(request):
#     """Displays the borrow items and allows adding items with quantity and borrow dates."""
#     if request.user.is_authenticated:
#         user = request.user
#     else:
#         return redirect("login")
#     print(f"displaying borrow list of user {user.username}, id: {user.user_id}")

#     borrow_items = BorrowItemList.objects.filter(user=user)
#     print(borrow_items)
#     all_items = list(CheapItem.objects.all()) + list(ExpensiveItem.objects.all())
    
#     today = date.today()
    
#     return render(request, "borrow_list.html", {
#         "borrow_items": borrow_items, 
#         "all_items": all_items,
#         "today": today  # Pass today's date to the template
#     })

def borrow_list_view(request):
    """Displays the borrow items and allows adding items with quantity and borrow dates."""
    if request.user.is_authenticated:
        user = request.user
    else:
        return redirect("login")
    print(f"displaying borrow list of user {user.username}, id: {user.user_id}")

    today = date.today()
    borrow_items = BorrowItemList.objects.filter(user=user)
    upcoming_items = []
    current_items = []
    history_items = []
    todays_pickup_items = []

    for item in borrow_items:
        if item.date_start == today:
            todays_pickup_items.append(item)
        elif item.date_start > today:
            upcoming_items.append(item)
        elif item.date_start < today <= item.date_end:
            current_items.append(item)
        elif item.date_end < today:
            history_items.append(item)

    return render(request, 'borrow_list.html', {
        'borrow_items': borrow_items,
        'todays_pickup_items': todays_pickup_items,
        'upcoming_items': upcoming_items,
        'current_items': current_items,
        'history_items': history_items,
        'today': today
    })

def add_to_borrow_list(request, item_id):
    """Adds an item to the borrow list with default values and notifies external service."""
    if not request.user.is_authenticated:
        return redirect("login")  # Redirect to login if not authenticated
    
    user = request.user
    today = date.today()
    start_date = today
    end_date = start_date + timezone.timedelta(days=6)  # Default borrow period = 1 week

    # Try to find the item
    cheap_item = CheapItem.objects.filter(component_id=item_id).first()
    expensive_item = ExpensiveItem.objects.filter(component_id=item_id).first()

    if cheap_item or expensive_item:
        item = cheap_item or expensive_item
        available_stock = item.stock - item.amount_reserve

        overlapping_bookings = BorrowItemList.objects.filter(
            models.Q(cheap_item=item) if isinstance(item, CheapItem) else models.Q(expensive_item_data__expensive_item=item),
            models.Q(date_start__lte=end_date) & models.Q(date_end__gte=start_date)
        )

        current_date = start_date
        can_borrow = True

        while current_date <= end_date:
            daily_available = available_stock
            for booking in overlapping_bookings:
                if booking.date_start <= current_date and booking.date_end >= current_date:
                    daily_available -= booking.quantity

            if daily_available - 1 < 0:
                can_borrow = False
                break

            current_date += timezone.timedelta(days=1)

        if can_borrow:
            borrow_item = BorrowItemList(
                user=user,
                quantity=1,
                date_start=start_date,
                date_end=end_date,
                date_specified=True
            )

            if cheap_item:
                borrow_item.cheap_item = cheap_item
                borrow_item.quantity_specified = False
            else:
                expensive_item_data = ExpensiveItemData.objects.filter(
                    expensive_item=expensive_item,
                    item_status='A'
                ).first()

                borrow_item.expensive_item_data = expensive_item_data
                borrow_item.quantity_specified = True

            borrow_item.save()

            # Call external API to notify another server
            api_url = "http://152.42.220.156:8030/service_requests/new"
            api_payload = {
                "request_id": borrow_item.id,  # Use the borrow item ID as request_id
                "organization_name": "YourOrganization",
                "organization_password": "YourSecretPassword",
                "use_dates": [start_date.strftime("%Y-%m-%d")]
            }

            try:
                response = requests.post(api_url, json=api_payload)
                response.raise_for_status()  # Raises an error if response is unsuccessful
            except requests.RequestException as e:
                print(f"Failed to notify service: {e}")  # Log the error

    return redirect("borrow_list_view")

def remove_from_borrow_list(request, booking_id):
    """Removes a specific booking from the borrow list."""
    if not request.user.is_authenticated:
        return redirect("login")
    
    user = request.user
    
    # Delete the borrow item if it exists and belongs to the user
    BorrowItemList.objects.filter(
        user=user, 
        borrow_id=booking_id
    ).delete()
    
    return redirect("borrow_list_view")

def get_qr_code(request, booking_id):
    """Generate QR code for a specific booking."""
    if not request.user.is_authenticated:
        return redirect("login")
    
    booking = get_object_or_404(BorrowItemList, borrow_id=booking_id, user=request.user)
    
    if booking.cheap_item:
        item_name = booking.cheap_item.name
        item_type = "cheap"
    elif booking.expensive_item_data:
        item_name = booking.expensive_item_data.expensive_item.name
        item_type = "expensive"
    else:
        raise Http404("Invalid booking")
    
    user = request.user.username
    request_id = booking_id
    organization_name = "SE_Locker"
    
    api_url = f"http://152.42.220.156:8030/qr/obtain_qr_str?user={user}&request_id={request_id}&organization_name={organization_name}"
    
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            qr_str = response.text
            
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(qr_str)
            qr.make(fit=True)
            img = qr.make_image(fill="black", back_color="white")
            
            # Convert QR code to base64 string
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            context = {
                "qr_code": img_str,
                "booking": booking,
                "item_name": item_name,
                "item_type": item_type
            }
            
            return render(request, "qr_display.html", context)
        else:
            # Handle API error
            return render(request, "error.html", {"message": f"API Error: {response.status_code}\n{user}, {request_id}, {organization_name}"})
    
    except Exception as e:
        # Handle other errors
        return render(request, "error.html", {"message": f"Error generating QR code: {str(e)}"})