from django.shortcuts import render
from inventory.models import CheapItem, ExpensiveItem

def list_items(request):
    query = request.GET.get('q', '')  # Get search query from request, default is empty
    cheap_items = CheapItem.objects.all()
    expensive_items = ExpensiveItem.objects.all()

    if query:
        cheap_items = cheap_items.filter(name__icontains=query)
        expensive_items = expensive_items.filter(name__icontains=query)

    context = {
        'cheap_items': cheap_items,
        'expensive_items': expensive_items,
        'query': query  # Pass the query back to the template
    }

    return render(request, 'item_list.html', context)

def item_detail(request, item_id):
    item = None

    # Try to find the item in CheapItem, then ExpensiveItem
    item = CheapItem.objects.filter(component_id=item_id).first() or ExpensiveItem.objects.filter(component_id=item_id).first()
    
    if not item:
        return render(request, '404.html', status=404)  # Render a 404 page if the item is not found
    
    return render(request, 'item_detail.html', {'item': item})