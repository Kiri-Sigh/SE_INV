from django.contrib import admin
from .models import (
    ComponentCategory, CheapItem, ExpensiveItem, ExpensiveItemData, BorrowItemList
)
from django.utils.timezone import now

@admin.register(ComponentCategory)
class ComponentCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'category')
    search_fields = ('category',)
    ordering = ('category',)


@admin.register(CheapItem)
class CheapItemAdmin(admin.ModelAdmin):
    list_display = ('component_id', 'name', 'category', 'stock', 'component_status', 'requires_admin_approval')
    list_filter = ('category', 'component_status', 'requires_admin_approval')
    search_fields = ('name', 'description')
    ordering = ('name',)
    readonly_fields = ('component_id', )
    fieldsets = (
        ('Basic Info', {'fields': ('name', 'category', 'description', 'image')}),
        ('Stock & Availability', {'fields': ('stock', 'component_status', 'amount_reserved_rn', 'amount_reserve')}),
        ('Time & Weight', {'fields': ('max_time', 'weight')}),
        ('Permissions', {'fields': ('requires_admin_approval',)}),
        #('Image', {'fields': ('image',)})
        
    )


# @admin.register(ExpensiveItem)
# class ExpensiveItemAdmin(admin.ModelAdmin):
#     list_display = ('component_id', 'name', 'category', 'component_status', 'requires_admin_approval', 'late_penalty')
#     list_filter = ('category', 'component_status', 'requires_admin_approval')
#     search_fields = ('name', 'description')
#     ordering = ('name',)
#     readonly_fields = ('component_id', 'image')
#     fieldsets = (
#         ('Basic Info', {'fields': ('name', 'category', 'description', 'image')}),
#         ('Stock & Availability', {'fields': ('component_status', 'amount_reserved_rn', 'amount_reserve')}),
#         ('Time & Weight', {'fields': ('max_time', 'weight', 'change_hands_interval')}),
#         ('Penalty & Permissions', {'fields': ('late_penalty', 'requires_admin_approval')}),
#     )


# @admin.register(ExpensiveItemData)
# class ExpensiveItemDataAdmin(admin.ModelAdmin):
#     list_display = ('item_id', 'expensive_item', 'user', 'serial_id', 'stock', 'item_status', 'reserved', 'force_reserved')
#     list_filter = ('item_status', 'reserved', 'force_reserved')
#     search_fields = ('serial_id', 'expensive_item__name', 'user__username')
#     ordering = ('serial_id',)
#     readonly_fields = ('item_id', 'image')
#     fieldsets = (
#         ('Item Details', {'fields': ('expensive_item', 'serial_id', 'image')}),
#         ('User & Status', {'fields': ('user', 'item_status', 'reserved', 'force_reserved')}),
#         ('Stock & Condition', {'fields': ('stock', 'weight', 'condition')}),
#         ('Time & Penalty', {'fields': ('max_time', 'late_penalty', 'change_hands_interval')}),
#         ('Approval', {'fields': ('requires_admin_approval',)}),
#     )


# @admin.register(BorrowItemList)
# class BorrowItemListAdmin(admin.ModelAdmin):
#     list_display = ('borrow_id', 'user', 'expensive_item_data', 'cheap_item', 'quantity_specified', 'date_start', 'date_end')
#     list_filter = ('quantity_specified', 'date_specified')
#     search_fields = ('user__username', 'expensive_item_data__serial_id', 'cheap_item__name')
#     ordering = ('date_start',)

#     fieldsets = (
#         ('Item in Locker Ready', {'fields': ('item_in_locker_done',)}),
#         ('Item Returned', {'fields': ('item_returned',)}),
#         ('Borrower Details', {'fields': ('user',)}),
#         ('Items Borrowed', {'fields': ('expensive_item_data', 'cheap_item')}), 
#         ('Quantity & Date', {'fields': ('quantity_specified', 'quantity', 'date_specified', 'date_start', 'date_end')}), 
#     )

@admin.register(BorrowItemList)

class CurrentBorrowItemToInteractList(admin.ModelAdmin):
    list_display = ('borrow_id', 'user', 'expensive_item_data', 'cheap_item', 'quantity_specified', 'date_start', 'date_end')
    list_filter = ('quantity_specified', 'date_specified')
    search_fields = ('user__username', 'expensive_item_data__serial_id', 'cheap_item__name')
    ordering = ('date_start',)

    fieldsets = (
        ('Item in Locker Ready', {'fields': ('item_in_locker_done',)}),
        ('Item Returned', {'fields': ('item_returned',)}),
        ('Borrower Details', {'fields': ('user',)}),
        ('Items Borrowed', {'fields': ('expensive_item_data', 'cheap_item')}), 
        ('Quantity & Date', {'fields': ('quantity_specified', 'quantity', 'date_specified', 'date_start', 'date_end')}), 
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(date_start__gte=now())

#admin.site.register(BorrowItemList, CurrentBorrowItemToInteractList)
