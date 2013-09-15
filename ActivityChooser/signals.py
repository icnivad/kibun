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
	ActivityRating.reparent_all_my_session_objects(request.session, user)

	
@receiver(user_logged_in)
def lazy_login(sender, **kwargs):
	request=kwargs['request']
	user=kwargs['user']
	if request.user.is_active:
		Activity.reparent_all_my_session_objects(request.session, user)
		ActivityRating.reparent_all_my_session_objects(request.session, user)

