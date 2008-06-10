#!/usr/bin/env python
#coding=utf-8
from django.conf.urls.defaults import *
from django.views.generic import list_detail 
from inmobil.balance.models import Consorcio, Administradora, Depto
from inmobil.views import *
from django.views.generic import create_update




urlpatterns = patterns('',
    
    (r'index/$', 'inmobil.views.index'), 
    
    (r'^consorcio/(?P<consorcio_id>\d+)/$', 'inmobil.balance.views.consorcio_detail'),
    
    (r'^consorcio/(?P<consorcio_id>\d+)/balance/new', 'inmobil.balance.views.balance_new'),
    (r'^consorcio/(?P<consorcio_id>\d+)/(?P<year>\d{4})-(?P<month>\d{2})/cerrar$', 'inmobil.balance.views.balance_cerrar'),    
    (r'^consorcio/(?P<consorcio_id>\d+)/(?P<year>\d{4})-(?P<month>\d{2})/$', 'inmobil.balance.views.balance_detail'),    
    #(r'^consorcio/(?P<consorcio_id>\d+)/balance/(?P<balance_id>\d+)', 'inmobil.balance.views.balance_add_modify'),
    
    
    (r'^consorcio/(?P<consorcio_id>\d+)/depto(?P<piso>\d+)-(?P<ala>[A-Z]{1})/', 'inmobil.historial.views.depto_balance_detail'),
    
    

    (r'^balance/detalle-(?P<balance_id>\d+)', 'inmobil.balance.views.balance_detail_table_ajax'),
    
    #esta url es para la modificacion inline de items.
    (r'^balance/item/(?P<campo>(concepto|categoria|monto))', 'inmobil.balance.views.balance_item_modify_ajax'),

    #(r'^consorcios/$', 'inmobil.views.listarConsorcios'),     
    


    (r'^consorcios/',   list_detail.object_list, consorcio_info), #generic view. ver http://djangobook.com/en/1.0/chapter09/
    (r'^administradoras/',   list_detail.object_list, administradora_info),
    
    


    #contenido estático: javascript, css, etc
 	(r'^static/(.*)$','django.views.static.serve',{'document_root': 'static/', 'show_indexes': True}),
    #directorio de uploads accesible via web
 	(r'^media/(.*)$','django.views.static.serve',{'document_root': 'upload/', 'show_indexes': True}),


   #Alta/Modificacion de nuevos departamentos 
  (r'^depto/create/$', create_update.create_object, depto),
  (r'^depto/(?P<consorcio_id>\d+)/(?P<piso_id>\d+)-(?P<ala_id>[A-Z]{1})/create/new', 'inmobil.balance.views.depto_new'),
  (r'^depto/edit/(?P<object_id>d+)/$', create_update.update_object, depto),



    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),
)
