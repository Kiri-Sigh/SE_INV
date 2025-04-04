# Generated by Django 5.1.6 on 2025-04-04 19:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='borrowitemlist',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='borrow_item_User', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='borrowitemlist',
            name='cheap_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='borrow_item_Cheap_item_data', to='inventory.cheapitem'),
        ),
        migrations.AddField(
            model_name='cheapitem',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cheap_item_Categories', to='inventory.componentcategory'),
        ),
        migrations.AddField(
            model_name='expensiveitem',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='exp_item_Categories', to='inventory.componentcategory'),
        ),
        migrations.AddField(
            model_name='expensiveitemdata',
            name='expensive_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expensive_item_data_Expensive_items', to='inventory.expensiveitem'),
        ),
        migrations.AddField(
            model_name='expensiveitemdata',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='expensive_item_data_Users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='borrowitemlist',
            name='expensive_item_data',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='borrow_item_Exp_item_data', to='inventory.expensiveitemdata'),
        ),
    ]
