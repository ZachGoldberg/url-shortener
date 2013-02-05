from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^$', 'url_shortener.views.index'),
    (r'^submit/$', 'url_shortener.views.submit'),
    url(r'^admin/', include(admin.site.urls)),
    (r'^(?P<shortcut>\w+)$', 'url_shortener.views.follow'),
    (r'^info/(?P<shortcut>\w+)$', 'url_shortener.views.info'),
)
