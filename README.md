# PARAplanner

A powerful and flexible task management tool based on the **PARA** methodology and **Second Brain system**.

PARAplanner helps you stay organized by managing Projects, Areas, Resources, and Tasks.
It also includes advanced features like tagging, comments, dashboards, and search filters
to enhance productivity. This project is built using Django and PostgreSQL to ensure scalability
and robust data handling.

### Table of Contents

1. Project Features
2. Technologies Used
3. How to Use PARAplanner
4. Getting Starte
5. Project Models
6. Admin Management
7. Future Improvements

### Project Features

- PARA Methodology:
    - Manage Projects, Areas, Resources, and Tasks for long-term organization.
- Universal Tag System:
    - Apply tags across different models (Projects, Areas, Tasks, Notes) using GenericForeignKey for cross-model
      tagging.
- Custom Search Filters:
    - Filter tasks and resources using Django Filter with support for multiple fields (title, description).
- Project Dashboards:
    - Display the latest entries for Projects, Areas, Resources, Notes, and Tasks on a dashboard.
- Comments with Generic Relations:
    - Add and manage comments across different models using a generic comment system.
- Task Archiving:
    - Archive any entity (Project, Area, Resource, or Task) with an is_archived flag.
- Image Uploads:
    - Upload cover images for projects and resources with automatic resizing for consistent visuals.
- Integrated PostgreSQL Database:
    - Seamless database configuration with PostgreSQL for better performance and scaling.

### Technologies Used

- Backend Framework: Django 5.1.1
- Database: PostgreSQL
- Frontend: Bootstrap-based templates
- ORM & Querying: Django ORM, Django Filters
- Image Handling: Pillow for resizing and handling cover images
- Admin Interface: Custom Django Admin for all models

### How to Use PARAplanner

1. Organize Tasks using PARA:

    - Projects: Manage specific, time-bound initiatives.
    - Areas: Oversee broad, ongoing areas of responsibility.
    - Resources: Keep track of tools, information, and reference materials.
    - Notes: Add personal notes connected to Projects, Areas, or Resources.
    - Tasks: Manage your own tasks with possibility to bound it to different areas, projects, resources.
2. Tagging System:
    - Apply tags across all entities for easy filtering and searching.

3. Comments and Discussions:
    - Add comments to various models to track discussions and thoughts.

4. Dashboard Overview:
    - Monitor the latest entries and active tasks directly on the dashboard.

5. Archiving:
    - Mark old or inactive tasks, projects, or areas as archived to keep the workspace clean.

### Getting Started

1. Prerequisites
    - Python 3.10+
    - PostgreSQL
    - Pipenv (or pip for package management)
    - Git
2. Clone the Repository
    ```
    git clone <repository-url>
    cd PARAplanner
    ```
3. Install Dependencies
    ```
    pip install -r requirements.txt
    ```
4. Set Up the PostgreSQL Database

- Create a new PostgreSQL database.
- Update your settings.py with the following configuration:
    ```
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': '<your-database-name>',
            'USER': '<your-username>',
            'PASSWORD': '<your-password>',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```

5. Apply Migrations
    ```
    python manage.py migrate
    ```
6. Create a Superuser:
    ```
    python manage.py createsuperuser
    ```
7. Run the local Development Server:
    ```
    python manage.py runserver
    ```
   (!) Access the project at: http://127.0.0.1:8000

### Project Models and Optimizations

1. Base Models
    - BaseParaModel (Abstract): Contains shared fields like title, description, author, is_archived.
    - Project, Area, Resource, Note, Task: Derived from the base model to handle different aspects of PARA.
2. Comment System
    - Comment: Supports comments on any model using GenericForeignKey.
    - Includes timestamps for creation and updates, and an active status to mark visibility.
3. Tags System
    - ParaTag: Tags with a Many-to-Many relationship across all entities.
4. Common logic for creating comments, PARA-elements etc. optimized for "reusability"
in whole project just by **"import <function-name>"**.
    
    **_Example of comment utils:_**
    ```python
    def handle_edit_request(request, obj, get_context_data_func):
   
        comment_id = request.POST.get('comment_id')
        comment = get_comment(comment_id, obj, type(obj))
    
        if user_is_author(comment, request.user):
            context = get_context_data_func()
            context.update({
                'editing_comment': comment,
                'comment_form': CommentForm(initial={'text': comment.text})
            })
            return context
        return {}  # Optional: Handle unauthorized access
   
   class AreaDetailView(DetailView, LoginRequiredMixin):
        ...
   
        def get_context_data(self, **kwargs):
            ...

        def post(self, request, *args, **kwargs):
            self.object = self.get_object()

            if 'submit_comment' in request.POST:
                return handle_comment_creation(request, self.object, self.redirect_url)

            elif 'edit_comment' in request.POST:
                return handle_comment_editing(request, self.object, self.redirect_url)

            elif 'edit' in request.POST:
                context = handle_edit_request(request, self.object, self.get_context_data)
                if context:
                return self.render_to_response(context)

            elif 'delete_comment' in request.POST:
                return handle_comment_deletion(request, self.object, self.redirect_url)

            return self.get(request, *args, **kwargs)
    ``` 
    
### Admin Management

- Admin Interface Customizations
    - All models are registered in the admin panel with custom configurations for better management.
    - Projects, Areas, Resources: Display related tags, authors, and deadlines in the list view.
    - Tags and Comments: Filterable by related fields (authors, status, depending).

_Example admin setup:_

```python
class BaseParaAdmin(admin.ModelAdmin):
    """Base admin configuration for models with similar admin behavior."""

    list_display = (
        'title',
        '...',
    )
    list_filter = (
        'title',
        '...',
    )
    search_fields = ('title', 'description', 'author__username')
    ordering = ('-created', 'priority', 'deadline')
    autocomplete_fields = ['tags']
    date_hierarchy = 'created'
    list_per_page = 20
    readonly_fields = ('id',)
    prepopulated_fields = {'title': ('title',)}

    def get_tags(self, obj):
        """Retrieve and display related tags as a comma-separated string."""

        return ", ".join([tag.title for tag in obj.tags.all()])

    get_tags.short_description = 'Tags'


# Наследуемся от базового класса для конкретных моделей

@admin.register(Area)
class AreaAdmin(BaseParaAdmin):
    """Admin configuration for the Area model."""
    pass

... ... ...
```

### Future Improvements

- User Administration Panel:
    - Add features for customize user's accounts, dashboard and control panel for improvement user experience.
- New front-end
    - Renew front-end part of the project via React library
- API Integration:
    - Create RESTful APIs to integrate with external apps or enable mobile access.
- Task Dependencies:
    - Allow tasks to depend on each other with automated notifications.
- Notification System:
    - Implement email or in-app notifications for task deadlines and updates.
- Chat System:
    - Implement chat application to improve communication between owners and users.
- Payment System:
    - Create payment system to put the project into market.

### Conclusion

_PARAplanner offers a powerful and structured way to organize your work and personal life
using the PARA methodology. With features like universal tagging, search filtering,
dashboards, and comments, it is an ideal solution for individuals or teams aiming to
manage their projects efficiently._

_Feel free to contribute, suggest improvements, or report issues on the repository!
Happy planning! 🎯_

### License

_**This project is licensed under the MIT License.**_