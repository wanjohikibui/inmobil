#!/usr/bin/env python
#coding=utf-8
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django import newforms as forms
from inmobil.balance.models import *

def index(request):
	"""vista de la pagina inicial del sistema"""
	administradora = Administradora.objects.get(id=1) #selecciono la 1º administrad **solo para probar
	return render_to_response('index.html', {'admin': administradora})




#def listarConsorcios(request):
#	"""Lista todos los consorcios que hay"""
#	consorcios = Consorcio.objects.all()
#	return render_to_response('balance/consorcio_list.html',{'consorcio_list': consorcios})


#def listarAdministradoras(reques):
#	"""Lista todas las administradoras que hay"""
#	administradoras = Administradora.objects.all()
#	return render_to_response('balance/administradora_list.html',{'administradora_list': administradoras})


administradora_info  = {
    "queryset" : Administradora.objects.all(),
    "template_object_name" : "administradora",    
}

consorcio_info  = {
    "queryset" : Consorcio.objects.all(),
    "template_object_name" : "consorcio",    
}