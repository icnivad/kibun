from django.http import HttpResponse
from django.shortcuts import render, redirect
from forms import ActivityChooseForm, ActivityRatingForm
from models import ActivityRating, Activity
import datetime
from operator import itemgetter
from django_session_stashable import SessionStashable


# Create your views here.
def index(request):
	return redirect('/activity/choose')

#my method of dealing with model ids is going to be hacky.  This should probably end up in a session when I make it possible to have
#users/passwords/etc...

def chooseActivity(request):
	if request.method=='POST':
		aform=ActivityChooseForm(request.POST)
		aRating=aform.save(commit=False)
		aRating.preDateTime=datetime.datetime.now()
		aRating.save(request)
		rform=ActivityRatingForm(instance=aRating)
		pk=aRating.id
		return render(request, 'activity/rate.html', {'rform':rform, 'activity':aRating.activity, 'pk':pk}) 
	aform=ActivityChooseForm()
	aform.fields['activity'].queryset=Activity.objects.all_with_permission(request)
	return render(request, 'activity/choose.html',{'aform':aform})

def rateActivity(request):
	if request.method=='POST':
		aRating=ActivityRating.objects.get_with_permission(request, pk=request.POST['pk'])
		rform=ActivityRatingForm(request.POST, instance=aRating)
		aRating=rform.save(commit=False)
		aRating.postDateTime=datetime.datetime.now()
		aRating.save(request)
		return redirect('/activity')
	else:
		pass	

def history(request):
	ratings=ActivityRating.objects.all_with_permission(request)
	return render(request, 'activity/history.html', {'ratings':reversed(ratings)})

def data(request):
	activities=Activity.objects.all_with_permission(request)
	actList=[]
	for activity in activities:
		actList.append({
			'id':activity.id,
			'activity':activity.name,
			'moodChange':activity.avgMoodChange(request),
			'feltBetter':activity.avgFeltBetter(request),
			'goodChoice':activity.avgGoodChoice(request),
			'count':activity.actCount(request),
		})
	actList=sorted(actList, key=itemgetter('moodChange'), reverse=True)
	return render(request, 'activity/data.html', {'actList':actList})

def detail(request, activity_id):
	activity=Activity.objects.get_with_permission(request, activity_id)
	ratings=ActivityRating.objects.special_filter(request, activity_id)
	return render(request, 'activity/detail.html', {'ratings':reversed(ratings), 'activity':activity})
