# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.views.generic import TemplateView

from ui.views import HomePageView

directives_patterns = [
    url(r'^language-choice.html$', TemplateView.as_view(template_name='angular/partials/directives/language-choice.html'), name='language-choice')
]

partial_patterns = [
    url(r'^language.html$', TemplateView.as_view(template_name='angular/partials/language.html'), name='language'),
]

urlpatterns = [
    url(r'^partials/', include(partial_patterns, namespace='partials')),
    url(r'^$', HomePageView.as_view(), name='home'),

]
