from django.db import models
import uuid  # For UUID generation
from expensive_item_model import ExpensiveItem
from cheap_item_model import CheapItem


class CheapItemSessionData(models.Model):
    cheap = models.ForeignKey(CheapItem, on_delete=models.CASCADE, related_name="cheap_items")
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="sessions")
    cheap_session_id = models.CharField(max_length=255, unique=True, editable=False)  
    quantity = models.Integer(max_digits=5)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    cheapItemSessionData_comment = models.TextField()
    STATUS_CHOICES = [('P', 'Pending'), ('C', 'Completed')]
    cheapItemSessionData_status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    locker = models.ForeignKey(Locker, on_delete=models.SET_NULL,null=True,blank=True, related_name="locker")

    class Meta:
        unique_together = [['name', 'author']]

    def save(self, *args, **kwargs):
        self.cheap_session_id = f"{self.session.id}_{self.cheap.id}" 
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ExpensiveItemSessionData(models.Model):
    expensive_id = models.ForeignKey(CheapItem, on_delete=models.CASCADE, related_name="cheap_items")
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="sessions")
    expensive_session_id = models.CharField(max_length=255, unique=True, editable=False)  
    quantity = models.Integer(default=1)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    cheapItemSessionData_comment = models.TextField()
    STATUS_CHOICES = [('P', 'Pending'), ('C', 'Completed')]
    cheapItemSessionData_status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    locker = models.ForeignKey(Locker, on_delete=models.SET_NULL,null=True,blank=True, related_name="locker")
    class Meta:
        unique_together = [['name', 'author']]

    def save(self, *args, **kwargs):
        self.cheap_session_id = f"{self.session_id.id}_{self.expensive_id.id}" 
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CompletedRecord(models.Model):
    record_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(StudentUser, on_delete=models.SET_NULL,null=True,blank=True, related_name="users")
    admin_user = models.ForeignKey(AdminUser, on_delete=models.SET_NULL,null=True,blank=True, related_name="admin_users")
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
