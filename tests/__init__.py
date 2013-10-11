from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from django_webtest import WebTest
from django_nose.tools import assert_equals, assert_contains

class MyTestCase(WebTest):

	def setUp(self):
		User.objects.create_user(
			username='test',
			password='test123',
			email='test@test.com',
		)

	def testLogin(self):
		response = self.app.get('/', user='test')
		assert_equals('200 OK', response.status)
		assert_contains(response, 'test', count=1, status_code=200)

	def testChangePassword(self):
		change=self.app.get('/accounts/password/reset/', user='test')
		change.form['email']='test@test.com'
		response=change.form.submit("Submit")
		assert_equals('302 FOUND', response.status) #because we're redirecting from the original link?
 	 