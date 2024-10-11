# Generated by Django 5.1.1 on 2024-10-06 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_paratag_content_type_remove_paratag_object_id'),
        ('tasks', '0007_delete_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='tasks', to='core.paratag', verbose_name='Тег'),
        ),
    ]