from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'testproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^rolodex/', include('rolodex.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name':'admin/login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
)
