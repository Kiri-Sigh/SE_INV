from django.db import models
import uuid  
from cloudinary.models import CloudinaryField  
from user.models import CustomUser
class ComponentCategory(models.Model):
    category_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.CharField(max_length=100,null=False,blank=False)
    def __str__(self):
        return self.category
    
class CheapItem(models.Model):
    component_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(ComponentCategory, on_delete=models.SET_NULL,null=True, blank=True,related_name="cheap_item_Categories")
    stock = models.IntegerField()
    description = models.TextField(default="hello, this is a default description")
    weight = models.IntegerField(default=0)
    max_time = models.IntegerField(default=30)
    STATUS_CHOICES = [('A', 'Available'), ('U', 'Unavailable')]
    component_status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')
    amount_reserved_rn = models.IntegerField(default=0)
    amount_reserve = models.IntegerField()
    requires_admin_approval = models.BooleanField(default=False)
    image = CloudinaryField('image')

    def __str__(self):
        return self.name



class ExpensiveItem(models.Model):
    #same item name as expensive_item
    component_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(blank=False,null=False,max_length=150)
    category = models.ForeignKey(ComponentCategory, on_delete=models.SET_NULL,null=True,blank=True, related_name="exp_item_Categories")
    # stock = models.IntegerField(default=1)
    description = models.TextField(default="hello, this is a default description")
    # quantity_available = models.IntegerField()
    # quantity_borrowed = models.IntegerField()
    #item_type = models.CharField(max_length=30,default='expensive')
    weight = models.IntegerField(default= 0)
    max_time = models.IntegerField(default=30)
    STATUS_CHOICES = [('A', 'Available'), ('U', 'Unavailable')]
    component_status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    amount_reserved_rn = models.IntegerField(default=0)
    amount_reserve = models.IntegerField()
    late_penalty = models.IntegerField(default=100)
    requires_admin_approval = models.BooleanField(default=False)
    change_hands_interval=models.IntegerField(default=7)
    image = CloudinaryField('image', blank=True, null=True)  

    def __str__(self):
        return self.name

class ExpensiveItemData(models.Model):
    #same item name as expensive_item
    item_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True,blank=True, related_name="expensive_item_data_Users")
    expensive_item = models.ForeignKey(ExpensiveItem, on_delete=models.CASCADE, null=False, related_name="expensive_item_data_Expensive_items")
    serial_id = models.CharField(max_length=100, default = "Default Serial ID")
    stock = models.IntegerField(default=1)
    STATUS_CHOICES = [('B', 'Borrowed'), ('A', 'Available')]
    item_status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    weight = models.IntegerField(default= 0)
    condition = models.TextField(default="This is an item's default condition")
    max_time = models.IntegerField(default=30)
    late_penalty = models.IntegerField(default= 100)
    requires_admin_approval = models.BooleanField(default=False)
    change_hands_interval=models.IntegerField(default=3)
    reserved = models.BooleanField(default=False)
    force_reserved = models.BooleanField(default=False)
    image = CloudinaryField('image', blank=True, null=True)

    def save(self, *args, **kwargs):
        self.student_id = f"{self.user.user_id}" 
        super().save(*args, **kwargs)

    def __str__(self):
        if self.serial_id:
            return self.serial_id
        else:
            return self.expensive_item.name


# class UserCart(models.Model):
#     #same item name as expensive_item
#     cart_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True,related_name="user_cart_Users")

#     def __str__(self):
#         return (f"{self.user.username},'s cart")

class BorrowItemList(models.Model):
    #same item name as expensive_item
    borrow_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,blank=True,related_name="borrow_item_User")
    expensive_item_data = models.ForeignKey(ExpensiveItemData,on_delete=models.SET_NULL,null=True,blank=True,related_name="borrow_item_Exp_item_data")
    cheap_item = models.ForeignKey(CheapItem, on_delete=models.SET_NULL, null=True, blank=True, related_name="borrow_item_Cheap_item_data")
    quantity_specified = models.BooleanField(default=False)
    date_specified = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    date_start = models.DateField()
    date_end = models.DateField()

    def save(self, *args, **kwargs):
        if self.expensive_item_data:
            self.quantity_specified = True
        elif  self.cheap_item:
            self.quantity_specified = False
        super().save(*args, **kwargs)

    def __str__(self):
        if self.expensive_item_data:
            return self.expensive_item_data.expensive_item.name
        elif self.cheap_item:
            return self.cheap_item.name
        return(str(self.borrow_id))







