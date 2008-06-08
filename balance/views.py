#!/usr/bin/env python
#coding=utf-8
from django.http import Http404, HttpResponseRedirect
from django.template import Template
from django.template import TemplateDoesNotExist
from inmobil.balance.models import * 
from django.shortcuts import render_to_response
from django import newforms as forms
from inmobil.historial.models import Pago
from django.db.models import Q

def consorcio_detail(request, consorcio_id):
    """muestra el detalle del consorcio y sus balances"""
    consorcio = Consorcio.objects.get(id=consorcio_id)
    deptos = Depto.objects.filter(consorcio=consorcio_id)
    balances = Balance.objects.filter(consorcio=consorcio_id).order_by("-fecha_vencimiento")
    return render_to_response('balance/consorcio_detail.html', {'consorcio': consorcio, 
                            'deptos':deptos, 'balances':balances})

FormBalanceNew = forms.form_for_model(Balance, fields=('fecha_vencimiento', 'observacion'))

def balance_new(request, consorcio_id):
    """vista de formulario para generar un nuevo balance para el consorcio."""   
    consorcio = Consorcio.objects.get(id=consorcio_id)
    form_nuevo_balance = FormBalanceNew(request.POST)
    if request.method == 'POST':
        #procesado de Formularios.             
        if  form_nuevo_balance.is_valid():
            #TODO verificar que no exista un balance para el mismo mes/año
            instance = form_nuevo_balance.save(commit=False) #hago un save falso para guardar los demas datos
            instance.consorcio = consorcio
            instance.save()
            print request.POST
            
            return HttpResponseRedirect('/consorcio/' +consorcio_id + '/' + request.POST['fecha_vencimiento'][0:7] + '/' )            
        else:
            form_nuevo_balance = FormBalanceNew()  
    return render_to_response('balance/balance_new.html',
                                {'form_balance': form_nuevo_balance, 'consorcio': consorcio})
    
    
FormAddItem = forms.form_for_model(ItemBalance, fields=('concepto', 'categoria','monto'))
    
def balance_detail(request, consorcio_id, year, month):
    """muestra el detalle de un balance, y la posibilidad de modificar o agregar items"""


    consorcio = Consorcio.objects.get(pk=consorcio_id)
    balance = Balance.objects.filter(consorcio__exact=consorcio, fecha_vencimiento__year=year, fecha_vencimiento__month=int(month))[0] #(se """SUPONE""" que hay solo 1 para este año/mes
    items = ItemBalance.objects.filter(balance__exact=balance)

    form_add_item = FormAddItem(request.POST)
    
    if request.method == 'POST':
        #procesado de Formularios.             
        if  form_add_item.is_valid():
            instance = form_add_item.save(commit=False) #hago un save falso para guardar los demas datos
            instance.balance = balance
            instance.save()
            return HttpResponseRedirect('/consorcio/' +consorcio_id + '/' + str(year) + '-' + str(month) +  '/' )            
        else:
            form_add_item = FormAddItem()
    return render_to_response('balance/balance_detail.html',{"consorcio":consorcio, "balance":balance, "items":items, 'form_add_item':form_add_item })
            
    
def balance_detail_table_ajax(request, balance_id):
    causa = Balance.objects.get(pk=balance_id)
    sentido = {'asc': '', 'desc': '-'}
    columna = ['id','concepto', 'categoria', 'monto']
    try:
        dir = request.GET['dir']
    except:
        dir = 'desc'
    try:
        orden = request.GET['sort'] 
    except:
        orden = 1

    items = ItemBalance.objects.filter(Q(balance=balance_id)).order_by(sentido[dir]+columna[int(orden)] )
    return render_to_response('balance/balance-tabla-ajax.html', {'items': items})
    
    
    
    
    
    
    
    
    
    
    
    
def pago_detail(request, pago_id):
    """Detalle de expensas para un departamento""" 
    #TODO Estudiar conceptualmente
    
    #Esto antes era balance_detail. Lo cual está MAL. Balance_detail es el detalle 
    #del gasto de todo el edificio, y pago_detail tiene que estar asociado a un depto en particular
    
    consorcio = Consorcio.objects.get(id=consorcio_id)
    deptos = Depto.objects.filter(consorcio=consorcio_id)
    monto = Pago.objects.filter(balance=consorcio_id)
    fecha = Balance.objects.filter(consorcio=consorcio_id)
    return render_to_response('balance/default_template.html', {'consorcio': consorcio, 'deptos':deptos, 'monto':monto, 'fecha': fecha})


def depto_balance_detail(reques, consorcio_id, piso="3ºD", ala="D"):
    """Lista balance por departamentos, ej http://zoka:8000/consorcio/1/depto3-D muestra el balance del departamento 3-D del consorcio 1"""
    #TODO falta el template
    #TODO No se como mierda recuperar el ID del departamento. 
    consorcio = Consorcio.objects.get(id=consorcio_id)
    deptos = Pago.objects.get(id="1")
    monto = Pago.objects.filter(depto="1")
    return render_to_response('balance/default_template.html', {'consorcio': consorcio,                             'deptos':deptos, 'monto':monto})


def listarAdministradora(request):
    m_list = Administradora.objects.all()
    return render_to_response('consorcios.html',{'m_list': m_list})    
    pass
    
def listarDepto(request):
    pass
    
def listarBalance(request):  
    pass
