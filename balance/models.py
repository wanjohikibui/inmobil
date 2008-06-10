#!/usr/bin/env python
#coding=utf-8
from django.db import models
PATH_ARCHIVOS = '%Y/%m/%d'

class Administradora(models.Model):
	"""El administrador del sistema"""
	nombre= models.CharField(max_length=200)
	direccion = models.CharField(max_length=250)
	observacion = models.TextField(blank=True, null=True)
	imagen = models.ImageField(upload_to=PATH_ARCHIVOS, height_field=100,width_field=100, null=True, blank=True)
	telefono = models.CharField(max_length=10)
	slogan = models.CharField(max_length=200, blank=True, null=True)
	email = models.EmailField(blank=True, null=True)
	sitio = models.URLField(verify_exists=False, blank=True, null=True)
	
	
	def __unicode__(self):
		return self.nombre
		
	
	class Admin:
		pass


class Consorcio(models.Model):
	"""El edificio administrado"""
	administradora = models.ForeignKey(Administradora)
	nombre= models.CharField(max_length=200)
	direccion = models.CharField(max_length=250)
	observacion = models.TextField(blank=True, null=True)
	
	def __unicode__(self):
		return self.nombre
		
	
	class Admin:
		pass	
	
class Depto(models.Model):
	"""cada una de las unidades de cobro"""
	consorcio = models.ForeignKey(Consorcio)
	piso = models.PositiveIntegerField()
	ala = models.CharField(max_length=2)
	coeficiente = models.DecimalField(max_digits=6, decimal_places=4)
	nombre_consorcista = models.CharField(max_length=200, blank=True, null=True)
	tel_consorcista = models.CharField(max_length=20, blank=True, null=True)
	email_consorcista = models.EmailField(blank=True, null=True)
	nombre_propietario = models.CharField(max_length=200, blank=True, null=True)
	direccion_propietario = models.CharField(max_length=200, blank=True, null=True)
	tel_propietario = models.TextField(max_length=20, blank=True, null=True)
	email_propietario = models.EmailField(blank=True, null=True)	
	
	def __unicode__(self):
		return unicode(self.piso) + u'º' + unicode(self.ala)

	class Admin:
		pass
	
class Balance(models.Model):
	consorcio = models.ForeignKey(Consorcio)
	fecha_creacion = models.DateField(auto_now=True)
	fecha_vencimiento = models.DateField()
	total = models.DecimalField(default=0, max_digits=8, decimal_places=2)
	observacion = models.TextField(blank=True, null=True)
	
	#cuando el usuario lo dispone, se cierra y se generan las expensas a pagar en el modelo pago., 
	balance_cerrado = models.BooleanField(default=False, editable=False) 
	
	def __unicode__(self):
		return u'%s %s' % (self.consorcio, self.fecha_vencimiento)
	
	class Admin:
		pass	
	

class CategoriaItem(models.Model):
	nombre = models.CharField(max_length=100, unique=True)

	def __unicode__(self):
		return self.nombre
	
	class Admin:
		pass	

class ItemBalance(models.Model):
	balance = models.ForeignKey(Balance)
	concepto = models.CharField(max_length=300)
	categoria = models.ForeignKey(CategoriaItem)
	monto = models.DecimalField(max_digits=8, decimal_places=2)
	
	def __unicode__(self):
		return self.concepto
	
	class Admin:
		pass

class ItemBalanceDefecto(models.Model):
	"""Estos son items que se ofrecen por defecto para un nuevo balance."""
	concepto = models.CharField(max_length=300)
	categoria = models.ForeignKey(CategoriaItem)
	monto = models.DecimalField(max_digits=8, decimal_places=2)	


	
	class Admin:
		pass	
	
