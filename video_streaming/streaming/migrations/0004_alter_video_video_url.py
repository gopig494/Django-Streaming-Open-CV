# Generated by Django 5.0.4 on 2024-04-18 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streaming', '0003_alter_video_video_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='video_url',
            field=models.FileField(upload_to='videos'),
        ),
    ]