how to check cheap availability -
check each date

cheap stock availability check -
from django.db.models import Sum, Q
from datetime import date

def is_item_available(item, start_date, end_date, quantity):
"""
Check if there is enough stock available to lend an item within the given date range.
""" # Get total stock
total_stock = item.total_stock

    # Get the total quantity already lent within the given date range
    lent_quantity = LendingTransaction.objects.filter(
        item=item,
        start_date__lte=end_date,  # Overlapping start
        end_date__gte=start_date   # Overlapping end
    ).aggregate(Sum('quantity'))['quantity__sum'] or 0  # Handle None case

    # Calculate available stock
    available_stock = total_stock - lent_quantity

    return available_stock >= quantity
