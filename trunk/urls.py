#!/usr/bin/env python
#coding=utf-8
from django.conf.urls.defaults import *
from django.views.generic import list_detail 
from inmobil.balance.models import Consorcio, Administradora
from inmobil.views import *


urlpatterns = patterns('',
    
    (r'index/$', 'inmobil.views.index'), 
    
    (r'^consorcio/(?P<consorcio_id>\d+)/$', 'inmobil.balance.views.consorcio_detail'),

    (r'^consorcio/(?P<consorcio_id>\d+)/(?P<year>\d{4})-(?P<month>\d{2})/$', 'inmobil.balance.views.balance_detail'),    
    (r'^consorcio/(?P<consorcio_id>\d+)/balance/new', 'inmobil.balance.views.balance_new'),
    (r'^consorcio/(?P<consorcio_id>\d+)/balance/(?P<balance_id>\d+)', 'inmobil.balance.views.balance_add_modify'),

    

    #(r'^consorcios/$', 'inmobil.views.listarConsorcios'),     
    


    (r'^consorcios/',   list_detail.object_list, consorcio_info), #generic view. ver http://djangobook.com/en/1.0/chapter09/
    (r'^administradoras/',   list_detail.object_list, administradora_info),
    
    


    #contenido estático: javascript, css, etc
 	(r'^static/(.*)$','django.views.static.serve',{'document_root': 'static/', 'show_indexes': True}),
    #directorio de uploads accesible via web
 	(r'^media/(.*)$','django.views.static.serve',{'document_root': 'upload/', 'show_indexes': True}),

    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),
)
