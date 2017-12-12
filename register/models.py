# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class User_Type(models.Model):
	id = models.AutoField(primary_key=True)
	type_name = models.CharField(max_length=15)
	canCheck = models.BooleanField(default=False) 
	gasPermission = models.BooleanField(default=False)
	electricityPermission = models.BooleanField(default=False)
	chimneyPermission = models.BooleanField(default=False)
	buildingPermission = models.BooleanField(default=False)
	isRegionalInspector = models.BooleanField(default=False)
	isStateInspector = models.BooleanField(default=False)

class State(models.Model):
        id = models.AutoField(primary_key=True)
        state_name = models.CharField(max_length=20)

class Region(models.Model):
        id = models.AutoField(primary_key=True)
        region_name = models.CharField(max_length=30)
        state = models.ForeignKey(State)

class City(models.Model):
        id = models.AutoField(primary_key=True)
        city_name = models.CharField(max_length=35)
        region = models.ForeignKey(Region)

class Street(models.Model):
        id = models.AutoField(primary_key=True)
        street_name = models.CharField(max_length=80)
        city = models.ForeignKey(City)

class User(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=30)
	second_name = models.CharField(max_length=30)
	region = models.ForeignKey(Region,null = True, default = None) #dla urzędnika
	address = models.CharField(max_length=60)
	city = models.CharField(max_length=30)
	postal_code = models.CharField(max_length=5)
	phone_number = models.CharField(max_length=15)
	password = models.CharField(max_length=512)
	username = models.CharField(max_length=64)
	type = models.ForeignKey(User_Type, null=True, on_delete=models.SET_NULL)

class Building(models.Model):
	id = models.AutoField(primary_key=True)
	street = models.ForeignKey(Street, null = True, default = None)
	number = models.CharField(max_length=60)
        postal_code = models.CharField(max_length=5)
	owner = models.CharField(max_length=60)
	owner_registered = models.ForeignKey(User, blank=True, null=True,default = None)


class Inspection(models.Model):
	id = models.AutoField(primary_key=True)
	controller_id = models.ForeignKey(User)
	building_id = models.ForeignKey(Building)
	gasInspection = models.BooleanField(default=False)
	electricityInspection = models.BooleanField(default=False)
        chimneyInspection = models.BooleanField(default=False)
        buildingInspection = models.BooleanField(default=False)
	date = models.DateTimeField(auto_now_add=True)
	description = models.CharField(max_length=500)

