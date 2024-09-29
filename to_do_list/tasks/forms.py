from django import forms

from .models import Task, Tag


class TaskForm(forms.ModelForm):
    new_tag = forms.CharField(max_length=25, required=False, help_text="Введите новый тег")

    class Meta:
        model = Task
        exclude = ('author',)
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'areaTitle',
                'placeholder': 'Введите заголовок'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'areaDescription',
                'placeholder': 'Описание области',
                'rows': 5
            }),
            'deadline': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control',
                'id': 'areaDeadline',
                'type': 'date'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select',
                'id': 'areaPriority'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
                'id': 'areaStatus'
            }),
            'is_archived': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'type': 'checkbox',
                'id': 'loginCheck',
            }),
            'area': forms.Select(attrs={
                'class': 'form-select',
                'id': 'areaStatus'
            }),
            'project': forms.Select(attrs={
                'class': 'form-select',
                'id': 'areaStatus'
            }),
            'resource': forms.Select(attrs={
                'class': 'form-select',
                'id': 'areaStatus'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        new_tag = cleaned_data.get('new_tag')
        tags = cleaned_data.get('tags')

        # Создайте или получите тег
        if new_tag:
            tag, created = Tag.objects.get_or_create(title=new_tag)
            if created:
                # Если тег был создан, он автоматически добавится в базу данных
                # Вам нужно вручную добавить его в теги задачи
                if tags:
                    tags = list(tags)  # Преобразуйте QuerySet в список
                    tags.append(tag)
                else:
                    tags = [tag]

        # Убедитесь, что значение tags вернется как список
        cleaned_data['tags'] = tags

        return cleaned_data
