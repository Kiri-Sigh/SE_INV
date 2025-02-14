# myapp/models/product_models.py
from django.db import models
import uuid
class CompletedRecord(models.Model):
    record_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True, related_name="users")
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
