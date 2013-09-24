from django.forms import ModelForm
from django.forms import widgets
from django import forms
import models

class ActivityChooseForm(ModelForm):
	readable_activity=forms.CharField(widget=forms.TextInput(attrs={'id':'activity_select'}))
	class Meta:
		model=models.ActivityRating
		widgets= {
			'feeling': widgets.Select(choices=models.presetFeelings) ,
			'preMood': widgets.Select(choices=models.presetMoods),
			'activity':widgets.HiddenInput(attrs={'id':'activity_hidden'}),
		}
		exclude=('user', 'preDateTime', 'postDateTime', 'postMood', 'feltBetter', 'goodChoice', 'comment')

class ActivityRatingForm(ModelForm):
	class Meta:
		model=models.ActivityRating
		widgets= {
			'postMood': widgets.Select(choices=models.presetMoods)
		}
		exclude=('user', 'preDateTime', 'postDateTime', 'feeling', 'preMood', 'activity')
