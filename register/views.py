# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import *
from django.template import loader

from datetime import datetime,timedelta

from django.utils import timezone
from django.contrib.auth import login,authenticate,logout
from django.http import JsonResponse

from django.contrib.auth import logout, login
from django.template import RequestContext

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect

from .forms import FormularzRejestracji, FormularzLogowania

def index(request):
	return HttpResponse("Hello")

def moveto(request):
	contents = {} 
	contents["user"] = user_check(request)
	if(contents["user"] != False):
		if(User.objects.filter(id=contents["user"]["user_id"]).count()>0):
			user = User.objects.get(id=contents["user"]["user_id"])
			if (int(user.type.id) == 2):
				return HttpResponseRedirect("/register/official/")
			elif (int(user.type.id) == 3  or int(user.type.id) == 4  or int(user.type.id) == 5  or int(user.type.id) == 9):
				return HttpResponseRedirect("/register/ovw/")
	return HttpResponseRedirect("/register/login/")

def overview_panel(request):
	check = user_check(request)
	if (check == False):
		return HttpResponseRedirect('/')
	elif (check['isElectricity'] == False and check['isGas'] == False and check['isChimney'] == False and check['isBuilding'] == False):
		return HttpResponseRedirect('/')

	contents = {} 
	contents["user"] = user_check(request)
	template = loader.get_template("register/overview_options.html")    
    	output = template.render(contents)
    	return HttpResponse(output)

def official_panel(request):
	check = user_check(request)
	if (check == False):
		return HttpResponseRedirect('/')
	elif check['isOfficial'] == False:
		return HttpResponseRedirect('/')

	contents = {} 
	contents["user"] = user_check(request)
	if(contents["user"] == False):
		if(User.objects.filter(id=contents["user"]["user_id"]).count()>0):
			user = User.objects.get(id=contents["user"]["user_id"]) ##to error
			if (int(user.type.id) == 2):
				return HttpResponseRedirect("/register/login/")
	template = loader.get_template("register/official_options.html")    
    	output = template.render(contents)
    	return HttpResponse(output)



def user_check(request):
	users = User.objects.all()
	types = User_Type.objects.all()
	if(not users or not types):
		contents = {'title':'Błąd!', 'messageType':'danger', 'message':'Nieoczekiwany błąd!'}
		return False
	if not('login_check' in request.session):
		return False
	else:
		for l_user in users:
			if(l_user.id==int(request.session['login_check']) and l_user.type_id==None):
				return {'user_id':l_user.id}
			elif(l_user.id==int(request.session['login_check'])):
				return {'user_id':int(l_user.id),'username':l_user.username,'isOfficial':int(User_Type.objects.get(id=l_user.type_id).canCheck), 'isGas':int(User_Type.objects.get(id=l_user.type_id).gasPermission),'isElectricity':int(User_Type.objects.get(id=l_user.type_id).electricityPermission),'isChimney':int(User_Type.objects.get(id=l_user.type_id).chimneyPermission),'isBuilding':int(User_Type.objects.get(id=l_user.type_id).buildingPermission),'regionId':int(Region.objects.get(id=l_user.region_id).id)}
			else:
				contents = False
	return contents


def user_login(request):
	form = FormularzLogowania()
	contents = {} 
	contents["user"] = user_check(request)
	#get user info
	if(contents["user"] != False):
		return HttpResponseRedirect('/register/moveto/')
		#if(User.objects.filter(id=contents["user"]["user_id"]).count()>0):
		#	user = User.objects.get(id=contents["user"]["user_id"])
		#	row = {'name': user.name, 'surname': user.second_name }
		#	contents["user"]["data"] = row
	user = contents["user"]

	if request.method == 'POST':
        	form = FormularzLogowania(request.POST)
		if form.is_valid():
			c_username=form.cleaned_data['username']
			c_password=form.cleaned_data['password']
			users = User.objects.all()
			for c_user in users:
				if((c_user.username==str(c_username)) and (c_password==c_user.password)):
					#messages.add_message(request, messages.SUCCESS, 'Zalogowano poprawnie')
					request.session['login_check']=c_user.id
					return HttpResponseRedirect('/register/moveto/')
				else:
					error = True
			if(error):
				messages.error(request,'Podaj poprawną nazwę użytkownika i/lub hasło!')
	
	template = loader.get_template("registration/login.html")    
    	variables = RequestContext(request,{'form':form})
    	output = template.render(variables)
    	return HttpResponse(output)

def user_logout(request):
	if('login_check' in request.session):
		del request.session['login_check']
	return HttpResponseRedirect("/")

def logout_page(request):
    logout(request)
    return HttpResponseRedirect("/")

def register_page(request):
    if request.method == 'POST':
        form = FormularzRejestracji(request.POST)
        if form.is_valid():
            user = User(
 	    name=form.cleaned_data['name'],
	    second_name=form.cleaned_data['second_name'],
	    address=form.cleaned_data['adress'],
	    city=form.cleaned_data['city'],
	    phone_number=form.cleaned_data['phone'],
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            )
            user.last_name = form.cleaned_data['phone']
            user.save()
            if form.cleaned_data['log_on']:
                user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password1'])
                login(request,user)
                template = loader.get_template("main_page.html")
                variables = RequestContext(request,{'user':user})
                output = template.render(variables)
                return HttpResponseRedirect("/") 
            else:    
                template = loader.get_template("registration/register_success.html")
                variables = RequestContext(request,{'username':form.cleaned_data['username']})
                output = template.render(variables)
                return HttpResponse(output)            
    else:
        form = FormularzRejestracji()
    template = loader.get_template("registration/register.html")    
    variables = RequestContext(request,{'form':form})
    output = template.render(variables)
    return HttpResponse(output)

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

def official_show_all(request):
	check = user_check(request)
	if (check == False):
		return HttpResponseRedirect('/')
	elif check['isOfficial'] == False:
		return HttpResponseRedirect('/')
	
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
			my_region = 0
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
									if curReg.id == check["regionId"]:
										my_region = 1
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
			if my_region == 1:
				row = {'number':curBuild.number, 'owner':curBuild.owner, 'gas':gas, 'chimney':chimney, 'electricity':electricity, 'building':building, 'street':street , 'city':city, 'region':region, 'state':state}
				toDisp.append(row)
	context = {'context':toDisp,'username':check["username"]}
	template = loader.get_template('register/index.html')

	output = {'output':( (datetime.now() - timedelta(days = 1*365)) > datetime.now()) }
	
	return HttpResponse(template.render(context,request))

def official_show_non_actual(request):
	check = user_check(request)
	if (check == False):
		return HttpResponseRedirect('/')
	elif check['isOfficial'] == False:
		return HttpResponseRedirect('/')
	
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
			all_actual = 0
			my_region = 0
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
									if curReg.id == check["regionId"]:
										my_region = 1
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
			if gas == electricity == chimney == building == 'Aktualne':
				all_actual = 1
			if (my_region == 1 and all_actual == 0):
				row = {'number':curBuild.number, 'owner':curBuild.owner, 'gas':gas, 'chimney':chimney, 'electricity':electricity, 'building':building, 'street':street , 'city':city, 'region':region, 'state':state}
				toDisp.append(row)
	context = {'context':toDisp,'username':check["username"]}
	template = loader.get_template('register/index.html')

	output = {'output':( (datetime.now() - timedelta(days = 1*365)) > datetime.now()) }
	
	return HttpResponse(template.render(context,request))

def overview(request,what_choosed): # 0 -> województwa ; 1 -> powiat ; 2 -> miasto ; 3 -> ulica ; 4 -> dom
	check = user_check(request)
	if (check == False):
		return HttpResponseRedirect('/')
	elif (check['isElectricity'] == False and check['isGas'] == False and check['isChimney'] == False and check['isBuilding'] == False):
		return HttpResponseRedirect('/')

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
		context = {'adress':adress ,'next':next, 'coto':adress, 'electricity':check['isElectricity'], 'gas':check['isGas'],'chimney':check['isChimney'], 'building':check['isBuilding'] }
		template = loader.get_template('register/overview_2.html')
		return HttpResponse(template.render(context,request))
	elif what_choosed == '6':
		
		if request.method == 'POST':
			build__id = int(request.POST.get('build_id'))
			if request.POST.get('chimney_checkbox') == 'on':
				chimney_d = request.POST.get('chimney_d')
				uzytkownik = User.objects.get(id=int(check['user_id']))
				budynek = Building.objects.get(id=build__id)
				newInspection = Inspection(controller_id = uzytkownik , building_id = budynek , gasInspection = False, electricityInspection = False, chimneyInspection = True, buildingInspection = False, date = timezone.now(), description = chimney_d)
				newInspection.save()

			if request.POST.get('electr_checkbox') == 'on':
				chimney_d = request.POST.get('electr_d')
				uzytkownik = User.objects.get(id=int(check['user_id']))
				budynek = Building.objects.get(id=build__id)
				newInspection = Inspection(controller_id = uzytkownik , building_id = budynek , gasInspection = False, electricityInspection = True, chimneyInspection = False, buildingInspection = False, date = timezone.now(), description = chimney_d)
				newInspection.save()

			if request.POST.get('gas_checkbox') == 'on':
				chimney_d = request.POST.get('gas_d')
				uzytkownik = User.objects.get(id=int(check['user_id']))
				budynek = Building.objects.get(id=build__id)
				newInspection = Inspection(controller_id = uzytkownik , building_id = budynek , gasInspection = True, electricityInspection = False, chimneyInspection = False, buildingInspection = False, date = timezone.now(), description = chimney_d)
				newInspection.save()

			if request.POST.get('build_checkbox') == 'on':
				chimney_d = request.POST.get('build_d')
				uzytkownik = User.objects.get(id=int(check['user_id']))
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

def show_my_overview(request):
	check = user_check(request)
	if (check == False):
		return HttpResponseRedirect('/')
	elif (check['isElectricity'] == False and check['isGas'] == False and check['isChimney'] == False and check['isBuilding'] == False):
		return HttpResponseRedirect('/')

	inspections = Inspection.objects.all()
	toDisp = []
	if(inspections.count() > 0):
		for curIns in inspections:
			if curIns.controller_id_id == int(check['user_id']):
				adress = build_adress(curIns.building_id_id)
				ins_type = ''
				if curIns.gasInspection == True:
					ins_type = 'Instalacji gazowej' 
				elif curIns.electricityInspection == True:
					ins_type = 'Instalacji elektrycznej' 
				elif curIns.chimneyInspection == True:
					ins_type = 'Instalacji kominowej' 
				elif curIns.buildingInspection == True:
					ins_type = 'Budowlany'
				row = {'ins_type':ins_type , 'adress':adress , 'data':curIns.date , 'description':curIns.description }
				toDisp.append(row)
	#if toDisp[0]["ins_type"] ==  'Instalacji gazowej':
	#	a = 5/0
	context = {'context':toDisp,'username':check["username"]}
	template = loader.get_template('register/my_overviews.html')
	return HttpResponse(template.render(context,request))

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

