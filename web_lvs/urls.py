from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('lvs.views',
    url(r'^addrealserver/$', 'AddRealserver', name='addRealserverurl'),
    url(r'^listrealserver/$', 'ListRealserver', name='listRealserverurl'),
    url(r'^editrealserver/(?P<ID>\d+)/$', 'EditRealserver', name='editRealserverurl'),
    url(r'^deleterealserver/(?P<ID>\d+)/$', 'DeleteRealserver', name='DeleteRealserverurl'),

    url(r'^addvip/$', 'AddVIP', name='addVIPurl'),
    url(r'^listvip/$', 'ListVIP', name='listVIPurl'),
    url(r'^editvip/(?P<ID>\d+)/$', 'EditVIP', name='editVIPurl'),
    url(r'^deletevip/(?P<ID>\d+)/$', 'DeleteVIP', name='DeleteVIPurl'),

    url(r'^keepalive/$', 'keepalive', name='keepaliveurl'),
    url(r'^createtemplate/$', 'createtemplate', name='createtemplateurl'),
    url(r'^rsynctemplate/$', 'rsynctemplate', name='rsynctemplateurl'),
    url(r'^admin/', include(admin.site.urls)),
)
