#!/usr/bin/env python
#coding=utf-8
from django.conf.urls.defaults import *
from django.shortcuts import render_to_response
from inmobil.balance.models import Consorcio, Administradora, Depto, CategoriaItem
from inmobil.views import *
from django.views.generic import create_update, list_detail



urlpatterns = patterns('',


    #panel de configuracion 
    (r'^configuracion/$', 'django.views.generic.simple.direct_to_template', {'template': 'configuracion.html'}),
    
    #CRUD para categorias
    (r'^configuracion/categoria/$', 'django.views.generic.list_detail.object_list',
     {'queryset': CategoriaItem.objects.all(),
      'allow_empty': True}),
   
    (r'^configuracion/categoria/new$', 'django.views.generic.create_update.create_object',
    {'model': CategoriaItem, 'post_save_redirect': '/configuracion/categoria/',}),

    (r'^configuracion/categoria/(?P<object_id>[0-9]+)/$', 'django.views.generic.create_update.update_object',
     {'model': CategoriaItem,
      'post_save_redirect': '/configuracion/categoria/'}),

    #del
    (r'^configuracion/categoria/delete/(?P<object_id>[0-9]+)$', 'django.views.generic.create_update.delete_object',
     {'model': CategoriaItem,
      'post_delete_redirect': '/configuracion/categoria/'}),


    #CRUD para administradoras
    (r'^configuracion/administradora/$', 'django.views.generic.list_detail.object_list',
     {'queryset': Administradora.objects.all(),
      'allow_empty': True}),

    (r'^configuracion/administradora/new$', 'django.views.generic.create_update.create_object',
    {'model': Administradora, 'post_save_redirect': '/configuracion/administradora/',}),

    (r'^configuracion/administradora/(?P<object_id>[0-9]+)/$', 'django.views.generic.create_update.update_object',
     {'model': Administradora,
      'post_save_redirect': '/configuracion/administradora/'}),

    (r'^configuracion/administradora/delete/(?P<object_id>[0-9]+)$', 'django.views.generic.create_update.delete_object',
     {'model': Administradora,
      'post_delete_redirect': '/configuracion/administradora/'}),



    
    
    
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
    
    #update de depto
    (r'^consorcio/(?P<consorcio_id>\d+)/depto(?P<piso>\d+)-(?P<ala>[A-Z]{1})/detalles', 'inmobil.views.depto_update'),
    

    #pago informe
    (r'^consorcio/(?P<consorcio_id>\d+)/depto(?P<piso>\d+)-(?P<ala>[A-Z]{1})/exp(?P<expensa>\d+)/imprimir_boleta', 'inmobil.balance.views.pago_informe'),            

    (r'^consorcio/(?P<consorcio_id>\d+)/depto(?P<piso>\d+)-(?P<ala>[A-Z]{1})/exp(?P<expensa>\d+)/imprimir_balance', 'inmobil.balance.views.pago_informe_balance'),            


    #pago y comprobante
    (r'^consorcio/(?P<consorcio_id>\d+)/depto(?P<piso>\d+)-(?P<ala>[A-Z]{1})/exp(?P<expensa>\d+)/cerrar', 'inmobil.balance.views.pago_detail_cerrar'),
    (r'^consorcio/(?P<consorcio_id>\d+)/depto(?P<piso>\d+)-(?P<ala>[A-Z]{1})/exp(?P<expensa>\d+)', 'inmobil.balance.views.pago_detail'),
    #historial de expensas para depto
    (r'^consorcio/(?P<consorcio_id>\d+)/depto(?P<piso>\d+)-(?P<ala>[A-Z]{1})/', 'inmobil.historial.views.depto_balance_detail'),
    
    #tabla de detalle del balance. usada por el grid
    (r'^balance/detalle-(?P<balance_id>\d+)', 'inmobil.balance.views.balance_detail_table_ajax'),
    
    #modificacion inline de items.
    (r'^balance/item/(?P<campo>(concepto|categoria|monto))', 'inmobil.balance.views.balance_item_modify_ajax'),

    #agregar nuevo consorcio y sus deptos asociados
    (r'^consorcios/new',  'inmobil.views.consorcio_new'),
    
    #agregar nueva categoria de items
    (r'^config/categoria',  'inmobil.views.categoria_item_new'),
    
            
    #listar consorcios generic view. ver http://djangobook.com/en/1.0/chapter09/
    (r'^consorcios/',   list_detail.object_list, consorcio_info), 
    
    
    
    
    (r'^administradoras/',   list_detail.object_list, administradora_info),
    
    


    #contenido estático: javascript, css, etc
 	(r'^static/(.*)$','django.views.static.serve',{'document_root': 'static/', 'show_indexes': True}),
    #directorio de uploads accesible via web
 	(r'^media/(.*)$','django.views.static.serve',{'document_root': 'upload/', 'show_indexes': True}),


   #modificacion inlinde de deptos.
    (r'^depto/ajax/(?P<campo>(coeficiente|consorcista|gasto_fijo|telefono|email))', 'inmobil.views.depto_modify_ajax'),
  

    #admin
    (r'^admin/', include('django.contrib.admin.urls')),
    #pagina principal
    (r'^$',  'django.views.generic.simple.redirect_to', {'url': '/consorcios'}), 
            
)
