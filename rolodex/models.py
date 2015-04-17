from django.db import models
from itertools import chain
from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils.translation import ugettext as _
from django.core.validators import URLValidator,validate_email


from rolodex.slug import unique_slugify

class GetOrNoneManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


###################
## Choice Models ##
###################

'''
Choice models are registered in the admin and are designed to be set by user prior to entering entities into Rolodex.
'''

class OpenRecordsLaw(models.Model):
	'''
	Which open records law applies to the org.
	'''
	slug = models.SlugField(unique=True,editable=False)
	name = models.CharField(max_length=250)
	link = models.URLField(blank=True,null=True)

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		unique_slugify(self,self.name)
		super(OpenRecordsLaw, self).save(*args, **kwargs)

class PersonRole(models.Model):
	'''
	Define some roles, preferably ones useful for filtering on, e.g. "Media Contact", "FOIA Officer".
	'''
	slug = models.SlugField(unique=True,editable=False)
	role = models.CharField(max_length=250)
	description = models.TextField(blank=True,null=True)

	def __unicode__(self):
		return self.role

	def save(self, *args, **kwargs):
		unique_slugify(self,self.role)
		super(PersonRole, self).save(*args, **kwargs)

class OrgContactRole(models.Model):
	'''
	Define roles for org contacts, e.g., FOIA email, etc.
	'''
	slug = models.SlugField(unique=True,editable=False)
	role = models.CharField(max_length=250)
	description = models.TextField(blank=True,null=True)

	def __unicode__(self):
		return self.role

	def save(self, *args, **kwargs):
		unique_slugify(self,self.role)
		super(OrgContactRole, self).save(*args, **kwargs)

'''
Relationship types
'''

class P2P_Type(models.Model):
	slug = models.SlugField(unique=True,editable=False)
	relationship_type = models.CharField(max_length=250)
	objects = GetOrNoneManager()

	def __unicode__(self):
		return self.relationship_type

	def save(self, *args, **kwargs):
		unique_slugify(self,self.relationship_type)
		super(P2P_Type, self).save(*args, **kwargs)

class Org2Org_Type(models.Model):
	slug = models.SlugField(unique=True,editable=False)
	relationship_type = models.CharField(max_length=250)
	objects = GetOrNoneManager()

	def __unicode__(self):
		return self.relationship_type

	def save(self, *args, **kwargs):
		unique_slugify(self,self.relationship_type)
		super(Org2Org_Type, self).save(*args, **kwargs)

class P2Org_Type(models.Model):
	slug = models.SlugField(unique=True,editable=False)
	relationship_type = models.CharField(max_length=250)
	objects = GetOrNoneManager()

	def __unicode__(self):
		return self.relationship_type

	def save(self, *args, **kwargs):
		unique_slugify(self,self.relationship_type)
		super(P2Org_Type, self).save(*args, **kwargs)
'''
2.0 feature??? 
'''
class Tag(models.Model):
	slug = models.SlugField(unique=True,editable=False)
	tag_name = models.CharField(max_length=250)
	objects = GetOrNoneManager()

	def __unicode__(self):
		return tag_name

	def save(self, *args, **kwargs):
		unique_slugify(self,self.tag_name)
		super(Tag, self).save(*args, **kwargs)

###################
## Contact Forms ##
###################
contact_types = (('email','email'),('phone','phone'),('link','link'),('address','address'))
class Contact(models.Model):
	'''
	A contact record for persons or orgs.
	'''
	person = models.ForeignKey('Person',blank=True,null=True,editable=False,related_name='person_contact')
	org = models.ForeignKey('Org',blank=True,null=True,editable=False,related_name='org_contact')
	
	type = models.CharField(max_length=100,choices=contact_types)
	contact = models.CharField(max_length=250,blank=True,null=True)
	role = models.ForeignKey('OrgContactRole',blank=True,null=True)
	notes = models.TextField(blank=True,null=True)
	
	def clean(self):
		if not self.person and not self.org:
			raise ValidationError(_('Contact information must be associated with either a person or an organization.'),code='no_ent')
		if self.person and self.org:
			raise ValidationError(_('Contact information should be associated with only one person or organization.'),code='too_many_ents')
		if self.type=='email':
			validate_email(self.contact)
		elif self.type=='link':
			url=URLValidator()
			url(self.contact)
		elif self.type=='phone':
			#Add a validator here?
			pass
		else:
			pass

	def __unicode__(self):
		if self.person:
			return self.person.lastName + ", " + self.person.firstName+": "+self.type
		else:
			return self.org.orgName+": "+self.type

###################
## Entity Models ##
###################

gender_types=((1,'Female'),(2,'Male'),(3,'Other'))

class Person(models.Model):
	slug = models.SlugField(unique=True,editable=False)
	lastName = models.CharField(max_length=100)
	firstName = models.CharField(max_length=100)
	role = models.ForeignKey('PersonRole',blank=True,null=True,related_name='person_role')
	position = models.CharField(max_length=250,blank=True,null=True)
	department = models.CharField(max_length=250,blank=True,null=True)
	gender = models.IntegerField(blank=True,null=True,choices=gender_types)
	#Relationships
	p_relations = models.ManyToManyField('self',through='P2P',symmetrical=False,related_name='+',blank=True)
	org_relations = models.ManyToManyField('Org',through='P2Org',related_name='people',blank=True)

	notes = models.TextField(blank=True, null=True)

	last_edited_by = models.CharField(max_length=250,blank=True,null=True)

	#2.0 feature
	tags = models.ManyToManyField(Tag,blank=True)

	def __unicode__(self):
		return self.lastName+", "+self.firstName

	def save(self, *args, **kwargs):
		unique_slugify(self,self.firstName +"-"+ self.lastName)
		super(Person, self).save(*args, **kwargs)

class Org(models.Model):
	slug = models.SlugField(unique=True,editable=False)
	orgName = models.CharField(max_length=200)
	openRecordsLaw = models.ForeignKey('OpenRecordsLaw',blank=True,null=True)
	#Relationships
	org_relations = models.ManyToManyField('self',through='Org2Org',symmetrical=False,related_name='+',blank=True)
	p_relations = models.ManyToManyField('Person',through="Org2P",related_name='orgs',blank=True)
	
	notes = models.TextField(blank=True, null=True)

	last_edited_by = models.CharField(max_length=250,blank=True,null=True)

	#2.0 feature
	tags = models.ManyToManyField(Tag,blank=True)

	def __unicode__(self):
		return self.orgName

	def save(self, *args, **kwargs):
		unique_slugify(self,self.orgName)
		super(Org, self).save(*args, **kwargs)

###################
## Relationships ##
###################

class P2P(models.Model):
	from_ent = models.ForeignKey(Person, related_name='p_from_p')
	to_ent   = models.ForeignKey(Person,related_name='p_to_p')
	relation = models.ForeignKey('P2P_Type',blank=True, null=True,related_name='p2p_relation')
	from_date = models.DateField(blank=True, null=True)
	to_date = models.DateField(blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	objects = GetOrNoneManager()
	def clean(self):
		if P2P.objects.get_or_none(from_ent=self.from_ent,to_ent=self.to_ent):
			raise ValidationError(_('That relationship already exists.'),code='already_exists')
		super(P2P, self).clean()

	def __unicode__(self):
		return self.from_ent.lastName +" ... "+self.to_ent.lastName
	'''
	Override save and delete methods to maintain relationship symmetry. 
	'''
	def save(self, *args, **kwargs):
		super(P2P, self).save(*args, **kwargs)
		#Enforce Symmetry
		P2P.objects.get_or_create(
			from_ent=self.to_ent,
			to_ent=self.from_ent,
			relation=self.relation,
			from_date=self.from_date,
			to_date=self.to_date,
			description=self.description)

	def delete(self):
		relation = P2P.objects.get_or_none(
			from_ent=self.to_ent,
			to_ent=self.from_ent,
			relation=self.relation,
			from_date=self.from_date,
			to_date=self.to_date,
			description=self.description)
		super(P2P, self).delete()
		if relation:
			relation.delete()
		


'''
We make Org2Org relationships unique in that they can have hierarchy. 
Could technically apply to other relationship types, but philosophically
we mean this to convey some principle of ownership. As such doesn't 
really apply to Org2P and definitely not to P2P.
'''
def hierarchy_test(self):
	'''
	Simple 3-way test.
	'''
	if self.hierarchy == 'none':
		return 'none'
	else:
		if self.hierarchy == 'child':
			return 'parent'
		else:
			return 'child'
hierarchy_types = (('parent','parent'),('child','child'),('none','none'))

class Org2Org(models.Model):
	from_ent = models.ForeignKey(Org,related_name='org_from_org')
	to_ent   = models.ForeignKey(Org,related_name='org_to_org')
	relation = models.ForeignKey('Org2Org_Type',blank=True, null=True,related_name='org2org_relation')
	from_date = models.DateField(blank=True, null=True)
	to_date = models.DateField(blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	hierarchy = models.CharField(choices=hierarchy_types, default='none', max_length=10)
	objects = GetOrNoneManager()
	
	def __unicode__(self):
		return self.from_ent.orgName +" ... "+self.to_ent.orgName
	
	def clean(self):
		if Org2Org.objects.get_or_none(from_ent=self.from_ent,to_ent=self.to_ent):
			raise ValidationError(_('That relationship already exists.'),code='already_exists')
		super(Org2Org, self).clean()
	
	def save(self, *args, **kwargs):
		super(Org2Org, self).save(*args, **kwargs)
		'''
		Enforce Symmetry.
		An issue: If you change a feature of a relationship, e.g., hierarchy, you'll end up creating a new relationship, and the stale one will persist.
		'''
		relation, got = Org2Org.objects.get_or_create(
			from_ent=self.to_ent,
			to_ent=self.from_ent,
			relation=self.relation,
			from_date=self.from_date,
			to_date=self.to_date,
			description=self.description,
			hierarchy=hierarchy_test(self))
	
	def delete(self,*args,**kwargs):
		#Enforce Symmetry
		relation = Org2Org.objects.get_or_none(
			from_ent=self.to_ent,
			to_ent=self.from_ent,
			relation=self.relation,
			from_date=self.from_date,
			to_date=self.to_date,
			description=self.description )
		super(Org2Org, self).delete(*args, **kwargs)
		if relation:
			relation.delete()


class P2Org(models.Model):
	from_ent = models.ForeignKey(Person,related_name='org_from_p')
	to_ent   = models.ForeignKey(Org,related_name='p_to_org')
	relation = models.ForeignKey('P2Org_Type',blank=True, null=True,related_name='p2org_relation')
	from_date = models.DateField(blank=True,null=True)
	to_date = models.DateField(blank=True,null=True)
	description = models.TextField(blank=True,null=True)
	objects = GetOrNoneManager()

	def __unicode__(self):
		return self.from_ent.lastName +" ... "+self.to_ent.orgName

	def clean(self):
		if P2Org.objects.get_or_none(from_ent=self.from_ent,to_ent=self.to_ent):
			raise ValidationError(_('That relationship already exists.'),code='already_exists')
		super(P2Org, self).clean()
	
	def save(self, *args, **kwargs):
		super(P2Org, self).save(*args, **kwargs)
		#Enforce Symmetry
		Org2P.objects.get_or_create(
			from_ent=self.to_ent,
			to_ent=self.from_ent,
			relation=self.relation,
			from_date=self.from_date,
			to_date=self.to_date,
			description=self.description)
	
	def delete(self,*args,**kwargs):
		#Enforce Symmetry
		relation = Org2P.objects.get_or_none(
			from_ent=self.to_ent,
			to_ent=self.from_ent,
			relation=self.relation,
			from_date=self.from_date,
			to_date=self.to_date,
			description=self.description)
		super(P2Org, self).delete(*args, **kwargs)
		if relation:
			relation.delete()

class Org2P(models.Model):
	from_ent = models.ForeignKey(Org, related_name='p_from_org')
	to_ent   = models.ForeignKey(Person,related_name='org_to_p')
	relation = models.ForeignKey('P2Org_Type',blank=True, null=True,related_name='org2p_relation')
	from_date = models.DateField(blank=True,null=True)
	to_date = models.DateField(blank=True,null=True)
	description = models.TextField(blank=True,null=True)
	objects = GetOrNoneManager()

	def __unicode__(self):
		return self.from_ent.orgName +" ... "+self.to_ent.lastName

	def clean(self):
		if Org2P.objects.get_or_none(from_ent=self.from_ent,to_ent=self.to_ent):
			raise ValidationError(_('That relationship already exists.'),code='already_exists')
		super(Org2P, self).clean()

	def save(self, *args, **kwargs):
		super(Org2P, self).save(*args, **kwargs)
		#Enforce Symmetry
		P2Org.objects.get_or_create(
			from_ent=self.to_ent,
			to_ent=self.from_ent,
			relation=self.relation,
			from_date=self.from_date,
			to_date=self.to_date,
			description=self.description)

	def delete(self,*args,**kwargs):
		#Enforce Symmetry
		relation = P2Org.objects.get_or_none(
			from_ent=self.to_ent,
			to_ent=self.from_ent,
			relation=self.relation,
			from_date=self.from_date,
			to_date=self.to_date,
			description=self.description)
		super(Org2P, self).delete(*args, **kwargs)
		if relation:
			relation.delete()

##################
## Setter Funcs ##
##################

def add_p2p(self, person,symm=True,**kwargs):
    relationship = P2P.objects.get_or_create(
        from_ent=self,
        to_ent=person,
        **kwargs)
    return relationship
def remove_p2p(self, person, symm=True,**kwargs):
	relation = P2P.objects.get_or_none(
        from_ent=self, 
        to_ent=person,
        **kwargs)
	if relation:
		relation.delete()
def add_org2org(self,org,symm=True,**kwargs):
	relationship = Org2Org.objects.get_or_create(
		from_ent=self,
		to_ent=org,
		**kwargs)
	return relationship
def remove_org2org(self,org,symm=True,**kwargs):
	relation = Org2Org.objects.get_or_none(
        from_ent=self, 
        to_ent=org,
        **kwargs)
	if relation:
		relation.delete()
def add_p2org(self,org,symm=True,**kwargs):
	relationship = P2Org.objects.get_or_create(
		from_ent=self,
		to_ent=org,
		**kwargs)
	return relationship
def remove_p2org(self,org,symm=True,**kwargs):
	relation = P2Org.objects.get_or_none(
        from_ent=self, 
        to_ent=org,
        **kwargs)
	if relation:
		relation.delete()
def add_org2p(self,person,symm=True,**kwargs):
	relationship = Org2P.objects.get_or_create(
		from_ent=self,
		to_ent=person,
		**kwargs)
	return relationship
def remove_org2p(self,person,symm=True,**kwargs):
	relation = Org2P.objects.get_or_none(
        from_ent=self, 
        to_ent=person,
        **kwargs)
	if relation:
		relation.delete()


##################
## Getter Funcs ##
##################

def get_relations(self):
	people=self.p_relations.all()
	orgs = self.org_relations.all()
	return {'people':people,'orgs':orgs}

def get_employer(self):
	relates=self.org_from_p.filter(relation__relationship_type='employment')
	employers=[r.to_ent for r in relates]
	return employers

def get_employees(self):
	relates=self.p_to_org.filter(relation__relationship_type='employment')
	employees=[r.from_ent for r in relates]
	return employees

def get_employees_by_role(self,role):
	'''
	Thinking preferable to pass a string? Could also refactor for role object.
	'''
	relates=self.p_to_org.filter(relation__relationship_type='employment',from_ent__role__role=role)
	employees=[r.from_ent for r in relates]
	return employees

def get_relations_by_type(self,type):
	'''
	Preferable to pass a string? Could also refactor for relation object.
	'''
	if self._meta.model_name == 'org':
		kith=self.p_to_org.filter(relation__relationship_type=type)
		kin=self.org_to_org.filter(relation__relationship_type=type)
		return {'people':collate_relations(kith),'orgs':collate_relations(kin)}
	else: # =='person'
		kith=self.org_to_p.filter(relation__relationship_type=type)
		kin=self.p_to_p.filter(relation__relationship_type=type)
		return {'orgs':collate_relations(kith),'people':collate_relations(kin)}

def get_relations_with_type(self):
	if self._meta.model_name == 'org':
		kith=self.p_to_org.all().order_by('id')
		kin=self.org_to_org.all().order_by('id')
		return {'people':collate_relations(kith),'orgs':collate_relations(kin)}
	else: # =='person'
		kith=self.org_to_p.all().order_by('id')
		kin=self.p_to_p.all().order_by('id')
		return {'orgs':collate_relations(kith),'people':collate_relations(kin)}

'''
hierarchy getters for orgs
'''
def get_children(self):
	orgs = self.org_to_org.filter(hierarchy='child')
	return [org.from_ent for org in orgs]

def get_parents(self):
	orgs = self.org_to_org.filter(hierarchy='parent')
	return [org.from_ent for org in orgs]


###################
## Network Funcs ##
###################

def collate_relations(queryset):
	'''
	Presumes self == to_ent
	'''
	relation_list=[]
	for q in queryset:
		if q.relation:
			relation_list.append({'type':q.relation.relationship_type,'relation':q.from_ent})
		else:
			relation_list.append({'type':'','relation':q.from_ent})
	return relation_list

import networkx as nx
def nx_add(graph,node):
	people = node.p_relations.all()
	orgs = node.org_relations.all()
	ents = list(chain(people,orgs))
	graph.add_nodes_from(ents)
	graph.add_edges_from([(node,n) for n in ents])
	return graph

def relation_list(self):
	return list( chain( self.p_relations.all(),self.org_relations.all() ) )

def nx_graph(self,hops=2):
	G = nx.Graph()
	G = nx_add(G,self)
	relations = relation_list(self)
	for i in range(hops-1):
		intermediate = []
		for r in relations:
			G = nx_add(G,r)
			intermediate = list( chain( intermediate,relation_list(r) ) ) 
		relations = list( chain( relations,intermediate ) )
	return G


###############
## Add funcs ##
###############

Person.add_p2p = add_p2p
Person.remove_p2p = remove_p2p
Person.add_p2org = add_p2org
Person.remove_p2org = remove_p2org
Person.get_relations = get_relations
Person.get_employer = get_employer
Person.get_relations_with_type = get_relations_with_type
Person.get_relations_by_type = get_relations_by_type
Person.nx_graph = nx_graph

Org.add_org2org = add_org2org
Org.remove_org2org = remove_org2org
Org.add_org2p = add_org2p
Org.remove_org2p = remove_org2p
Org.get_relations = get_relations
Org.get_employees = get_employees
Org.get_employees_by_role = get_employees_by_role
Org.get_relations_with_type = get_relations_with_type
Org.get_relations_by_type = get_relations_by_type
Org.get_parents = get_parents
Org.get_children = get_children
Org.nx_graph = nx_graph