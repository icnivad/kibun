from django.forms import ModelForm
from django.forms import widgets
import models

class ActivityChooseForm(ModelForm):
	class Meta:
		model=models.ActivityRating
		widgets= {
			'feeling': widgets.Select(choices=models.presetFeelings) ,
			'preMood': widgets.Select(choices=models.presetMoods),
		}
		exclude=('user', 'preDateTime', 'postDateTime', 'postMood', 'feltBetter', 'goodChoice', 'comment')

class ActivityRatingForm(ModelForm):
	class Meta:
		model=models.ActivityRating
		widgets= {
			'postMood': widgets.Select(choices=models.presetMoods)
		}
		exclude=('user', 'preDateTime', 'postDateTime', 'feeling', 'preMood', 'activity')
