# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import TemplateView
from .models import MainModel


class MainView(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['total'] = MainModel.objects.count()
        return context
