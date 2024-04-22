# Generated by Django 5.0.4 on 2024-04-21 08:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('machine_name', models.CharField(max_length=200)),
                ('machine_serial_no', models.CharField(max_length=30)),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductionLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cycle_no', models.CharField(max_length=200)),
                ('unique_id', models.CharField(max_length=30, unique=True)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('duration', models.DurationField()),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='machine_efficiency.machine')),
            ],
        ),
    ]