from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'incoming', views.incoming, name='incoming'),
    url(r'registration', views.registration, name='registration'),
    url(r'confirmation', views.confirmation, name='confirmation'),
    url(r'appointment', views.appointment, name='appointment'),
    url(r'complete_menu', views.complete_menu, name='complete_menu')
]
