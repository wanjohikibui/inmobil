#!/usr/bin/env python
#coding=utf-8
from django.http import Http404, HttpResponseRedirect
from django.template import Template
from django.template import TemplateDoesNotExist
from inmobil.balance.models import * 
from django.shortcuts import render_to_response
from django import newforms as forms
from inmobil.historial.models import Pago


def consorcio_detail(request, consorcio_id):
    """muestra el detalle del consorcio y sus balances"""
    consorcio = Consorcio.objects.get(id=consorcio_id)
    deptos = Depto.objects.filter(consorcio=consorcio_id)
    balances = Balance.objects.filter(consorcio=consorcio_id).order_by("-fecha_vencimiento")
    return render_to_response('balance/consorcio_detail.html', {'consorcio': consorcio, 
                            'deptos':deptos, 'balances':balances})


FormBalanceNew = forms.form_for_model(Balance, fields=('fecha_vencimiento', 'observacion'))
FormAddItem = forms.form_for_model(ItemBalance, fields=('concepto', 'categoria','monto'))


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
    
    
    
    
    
    
def balance_detail(request, year, month, consorcio_id):
    """muestra el detalle del pago por departamento"""
    consorcio = Consorcio.objects.get(id=consorcio_id)
    deptos = Depto.objects.filter(consorcio=consorcio_id)
    monto = Pago.objects.filter(balance=consorcio_id)
    fecha = Balance.objects.filter(consorcio=consorcio_id)
    return render_to_response('balance/pago_detail.html', {'consorcio': consorcio,                             'deptos':deptos, 'monto':monto, 'fecha': fecha})



def listarAdministradora(request):
    m_list = Administradora.objects.all()
    return render_to_response('consorcios.html',{'m_list': m_list})    
    pass
    
def listarDepto(request):
    pass
    
def listarBalance(request):  
    pass
