#!/usr/bin/env python
#coding=utf-8
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.template import Template
from django.template import TemplateDoesNotExist
from inmobil.balance.models import * 
from django.shortcuts import render_to_response
from django import newforms as forms
from inmobil.historial.models import Pago
from django.db.models import Q
import datetime


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
            instance.fecha_balance = instance.fecha_vencimiento - datetime.timedelta(30)
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
   
    #TODO se """SUPONE""" que hay solo 1 para este año/mes. Comprobarlo en la validacion del formulario de balances
    balance = Balance.objects.filter(consorcio__exact=consorcio, fecha_vencimiento__year=year, fecha_vencimiento__month=int(month))[0] 
    items = ItemBalance.objects.filter(balance__exact=balance)
    total = 0.0
    for item in items:
        total = total + float(item.monto)
        
        balance.total = total #guardo el total actual.
        balance.save()
        
    alto = int(len(items) * 19) + 19
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
            
            
    return render_to_response('balance/balance_detail.html',{"consorcio":consorcio, "balance":balance, 'items':items, 'form_add_item':form_add_item, 'alto':alto})


def balance_cerrar(request, consorcio_id, year, month):
    """ vista que confirma el cierre de un balance. Se genera una nueva expensa 
    para cada depto"""
    
    consorcio = Consorcio.objects.get(pk=consorcio_id)    
    #TODO se """SUPONE""" que hay solo 1 para este año/mes. Comprobarlo en la validacion del formulario de balances
    balance = Balance.objects.filter(consorcio__exact=consorcio, fecha_vencimiento__year=year, fecha_vencimiento__month=int(month))[0]
    if not balance.balance_cerrado:
        balance.balance_cerrado = True
        balance.save()
        #se agregan expensas (pagos) para todos los deptos de consorcio
        deptos = Depto.objects.filter(consorcio__exact=consorcio)
        for depto in deptos:
            nuevo_pago = Pago()
            nuevo_pago.depto = depto
            nuevo_pago.balance = balance
            nuevo_pago.monto_a_pagar = float(balance.total) * float(depto.coeficiente)
            nuevo_pago.save()
        
        return render_to_response('balance/balance_cerrado.html',{"consorcio":consorcio, "balance":balance})
    else:
        return HttpResponseRedirect('/consorcio/' +consorcio_id + '/' + str(year) + '-' + str(month) +  '/' )            

            
    
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
    
    
def balance_item_modify_ajax(request, campo):
    print request.POST
    try:
        id = int(request.POST[u'id'][0])
    except KeyError:
        return HttpResponse('no hay valor')                
        
    item = ItemBalance.objects.get(pk=id)
    print u"item: " + unicode(item)

    if campo=='concepto':
        item.concepto = request.POST['value']
    if campo=='categoria':
        categ = CategoriaItem.objects.get(nombre=request.POST['value'])
        item.categoria = categ
    if campo=='monto':
        item.monto = request.POST['value']
    item.save()
    return HttpResponse(request.POST['value'])
    
    
    
    
def pago_detail(request, consorcio_id, piso, ala, expensa):
    """Pago para un depto""" 
    #TODO Estudiar conceptualmente
    
   
    consorcio = Consorcio.objects.get(id=consorcio_id)
    depto = Depto.objects.filter(consorcio__exact=consorcio_id, piso__exact=piso, ala__exact=ala)[0]
    pago = Pago.objects.get(id=expensa)
    if not pago.depto==depto:
        return HttpResponse('esta expensa no corresponde a este depto')
    
    
    
    dif = datetime.date.today() - pago.balance.fecha_vencimiento
    if dif.days > 0:
        if pago.punitorios:
            punitorios = pago.punitorios
        else:
            punitorios = consorcio.administradora.interes_diario * dif.days * pago.monto_a_pagar
    else:
        punitorios = 0
    total = pago.monto_a_pagar + punitorios
    return render_to_response('balance/pago_detail.html', {'consorcio': consorcio, 'depto':depto, 'pago':pago, 'punitorios':punitorios, 'total':total})

def pago_detail_cerrar(request, consorcio_id, piso, ala, expensa):
    consorcio = Consorcio.objects.get(id=consorcio_id)
    depto = Depto.objects.filter(consorcio__exact=consorcio_id, piso__exact=piso, ala__exact=ala)[0]
    pago = Pago.objects.get(id=expensa)

    if not pago.depto==depto:
        return HttpResponse('esta expensa no corresponde a este depto')    
    
    pago.fecha_pago = datetime.date.today   ()
    dif = pago.fecha_pago - pago.balance.fecha_vencimiento
    if dif.days > 0:
        pago.punitorios = consorcio.administradora.interes_diario * dif.days * pago.monto_a_pagar
    else:
        pago.punitorios = 0
    pago.save()
    return HttpResponseRedirect('/consorcio/' +consorcio_id + '/depto' + str(depto.piso) + '-' + str(depto.ala) + '/exp' + str(pago.id))


def pago_informe(request, consorcio_id, piso, ala, expensa):
    consorcio = Consorcio.objects.get(id=consorcio_id)
    depto = Depto.objects.filter(consorcio__exact=consorcio_id, piso__exact=piso, ala__exact=ala)[0]
    pago = Pago.objects.get(id=expensa)    
    balance = pago.balance
    items = ItemBalance.objects.filter(balance__exact=balance)
    total = 0
    for item in items:
        total = total + item.monto
            
    return render_to_response('balance/informe.html',{"consorcio":consorcio, "balance":balance, 'items':items, 'pago':pago, 'depto':depto, 'total':total})


FormAddDepto = forms.form_for_model(Depto, fields=('consorcio_id', 'piso_id','ala_id'))
##FormBalanceNew = forms.form_for_model(Balance, fields=('fecha_vencimiento', 'observacion'))
def depto_new(request, consorcio_id, piso_id, ala_id):
    
    consorcio = Consorcio.objects.get(id=consorcio_id)
    
    form_nuevo_depto = FormAddDepto(request.POST)
    if request.method == 'POST':
        #procesado de Formularios.             
        if  form_nuevo_depto.is_valid():
            #TODO verificar que no exista un balance para el mismo mes/año
            instance = form_nuevo_depto.save(commit=False) #hago un save falso para guardar los demas datos
            instance.consorcio = consorcio_id
            instance.piso = piso_id
            instance.ala = ala_id
            instance.save()
            print request.POST
            
            return HttpResponseRedirect('/consorcio/' +consorcio_id + '/' + request.POST['fecha_vencimiento'][0:7] + '/' )            
        else:
            form_nuevo_depto = FormAddDepto()  
    return render_to_response('balance/depto_new.html',
                                {'form_depto': form_nuevo_depto, 'consorcio': consorcio})


def listarAdministradora(request):
    m_list = Administradora.objects.all()
    return render_to_response('consorcios.html',{'m_list': m_list})    
    pass
