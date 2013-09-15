from django.conf.urls import patterns, include, url
import views, settings
import ActivityChooser
from django.contrib.auth.views import password_reset, password_reset_done, password_change, password_change_done
from django.views.generic import TemplateView, RedirectView


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.index, name='homepage'),
    url(r'users/', RedirectView.as_view(url='/activity/history')), #terrible, terrible way to do things, but it will work for the moment
    url(r'^activity/', include('ActivityChooser.urls', namespace='activity')),
    # url(r'^kibun/', include('kibun.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
     (r'^accounts/', include('registration.backends.simple.urls')),
)

urlpatterns += patterns('',
  (r'^accounts/profile/$', TemplateView.as_view(template_name='registration/profile.html')),
  (r'^accounts/password_reset/$', password_reset, {'template_name': 'registration/password_reset.html'}),
  (r'^accounts/password_reset_done/$', password_reset_done, {'template_name': 'registration/password_reset_done.html'}),
  (r'^accounts/password_change/$', password_change, {'template_name': 'registration/password_change.html'}),
  (r'^accounts/password_change_done/$', password_change_done, {'template_name': 'registration/password_change_done.html'}),
)


