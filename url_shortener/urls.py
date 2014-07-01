from django.conf.urls import patterns, url, include
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^$', 'url_shortener.views.index'),
    (r'^submit/$', 'url_shortener.views.submit'),
    (r'^edit/(?P<shortcut>\w+)$', 'url_shortener.views.edit'),
    url(r'^admin/', include(admin.site.urls)),
    (r'^info/(?P<shortcut>\w+)$', 'url_shortener.views.info'),
    (r'^(?P<shortcut>\w+)$', 'url_shortener.views.follow'),
    (r'^(?P<shortcut>\w+)/(?P<params>.*)$', 'url_shortener.views.follow'),
)
