# Create your views here.
from inmobil.historial.models import Pago
from django.http import Http404
from django.template import Template
from django.template import TemplateDoesNotExist
from inmobil.balance.models import * 
from django.shortcuts import render_to_response

def pago_detail(request, year, day, month, consorcio_id):
    """muestra el detalle del pago por departamento"""
    consorcio = Consorcio.objects.get(id=consorcio_id)
    deptos = Depto.objects.filter(consorcio=consorcio_id)
    monto = Pago.objects.filter(balance=consorcio_id)
    fecha = Balance.objects.filter(consorcio=consorcio_id)
    return render_to_response('balance/pago_detail.html', {'consorcio': consorcio,                             'deptos':deptos, 'monto':monto, 'fecha': fecha})