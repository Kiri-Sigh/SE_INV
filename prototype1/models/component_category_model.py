# myapp/models/product_models.py
from django.db import models
from expensive_item_model import ExpensiveItem
import uuid  # To generate UUIDs

class ComponentCategoryModel(models.Model):
    category_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.CharField(max_length=100,required=True)
    def __str__(self):
        return self.name



