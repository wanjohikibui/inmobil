#!/usr/bin/env python
#coding=utf-8
from django.db import models
from inmobil.balance.models import Depto, Balance, Consorcio


class Pago(models.Model):
	"""pago de la expensas del Depto asociada a un Balance"""
	#consorsio = models.ForeignKey(Consorcio)
	#TODO aca el problema es que se pierde la relacion entre los departamentos y los consorcios, dejandote asignar un pago a cualquier departamento con cualquier consorcio.
	depto = models.ForeignKey(Depto)
	balance = models.ForeignKey(Balance) #esta asociado a un mes/año
	monto_a_pagar = models.DecimalField(max_digits=6, decimal_places=2)  #(balance.total * depto.coeficiente)* (1 + punitorios_mes_anterior)
	fecha_pago = models.DateField(null=True, blank=True)
	punitorios = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)
	
	def __unicode__(self):
		return unicode(self.depto) + " - " +  unicode(self.balance)
	
	class Admin:
		pass
	
