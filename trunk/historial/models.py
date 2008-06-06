#!/usr/bin/env python
#coding=utf-8
from django.db import models
from balance.models import Depto, Balance


class Pago(models.Model):
	"""pago de la expensas del Depto asociada a un Balance"""
	depto = models.ForeignKey(Depto)
	balance = models.ForeignKey(Balance) #esta asociado a un mes/año
	monto_a_pagar = models.DecimalField(max_digits=6, decimal_places=2)  #(balance.total * depto.coeficiente)* (1 + punitorios)
	fecha_pago = models.DateField()
	punitorios = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)
	
	def __unicode__(self):
		return unicode(self.depto) + " - " +  unicode(self.balance)
	
	class Admin:
		pass
	
#TODO lala