# Generated by Django 5.1.1 on 2024-10-11 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0008_task_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='covers/', verbose_name='Обложка'),
        ),
    ]
