from django.conf.urls import patterns, include, url
from ActivityChooser import views

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.index, name="index"),
    url(r'dashboard/', views.dashboard, name='dashboard'),
    url(r'choose/', views.chooseActivity, name='choose'),
    url(r'(?P<rating_id>\d*)/rate/', views.rateActivity, name='rate'),
    url(r'history/', views.history, name='history'),
    url(r'data/', views.data, name='data'),
    url(r'detail/(?P<activity_id>\d*)', views.detail, name='activity_detail'),
    url(r'getActivities/', views.getActivities, name='getActivities'),
    url(r'edit/', views.editActivities, name='editActivities'),
    url(r'delete/', views.deleteActivity, name='deleteActivity'),

)
