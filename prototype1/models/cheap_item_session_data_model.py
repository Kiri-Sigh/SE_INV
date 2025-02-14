from django.db import models
import uuid  # For UUID generation
from expensive_item_model import ExpensiveItem
from cheap_item_model import CheapItem
from session_model import Session
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
