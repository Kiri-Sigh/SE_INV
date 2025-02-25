import calendar
from django.shortcuts import render
from datetime import date
from django.utils.safestring import mark_safe
from inventory.models import CheapItem, ExpensiveItem
from user.utils import get_google_profile


def handler404(request, exception=None):
    """Custom 404 handler"""
    template = loader.get_template('404.html')
    return TemplateResponse(request, template, {'error_message': str(exception)}, status=404)

class MainPage(View):
    template_name = 'item_list.html'

    google_data = ""
    if request.user.is_authenticated:
        user = request.user
        google_data = get_google_profile(user)

    context = {
        'cheap_items': cheap_items,
        'expensive_items': expensive_items,
        'query': query,  # Pass the query back to the template
        'google_data': google_data
    }


        if query:
            cheap_items = cheap_items.filter(name__icontains=query)
            expensive_items = expensive_items.filter(name__icontains=query)
        
        return cheap_items, expensive_items

    def load_items(self):
        """Load all items"""
        cheap_items, expensive_items = self.filter_items()
        return {
            'cheap_items': cheap_items,
            'expensive_items': expensive_items,
            'query': self.request.GET.get('q', '')
        }

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

    return render(request, 'item_detail.html', {
        'item': item,
        'calendar': mark_safe(html_calendar),
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
        })

