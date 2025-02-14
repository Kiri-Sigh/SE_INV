from django.db import models
import uuid  
from cloudinary.models import CloudinaryField  

class ComponentCategory(models.Model):
    category_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.CharField(max_length=100,required=True)
    def __str__(self):
        return self.name
    
class CheapItem(models.Model):
    component_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    stock = models.IntegerField(max_digits=4)
    description = models.TextField()
    quantity_available = models.Integer(max_digits=4)
    quantity_borrowed = models.Integer(max_digits=4)
    #item_type = models.CharField(default="cheap")
    weight = models.Integer(max_digits=6)
    max_time = models.Integer(default=0,max_digits=4)
    amount_reserved = models.IntegerField(max_digits=3)
    percent_reserved = models.IntegerField(max_digits=3)
    category = models.ForeignKey(ComponentCategory, on_delete=models.SET_NULL,null=True, blank=True)
    requires_admin_approval = models.BooleanField(default=False)

    image = CloudinaryField('image')

    def __str__(self):
        return self.name



class ExpensiveItem(models.Model):
    #same item name as expensive_item
    component_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(required=True,blank=False,null=False,max_length=150)
    stock = models.IntegerField(default=1,max_digits=5)
    category = models.ForeignKey(ComponentCategory, on_delete=models.SET_NULL,null=True,blank=True, related_name="category")
    description = models.TextField()
    quantity_available = models.Integer(max_digits=4)
    quantity_borrowed = models.Integer(max_digits=4)
    #item_type = models.CharField(max_length=30,default='expensive')
    STATUS_CHOICES = [('P', 'Pending'), ('C', 'Completed')]
    component_status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    amount_reserved = models.IntegerField(max_digits=3)
    percent_reserved = models.IntegerField(max_digits=3)
    max_time = models.IntegerField(default=30,max_digits=5)
    requires_admin_approval = models.BooleanField(default=False)
    change_hands_interval=models.IntegerField(max_digits=2)
    late_penalty = models.IntegerField(default= 100,max_digits=6)
    weight = models.IntegerField(default= 0,max_digits=6)
    image = CloudinaryField('image', blank=True, null=True)  

    def __str__(self):
        return self.name

class ExpensiveItemData(models.Model):
    #same item name as expensive_item
    item_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(StudentUser,on_delete=models.SET_NULL,null=True,blank=True,related_name="user")
    expensive_item = models.ForeignKey(ExpensiveItem, on_delete=models.CASCADE, null=False,      related_name="expensive_items")
    serial_id = models.CharField(max_length=100)
    stock = models.IntegerField(default=1,max_digits=5)
    condition = models.TextField()
    STATUS_CHOICES = [('P', 'Pending'), ('C', 'Completed')]
    item_status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    max_time = models.IntegerField(default=30,max_digits=5)
    requires_admin_approval = models.BooleanField(default=False)
    change_hands_interval=models.IntegerField(max_digits=2)
    late_penalty = models.IntegerField(default= 100,max_digits=6)
    weight = models.IntegerField(default= 0,max_digits=6)
    reserved = models.BooleanField(default=False)
    image = CloudinaryField('image', blank=True, null=True)  

    def save(self, *args, **kwargs):
        self.student_id = f"{self.user.student_id}" 
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name






