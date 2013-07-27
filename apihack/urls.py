from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^nodes$',                                        'nodes.views.nodes'),
    url(r'^nodes/(?P<node_id>\d+)$',                       'nodes.views.nodes'),
    url(r'^nodes/(?P<node_id>\d+)/evaluate$',              'nodes.views.evaluate'),
    url(r'^functions$',                                    'nodes.views.functions'),
    url(r'^functions/(?P<node_id>\d+)$',                   'nodes.views.functions'),
    url(r'^functions/builtin/(?P<name>(add|mult|lt|if))$', 'nodes.views.builtin'),
)
