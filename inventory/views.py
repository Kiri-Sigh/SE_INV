from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView
from django.http import Http404
from inventory.models import CheapItem, ExpensiveItem
from django.template.response import TemplateResponse
from django.template import loader

def handler404(request, exception=None):
    """Custom 404 handler"""
    template = loader.get_template('404.html')
    return TemplateResponse(request, template, {'error_message': str(exception)}, status=404)

class MainPage(View):
    template_name = 'item_list.html'

    def filter_items(self):
        """Filter items based on search query"""
        query = self.request.GET.get('q', '')
        cheap_items = CheapItem.objects.all()
        expensive_items = ExpensiveItem.objects.all()

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

    def get(self, request, *args, **kwargs):
        """Handle GET request"""
        self.request = request
        try:
            context = self.load_items()
            return TemplateResponse(request, self.template_name, context)
        except Exception as e:
            return handler404(request, e)

class DetailPage(DetailView):
    template_name = 'item_detail.html'
    context_object_name = 'item'
    
    def get_object(self, queryset=None):
        """Get the object this view is displaying"""
        item_id = self.kwargs.get('item_id')
        
        # Try to find in CheapItem first
        try:
            return CheapItem.objects.get(component_id=item_id)
        except CheapItem.DoesNotExist:
            # If not found in CheapItem, try ExpensiveItem
            try:
                return ExpensiveItem.objects.get(component_id=item_id)
            except ExpensiveItem.DoesNotExist:
                raise Http404(f"No item found with ID: {item_id}")

    def get(self, request, *args, **kwargs):
        """Handle GET request"""
        try:
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return TemplateResponse(request, self.template_name, context)
        except Http404 as e:
            return handler404(request, e)