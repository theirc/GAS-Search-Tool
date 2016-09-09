# -*- coding: utf-8 -*-

import json
from django.conf import settings


def languages(request):
    return {
        'LANGUAGES': json.dumps([{'code': x[0], 'name': x[1]} for x in settings.LANGUAGES])
    }


def static_url(request):
    return {
        'STATIC_URL': settings.STATIC_URL,
    }


def url(request):
    return {
        'API_URL': settings.API_URL,
    }
