# Generated by Django 5.1.6 on 2025-02-20 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qr_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qrlog',
            name='qr_code',
            field=models.TextField(),
        ),
    ]
