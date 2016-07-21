from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.uebersicht, name='uebersicht'),

    # /KRC001/
    #url(r'^(?P<reise_id>[0-9]+)/$', views.reiseseite, name='reiseseite'),

    url(r'^(?P<reise_slug>[-\w]+)/$', views.reiseseite, name='reiseseite'),

    # /china-mit-yangtze/161023
    url(r'^(?P<reise_slug>[-\w]+)/(?P<termin_slug>[-\w]+)/$', views.terminseite, name='terminseite'),

    # /china-mit-yangtze/161023/add
    url(r'^(?P<reise_slug>[-\w]+)/(?P<termin_slug>[-\w]+)/add$', views.add_day, name='day_add'),

    #url(r'^(?P<reise_slug>[-\w]+)/(?P<termin_slug>[-\w]+)/$', views.terminseite, name='terminseite'),

    # /KRC001/161023/tag2
    url(r'^(?P<reise_kurzel>[a-zA-z]{3,5}[0-9]{3,5})/(?P<datum>\d{6})/tag(?P<tag>\d{1,3})$', views.tagseite, name='tagseite'),

    # /KRC001/161023/add
    #url(r'^(?P<reise_kurzel>[a-zA-z]{3,5}[0-9]{3,5})/(?P<datum>\d{6})/add$', views.add_day, name='day_add'),

    # /Termine
    #url(r'^Termine$', views.termine, name='termine'),
]
