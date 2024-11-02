from django.views.generic import TemplateView


class HomePage(TemplateView):
    """View for rendering the homepage."""

    template_name = 'index_mdb.html'
