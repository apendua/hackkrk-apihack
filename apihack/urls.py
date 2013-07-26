from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^nodes$',                                     'apihack.api.nodes'),
    url(r'^nodes/(?P<node_id>\d+)$',                    'apihack.api.nodes'),
    url(r'^nodes/(?P<node_id>\d+)/evaluate$',           'apihack.api.evaluate'),
    url(r'^functions$',                                 'apihack.api.functions'),
    url(r'^functions/(?P<func_id>\d+)$',                'apihack.api.functions'),
    url(r'^functions/builtin/(?P<name>(add|mult|lt))$', 'apihack.api.builtin'),
)
