# Create your views here.
from django.http import Http404
from django.template import Template
from django.template import TemplateDoesNotExist
from inmobil.balance.models import Consorcio 
from django.shortcuts import render_to_response

def listarConsorcios(request):
    m_list = Consorcio.objects.all()
    return render_to_response('consorcios.html',{'m_list': m_list})

def listarAdministradora(request):
    m_list = Administradora.objects.all()
    return render_to_response('consorcios.html',{'m_list': m_list})    
    pass
    
def listarDepto(request):

    pass
    
def listarBalance(request):
    
    
    pass