from django.http import HttpResponse
from django.shortcuts import render, redirect
from forms import ActivityChooseForm, ActivityRatingForm
from models import ActivityRating, Activity
import datetime
from operator import itemgetter
from django_session_stashable import SessionStashable
import json

# Create your views here.
def index(request):
	if request.user.is_authenticated():
		return redirect('/activity/dashboard/')
	return redirect('/activity/choose')

#my method of dealing with model ids is going to be hacky.  This should probably end up in a session when I make it possible to have
#users/passwords/etc...

def chooseActivity(request):
	if request.method=='POST':
		
		#OK this is super not the way to do this, but oh well
		#also, may end up trying to add an activity and not be able to
		#super confusing probably, not at all the right way to do things
		pvalues=request.POST.copy()
		if not request.POST['activity']:
			if len(request.POST['add_activity']):
				newActivity=Activity(name=request.POST['add_activity'])
				newActivity.save(request)
				pvalues['activity']=newActivity.id
		aform=ActivityChooseForm(pvalues, request=request)
		
		if aform.is_valid():
			aRating=aform.save(commit=False)
			aRating.preDateTime=datetime.datetime.now()
			aRating.save(request)
			rform=ActivityRatingForm(instance=aRating)
			pk=aRating.id
			redirectURL='/activity/'+str(pk)+'/rate/'
			return redirect(redirectURL) 
		else:
			return render(request, 'activity/choose.html', {'aform':aform})
	aform=ActivityChooseForm(request=request)
	return render(request, 'activity/choose.html',{'aform':aform})

#This can probably be cleaned up a bunch - kind of crufty
def rateActivity(request, rating_id):
	if request.method=='POST':
		aRating=ActivityRating.objects.get_with_permission(request, pk=rating_id)
		rform=ActivityRatingForm(request.POST, instance=aRating)
		aRating=rform.save(commit=False)
		aRating.postDateTime=datetime.datetime.now()
		aRating.save(request)
		return redirect('/activity')
	else:
		aRating=ActivityRating.objects.get_with_permission(request, pk=rating_id)
		rform=ActivityRatingForm(instance=aRating)
		return render(request, 'activity/rate.html', {'rform':rform, 'activity':aRating.activity.name, 'pk':rating_id})

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
	return render(request, 'activity/data_summary.html', {'actList':actList})

def detail(request, activity_id):
	activity=Activity.objects.get_with_permission(request, activity_id)
	ratings=ActivityRating.objects.special_filter(request, activity_id)
	return render(request, 'activity/detail.html', {'ratings':reversed(ratings),'activity':activity})


def getActivities(request):
	activities=Activity.objects.all_with_permission(request)
	act=[]
	for a in activities:
		act.append({'label':a.name, 'value':str(a.pk)})
	return HttpResponse(json.dumps(act))

def editActivities(request):
	activities=Activity.objects.all_with_permission(request)
	actList=[]
	for activity in activities:
		actList.append({
			'id':activity.id,
			'activity':activity.name,
			'tags':activity.activitytags.all(),
			'count':activity.actCount(request),
		})
	return render(request, 'activity/edit.html', {'actList':actList})

def dashboard(request):
	unrated=ActivityRating.objects.get_recent_unrated(request)
	recent=ActivityRating.objects.get_recent_rated(request)
	
	now=datetime.datetime.now()
	start=now-datetime.timedelta(hours=36)
	unrated=unrated.filter(preDateTime__range=(start, now))
	
	return render(request, 'activity/dashboard.html', {'unrated':unrated, 'recent':recent[:5]})
