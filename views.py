#!/usr/bin/env python
#coding=utf-8
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django import newforms as forms
from inmobil.balance.models import Administradora

def index(request):
	"""vista de la pagina inicial del sistema"""
	administradora = Administradora.objects.get(id=1) #selecciono la 1º administrad **solo para probar
	return render_to_response('index.html', {'admin': administradora})




