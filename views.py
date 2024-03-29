#!/usr/bin/env python
#coding=utf-8
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django import newforms as forms
from inmobil.balance.models import *
from inmobil.historial.models import Pago

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
	"extra_context": {"administradoras": Administradora.objects.all()},
}

#Para info sobre crear/modificar/borrar objetos con vistas genericas ver pag 379 djangobook, "D5 Vistas genericas para crear/modificar/borrar"
#No se si el template depto_new.html tiene que estar dentro de balance.. :-/
depto = {
"model" : Depto,
"template_name": "balance/depto_new.html",
}


depto1 = {
"model" : Depto,
}


FormConsorcioNew = forms.form_for_model(Consorcio)
FormCategoriaItemNew = forms.form_for_model(CategoriaItem)


def consorcio_new(request):
    """vista de formulario para crear un nuevo consorcio y sus deptos."""   

    if request.method == 'POST':
		form_nuevo_consorcio = FormConsorcioNew(request.POST)
        #procesado de Formularios.             
		if  form_nuevo_consorcio.is_valid():
			consorcio = form_nuevo_consorcio.save()
			cantidad = consorcio.pisos * consorcio.alas
			for piso in range(consorcio.pisos):
				for ala in map(chr, range(65, 65+consorcio.alas)):
					new_depto = Depto()
					new_depto.consorcio = consorcio
					new_depto.piso = piso
					new_depto.ala = ala
					new_depto.coeficiente = 1 / float(cantidad)
					new_depto.gasto_fijo = float(consorcio.gasto_mensual_promedio) / float(cantidad)
					new_depto.save()
					
					
			return HttpResponseRedirect('/consorcio/' + str(consorcio.id) + '/deptos')
			
    else:
        form_nuevo_consorcio = FormConsorcioNew()  	
		
	
    return render_to_response('consorcio_new.html',
                                {'form_consorcio': form_nuevo_consorcio})





FormDeptoNew = forms.form_for_model(Depto, fields=('piso', 'ala', 'coeficiente','gasto_fijo','nombre_consorcista', 
					'tel_consorcista', 'email_consorcista', 'nombre_propietario', 'direccion_propietario'
					'tel_propietario','email_propietario'))

def consorcio_deptos(request, consorcio_id):
	consorcio = Consorcio.objects.get(id=consorcio_id)
	deptos = Depto.objects.filter(consorcio__exact=consorcio)
	#print consorcio
	alto = int(len(deptos) * 19) + 19
	
	
	if request.method == 'POST':
		form_nuevo_depto = FormDeptoNew(request.POST)	
		#procesado de Formularios.             
		if  form_nuevo_depto.is_valid():
			depto = form_nuevo_depto.save(commit=False)
			depto.consorcio = consorcio
			depto.save()
			
			
			return HttpResponseRedirect('/consorcio/' + str(consorcio.id) + '/deptos')
			
	else:
		form_nuevo_depto = FormDeptoNew()  	
			
	return render_to_response('consorcio_deptos.html', {'consorcio':consorcio, 'deptos':deptos, 'alto':alto, 'form_nuevo_depto':form_nuevo_depto})



def depto_delete(request, consorcio_id, depto_id):
	consorcio = Consorcio.objects.get(id=consorcio_id)
	depto = Depto.objects.get(id=depto_id)
	if depto.consorcio == consorcio:
		try:
			confirm = request.GET['confirm']
			#borra tambien todas las expensas de este depto. 
			pagos = Pago.objects.filter(depto__exact=depto)
			for pago in pagos:
				pago.delete()
			depto.delete() 
			return HttpResponseRedirect('/consorcio/' + str(consorcio.id) + '/deptos')
		except:
			return render_to_response('balance/depto_confirm_delete.html', {'consorcio':consorcio, 'depto':depto})
	else:
		return HttpResponse('el depto no pertenece a este consorcio')
			
		
def depto_modify_ajax(request, campo):
    try:
		value = request.POST['value']
		depto1 = Depto.objects.get(id=int(request.POST[u'id']))
		if campo=='gasto_fijo': #por qué concha tuve que ponerlo acá y no abajo.
								#no me lo explico
			depto1.gasto_fijo = float(value)		
    except KeyError:
        return HttpResponse('no hay valor')                
	
	print campo
	
    if campo=='coeficiente':
        depto1.coeficiente = float(value)
    if campo=='consorcista':
        depto1.nombre_consorcista = value
    if campo=='telefono':
        depto1.tel_consorcista = value
	if campo=='email':
		depto1.email_consorcista = value
    depto1.save()
    return HttpResponse(value)
    

##FormBalanceNew = forms.form_for_model(Balance, fields=('fecha_vencimiento', 'observacion'))

def depto_update(request, consorcio_id, piso, ala):
	depto = Depto.objects.filter(consorcio__exact=consorcio_id, piso__exact=piso, ala__exact=ala)[0]
	consorcio = Consorcio.objects.get(id=consorcio_id)
	
	EditDeptoForm = forms.form_for_instance(depto, fields=('piso', 'ala', 'coeficiente','gasto_fijo','nombre_consorcista', 
					'tel_consorcista', 'email_consorcista', 'nombre_propietario', 'direccion_propietario'
					'tel_propietario','email_propietario'))
	
	if request.method == 'POST':
		form_edit_depto = EditDeptoForm(request.POST)
		#procesado de Formularios.             
		if  form_edit_depto.is_valid():
			form_edit_depto.save()
			return HttpResponseRedirect('/consorcio/' + str(consorcio.id) + '/deptos')
	else:
		form_edit_depto = EditDeptoForm()		
	return render_to_response('depto_update.html', {'consorcio':consorcio, 'depto':depto, 'form_edit_depto' :form_edit_depto})
    
