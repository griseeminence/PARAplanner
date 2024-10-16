# Generated by Django 5.1.1 on 2024-10-16 12:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_paratag_options_alter_paratag_title'),
        ('para', '0007_area_cover_image_project_cover_image_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='area',
            options={'ordering': ('title',), 'verbose_name': 'Area', 'verbose_name_plural': 'Areas'},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ('title',), 'verbose_name': 'Project', 'verbose_name_plural': 'Projects'},
        ),
        migrations.AlterModelOptions(
            name='resource',
            options={'ordering': ('title',), 'verbose_name': 'Resource', 'verbose_name_plural': 'Resources'},
        ),
        migrations.AlterField(
            model_name='area',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
        migrations.AlterField(
            model_name='area',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='covers/', verbose_name='Cover Image'),
        ),
        migrations.AlterField(
            model_name='area',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='area',
            name='deadline',
            field=models.DateField(blank=True, null=True, verbose_name='Deadline'),
        ),
        migrations.AlterField(
            model_name='area',
            name='description',
            field=models.TextField(max_length=1000, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='area',
            name='is_archived',
            field=models.BooleanField(default=False, verbose_name='Archive'),
        ),
        migrations.AlterField(
            model_name='area',
            name='priority',
            field=models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default=2, verbose_name='Priority'),
        ),
        migrations.AlterField(
            model_name='area',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('completed', 'Completed'), ('on_hold', 'On Hold')], default='active', max_length=10),
        ),
        migrations.AlterField(
            model_name='area',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='areas', to='core.paratag', verbose_name='Tag'),
        ),
        migrations.AlterField(
            model_name='area',
            name='title',
            field=models.CharField(max_length=25, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='project',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
        migrations.AlterField(
            model_name='project',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='covers/', verbose_name='Cover Image'),
        ),
        migrations.AlterField(
            model_name='project',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='project',
            name='deadline',
            field=models.DateField(blank=True, null=True, verbose_name='Deadline'),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(max_length=1000, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='project',
            name='is_archived',
            field=models.BooleanField(default=False, verbose_name='Archive'),
        ),
        migrations.AlterField(
            model_name='project',
            name='priority',
            field=models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default=2, verbose_name='Priority'),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('completed', 'Completed'), ('on_hold', 'On Hold')], default='active', max_length=10),
        ),
        migrations.AlterField(
            model_name='project',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='projects', to='core.paratag', verbose_name='Tag'),
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(max_length=25, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='covers/', verbose_name='Cover Image'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='deadline',
            field=models.DateField(blank=True, null=True, verbose_name='Deadline'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='description',
            field=models.TextField(max_length=1000, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='is_archived',
            field=models.BooleanField(default=False, verbose_name='Archive'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='priority',
            field=models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default=2, verbose_name='Priority'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='resource_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='para.resourcetype', verbose_name='Resource Type'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('completed', 'Completed'), ('on_hold', 'On Hold')], default='active', max_length=10),
        ),
        migrations.AlterField(
            model_name='resource',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='resources', to='core.paratag', verbose_name='Tag'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='title',
            field=models.CharField(max_length=25, verbose_name='Title'),
        ),
    ]
