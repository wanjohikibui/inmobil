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


administradora_info  = {
    "queryset" : Administradora.objects.all(),
    "template_object_name" : "administradora",    
}

consorcio_info  = {
    "queryset" : Consorcio.objects.all(),
    "template_object_name" : "consorcio",    
}

#Para info sobre crear/modificar/borrar objetos con vistas genericas ver pag 379 djangobook, "D5 Vistas genericas para crear/modificar/borrar"
#No se si el template depto_new.html tiene que estar dentro de balance.. :-/
depto = {
"model" : Depto,
"template_name": "balance/depto_new.html",
}

FormConsorcioNew = forms.form_for_model(Consorcio)

def consorcio_new(request):
    """vista de formulario para crear un nuevo consorcio y sus deptos."""   
    form_nuevo_consorcio = FormConsorcioNew(request.POST)
    if request.method == 'POST':
        #procesado de Formularios.             
        if  form_nuevo_consorcio.is_valid():
			consorcio = form_nuevo_consorcio.save()
			cantidad = consorcio.pisos * consorcio.alas
			for piso in range(consorcio.pisos):
				for ala in map(chr, range(65, 65+consorcio.pisos)):
					new_depto = Depto()
					new_depto.consorcio = consorcio
					new_depto.piso = piso
					new_depto.ala = ala
					new_depto.coeficiente = 1 / float(cantidad)
					new_depto.save()
			
			return HttpResponseRedirect('/consorcio/' + str(consorcio.id) + '/deptos')
		
        else:
            form_nuevo_consorcio = FormConsorcioNew()  
			
    return render_to_response('consorcio_new.html',
                                {'form_consorcio': form_nuevo_consorcio})


def consorcio_deptos(request, consorcio_id):
	consorcio = Consorcio.objects.get(id=consorcio_id)
	deptos = Depto.objects.filter(consorcio__exact=consorcio)
	alto = int(len(deptos) * 19) + 19
	return render_to_response('consorcio_deptos.html', {'consorcio':consorcio, 'deptos':deptos, 'alto':alto})


	

