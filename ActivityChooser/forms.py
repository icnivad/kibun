from django.forms import ModelForm
from django.forms import widgets
from django import forms
from crispy_forms.helper import FormHelper
import models

class ActivityChooseForm(ModelForm):
	def __init__(self, *args, **kwargs):
		self.request=kwargs.pop('request')
		super(ActivityChooseForm, self).__init__(*args, **kwargs)
		#self.helper = FormHelper()
		#self.helper.help_text_inline = True
		 
		choices=[(x.id, x.name) for x in models.Activity.objects.all_with_permission(self.request)]
		first=[('', '-------'), ('', 'ADD NEW ACTIVITY')]
		first.extend(choices)
		self.fields['activity'].choices=first
		self.fields['preMood'].help_text="For mood, 0 is the worst you've ever felt, 10 is the best you've ever felt"

	def clean_activity(self): #Really need to work on making this code less hacky!
		data=self.cleaned_data.get('activity')
		try:
			data=models.Activity.objects.get_with_permission(self.request, pk=data)
		except models.Activity.DoesNotExist:
			raise forms.ValidationError("Couldn't find activity")
		return data

	add_activity=forms.CharField(label="New Activity", widget=forms.TextInput(attrs={'id':'add_activity'}), required=False)
	activity=forms.ChoiceField()
	
	class Meta:
		model=models.ActivityRating
		widgets= {
			'feeling': widgets.Select(choices=models.presetFeelings) ,
			'preMood': widgets.Select(choices=models.presetMoods),
			'activity':widgets.Select(attrs={'id':'activity_original'}),
		}
		exclude=('user', 'preDateTime', 'postDateTime', 'postMood', 'feltBetter', 'goodChoice', 'comment')
	

class ActivityRatingForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(ActivityRatingForm, self).__init__(*args, **kwargs)
		self.fields['postMood'].required = True
		self.fields['postMood'].help_text="For mood, 0 is the worst you've ever felt, 10 is the best you've ever felt"

	
	class Meta:
		model=models.ActivityRating
		widgets= {
			'postMood': widgets.Select(choices=models.presetMoods)
		}
		exclude=('user', 'preDateTime', 'postDateTime', 'feeling', 'preMood', 'activity')

class ActivityForm(ModelForm):
	class Meta:
		model=models.Activity
		exclude=('user', 'is_default')