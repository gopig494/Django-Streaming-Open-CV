# Generated by Django 5.0.4 on 2024-04-20 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streaming', '0005_alter_video_video_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='video_url',
            field=models.FileField(blank=True, null=True, upload_to='videos'),
        ),
    ]
