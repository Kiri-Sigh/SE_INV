from django.db import models
from expensive_item_model import ExpensiveItem
import uuid

class AdminUser(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    STATUS_CHOICES = [('S', 'Super'), ('N', 'Normal')]
    role = models.CharField(max_length=1, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name



