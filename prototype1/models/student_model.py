# myapp/models/product_models.py
from django.db import models
from expensive_item_model import ExpensiveItem
import uuid  # To generate UUIDs

class Student(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    author = models.ForeignKey(ExpensiveItem, on_delete=models.CASCADE)
    STATUS_CHOICES = [('P', 'Pending'), ('C', 'Completed')]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name



