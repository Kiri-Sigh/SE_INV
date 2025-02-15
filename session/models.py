from django.db import models
import uuid 
from inventory.models import CheapItem
#from locker.models import Locker
from inventory.models import ExpensiveItem
from user.models import CustomUser
class Session(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    author = models.ForeignKey(ExpensiveItem, on_delete=models.CASCADE)
    STATUS_CHOICES = [('P', 'Pending'), ('C', 'Completed')]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name



class CheapItemSessionData(models.Model):
    cheap = models.ForeignKey(CheapItem, on_delete=models.CASCADE, related_name="cheap_item_session_data_Cheap_items")
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="cheap_item_session_data_Sessions")
    cheap_session_id = models.CharField(max_length=255, unique=True, editable=False)  
    quantity = models.IntegerField()
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    cheapItemSessionData_comment = models.TextField()
    STATUS_CHOICES = [('P', 'Pending'), ('C', 'Completed')]
    cheapItemSessionData_status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    locker = models.ForeignKey('locker.Locker', on_delete=models.SET_NULL,null=True,blank=True, related_name="cheap_item_session_data_Lockers")

    class Meta:
        unique_together = [['cheap', 'session']]

    def save(self, *args, **kwargs):
        self.cheap_session_id = f"{self.session.id}_{self.cheap.id}" 
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ExpensiveItemSessionData(models.Model):
    expensive = models.ForeignKey(CheapItem, on_delete=models.CASCADE, related_name="expensive_item_session_data_Cheap_items")
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="expensive_item_session_data_Sessions")
    expensive_session_id = models.CharField(max_length=255, unique=True, editable=False)  
    quantity = models.IntegerField(default=1)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    cheapItemSessionData_comment = models.TextField()
    STATUS_CHOICES = [('P', 'Pending'), ('C', 'Completed')]
    cheapItemSessionData_status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    locker = models.ForeignKey('locker.Locker', on_delete=models.SET_NULL,null=True,blank=True, related_name="expensive_item_session_data_Lockers")
    class Meta:
        unique_together = [['expensive', 'session']]

    def save(self, *args, **kwargs):
        self.cheap_session_id = f"{self.session_id.id}_{self.expensive_id.id}" 
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CompletedRecord(models.Model):
    record_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,null=True,blank=True, related_name="completed_record_Users")
    admin_user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,null=True,blank=True, related_name="completed_record_admin_Users")
    student_id = models.CharField(max_length=255, unique=False, editable=False)  
    session_date_posted = models.DateTimeField()
    record_date_posted = models.DateTimeField()    
    condition = models.TextField()
    session_user_comment = models.TextField()
    session_admin_comment = models.TextField()
    STATUS_CHOICES = [('P', 'Pending'), ('C', 'Completed')]
    session_status_final = models.CharField(max_length=1, choices=STATUS_CHOICES)
    def save(self, *args, **kwargs):
        self.student_id = f"{self.user.student_id}" 
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
