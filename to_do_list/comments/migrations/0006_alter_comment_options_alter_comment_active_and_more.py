# Generated by Django 5.1.1 on 2024-10-16 12:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0005_alter_comment_text'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-created',), 'verbose_name': 'Comment', 'verbose_name_plural': 'Comments'},
        ),
        migrations.AlterField(
            model_name='comment',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype', verbose_name='Content Type'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(blank=True, max_length=2000, null=True, verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated'),
        ),
    ]