# Generated by Django 5.1.1 on 2024-09-26 13:21

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('para', '0003_alter_area_title_alter_project_title_and_more'),
        ('tasks', '0004_task_created'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['-id'], 'verbose_name': 'ТегУДАЛИТЬМОДЕЛЬ', 'verbose_name_plural': 'ТегиУДАЛИТЬМОДЕЛЬ'},
        ),
        migrations.RemoveField(
            model_name='task',
            name='due_date',
        ),
        migrations.RemoveField(
            model_name='task',
            name='tags',
        ),
        migrations.AddField(
            model_name='task',
            name='area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='para.area'),
        ),
        migrations.AddField(
            model_name='task',
            name='deadline',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дедлайн'),
        ),
        migrations.AddField(
            model_name='task',
            name='is_archived',
            field=models.BooleanField(default=False, verbose_name='Архив'),
        ),
        migrations.AddField(
            model_name='task',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='para.project'),
        ),
        migrations.AddField(
            model_name='task',
            name='resource',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='para.resource'),
        ),
        migrations.AlterField(
            model_name='task',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='task',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 9, 26, 13, 21, 10, 933876, tzinfo=datetime.timezone.utc), verbose_name='Добавлено'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(max_length=1000, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.IntegerField(choices=[(1, 'Низкий'), (2, 'Средний'), (3, 'Высокий')], default=2, verbose_name='Приоритет'),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('active', 'Активный'), ('completed', 'Завершенный'), ('on_hold', 'Отложенный')], default='active', max_length=10),
        ),
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(max_length=25, verbose_name='Заголовок'),
        ),
    ]