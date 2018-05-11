from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns=[
    #url(r'^login/$',views.user_login,name='user_login'),
    url(r'login/$', auth_views.login, name='user_login'),
    url(r'logout/$', auth_views.logout,name='user_logout'),
    url(r'^register/$',views.register,name='register'),
    url(r'^change/$', auth_views.password_change,name='password_change')
]