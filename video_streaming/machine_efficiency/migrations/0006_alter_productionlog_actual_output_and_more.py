# Generated by Django 5.0.4 on 2024-04-21 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machine_efficiency', '0005_productionlog_actual_output_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productionlog',
            name='actual_output',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='productionlog',
            name='available_operating_time',
            field=models.DurationField(),
        ),
        migrations.AlterField(
            model_name='productionlog',
            name='bad_product',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='productionlog',
            name='good_product',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='productionlog',
            name='ideal_cycle_time',
            field=models.DurationField(),
        ),
        migrations.AlterField(
            model_name='productionlog',
            name='total_product',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='productionlog',
            name='unplanned_downtime',
            field=models.DurationField(),
        ),
    ]
