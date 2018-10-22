from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^create/$', views.create),
    url(r'^login/$', views.login),
    url(r'^dashboard/$', views.dashboard),
    url(r'^jobs/new/$', views.add_job),
    url(r'^jobs/process/$', views.process),
    url(r'^remove/$', views.remove),
    url(r'^jobs/(?P<id>\d+)/$', views.job),
    url(r'^jobs/edit/(?P<id>\d+)/$', views.edit_job),
    url(r'^jobs/edit/(?P<id>\d+)/process/$', views.edit_process),
    url(r'^logout/', views.logout),

]
