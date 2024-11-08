# Generated by Django 5.1.1 on 2024-10-06 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_paratag_content_type_remove_paratag_object_id'),
        ('para', '0005_alter_area_deadline_alter_project_deadline_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='areas', to='core.paratag', verbose_name='Тег'),
        ),
        migrations.AddField(
            model_name='project',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='projects', to='core.paratag', verbose_name='Тег'),
        ),
        migrations.AddField(
            model_name='resource',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='resources', to='core.paratag', verbose_name='Тег'),
        ),
    ]
