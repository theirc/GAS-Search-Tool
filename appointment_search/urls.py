from django.conf.urls import url

import views

urlpatterns = [
    url(r'search$', views.SearchJSONView.as_view(), ),

]
