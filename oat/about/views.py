from django.views.generic.base import TemplateView


class InfoView(TemplateView):
    template_name = 'about/info.html'
