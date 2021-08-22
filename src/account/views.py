from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm
from account.models import City
from requests import get
from json import loads

def registration_form(request):
	context={}
	if request.POST:
		form=RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			login(request, account)
			return redirect('home')
		else:
			context['registration_form'] = form
	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'account/register.html', context)

def logout_view(request):
	logout(request)
	return redirect('home')

def showlist(request):
	results=City.objects.all
	
	if request.POST:
		val = request.POST["city"]
		print(val)
		url = 'https://danepubliczne.imgw.pl/api/data/synop'
		response = get(url)
		for row in loads(response.text):
			if row['stacja'] == 'Warszawa':
				print(row)
				return render(request, 'account/dropdown.html',{"showcity":results, "stacja":row})
	return render(request, 'account/dropdown.html',{"showcity":results})

# Create your views here.
