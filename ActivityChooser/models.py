from django.db import models
from django.db.models import Avg
import math 

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
	)

presetMoods=(
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

class Activity(models.Model):
	name=models.CharField(max_length=200)

	def __str__(self):
		return self.name
	
	def avgMoodChange(self):
		ratings=ActivityRating.objects.filter(activity=self.id)
		count=len(ratings)
		if (count==0):
			return ""
		else:
			avg=0
			for r in ratings:
				if((r.postMood==None) or (r.preMood==None)):
					pass
				else:
					avg+=r.postMood - r.preMood
			avg=avg/len(ratings)
			return math.ceil(avg*100)/100
		
	def avgFeltBetter(self):
		pcount=ActivityRating.objects.filter(activity=self.id).filter(feltBetter="Yes").count()
		ncount=ActivityRating.objects.filter(activity=self.id).filter(feltBetter="No").count()
		if (pcount+ncount)==0:
			return "More Data Needed"
		else:
			return (pcount-ncount)/(pcount+ncount)
	
	def avgGoodChoice(self):
		pcount=ActivityRating.objects.filter(activity=self.id).filter(goodChoice="Yes").count()
		ncount=ActivityRating.objects.filter(activity=self.id).filter(goodChoice="No").count()
		if (pcount+ncount)==0:
			return "More Data Needed"
		else:
			return (pcount-ncount)/(pcount+ncount)	

class ActivityRating(models.Model):
	feeling=models.CharField(max_length=200)
	preMood=models.DecimalField(max_digits=3, decimal_places=1)
	preDateTime=models.DateTimeField()

	activity=models.ForeignKey(Activity)

	#Info below is filled out only after activity is completed
	postMood=models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
	postDateTime=models.DateTimeField(blank=True, null=True)	

	feltBetter=models.CharField(verbose_name="Do you feel better?", choices=boolChoices, blank=True, default="", max_length=50)
	goodChoice=models.CharField(verbose_name="Are you glad you did this activity?", choices=boolChoices, blank=True, default="", max_length=50) # are you glad you did the activity?
	comment=models.TextField(blank=True, default="")

	# may want to consider adding a checkbox for Did not complete activity (then would go to what did you do instead, etc...)

	def __str__(self):
		toReturn=str(self.preDateTime) + " " + str(self.preMood) + " " + str(self.activity) + " " + str(self.postMood)
		return toReturn
		
		
		
		
		
		