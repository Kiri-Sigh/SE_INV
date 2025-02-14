# myapp/models/product_models.py
from django.db import models
from admin_user_model import AdminUser
class LockerInteractionLog(models.Model):
    locker_log_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=False, editable=False)
    gmail= models.EmailField(max_length=100, unique=False, editable=False)
    start_date_pos = models.DateTimeField()
    end_date_pos = models.DateTimeField()    
    student = models.ForeignKey(Student, on_delete=models.SET_NULL,null=True,blank=True, related_name="category")
    admin = models.ForeignKey(AdminUser, on_delete=models.SET_NULL,null=True,blank=True, related_name="category")
    date_time_interaction=models.DateTimeField()
    STATUS_CHOICES = [('G', 'Get Item'), ('P', 'Put Item')]
    operation = models.CharField(max_length=2, choices=STATUS_CHOICES)
    str_log = models.TextField(blank=True,editable=False)
    def save(self, *args, **kwargs):
        if self.student and self.admin:
            raise ValueError("Only a student OR an admin can be assigned, not both.")
        if self.student:
            self.name = self.student.name  
            self.gmail = self.student.gmail  

        elif self.admin:
            self.name = self.admin.name 
            self.gmail = self.admin.gmail  
 
        else:
            self.name = "Unknown"
            self.gmail = "Unknown" 
        self.str_log=f"{"log_id: "+self.locker_log_id+", name: "+self.name+", email: "+self.email+", possible date-time use of locker"+self.start_date_pos+" - "+self.end_date_pos+", use locker date-time: "+self.date_time_interaction+", operation done: "+self.operation}"
        
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name
