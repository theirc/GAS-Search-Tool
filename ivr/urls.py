from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.test, name='test'),
    url(r'incoming', views.incoming, name='incoming'),
    url(r'registration', views.registration, name='registration'),
    url(r'appointment', views.appointment, name='appointment'),
    url(r'complete_menu', views.complete_menu, name='complete_menu'),
]
