# Generated by Django 5.0.3 on 2025-07-12 10:21

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='aadhar',
            field=models.CharField(default='NA', max_length=12),
        ),
        migrations.AddField(
            model_name='booking',
            name='booking_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='booking',
            name='fee_status',
            field=models.CharField(choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')], default='Unpaid', max_length=10),
        ),
        migrations.AddField(
            model_name='booking',
            name='mobile',
            field=models.CharField(default='NA', max_length=15),
        ),
        migrations.AddField(
            model_name='booking',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='booking',
            name='sheet_number',
            field=models.PositiveIntegerField(default=0, unique=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='shift',
            field=models.CharField(default='', max_length=20),
        ),
    ]
