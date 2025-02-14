#NOT IN USE
from django.db import models

class Config(models.Model):
    max_time=models.IntegerField(max_digits=6)
    change_hands_interval=models.IntegerField(max_digits=2)
    STATUS_CHOICES = [('P', 'Pending'), ('C', 'Completed')]
    item_status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    requires_admin_approval = models.BooleanField(default=False)
    weight=models.IntegerField(max_digits=2)
    name = models.CharField(max_length=100)
    condition = models.TextField()

    def __str__(self):
        return self.name
