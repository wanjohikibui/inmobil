# Create your views here.
from inmobil.historial.models import Pago
from django.http import Http404
from django.template import Template
from django.template import TemplateDoesNotExist
from inmobil.balance.models import * 
from inmobil.historial.models import Pago
from django.shortcuts import render_to_response



def pago_detail(request, year, day, month, consorcio_id):
    """muestra el detalle del pago por departamento"""
    consorcio = Consorcio.objects.get(id=consorcio_id)
    deptos = Depto.objects.filter(consorcio=consorcio_id)
    monto = Pago.objects.filter(balance=consorcio_id)
    fecha = Balance.objects.filter(consorcio=consorcio_id)
    return render_to_response('balance/pago_detail.html', {'consorcio': consorcio,                             'deptos':deptos, 'monto':monto, 'fecha': fecha})

def depto_balance_detail(request, consorcio_id, piso, ala):
    """Lista balance por departamentos, ej http://zoka:8000/consorcio/1/depto3-D muestra el balance del departamento 3-D del consorcio 1"""
    
    #consorcio = Consorcio.objects.get(id=consorcio_id)
    consorcio = Consorcio.objects.get(pk=consorcio_id)
    balances = Balance.objects.filter(consorcio__exact=consorcio)
    depto = Depto.objects.filter(consorcio__exact=consorcio_id, piso__exact=piso, ala__exact=ala)[0]
    pagos = Pago.objects.filter(depto__exact=depto)
    return render_to_response('historial/depto_history.html', {'consorcio': consorcio,'depto': depto, 'balances':balances, 'pagos': pagos})
