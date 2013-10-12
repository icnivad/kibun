from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
def index(request):
	if request.user.is_authenticated():
		return redirect('/activity/dashboard/')
	return render(request, 'index.html', {})