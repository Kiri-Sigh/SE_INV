# Generated by Django 5.1.6 on 2025-02-16 09:23

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory', '0002_initial'),
        ('session', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NotifyUserCheapItem',
            fields=[
                ('notify_user_cheap_item_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('notified', models.BooleanField(default=False)),
                ('cheap_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notify_cheap_item_Cheap_items', to='inventory.cheapitem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notify_cheap_item_Users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NotifyUserExpensiveGroup',
            fields=[
                ('notify_user_exp_item_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('notified', models.BooleanField(default=False)),
                ('exp_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notify_exp_group_Expensive_items', to='inventory.expensiveitem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notify_exp_group_Users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NotifyUserExpensiveItem',
            fields=[
                ('notify_user_exp_item_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('notified', models.BooleanField(default=False)),
                ('exp_item_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notfiy_exp_item_Expensive_item_datas', to='inventory.expensiveitemdata')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notify_exp_item_Users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('reminder_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('reminder_date_time', models.DateTimeField()),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reminder_Sessions', to='session.session')),
            ],
        ),
    ]
