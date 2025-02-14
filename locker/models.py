from django.db import models
from user.models import AdminUser
import uuid

class LockerSet(models.Model):
    locker_set_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    available = models.BooleanField(default=True)
    location = models.CharField(max_length=255)
    locker_colors= models.CharField(max_length=30,blank=True,null=True)
    locker_set_dimensions_x = models.IntegerField()
    locker_set_dimensions_y =  models.IntegerField()

    def __str__(self):
        return self.name
    
class Locker(models.Model):
    locker_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField()
    locker_set= models.ForeignKey(LockerSet, on_delete=models.CASCADE,null=True,blank=True, related_name="locker_set")
    cheap_session = models.ForeignKey(CheapSessionItemData, on_delete=models.SET_NULL,null=True,blank=True, related_name="student_users")
    expensive_session = models.ForeignKey(ExpensiveSessionItemData, on_delete=models.SET_NULL,null=True,blank=True, related_name="admin_users")

    def save(self, *args, **kwargs):
        if self.student and self.admin:
            raise ValueError("Only a cheap OR an admin can be assigned, not both.")
        if self.student:
            self.name = self.student.name  
            self.gmail = self.student.gmail  

        elif self.admin:
            self.name = self.admin.name 
            self.gmail = self.admin.gmail  
 
        else:
            self.name = "Unknown"
            self.gmail = "Unknown" 
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class ItemInOneLocker(models.Model):
    item_in_one_locker_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    locker=models.ForeignKey(Locker, on_delete=models.CASCADE, related_name="lockers")

    
class RelItemInOneLocker(models.Model):
    rel_item_in_one_locker_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    locker=models.ForeignKey(ItemInOneLocker, on_delete=models.CASCADE, related_name="item_in_one_lockers")
    expensive_session=models.ForeignKey(ItemInOneLocker, on_delete=models.CASCADE, related_name="expensive_session")
    cheap_session=models.ForeignKey(Cheap, on_delete=models.CASCADE, related_name="cheap_session")

class LockerInteractionLog(models.Model):
    locker_log_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    locker= models.ForeignKey(Locker, on_delete=models.SET_NULL,null=True,blank=True, related_name="lockers")

    name = models.CharField(max_length=100, unique=False, editable=False)
    gmail= models.EmailField(max_length=100, unique=False, editable=False)
    start_date_pos = models.DateTimeField()
    end_date_pos = models.DateTimeField()   
    student = models.ForeignKey(StudentUser, on_delete=models.SET_NULL,null=True,blank=True, related_name="student_users")
    admin = models.ForeignKey(AdminUser, on_delete=models.SET_NULL,null=True,blank=True, related_name="admin_users")
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



