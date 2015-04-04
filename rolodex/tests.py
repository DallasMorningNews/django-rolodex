from django.test import TestCase, RequestFactory
from django.test import Client
from django.core.urlresolvers import reverse
from rolodex.models import *
from django_webtest import WebTest
import pdb

client = Client()

class RolodexModelsTestCase(TestCase):

	print("Starting models tests...")

	fixtures = ['rolodex_models_testdata.json']
	
	def setUp(self):
		self.o1 = Org.objects.get(slug="acme-corp")
		self.p1 = Person.objects.get(slug="john-doe")
		self.o2 = Org.objects.get(slug="ajax-corp")
		self.p2 = Person.objects.get(slug="jane-doe")

	def test_getter_methods(self):
		self.assertEqual(list(self.p1.get_relations()['orgs']),[self.o1])
		self.assertEqual(list(self.p1.get_employer()),[self.o1])
		self.assertEqual(list(self.o1.get_employees()),[self.p1])
		self.assertEqual(list(self.o1.get_employees_by_role('boss')),[self.p1])
		self.assertEqual(self.o1.get_relations_by_type('employment')['people'],[{'type':'employment','relation':self.p1}])
		self.assertEqual(self.o1.get_relations_with_type()['people'],[{'type':'employment','relation':self.p1}] )
		self.assertEqual(self.p1.nx_graph().has_node(self.o1),True)
		print(" >> Passed getter methods")
	
	def test_create_relationships(self):
		self.p1.add_p2p(self.p2)
		self.assertEqual(list(self.p1.get_relations()['people']),[self.p2])
		
		self.o1.add_org2org(self.o2,**{'hierarchy':'parent'})
		self.assertEqual(Org2Org.objects.get(from_ent=self.o2,to_ent=self.o1).hierarchy,'child')

		self.o1.add_org2p(self.p2)
		self.assertEqual(list(self.p2.get_relations()['orgs']),[self.o1])
		print(" >> Passed relationship create methods")

	def test_delete_relationships(self):
		self.p1.remove_p2p(self.p2)
		self.assertEqual(list(self.p2.get_relations_with_type()['people']),[])

		self.o1.remove_org2org(self.o2)
		self.assertEqual(list(self.o2.get_relations()['orgs']),[])
		
		self.o1.remove_org2p(self.p2)
		self.assertEqual(list(self.p2.get_relations()['orgs']),[])
		print(" >> Passed relationship delete methods")


	'''
	This test is not passing right now. See Org2Org model save method.
	'''
	# def test_hierarchy_recursion(self):
	# 	self.o1.add_org2org(self.o2)
	# 	relation = Org2Org.objects.get(from_ent=self.o1,to_ent=self.o2)
	# 	relation.hierarchy = 'parent'
	# 	relation.save()
	# 	self.assertEqual(Org2Org.objects.get(from_ent=self.o2,to_ent=self.o1).hierarchy,'child')
	# 	print(" >> Passed hierarchy recursion")

class RolodexViewsTestCase(WebTest):

	print("Starting views tests...")

	fixtures = ['rolodex_views_testdata.json']
	
	def setUp(self):
		self.o1 = Org.objects.get(slug="acme-corp")
		self.p1 = Person.objects.get(slug="john-doe")
		self.o2 = Org.objects.get(slug="ajax-corp")
		self.p2 = Person.objects.get(slug="jane-doe")

	def test_home(self):	
		response = client.get(reverse('rolodex_home'))
		self.assertEqual(response.status_code,200)
		print(" >> Passed home")
	
	def test_search(self):
		response = client.get(reverse('rolodex_org',args=[self.o1.slug]))
		self.assertContains(response, self.o1.orgName , status_code=200)
		response = client.get(reverse('rolodex_person',args=[self.p1.slug]))
		self.assertContains(response, self.p1.lastName , status_code=200)
		print(" >> Passed entity pages")

	def test_create_edit(self):
		'''
		Add a person with a bad email address. Fix the email and check for successful resubmit.
		'''
		form = self.app.get(reverse('rolodex_new_person',args=[self.o2.slug])).form
		form['lastName'] = 'Rabbit'
		form['firstName'] = 'Roger'
		form['person_contact-0-contact'] = 'nobugsbunny'
		form['person_contact-0-type'] = 'email'
		print(form['lastName'].value)
		response = form.submit()
		self.assertContains(response, 'Enter a valid email address.')
		form = response.form
		form['person_contact-0-contact'] = 'nobugs@gmail.com'
		response = form.submit()
		self.assertEqual(response.context['success'], True )
		'''
		Edit Person
		'''
		form = self.app.get(reverse('rolodex_edit_person',args=[self.p2.slug])).form
		form['lastName'] = 'Doe, Jr.'
		form['position'] = 'Scientist'
		response = form.submit().follow()
		self.assertContains(response, 'Doe, Jr.' , status_code=200)
		'''
		Edit Org
		'''
		form = self.app.get(reverse('rolodex_edit_org',args=[self.o2.slug])).form
		form['orgName'] = 'AJAX, Inc.'
		response = form.submit().follow()
		self.assertContains(response, 'AJAX, Inc.' , status_code=200)
		'''
		Edit Contact
		'''
		form = self.app.get(reverse('rolodex_edit_person',args=['roger-rabbit'])).form
		form['person_contact-0-contact'] = 'theRealRoger@gmail.com'
		response= form.submit().follow()
		self.assertContains(response, 'theRealRoger@gmail.com')
		#Delete the contact
		form = self.app.get(reverse('rolodex_edit_person',args=['roger-rabbit'])).form
		form['person_contact-0-DELETE'] = True
		response = form.submit().follow()
		self.assertNotContains(response, 'nobugs@gmail.com' , status_code=200)
		print(" >> Passed entity create and edit pages")

	def test_relation_create(self):
		'''
		Correspond to the new_org_relation & new_person_relation views.

		Org2Org
		'''
		form = self.app.get(reverse('rolodex_new_org_relation',args=[self.o1.slug])).forms[0]
		form['to_ent'] = self.o2.pk
		form['hierarchy'] = 'parent'
		response = form.submit()
		self.assertEqual(response.status_code,200)
		self.assertEqual(Org2Org.objects.get(from_ent=self.o2,to_ent=self.o1).hierarchy,'child')
		'''
		Check no duplicate relationships
		'''
		form = self.app.get(reverse('rolodex_new_org_relation',args=[self.o1.slug])).forms[0]
		form['to_ent'] = self.o2.pk
		response = form.submit()
		self.assertContains(response, 'That relationship already exists.')

		'''
		Org2P
		'''
		form = self.app.get(reverse('rolodex_new_org_relation',args=[self.o2.slug])).forms[1]
		form['to_ent'] = self.p2.pk
		response = form.submit()
		self.assertEqual(response.context['saved'],True)
		'''
		P2P
		'''
		form = self.app.get(reverse('rolodex_new_person_relation',args=[self.p2.slug])).forms[1]
		form['to_ent'] = self.p1.pk
		response = form.submit()
		self.assertEqual(response.context['saved'],True)
		'''
		P2Org
		'''
		form = self.app.get(reverse('rolodex_new_person_relation',args=[self.p2.slug])).forms[0]
		form['to_ent'] = self.o1.pk
		response = form.submit()
		self.assertEqual(response.context['saved'],True)

		print(" >> Passed relationship create page")

	def test_delete(self):
		response = client.post(reverse('rolodex_delete_person',args=[self.p2.slug]))
		self.assertEqual(response.status_code , 302)
		response = client.post(reverse('rolodex_delete_org',args=[self.o2.slug]))
		self.assertEqual(response.status_code , 302)
		print(" >> Passed delete page")



'''
Fixtures...
'''
# from rolodex.models import *
# RELATION, get = P2Org_Type.objects.get_or_create(relationship_type='employment')
# ROLE = PersonRole.objects.create(role="boss")
# CONTACT_ROLE = OrgContactRole.objects.create(role="front desk")
# o1 = Org.objects.create(orgName="ACME, Corp.")
# p1 = Person.objects.create(firstName='John', lastName='Doe', role=ROLE)
# p1.add_p2org(o1,**{'relation':RELATION})
# Org.objects.create(orgName="AJAX, Corp.")
# Person.objects.create(firstName='Jane', lastName='Doe')

#python manage.py dumpdata rolodex --format=json --indent=4 > testproject/fixtures/rolodex_models_testdata.json
#python manage.py dumpdata rolodex --format=json --indent=4 > testproject/fixtures/rolodex_views_testdata.json