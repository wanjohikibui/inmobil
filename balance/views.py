# Create your views here.
from django.http import Http404
from django.template import Template
from django.template import TemplateDoesNotExist
from inmobil.balance.models import * 
from django.shortcuts import render_to_response


def consorcio_detail(request, consorcio_id):
    """muestra el detalle del consorcio y sus balances"""
    consorcio = Consorcio.objects.get(id=consorcio_id)
    deptos = Depto.objects.filter(consorcio=consorcio_id)
    balances = Balance.objects.filter(consorcio=consorcio_id).order_by("-fecha_vencimiento")
    return render_to_response('balance/consorcio_detail.html', {'consorcio': consorcio, 
                            'deptos':deptos, 'balances':balances})        
       


def listarAdministradora(request):
    m_list = Administradora.objects.all()
    return render_to_response('consorcios.html',{'m_list': m_list})    
    pass
    
def listarDepto(request):
    pass
    
def listarBalance(request):  
    pass
