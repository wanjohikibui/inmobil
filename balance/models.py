#!/usr/bin/env python
#coding=utf-8
from django.db import models


class Administradora(models.Model):
	"""El administrador del sistema"""
	nombre= models.CharField(max_length=200)
	direccion = models.CharField(max_length=250)
	observacion = models.TextField(blank=True, null=True)
	imagen = models.ImageField(upload_to='/upload', height_field=50,width_field=50, null=True, blank=True)
	telefono = models.CharField(max_length=10)
	slogan = models.TextField(blank=True, null=True)
	email = models.CharField(max_length=100)
	
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
	
	def __unicode__(self):
		return unicode(self.piso) + u'º' + unicode(self.ala)

	class Admin:
		pass
	
class Balance(models.Model):
	consorcio = models.ForeignKey(Consorcio)
#	mes = models.IntegerField() Por las dudas las dejo comentadas
#	ano = models.IntegerField() Por las dudas las dejo comentadas
	fecha_creacion = models.DateField(auto_now=True)
	fecha_vencimiento = models.DateField()
	observacion = models.TextField(blank=True, null=True)
	
	def __unicode__(self):
		return u'%s (%i/%i)' % (self.consorcio, self.mes, self.ano)
	
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

class ItemBalanceDefecto(models.Model):
	"""Estos son items que se ofrecen por defecto para un nuevo balance."""
	concepto = models.CharField(max_length=300)
	categoria = models.ForeignKey(CategoriaItem)
	monto = models.DecimalField(max_digits=8, decimal_places=2)	


	
	class Admin:
		pass	
	
