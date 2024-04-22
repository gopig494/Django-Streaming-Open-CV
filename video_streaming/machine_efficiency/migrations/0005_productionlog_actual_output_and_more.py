# Generated by Django 5.0.4 on 2024-04-21 10:07

import machine_efficiency.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machine_efficiency', '0004_productionlog_ideal_cycle_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='productionlog',
            name='actual_output',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='productionlog',
            name='available_operating_time',
            field=models.DurationField(default=machine_efficiency.models.default_duration),
        ),
        migrations.AddField(
            model_name='productionlog',
            name='bad_product',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='productionlog',
            name='good_product',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='productionlog',
            name='unplanned_downtime',
            field=models.DurationField(default=machine_efficiency.models.default_duration),
        ),
        migrations.AlterField(
            model_name='productionlog',
            name='total_product',
            field=models.IntegerField(default=0),
        ),
    ]
