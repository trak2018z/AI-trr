# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import *
from django.template import loader

from datetime import datetime,timedelta

from django.utils import timezone

from django.http import JsonResponse

# Create your views here.
from django.http import HttpResponse

def index(request):
	return HttpResponse("Hello")

def official(request):
	buildings = Building.objects.all()
	inspections = Inspection.objects.all()
	streets = Street.objects.all()
	citys = City.objects.all()
	regions = Region.objects.all()
	states= State.objects.all()

	gas_chimney = timezone.now() - timedelta(days = 1*365)
	electricity_build = timezone.now() - timedelta(days = 5*365)
	if(buildings.count() > 0):
		toDisp = []
		for curBuild in buildings:
			street = ''
			city = ''
			region = ''
			state = ''
			for curStreet in streets:
				if(curStreet.id == curBuild.street_id):
					street =  curStreet.street_name
					for curCity in citys:
						if(curCity.id == curStreet.city_id):
							city = curCity.city_name
							for curReg in regions:
								if(curReg.id == curCity.region_id):
									region = curReg.region_name
									for curState in states:
										if(curState.id == curReg.state_id):
											state=curState.state_name				
 					

			gas = 'Nieaktualne'
                        electricity = 'Nieaktualne'
                        chimney = 'Nieaktualne'
                        building = 'Nieaktualne'
			for curInsp in inspections:
				if(curBuild.id == curInsp.building_id_id):
					if(curInsp.gasInspection == True and curInsp.date > gas_chimney):
						gas = 'Aktualne'
					if(curInsp.chimneyInspection == True and curInsp.date > gas_chimney):
                                                chimney = 'Aktualne'
					if(curInsp.electricityInspection == True and curInsp.date > electricity_build ):
                                                electricity = 'Aktualne'
					if(curInsp.buildingInspection == True and curInsp.date > electricity_build):
						building = 'Aktualne'

			row = {'number':curBuild.number, 'owner':curBuild.owner, 'gas':gas, 'chimney':chimney, 'electricity':electricity, 'building':building, 'street':street , 'city':city, 'region':region, 'state':state}
			toDisp.append(row)
	context = {'context':toDisp}
	template = loader.get_template('register/index.html')

	output = {'output':( (datetime.now() - timedelta(days = 1*365)) > datetime.now()) }
	
	return HttpResponse(template.render(context,request))


def overview(request,what_choosed): # 0 -> województwa ; 1 -> powiat ; 2 -> miasto ; 3 -> ulica ; 4 -> dom
	streets = Street.objects.all()
	citys = City.objects.all()
	regions = Region.objects.all()
	states = State.objects.all()

	buildings = Building.objects.all()

	toDisp = []


	#choosed_id = '0'
	next = '0'
	zmienna = '0'
	label = ''
	#if request.method == 'POST':
	#	choosed_id = request.POST.get('objects')
	#	zmienna = choosed_id

	if what_choosed == '0':
		for curState in states:
			row = {'object_name':curState.state_name, 'object_id':curState.id}
			toDisp.append(row)
		next = '1'
		label = 'wybierz województwo'
	elif what_choosed == '1':
		if request.method == 'POST':
			choosed_id = request.POST.get('objects')
		for curRegion in regions:
			if curRegion.state_id == int(choosed_id):
				row = {'object_name':curRegion.region_name, 'object_id':curRegion.id}
				toDisp.append(row)
		next = '2'
		label = 'wybierz powiat'
	elif what_choosed == '2':
		if request.method == 'POST':
			choosed_id = request.POST.get('objects')
		for curCity in citys:
			if curCity.region_id == int(choosed_id):
				row = {'object_name':curCity.city_name, 'object_id':curCity.id}
				toDisp.append(row)
		next = '3'
		label = 'wybierz miasto'
	elif what_choosed == '3':
		if request.method == 'POST':
			choosed_id = request.POST.get('objects')
		for curStreet in streets:
			if curStreet.city_id == int(choosed_id):
				row = {'object_name':curStreet.street_name, 'object_id':curStreet.id}
				toDisp.append(row)
		next = '4'
		label = 'wybierz ulicę'
	elif what_choosed == '4':
		if request.method == 'POST':
			choosed_id = request.POST.get('objects')
		for curBuild in buildings:
			if curBuild.street_id == int(choosed_id):
				row = {'object_name':curBuild.number, 'object_id':curBuild.id}
				toDisp.append(row)
		next = '5'
		label = 'wybierz budynek'

		
	elif what_choosed == '5':
		next = '6'
		if request.method == 'POST':
			choosed_id = request.POST.get('objects')
		for curBuild in buildings:
			if(curBuild.id == int(choosed_id)):
				zmienna = curBuild.id
		adress = build_adress(int(choosed_id))
		context = {'adress':adress ,'next':next, 'coto':adress}
		template = loader.get_template('register/overview_2.html')
		return HttpResponse(template.render(context,request))
	elif what_choosed == '6':
		
		if request.method == 'POST':
			build__id = int(request.POST.get('build_id'))
			if request.POST.get('chimney_checkbox') == 'on':
				chimney_d = request.POST.get('chimney_d')
				uzytkownik = User.objects.get(id=1)
				budynek = Building.objects.get(id=build__id)
				newInspection = Inspection(controller_id = uzytkownik , building_id = budynek , gasInspection = False, electricityInspection = False, chimneyInspection = True, buildingInspection = False, date = timezone.now(), description = chimney_d)
				newInspection.save()

			if request.POST.get('electr_checkbox') == 'on':
				chimney_d = request.POST.get('electr_d')
				uzytkownik = User.objects.get(id=1)
				budynek = Building.objects.get(id=build__id)
				newInspection = Inspection(controller_id = uzytkownik , building_id = budynek , gasInspection = False, electricityInspection = True, chimneyInspection = False, buildingInspection = False, date = timezone.now(), description = chimney_d)
				newInspection.save()

			if request.POST.get('gas_checkbox') == 'on':
				chimney_d = request.POST.get('gas_d')
				uzytkownik = User.objects.get(id=1)
				budynek = Building.objects.get(id=build__id)
				newInspection = Inspection(controller_id = uzytkownik , building_id = budynek , gasInspection = True, electricityInspection = False, chimneyInspection = False, buildingInspection = False, date = timezone.now(), description = chimney_d)
				newInspection.save()

			if request.POST.get('build_checkbox') == 'on':
				chimney_d = request.POST.get('build_d')
				uzytkownik = User.objects.get(id=1)
				budynek = Building.objects.get(id=build__id)
				newInspection = Inspection(controller_id = uzytkownik , building_id = budynek , gasInspection = False, electricityInspection = False, chimneyInspection = False, buildingInspection = True, date = timezone.now(), description = chimney_d)
				newInspection.save()

		context = {'next':next, 'coto':zmienna}
		template = loader.get_template('register/overview_apply.html')
		return HttpResponse(template.render(context,request))
	
		
	context = {'context':toDisp ,'next':next,'label':label , 'coto':zmienna}
	template = loader.get_template('register/overview.html')
	return HttpResponse(template.render(context,request))

def build_adress(build_id):
	buildings = Building.objects.all()
	streets = Street.objects.all()
	citys = City.objects.all()
	regions = Region.objects.all()
	states= State.objects.all()
		
	toDisp = []
	if(buildings.count() > 0):
		street = ''
		city = ''
		region = ''
		state = ''
		number= ''
		for curBuild in buildings:
			if(curBuild.id == build_id):
				number = curBuild.number
				for curStreet in streets:
					if(curStreet.id == curBuild.street_id):
						street =  curStreet.street_name
						for curCity in citys:
							if(curCity.id == curStreet.city_id):
								city = curCity.city_name
								for curReg in regions:
									if(curReg.id == curCity.region_id):
										region = curReg.region_name
										for curState in states:
											if(curState.id == curReg.state_id):
												state=curState.state_name
	output = {'state':state, 'region':region, 'city':city, 'street':street, 'number':number, 'build_id':build_id}
	return output

def overview_summary(request,build_id):
	zmienna = '5'
	if request.method == 'POST':
		choosed_id = request.POST.get('objects')
	adress = build_adress(int(choosed_id))
	context = {'adress':adress ,'next':next, 'coto':zmienna}
	template = loader.get_template('register/overview_2.html')
	return HttpResponse(template.render(context,request))

def overview_apply(request,build_id):
	
	context = {}
	template = loader.get_template('register/overview_apply.html')
	return HttpResponse(template.render(context,request))

