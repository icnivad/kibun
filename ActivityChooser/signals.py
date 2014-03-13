from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from registration.signals import user_registered
from models import Activity, ActivityRating
import pdb

@receiver(user_registered)
def lazy_signup(sender, **kwargs):
	request=kwargs['request']
	user=kwargs['user']
	
	Activity.reparent_all_my_session_objects(request.session, user)
	ActivityRating.reparent_all_my_session_objects(request.session, user, request)

	
@receiver(user_logged_in)
def lazy_login(sender, **kwargs):
	request=kwargs['request']
	user=kwargs['user']
	
	if request.user.is_active:
	
		#This is not at all where I want to put this code, but hopefully this should work for now more or less. 
		#Damn I need to debug things!
		if Activity.objects.all_with_permission(request).count()==0:
			#first create default activities
			defActs=Activity.objects.filter(is_default=1)
			for act in defActs:
				act.pk=None
				act.is_default=0
				act.save(request)

		Activity.reparent_all_my_session_objects(request.session, user)
		ActivityRating.reparent_all_my_session_objects(request.session, user, request)

