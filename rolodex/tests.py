from django.test import TestCase, RequestFactory
from django.test import Client
from django.core.urlresolvers import reverse
from rolodex.models import *
from django_webtest import WebTest
import pdb

client = Client()

class RolodexModelsTestCase(TestCase):
	
	def setUp(self):
		'''
		Add and get some types & roles.
		'''
		RELATION, get = p2org_type.objects.get_or_create(relationship_type='employment')
		ROLE = role.objects.create(role="boss")
		CONTACT_ROLE = org_contact_role.objects.create(role="front desk")
		
		'''
		Add two entities with a relation type employment.
		'''
		self.o1 = Org.objects.create(orgName="ACME, Corp.")
		self.p1 = Person.objects.create(firstName='John', lastName='Doe', role=ROLE)
		self.p1.add_p2org(self.o1,**{'relation':RELATION})

		'''
		Add two more entities that have no relationships.
		'''
		self.o2 = Org.objects.create(orgName="AJAX, Corp.")
		self.p2 = Person.objects.create(firstName='Jane', lastName='Doe')

	def test_relationship_methods(self):
		self.p1.add_p2p(self.p2)
		self.p1.remove_p2p(self.p2)
		self.o1.add_org2org(self.o2)
		self.o1.remove_org2org(self.o2)
		self.o1.add_org2p(self.p2)
		self.o1.remove_org2p(self.p2)

	def test_getter_methods(self):
		self.assertEqual(list(self.p1.get_relations()['orgs']),[self.o1])
		self.assertEqual(list(self.p1.get_employer()),[self.o1])
		self.assertEqual(list(self.o1.get_employees()),[self.p1])
		self.assertEqual(list(self.o1.get_employees_by_role('boss')),[self.p1])
		self.assertEqual(self.o1.get_relations_by_type('employment')['people'],[{'type':'employment','relation':self.p1}])
		self.assertEqual(self.o1.get_relations_with_type()['people'],[{'type':'employment','relation':self.p1}] )
		self.assertEqual(self.p1.nxGraph().has_node(self.o1),True)

class RolodexSimpleViewsTestCase(TestCase):
	
	def setUp(self):
		'''
		Add and get some types & roles.
		'''
		RELATION, get = p2org_type.objects.get_or_create(relationship_type='employment')
		ROLE = role.objects.create(role="boss")
		CONTACT_ROLE = org_contact_role.objects.create(role="front desk")
		
		'''
		Add two entities with a relation type employment.
		'''
		self.o1 = Org.objects.create(orgName="ACME, Corp.")
		self.p1 = Person.objects.create(firstName='John', lastName='Doe', role=ROLE)
		self.p1.add_p2org(self.o1,**{'relation':RELATION})

		'''
		Add two more entities that have no relationships.
		'''
		self.o2 = Org.objects.create(orgName="AJAX, Corp.")
		self.p2 = Person.objects.create(firstName='Jane', lastName='Doe')

		self.factory = RequestFactory()


	def test_home(self):	
		response = client.get(reverse('rolodex_home'))
		self.assertEqual(response.status_code,200)
	
	def test_search(self):
		response = client.get(reverse('rolodex_org',args=[self.o1.pk]))
		self.assertContains(response, self.o1.orgName , status_code=200)
		response = client.get(reverse('rolodex_person',args=[self.p1.pk]))
		self.assertContains(response, self.p1.lastName , status_code=200)
	


	def test_delete(self):
		response = client.post(reverse('rolodex_delete_person',args=[self.p2.pk]))
		self.assertEqual(response.status_code , 302)
		response = client.post(reverse('rolodex_delete_org',args=[self.o2.pk]))
		self.assertEqual(response.status_code , 302)

	

class RolodexFormsTestCase(WebTest):
	def setUp(self):
		'''
		Add and get some types & roles.
		'''
		RELATION, get = p2org_type.objects.get_or_create(relationship_type='employment')
		ROLE = role.objects.create(role="boss")
		CONTACT_ROLE = org_contact_role.objects.create(role="front desk")
		
		'''
		Add two entities with a relation type employment.
		'''
		self.o1 = Org.objects.create(orgName="ACME, Corp.")
		self.p1 = Person.objects.create(firstName='John', lastName='Doe', role=ROLE)
		self.p1.add_p2org(self.o1,**{'relation':RELATION})

		'''
		Add two more entities that have no relationships.
		'''
		self.o2 = Org.objects.create(orgName="AJAX, Corp.")
		self.p2 = Person.objects.create(firstName='Jane', lastName='Doe')


	def test_edit(self):
		form = self.app.get(reverse('rolodex_edit_person',args=[self.p2.pk])).form
		form['lastName'] = 'Doe, Jr.'
		form['position'] = 'Scientist'
		response = form.submit().follow()
		self.assertContains(response, 'Doe, Jr.' , status_code=200)

		form = self.app.get(reverse('rolodex_edit_org',args=[self.o2.pk])).form
		form['orgName'] = 'AJAX, Inc.'
		response = form.submit().follow()
		self.assertContains(response, 'AJAX, Inc.' , status_code=200)

	def test_create(self):
		'''
		Add a person with a bad email address. Fix the email and check for successful resubmit.
		'''
		form = self.app.get(reverse('rolodex_new_person',args=[self.o2.pk])).form
		form['lastName'] = 'Rabbit'
		form['firstName'] = 'Roger'
		form['person_contact-0-contact'] = 'nobugsbunny'
		form['person_contact-0-type'] = 'email'
		response = form.submit()
		self.assertContains(response, 'Enter a valid email address.')
		form = response.form
		form['person_contact-0-contact'] = 'nobugs@gmail.com'
		response = form.submit()
		self.assertContains(response, 'Person added! Add another?',status_code=200)