from django.conf.urls import url

from . import views

app_name = 'forms'

urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^create/', views.create_form),	
]