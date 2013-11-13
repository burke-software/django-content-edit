from django.conf.urls import *
from content_edit import views

urlpatterns = patterns('',
    url('^ajax_save_content/$', views.ajax_save_content, name='ajax_save_content'),
    url('^sample_content_edit/$', views.sample_content_edit, name='sample_content_edit'),

)
