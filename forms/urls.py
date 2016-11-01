from django.conf.urls import url
from django.contrib.auth.views import login, logout
from . import views, forms

app_name = 'forms'

urlpatterns = [
    url(r'^$', views.home, name='home'),
	url(r'^create/', views.create_form, name='create'),
	url(r'^reschedule/', views.reschedule, name='reschedule'),
    url(r'^display/', views.display, name='display'),
    url(r'^detail/', views.detail, name='detail'),
    url(r'^approve/', views.approve, name='approve'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^login/$', login, {'template_name': 'login.html', 'authentication_form': forms.LoginForm}, name='login'),
    url(r'^logout/$', logout, {'next_page': 'forms:login'}, name='logout'),	
]