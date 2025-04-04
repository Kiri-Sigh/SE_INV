# from django.db import models
# import uuid 
# from inventory.models import CheapItem
# #from locker.models import Locker
# from inventory.models import ExpensiveItem
# from user.models import CustomUser
# from django.utils import timezone

# class Session(models.Model):
#     session_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     session_date_posted = models.DateTimeField(auto_now_add=True)
#     user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,null=True,blank=True, related_name="session_Users")
#     admin_user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,null=True,blank=True, related_name="session_admin_Users")
#     STATUS_CHOICES = [('P', 'Pending'), ('C', 'Completed')]
#     session_status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    
#     user_comment = models.TextField()
#     admin_user_comment = models.TextField()

#     def __str__(self):
#         return ("session: "+self.session_id+" created: "+self.session_date_posted+" user: ")



# class CheapItemSessionData(models.Model):
#     cheap = models.ForeignKey(CheapItem, on_delete=models.CASCADE, related_name="cheap_item_session_data_Cheap_items")
#     session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="cheap_item_session_data_Sessions")
#     cheap_session_id = models.CharField(max_length=255, unique=True, editable=False)  
#     quantity = models.IntegerField()
#     date_start = models.DateField()
#     date_end = models.DateField()
#     cheapItemSessionData_comment = models.TextField()
#     STATUS_CHOICES = [('P', 'Pending'), ('C', 'Completed')]
#     cheapItemSessionData_status = models.CharField(max_length=1, choices=STATUS_CHOICES)
#     locker = models.ForeignKey('locker.Locker', on_delete=models.SET_NULL,null=True,blank=True, related_name="cheap_item_session_data_Lockers")

#     class Meta:
#         unique_together = [['cheap', 'session']]

#     def save(self, *args, **kwargs):
#         self.cheap_session_id = f"{self.session.session_id}_{self.cheap.cheap_id}" 
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return ("CheapItemSessionData cheap_session_id: ",self.cheap_session_id)


# class ExpensiveItemSessionData(models.Model):
#     expensive = models.ForeignKey(CheapItem, on_delete=models.CASCADE, related_name="expensive_item_session_data_Cheap_items")
#     session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="expensive_item_session_data_Sessions")
#     expensive_session_id = models.CharField(max_length=255, unique=True, blank=True,editable=False)  
#     quantity = models.IntegerField(default=1)
#     date_start = models.DateField()
#     date_end = models.DateField()
#     cheapItemSessionData_comment = models.TextField()
#     STATUS_CHOICES = [('P', 'Pending'), ('C', 'Completed')]
#     cheapItemSessionData_status = models.CharField(max_length=1, choices=STATUS_CHOICES)
#     locker = models.ForeignKey('locker.Locker', on_delete=models.SET_NULL,null=True,blank=True, related_name="expensive_item_session_data_Lockers")
#     class Meta:
#         unique_together = [['expensive', 'session']]

#     def save(self, *args, **kwargs):
#         self.expensive_session_id = f"{self.session.session_id}_{self.expensive.expensive_id}" 
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return ("ExpensiveItemSessionData expensive_session_id: ",self.expensive_session_id)


# class CompletedRecord(models.Model):
#     record_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,null=True,blank=True, related_name="completed_record_Users")
#     admin_user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,null=True,blank=True, related_name="completed_record_admin_Users")
#     student_id = models.CharField(max_length=255, unique=False, editable=False)  
#     session_date_posted = models.DateTimeField(default=None)
#     record_date_posted = models.DateTimeField(auto_now_add=True)    
#     condition = models.TextField()
#     session_user_comment = models.TextField()
#     session_admin_comment = models.TextField()
#     STATUS_CHOICES = [('P', 'Pending'), ('C', 'Completed')]
#     session_status_final = models.CharField(max_length=1, choices=STATUS_CHOICES)
#     def save(self, *args, **kwargs):
#         self.student_id = f"{self.user.user_id}" 
#         self.admin_id = f"{self.admin_user.user_id}" 
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return ("CompletedRecord record_id: ",self.record_id)
