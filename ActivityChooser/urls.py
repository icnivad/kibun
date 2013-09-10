from django.conf.urls import patterns, include, url
from ActivityChooser import views

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.index, name="index"),
    url(r'choose/', views.chooseActivity, name='choose'),
    url(r'rate/', views.rateActivity, name='rate'),
    url(r'history/', views.history, name='history'),
    url(r'data/', views.data, name='data'),
)
