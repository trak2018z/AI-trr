# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import *
from django.template import loader

from datetime import datetime,timedelta

from django.utils import timezone

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
