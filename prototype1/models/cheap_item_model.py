from django.db import models
from expensive_item_model import ExpensiveItem
import uuid  
from cloudinary.models import CloudinaryField  

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



