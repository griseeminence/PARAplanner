# Generated by Django 5.1.1 on 2024-09-29 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_alter_comment_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(max_length=2000, verbose_name='Текст комментария'),
        ),
    ]
