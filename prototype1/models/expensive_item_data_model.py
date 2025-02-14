from django.db import models
from expensive_item_model import ExpensiveItem
import uuid  
from cloudinary.models import CloudinaryField  

class ExpensiveItemData(models.Model):
    #same item name as expensive_item
    item_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name="user")
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
