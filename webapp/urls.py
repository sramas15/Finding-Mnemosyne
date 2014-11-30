from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^json/new_log/(?P<card_id>\d+)/(?P<grade>\d+)/$', 'cards.views.new_log', name='new_log'),
    url(r'^json/get_study_queue/$', 'cards.views.get_study_queue', name='get_study_queue'),
    url(r'^json/get_study_queue/(?P<add_new>new)/$', 'cards.views.get_study_queue', name='get_study_queue'),
    url(r'^json/add_card_set/(?P<card_set_id>\d+)/$', 'cards.views.add_card_set', name='add_card_set'),
    url(r'^$', 'webapp.views.home', name='home'),
    url(r'^study/$', 'webapp.views.study', name='study'),
    url(r'^upload/$', 'webapp.views.upload_card_set', name='upload_card_set'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
)
