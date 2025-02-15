# myapp/models/product_models.py
from django.db import models
import uuid
from inventory.models import CheapItem,ExpensiveItemData,ExpensiveItem
from user.models import CustomUser
from session.models import Session
class NotifyUserCheapItem(models.Model):
    notify_user_cheap_item_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cheap_item = models.ForeignKey(CheapItem, on_delete=models.CASCADE, related_name="notify_cheap_item_Cheap_items")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name="notify_cheap_item_Users")
    notified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name


class NotifyUserExpensiveGroup(models.Model):
    notify_user_exp_item_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exp_item = models.ForeignKey(ExpensiveItem, on_delete=models.CASCADE, related_name="notify_exp_group_Expensive_items")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name="notify_exp_group_Users")
    notified = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class NotifyUserExpensiveItem(models.Model):
    notify_user_exp_item_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exp_item_data = models.ForeignKey(ExpensiveItemData, on_delete=models.CASCADE, related_name="notfiy_exp_item_Expensive_item_datas")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name="notify_exp_item_Users")
    notified = models.BooleanField(default=False)

    def __str__(self):
        return self.name

# myapp/models/product_models.py
from django.db import models

class Reminder(models.Model):
    reminder_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="reminder_Sessions")    
    reminder_date_time = models.DateTimeField()

    def __str__(self):
        return self.name
