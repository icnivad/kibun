from django.contrib import admin
from ActivityChooser.models import Activity, ActivityRating
from django import forms
from django.contrib.auth.models import User

class CustomActivityForm(forms.ModelForm):
	user=forms.ModelChoiceField(queryset=User.objects.all(), empty_label="None", required=False)
	class Meta:
		model=Activity

class ActivityAdmin(admin.ModelAdmin):
	form=CustomActivityForm

	def save_model(self, request, obj, form, change):
		super(Activity, obj).save()

class ActivityRatingAdmin(admin.ModelAdmin):
	readonly_fields=('user',)
	
	def save_model(self, request, obj, form, change):
		super(ActivityRating, obj).save()

admin.site.register(Activity, ActivityAdmin)
admin.site.register(ActivityRating, ActivityRatingAdmin)