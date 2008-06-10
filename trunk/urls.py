#!/usr/bin/env python
#coding=utf-8
from django.conf.urls.defaults import *
from django.views.generic import list_detail 
from inmobil.balance.models import Consorcio, Administradora, Depto
from inmobil.views import *
from django.views.generic import create_update




urlpatterns = patterns('',
    #pagina principal
    (r'index/$', 'inmobil.views.index'), 
    
    
    
    #detalle consorcio
    (r'^consorcio/(?P<consorcio_id>\d+)/$', 'inmobil.balance.views.consorcio_detail'),
    

    
    #delete depto
    (r'^consorcio/(?P<consorcio_id>\d+)/deptos/(?P<depto_id>\d+)/delete$', 'inmobil.views.depto_delete'),    
  
    #agregar modificar departamentos de un consorcio
    (r'^consorcio/(?P<consorcio_id>\d+)/deptos$', 'inmobil.views.consorcio_deptos'),    
    
    
    #nuevo balance para el consorcio
    (r'^consorcio/(?P<consorcio_id>\d+)/balance/new', 'inmobil.balance.views.balance_new'),
    
    #cerrar balance 
    (r'^consorcio/(?P<consorcio_id>\d+)/(?P<year>\d{4})-(?P<month>\d{2})/cerrar$', 'inmobil.balance.views.balance_cerrar'),    
    
    #detalle de balance
    (r'^consorcio/(?P<consorcio_id>\d+)/(?P<year>\d{4})-(?P<month>\d{2})/$', 'inmobil.balance.views.balance_detail'),    
    
    #historial de expensas para depto
    (r'^consorcio/(?P<consorcio_id>\d+)/depto(?P<piso>\d+)-(?P<ala>[A-Z]{1})/', 'inmobil.historial.views.depto_balance_detail'),
    
    #tabla de detalle del balance. usada por el grid
    (r'^balance/detalle-(?P<balance_id>\d+)', 'inmobil.balance.views.balance_detail_table_ajax'),
    
    #modificacion inline de items.
    (r'^balance/item/(?P<campo>(concepto|categoria|monto))', 'inmobil.balance.views.balance_item_modify_ajax'),

    #agregar nuevo consorcio y sus deptos asociados
    (r'^consorcios/new',  'inmobil.views.consorcio_new'),
            
    #listar consorcios generic view. ver http://djangobook.com/en/1.0/chapter09/
    (r'^consorcios/',   list_detail.object_list, consorcio_info), 
    
    
    
    
    (r'^administradoras/',   list_detail.object_list, administradora_info),
    
    


    #contenido estático: javascript, css, etc
 	(r'^static/(.*)$','django.views.static.serve',{'document_root': 'static/', 'show_indexes': True}),
    #directorio de uploads accesible via web
 	(r'^media/(.*)$','django.views.static.serve',{'document_root': 'upload/', 'show_indexes': True}),


   #modificacion inlinde de deptos.
  
    (r'^depto/ajax/(?P<campo>(coeficiente|consorcista|telefono|email))', 'inmobil.views.depto_modify_ajax'),
  



    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),
)
