# Generated by Django 5.1.6 on 2025-04-04 19:54

import cloudinary.models
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BorrowItemList',
            fields=[
                ('borrow_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quantity_specified', models.BooleanField(default=False)),
                ('date_specified', models.BooleanField(default=False)),
                ('quantity', models.IntegerField(default=1)),
                ('date_start', models.DateField()),
                ('date_end', models.DateField()),
                ('item_returned', models.BooleanField(default=False)),
                ('item_in_locker_done', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CheapItem',
            fields=[
                ('component_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('stock', models.IntegerField()),
                ('description', models.TextField(default='hello, this is a default description')),
                ('weight', models.IntegerField(default=0)),
                ('max_time', models.IntegerField(default=30)),
                ('component_status', models.CharField(choices=[('A', 'Available'), ('U', 'Unavailable')], default='A', max_length=1)),
                ('amount_reserved_rn', models.IntegerField(default=0)),
                ('amount_reserve', models.IntegerField()),
                ('requires_admin_approval', models.BooleanField(default=False)),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
            ],
        ),
        migrations.CreateModel(
            name='ComponentCategory',
            fields=[
                ('category_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('category', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ExpensiveItem',
            fields=[
                ('component_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField(default='hello, this is a default description')),
                ('weight', models.IntegerField(default=0)),
                ('max_time', models.IntegerField(default=30)),
                ('component_status', models.CharField(choices=[('A', 'Available'), ('U', 'Unavailable')], max_length=1)),
                ('amount_reserved_rn', models.IntegerField(default=0)),
                ('amount_reserve', models.IntegerField()),
                ('late_penalty', models.IntegerField(default=100)),
                ('requires_admin_approval', models.BooleanField(default=False)),
                ('change_hands_interval', models.IntegerField(default=7)),
                ('image', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
            ],
        ),
        migrations.CreateModel(
            name='ExpensiveItemData',
            fields=[
                ('item_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('serial_id', models.CharField(default='Default Serial ID', max_length=100)),
                ('stock', models.IntegerField(default=1)),
                ('item_status', models.CharField(choices=[('B', 'Borrowed'), ('A', 'Available')], max_length=1)),
                ('weight', models.IntegerField(default=0)),
                ('condition', models.TextField(default="This is an item's default condition")),
                ('max_time', models.IntegerField(default=30)),
                ('late_penalty', models.IntegerField(default=100)),
                ('requires_admin_approval', models.BooleanField(default=False)),
                ('change_hands_interval', models.IntegerField(default=3)),
                ('reserved', models.BooleanField(default=False)),
                ('force_reserved', models.BooleanField(default=False)),
                ('image', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
            ],
        ),
    ]
