#from django.contrib import admin
#from django.contrib.auth.admin import UserAdmin
# from your_app.models import StudentUser
#rom inventory.models import CheapItem,ExpensiveItem,ExpensiveItemData,ComponentCategory
#from locker.models import Locker,LockerSet,LockerInteractionLog,ItemInOneLocker,RelItemInOneLocker
#from notification.models import NotifyUserCheapItem,NotifyUserExpensiveGroup,NotifyUserExpensiveItem,Reminder
#from session.models import Session,CheapItemSessionData,ExpensiveItemSessionData,CompletedRecord
#from user.models import CustomUser
# class StudentUserAdmin(UserAdmin):  # Use Django’s built-in UserAdmin
#     fieldsets = UserAdmin.fieldsets + (  # Add extra fields
#         ('Student Info', {'fields': ('enrolled_year', 'enrolled_department', 'merit', 'level')}),
#     )

# admin.site.register(StudentUser, StudentUserAdmin)
#admin.site.register(CheapItem)
#admin.site.register(ExpensiveItem)
#admin.site.register(ExpensiveItemData)
#admin.site.register(ComponentCategory)
# admin.site.register(Locker)
# admin.site.register(LockerSet)
# admin.site.register(LockerInteractionLog)
# admin.site.register(ItemInOneLocker)
# admin.site.register(RelItemInOneLocker)
# admin.site.register(NotifyUserCheapItem)
# admin.site.register(NotifyUserExpensiveGroup)
# admin.site.register(NotifyUserExpensiveItem)
# admin.site.register(Reminder)
# admin.site.register(Session)
# admin.site.register(CheapItemSessionData)
# admin.site.register(ExpensiveItemSessionData)
# admin.site.register(CompletedRecord)
#admin.site.register(CustomUser)

from django.contrib import admin
from social_django.models import UserSocialAuth ,Association,Nonce
admin.site.unregister(UserSocialAuth) 
admin.site.unregister(Association) 
admin.site.unregister(Nonce) 
