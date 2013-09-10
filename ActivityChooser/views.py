from django.http import HttpResponse
from django.shortcuts import render, redirect
from forms import ActivityChooseForm, ActivityRatingForm
from models import ActivityRating, Activity
import datetime

# Create your views here.
def index(request):
	return redirect('activity/choose')

#my method of dealing with model ids is going to be hacky.  This should probably end up in a session when I make it possible to have
#users/passwords/etc...

def chooseActivity(request):
	if request.method=='POST':
		aform=ActivityChooseForm(request.POST)
		aRating=aform.save(commit=False)
		aRating.preDateTime=datetime.datetime.now()
		aRating.save()
		rform=ActivityRatingForm(instance=aRating)
		pk=aRating.id
		return render(request, 'activity/rate.html', {'rform':rform, 'activity':aRating.activity, 'pk':pk}) 
	aform=ActivityChooseForm()
	return render(request, 'activity/choose.html',{'aform':aform})

def rateActivity(request):
	if request.method=='POST':
		aRating=ActivityRating.objects.get(pk=request.POST['pk'])
		rform=ActivityRatingForm(request.POST, instance=aRating)
		aRating=rform.save(commit=False)
		aRating.postDateTime=datetime.datetime.now()
		aRating.save()
		return redirect('/activity')
	else:
		pass	

def history(request):
	ratings=ActivityRating.objects.all()
	print len(ratings)
	return render(request, 'activity/history.html', {'ratings':ratings})

def data(request):
	activities=Activity.objects.all()
	return render(request, 'activity/data.html', {'activities':activities})
