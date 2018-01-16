from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect

def index(request):
	return HttpResponseRedirect("/register/moveto/")
