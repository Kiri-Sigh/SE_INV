# Generated by Django 5.1.6 on 2025-02-15 09:45

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ItemInOneLocker',
            fields=[
                ('item_in_one_locker_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='LockerSet',
            fields=[
                ('locker_set_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('locker_set_dimensions_x', models.IntegerField()),
                ('locker_set_dimensions_y', models.IntegerField()),
                ('available', models.BooleanField(default=True)),
                ('location', models.CharField(max_length=255)),
                ('locker_colors', models.CharField(blank=True, max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RelItemInOneLocker',
            fields=[
                ('rel_item_in_one_locker_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Locker',
            fields=[
                ('locker_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('locker_position_x', models.IntegerField()),
                ('locker_position_y', models.IntegerField()),
                ('deplayment_date', models.DateTimeField(blank=True, null=True)),
                ('recent_maintenance_date', models.DateTimeField(blank=True, null=True)),
                ('next_scheduled_date', models.DateTimeField(blank=True, null=True)),
                ('in_use', models.BooleanField(default=False)),
                ('functional', models.BooleanField(default=False)),
                ('condition', models.TextField()),
                ('item_in_one_locker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='locker_Item_in_one_lockers', to='locker.iteminonelocker')),
            ],
        ),
        migrations.CreateModel(
            name='LockerInteractionLog',
            fields=[
                ('locker_log_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(editable=False, max_length=100)),
                ('start_date_pos', models.DateTimeField()),
                ('end_date_pos', models.DateTimeField()),
                ('date_time_interaction', models.DateTimeField()),
                ('operation', models.CharField(choices=[('G', 'Get Item'), ('P', 'Put Item')], max_length=2)),
                ('str_log', models.TextField(blank=True, editable=False)),
                ('itemInOneLocker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='locker_log_Item_in_one_lockers', to='locker.iteminonelocker')),
                ('locker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='locker_log_Lockers', to='locker.locker')),
            ],
        ),
    ]
