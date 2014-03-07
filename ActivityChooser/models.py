from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User
from django_session_stashable import SessionStashable

import math, decimal

# Create your models here.

#built in choices
presetFeelings=(
	('1', 'happy'),
	('2', 'sad'),
	('3', 'angry'),
	('4', 'stressed'),
	('5', 'annoyed'),
	('6', 'anxious'),
	('7', 'ok'),
	('8', 'other'),
	('9', 'tired'),
	('10', 'lonely'),
	)

presetMoods=(
	('', '---------'),
	('0', '0'),
	('1', '1'),
	('2', '2'),
	('3', '3'),
	('4', '4'),
	('5', '5'),
	('6', '6'),
	('7', '7'),
	('8', '8'),
	('9', '9'),
	('10', '10'),
	)

boolChoices=(
	("No", "No"), 
	("Yes", "Yes"),
	("Not sure", "Not sure"),
)



class UserData(models.Model):
	user=models.ForeignKey(User, blank=True, null=True)
	creator_field='user'
	class Meta:
		abstract=True

class ActivityTag(UserData, SessionStashable):
	session_variable='tag_stash'
	name=models.CharField(max_length=200)
	activities=models.ManyToManyField('Activity', related_name="activitytags")

	
class ActivityManager(models.Manager):
	def all_with_permission(self, request):
		defActs=self.filter(is_default=True)
		activities=[]
		if request.user.is_active:
			activities=self.filter(user=request.user)
		else:
			activities=Activity.get_stashed_in_session(request.session)
		return (defActs | activities)
	
	def get_with_permission(self, request, pk):
		activity=self.get(pk=pk)
		if ((activity.is_default) or (activity.user==request.user) or (activity.stashed_in_session(request.session))):
			return activity
		return None
	
	def delete_with_permission(self, request, pk):
		activity=self.get(pk=pk)
		if ((activity.user==request.user) or (activity.stashed_in_session(request.session))):
			activity.delete()
			return True
		return False
	
class Activity(UserData, SessionStashable):
	context_count_name="activity_count"
	name=models.CharField(max_length=200, verbose_name="Activity Name")
	objects=ActivityManager()
	
	is_default=models.BooleanField(default=False)
	
	#django-sessionstashable
	session_variable='activity_stash'
	
	def __str__(self):
		return self.name
	
	def save(self, request):
		if request.user.is_active:
			self.user=request.user
			super(Activity, self).save()
		else:
			super(Activity, self).save()
			self.stash_in_session(request.session)
	
	def actCount(self, request):
		ratings=ActivityRating.objects.special_filter(request, self.id)
		return len(ratings)
	
	def avgMoodChange(self, request):
		ratings=ActivityRating.objects.special_filter(request, self.id)
		count=len(ratings)
		if (count==0):
			return None
		else:
			avg=0
			completeRatings=0.0
			for r in ratings:
				if((r.postMood==None) or (r.preMood==None)):
					pass
				else:
					completeRatings+=1.0
					avg+=r.postMood - r.preMood
			if completeRatings>0:
				avg=avg/decimal.Decimal(completeRatings)
				return math.ceil(avg*100)/100
			else:
				return None
		
	def avgFeltBetter(self, request):
		pcount=ActivityRating.objects.special_filter(request, self.id).filter(feltBetter="Yes").count()
		ncount=ActivityRating.objects.special_filter(request, self.id).filter(feltBetter="No").count()
		#don't want to get zero when we divide -> so convert to floats
		pcount=float(pcount)
		ncount=float(ncount)
		if (pcount+ncount)==0:
			return "More Data Needed"
		else:
			return (pcount-ncount)/(pcount+ncount)
	
	def avgGoodChoice(self, request):
		pcount=ActivityRating.objects.special_filter(request, self.id).filter(goodChoice="Yes").count()
		ncount=ActivityRating.objects.special_filter(request, self.id).filter(goodChoice="No").count()
		#don't want to get zero when we divide -> so convert to floats
		pcount=float(pcount)
		ncount=float(ncount)

		if (pcount+ncount)==0:
			return "More Data Needed"
		else:
			return (pcount-ncount)/(pcount+ncount)	

class ActivityRatingManager(models.Manager):
	def get_with_permission(self, request, pk):
		arating=self.get(pk=pk)
		if ((arating.user==request.user) or (arating.stashed_in_session(request.session))):
			return arating
		return None
		
	def all_with_permission(self, request):
		aratings=ActivityRating.get_stashed_in_session(request.session)
		if request.user.is_active:
			aratings=aratings | self.filter(user=request.user)
		return aratings
	
	def special_filter(self, request, activity_id):
		aratings=ActivityRating.get_stashed_in_session(request.session).filter(activity=activity_id)
		if request.user.is_active:
			aratings=aratings | self.filter(user=request.user).filter(activity=activity_id)
		return aratings
	
	def get_recent_unrated(self, request):
		aratings=ActivityRating.get_stashed_in_session(request.session).filter(postMood__isnull=True)
		if request.user.is_active:
			aratings=aratings | self.filter(user=request.user, postMood__isnull=True)
		return aratings.order_by('-preDateTime')
		
	def get_recent_rated(self, request):
		aratings=ActivityRating.get_stashed_in_session(request.session).filter(postMood__isnull=False)
		if request.user.is_active:
			aratings=aratings | self.filter(user=request.user, postMood__isnull=False)
		return aratings.order_by('-preDateTime')
	
	def best_moods(self, request):
		pass
		
	def worst_moods(self, request):
		pass


class ActivityRating(UserData, SessionStashable):
	context_count_name="activity_rating_count"
	
	#django-sessionstashable
	session_variable='activity_rating_stash'
	
	objects=ActivityRatingManager()
	
	feeling=models.CharField(max_length=200, choices=presetFeelings)
	preMood=models.DecimalField(verbose_name="What's your mood?", max_digits=3, decimal_places=1)
	preDateTime=models.DateTimeField()

	activity=models.ForeignKey(Activity)

	#Info below is filled out only after activity is completed
	postMood=models.DecimalField(verbose_name="What's your mood now?", max_digits=3, decimal_places=1, blank=True, null=True)
	postDateTime=models.DateTimeField(blank=True, null=True)	

	#just changed felt better to enjoyThisActivity -> all previous assoc. data is probably bad now.  
	#also should change name of field!!!! But that can wait I guess
	feltBetter=models.CharField(verbose_name="Did you enjoy this activity?", choices=boolChoices, blank=True, default="", max_length=50)
	goodChoice=models.CharField(verbose_name="Are you glad you did this activity?", choices=boolChoices, blank=True, default="", max_length=50) # are you glad you did the activity?
	comment=models.TextField(blank=True, default="")

	# may want to consider adding a checkbox for Did not complete activity (then would go to what did you do instead, etc...)

	def __str__(self):
		toReturn=str(self.preDateTime) + " " + str(self.preMood) + " " + str(self.activity) + " " + str(self.postMood)
		return toReturn
	
	def save(self, request):
		if request.user.is_active:
			self.user=request.user
			super(ActivityRating, self).save()
		else:
			super(ActivityRating, self).save()
			self.stash_in_session(request.session)
		
	
		
		
		
		
		