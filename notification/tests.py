# from django.test import TestCase
# from django.utils import timezone
# from datetime import timedelta
# from .models import NotifyUserCheapItem, NotifyUserExpensiveGroup, NotifyUserExpensiveItem, Reminder
# from inventory.models import CheapItem, ExpensiveItem, ExpensiveItemData, ComponentCategory
# from user.models import CustomUser
# from session.models import Session
# import uuid

# class NotifyUserCheapItemTests(TestCase):
#     def setUp(self):
#         # Create necessary related objects
#         self.category = ComponentCategory.objects.create(category="Electronics")
#         self.cheap_item = CheapItem.objects.create(
#             name="Test Cheap Item",
#             category=self.category,
#             stock=100,
#             description="Test description",
#             quantity_available=90,
#             quantity_borrowed=10,
#             weight=1,
#             amount_reserve=20,
#             percent_reserve=20
#         )
        
#         self.user = CustomUser.objects.create_user(
#             username="testuser",
#             password="testpass123"
#         )
        
#         self.notification = NotifyUserCheapItem.objects.create(
#             cheap_item=self.cheap_item,
#             user=self.user,
#             notified=False
#         )

#     def test_notification_creation(self):
#         self.assertEqual(self.notification.cheap_item, self.cheap_item)
#         self.assertEqual(self.notification.user, self.user)
#         self.assertFalse(self.notification.notified)
#         self.assertIsInstance(self.notification.notify_user_cheap_item_id, uuid.UUID)

# class NotifyUserExpensiveGroupTests(TestCase):
#     def setUp(self):
#         # Create necessary related objects
#         self.category = ComponentCategory.objects.create(category="Electronics")
#         self.expensive_item = ExpensiveItem.objects.create(
#             name="Test Expensive Item",
#             category=self.category,
#             stock=5,
#             description="Test description",
#             quantity_available=4,
#             quantity_borrowed=1,
#             component_status='P',
#             amount_reserve=1,
#             percent_reserve=20,
#             weight=5
#         )
        
#         self.user = CustomUser.objects.create_user(
#             username="testuser",
#             password="testpass123"
#         )
        
#         self.notification = NotifyUserExpensiveGroup.objects.create(
#             exp_item=self.expensive_item,
#             user=self.user,
#             notified=False
#         )

#     def test_notification_creation(self):
#         self.assertEqual(self.notification.exp_item, self.expensive_item)
#         self.assertEqual(self.notification.user, self.user)
#         self.assertFalse(self.notification.notified)
#         self.assertIsInstance(self.notification.notify_user_exp_item_id, uuid.UUID)

# # class NotifyUserExpensiveItemTests(TestCase):
# #     def setUp(self):
# #         self.user = CustomUser.objects.create_user(
# #             username="testuser",
# #             password="testpass123",
# #             email="test@example.com",
# #             enrolled_year=2024,
# #             enrolled_department="Computer Science"
# #         )
        
# #         self.category = ComponentCategory.objects.create(category="Electronics")
# #         self.expensive_item = ExpensiveItem.objects.create(
# #             name="Test Item",
# #             category=self.category,
# #             stock=5,
# #             description="Test description",
# #             quantity_available=4,
# #             quantity_borrowed=1,
# #             component_status='P',
# #             amount_reserve=1,
# #             percent_reserve=20,
# #             weight=5
# #         )
        
# #         self.expensive_item_data = ExpensiveItemData.objects.create(
# #             user=self.user,
# #             expensive_item=self.expensive_item,
# #             serial_id="TEST001",
# #             stock=1,
# #             item_status='P',
# #             weight=5,
# #             condition="Good condition",
# #             max_time=30,
# #             late_penalty=100,
# #             change_hands_interval=7
# #         )
        
# #         self.notification = NotifyUserExpensiveItem.objects.create(
# #             exp_item_data=self.expensive_item_data,
# #             user=self.user,
# #             notified=False
# #         )

# #     def test_notification_creation(self):
# #         self.assertEqual(self.notification.exp_item_data, self.expensive_item_data)
# #         self.assertEqual(self.notification.user, self.user)
# #         self.assertFalse(self.notification.notified)
# #         self.assertIsInstance(self.notification.notify_user_exp_item_id, uuid.UUID)

# class ReminderTests(TestCase):
#     def setUp(self):
#         # Create necessary related objects
#         self.category = ComponentCategory.objects.create(category="Electronics")
#         self.expensive_item = ExpensiveItem.objects.create(
#             name="Test Item",
#             category=self.category,
#             stock=5,
#             description="Test description",
#             quantity_available=4,
#             quantity_borrowed=1,
#             component_status='P',
#             amount_reserve=1,
#             percent_reserve=20,
#             weight=5
#         )
        
#         self.session = Session.objects.create(
#             name="Test Session",
#             price=99.99,
#             description="Test session description",
#             author=self.expensive_item,
#             status='P'
#         )
        
#         self.current_time = timezone.now()
#         self.reminder = Reminder.objects.create(
#             session=self.session,
#             reminder_date_time=self.current_time + timedelta(days=1)
#         )

#     def test_reminder_creation(self):
#         self.assertEqual(self.reminder.session, self.session)
#         self.assertEqual(self.reminder.reminder_date_time, self.current_time + timedelta(days=1))
#         self.assertIsInstance(self.reminder.reminder_id, uuid.UUID)
