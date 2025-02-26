from django.db import models
#from user.models import AdminUser
import uuid
from session.models import CheapItemSessionData,ExpensiveItemSessionData
from user.models import CustomUser



class LockerSet(models.Model):
    locker_set_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #locker_set_open is for when opening locker(identifies the locker set)
    locker_set_open = models.IntegerField(null=True)
    locker_set_dimensions_x = models.IntegerField()
    locker_set_dimensions_y =  models.IntegerField()
    available = models.BooleanField(default=True)
    location = models.CharField(max_length=255)
    locker_colors= models.CharField(max_length=30,blank=True,null=True)

    def __str__(self):
        return ("LockerSet locker_set_id: ",self.locker_set_id)
    
class ItemInOneLocker(models.Model):
    item_in_one_locker_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Locker(models.Model):
    locker_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    locker_position_x =  models.IntegerField()
    locker_position_y =  models.IntegerField()
    locker_set= models.ForeignKey(LockerSet, on_delete=models.CASCADE,null=True,blank=True, related_name="locker_Locker_sets")
    item_in_one_locker = models.ForeignKey(ItemInOneLocker, on_delete=models.SET_NULL,null=True,blank=True, related_name="locker_Item_in_one_lockers")
    deplayment_date = models.DateField(blank=True, null=True)
    recent_maintenance_date = models.DateField(blank=True, null=True)
    next_scheduled_date = models.DateField(blank=True, null=True)
    in_use=models.BooleanField(default=False)
    functional = models.BooleanField(default=False)
    condition = models.TextField()
    # cheap_session = models.ForeignKey(CheapItemSessionData, on_delete=models.SET_NULL,null=True,blank=True, related_name="student_users")
    # expensive_session = models.ForeignKey(ExpensiveItemSessionData, on_delete=models.SET_NULL,null=True,blank=True, related_name="admin_users")

    # def save(self, *args, **kwargs):
    #     if self.student and self.admin:
    #         raise ValueError("Only a cheap OR an admin can be assigned, not both.")
    #         raise ValueError("Only a student OR an admin can be assigned, not both.")
    #     if self.student:
    #         self.name = self.student.name  
    #         self.gmail = self.student.gmail  

    #     elif self.admin:
    #         self.name = self.admin.name 
    #         self.gmail = self.admin.gmail  
 
    #     else:
    #         self.name = "Unknown"
    #         self.gmail = "Unknown" 
    #     super().save(*args, **kwargs)

    def __str__(self):
        return ("Locker locker_id: ",self.locker_id)
    

    
class RelItemInOneLocker(models.Model):
    rel_item_in_one_locker_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item_in_one_locker=models.ForeignKey(ItemInOneLocker, on_delete=models.CASCADE, related_name="rel_item_in_one_locker_Item_in_one_lockers")
    expensive_session=models.ForeignKey(ExpensiveItemSessionData, on_delete=models.CASCADE, related_name="rel_item_in_one_locker_Expensive_sessions")
    cheap_session=models.ForeignKey(CheapItemSessionData, on_delete=models.CASCADE, related_name="rel_item_in_one_locker_Cheap_sessions")

    def __str__(self):
        return ("RelItemInOneLocker rel_item_in_one_locker_id: ",self.rel_item_in_one_locker_id)


class LockerInteractionLog(models.Model):
    locker_log_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=False, editable=False)
    locker= models.ForeignKey(Locker, on_delete=models.SET_NULL,null=True,blank=True, related_name="locker_log_Lockers")
    #gmail= models.EmailField(max_length=100, unique=False, editable=False)
    start_date_pos = models.DateField()
    end_date_pos = models.DateField()   
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,null=True,blank=True, related_name="locker_log_Users")
    #admin = models.ForeignKey(AdminUser, on_delete=models.SET_NULL,null=True,blank=True, related_name="admin_users")
    date_time_interaction=models.DateField()
    STATUS_CHOICES = [('G', 'Get Item'), ('P', 'Put Item')]
    operation = models.CharField(max_length=2, choices=STATUS_CHOICES)
    str_log = models.TextField(blank=True,editable=False)
    itemInOneLocker = models.ForeignKey(ItemInOneLocker, on_delete=models.SET_NULL,null=True,blank=True, related_name="locker_log_Item_in_one_lockers")

    def save(self, *args, **kwargs):
        if self.user:
            self.name = self.user.username
            self.str_log=f"{"log_id: "+self.locker_log_id+", name: "+self.name+", email: "+self.user.email+", possible date-time use of locker"+self.start_date_pos+" - "+self.end_date_pos+", use locker date-time: "+self.date_time_interaction+", operation done: "+self.operation}"
                        
        super().save(*args, **kwargs)
    def __str__(self):
        return ("LockerInteractionLog locker_log_id: ",self.locker_log_id)
