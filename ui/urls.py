# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.views.generic import TemplateView

from ui.views import HomePageView

directives_patterns = [
    url(r'^language-choice.html$',
        TemplateView.as_view(template_name='angular/partials/directives/language-choice.html'), name='language-choice'),
    url(r'^forward-button.html$',
        TemplateView.as_view(template_name='angular/partials/directives/forward-button.html'), name='forward-button'),
    url(r'^back-button.html$',
        TemplateView.as_view(template_name='angular/partials/directives/back-button.html'), name='back-button'),
    url(r'^input-form.html$',
        TemplateView.as_view(template_name='angular/partials/directives/input-form.html'), name='input-form')
]

partial_patterns = [
    url(r'^language.html$', TemplateView.as_view(template_name='angular/partials/language.html'), name='language'),
    url(r'^searching-for.html$', TemplateView.as_view(template_name='angular/partials/searching-for.html'),
        name='searching-for'),
    url(r'^input.html$', TemplateView.as_view(template_name='angular/partials/input.html'),
        name='input'),
    url(r'^results.html$', TemplateView.as_view(template_name='angular/partials/results.html'), name='results'),

    url(r'^directives/', include(directives_patterns, namespace='directives'))
]

urlpatterns = [
    url(r'^partials/', include(partial_patterns, namespace='partials')),
    url(r'^$', HomePageView.as_view(), name='home'),
]
