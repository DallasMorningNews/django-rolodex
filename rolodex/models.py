from django.db import models
from itertools import chain
from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils.translation import ugettext as _
from django.core.validators import URLValidator,validate_email

###################
## Choice Models ##
###################
## These are all registered in admin.

class openRecordsLaw(models.Model):
	'''
	Which open records law applies to the org.
	'''
	id = models.CharField(max_length=250,primary_key=True,editable=False)
	name = models.CharField(max_length=250)
	link = models.URLField(blank=True,null=True)
	def __unicode__(self):
		return self.name
	def save(self, *args, **kwargs):
		self.id = slugify(unicode(self.name))
		super(openRecordsLaw, self).save(*args, **kwargs)

class role(models.Model):
	'''
	Define some roles, preferably ones useful for filtering on, e.g. "Media Contact", "FOIA Officer".
	'''
	id = models.CharField(max_length=250,primary_key=True,editable=False)
	role = models.CharField(max_length=250)
	description = models.TextField(blank=True,null=True)
	def __unicode__(self):
		return self.role
	def save(self, *args, **kwargs):
		self.id = slugify(unicode(self.role))
		super(role, self).save(*args, **kwargs)

class org_contact_role(models.Model):
	'''
	Define roles for org contacts, e.g., FOIA email, etc.
	'''
	id = models.CharField(max_length=250,primary_key=True,editable=False)
	role = models.CharField(max_length=250)
	description = models.TextField(blank=True,null=True)
	def __unicode__(self):
		return self.role
	def save(self, *args, **kwargs):
		self.id = slugify(unicode(self.role))
		super(org_contact_role, self).save(*args, **kwargs)

class GetOrNoneManager(models.Manager):
    """Adds get_or_none method to objects
    """
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None

class p2p_type(models.Model):
	id = models.CharField(max_length=250,primary_key=True,editable=False)
	relationship_type = models.CharField(max_length=250)
	objects = GetOrNoneManager()
	def __unicode__(self):
		return self.relationship_type
	def save(self, *args, **kwargs):
		self.id = slugify(unicode(self.relationship_type))
		super(p2p_type, self).save(*args, **kwargs)

class org2org_type(models.Model):
	id = models.CharField(max_length=250,primary_key=True,editable=False)
	relationship_type = models.CharField(max_length=250)
	objects = GetOrNoneManager()
	def __unicode__(self):
		return self.relationship_type
	def save(self, *args, **kwargs):
		self.id = slugify(unicode(self.relationship_type))
		super(org2org_type, self).save(*args, **kwargs)

class p2org_type(models.Model):
	id = models.CharField(max_length=250,primary_key=True,editable=False)
	relationship_type = models.CharField(max_length=250)
	objects = GetOrNoneManager()
	def __unicode__(self):
		return self.relationship_type
	def save(self, *args, **kwargs):
		self.id = slugify(unicode(self.relationship_type))
		super(p2org_type, self).save(*args, **kwargs)

class Tag(models.Model):
	id = models.CharField(max_length=250,primary_key=True,editable=False)
	tag_name = models.CharField(max_length=250)
	objects = GetOrNoneManager()
	def __unicode__(self):
		return tag_name
	def save(self, *args, **kwargs):
		self.id = slugify(unicode(self.tag_name))
		super(Tag, self).save(*args, **kwargs)

###################
## Contact Forms ##
###################
contact_types = (('email','email'),('phone','phone'),('link','link'),('address','address'))
class contact(models.Model):
	'''
	A contact record for persons or orgs.
	'''
	person = models.ForeignKey('Person',blank=True,null=True,editable=False,related_name='person_contact')
	org = models.ForeignKey('Org',blank=True,null=True,editable=False,related_name='org_contact')
	
	type = models.CharField(max_length=100,choices=contact_types)
	contact = models.CharField(max_length=250,blank=True,null=True)
	role = models.ForeignKey('org_contact_role',blank=True,null=True)
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
			#Add a validator?
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
	lastName = models.CharField(max_length=100)
	firstName = models.CharField(max_length=100)
	role = models.ForeignKey('role',blank=True,null=True,related_name='person_role')
	position = models.CharField(max_length=250,blank=True,null=True)
	department = models.CharField(max_length=250,blank=True,null=True)
	gender = models.IntegerField(blank=True,null=True,choices=gender_types)
	#Relationships
	p_relations = models.ManyToManyField('self',through='P2P',symmetrical=False,related_name='+',blank=True)
	org_relations = models.ManyToManyField('Org',through='P2Org',related_name='people',blank=True)

	tags = models.ManyToManyField(Tag,blank=True)
	def __unicode__(self):
		return self.lastName+", "+self.firstName


class Org(models.Model):
	orgName = models.CharField(max_length=200)
	openRecordsLaw = models.ForeignKey('openRecordsLaw',blank=True,null=True)
	#Relationships
	org_relations = models.ManyToManyField('self',through='Org2Org',symmetrical=False,related_name='+',blank=True)
	p_relations = models.ManyToManyField('Person',through="Org2P",related_name='orgs',blank=True)
	
	tags = models.ManyToManyField(Tag,blank=True)
	def __unicode__(self):
		return self.orgName

###################
## Relationships ##
###################

class P2P(models.Model):
	from_ent = models.ForeignKey(Person, related_name='p_from_p')
	to_ent   = models.ForeignKey(Person,related_name='p_to_p')
	relation = models.ForeignKey('p2p_type',blank=True, null=True,related_name='p2p_relation')
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
	Same is enforced in the add_ and remove_(relationship) model methods. 
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
	def delete(self,*args,**kwargs):
		super(P2P, self).delete(*args, **kwargs)
		relation = P2P.objects.get_or_none(
			from_ent=self.to_ent,
			to_ent=self.from_ent,
			relation=self.relation,
			from_date=self.from_date,
			to_date=self.to_date,
			description=self.description)
		if relation:
			relation.delete();


class Org2Org(models.Model):
	from_ent = models.ForeignKey(Org,related_name='org_from_org')
	to_ent   = models.ForeignKey(Org,related_name='org_to_org')
	relation = models.ForeignKey('org2org_type',blank=True, null=True,related_name='org2org_relation')
	from_date = models.DateField(blank=True, null=True)
	to_date = models.DateField(blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	objects = GetOrNoneManager()
	def clean(self):
		if Org2Org.objects.get_or_none(from_ent=self.from_ent,to_ent=self.to_ent):
			raise ValidationError(_('That relationship already exists.'),code='already_exists')
		super(Org2Org, self).clean()
	def __unicode__(self):
		return self.from_ent.orgName +" ... "+self.to_ent.orgName
	def save(self, *args, **kwargs):
		super(Org2Org, self).save(*args, **kwargs)
		#Enforce Symmetry
		Org2Org.objects.get_or_create(
			from_ent=self.to_ent,
			to_ent=self.from_ent,
			relation=self.relation,
			from_date=self.from_date,
			to_date=self.to_date,
			description=self.description)
	def delete(self,*args,**kwargs):
		super(Org2Org, self).delete(*args, **kwargs)
		relation = Org2Org.objects.get_or_none(
			from_ent=self.to_ent,
			to_ent=self.from_ent,
			relation=self.relation,
			from_date=self.from_date,
			to_date=self.to_date,
			description=self.description)
		if relation:
			relation.delete()

class P2Org(models.Model):
	from_ent = models.ForeignKey(Person,related_name='org_from_p')
	to_ent   = models.ForeignKey(Org,related_name='p_to_org')
	relation = models.ForeignKey('p2org_type',blank=True, null=True,related_name='p2org_relation')
	from_date = models.DateField(blank=True,null=True)
	to_date = models.DateField(blank=True,null=True)
	description = models.TextField(blank=True,null=True)
	objects = GetOrNoneManager()
	def clean(self):
		if P2Org.objects.get_or_none(from_ent=self.from_ent,to_ent=self.to_ent):
			raise ValidationError(_('That relationship already exists.'),code='already_exists')
		super(P2Org, self).clean()
	def __unicode__(self):
		return self.from_ent.lastName +" ... "+self.to_ent.orgName
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
		super(P2Org, self).delete(*args, **kwargs)
		relation = Org2P.objects.get_or_none(
			from_ent=self.to_ent,
			to_ent=self.from_ent,
			relation=self.relation,
			from_date=self.from_date,
			to_date=self.to_date,
			description=self.description)
		if relation:
			relation.delete()

class Org2P(models.Model):
	from_ent = models.ForeignKey(Org, related_name='p_from_org')
	to_ent   = models.ForeignKey(Person,related_name='org_to_p')
	relation = models.ForeignKey('p2org_type',blank=True, null=True,related_name='org2p_relation')
	from_date = models.DateField(blank=True,null=True)
	to_date = models.DateField(blank=True,null=True)
	description = models.TextField(blank=True,null=True)
	objects = GetOrNoneManager()
	def clean(self):
		if Org2P.objects.get_or_none(from_ent=self.from_ent,to_ent=self.to_ent):
			raise ValidationError(_('That relationship already exists.'),code='already_exists')
		super(Org2P, self).clean()
	def __unicode__(self):
		return self.from_ent.orgName +" ... "+self.to_ent.lastName
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
		super(Org2P, self).delete(*args, **kwargs)
		relation = P2Org.objects.get_or_none(
			from_ent=self.to_ent,
			to_ent=self.from_ent,
			relation=self.relation,
			from_date=self.from_date,
			to_date=self.to_date,
			description=self.description)
		if relation:
			relation.delete()

##################
## Helper Funcs ##
##################

def add_p2p(self, person,symm=True,**kwargs):
    relationship = P2P.objects.get_or_create(
        from_ent=self,
        to_ent=person,
        **kwargs)
    if symm:
        person.add_p2p(self, symm=False, **kwargs)
    return relationship
def remove_p2p(self, person, symm=True,**kwargs):
    P2P.objects.filter(
        from_ent=self, 
        to_ent=person,
        **kwargs).delete()
    if symm:
        person.remove_p2p(self, symm=False,**kwargs)
def add_org2org(self,org,symm=True,**kwargs):
	relationship = Org2Org.objects.get_or_create(
		from_ent=self,
		to_ent=org,
		**kwargs)
	if symm:
		org.add_org2org(self,symm=False,**kwargs)
	return relationship
def remove_org2org(self,org,symm=True,**kwargs):
	Org2Org.objects.filter(
		from_ent=self,
		to_ent=org,
		**kwargs).delete()
	if symm:
		org.remove_org2org(self,symm=False,**kwargs)

def add_p2org(self,org,symm=True,**kwargs):
	relationship = P2Org.objects.get_or_create(
		from_ent=self,
		to_ent=org,
		**kwargs
		)
	if symm:
		org.add_org2p(self,symm=False,**kwargs)
	return relationship
def remove_p2org(self,org,symm=True,**kwargs):
	P2Org.objects.filter(
		from_ent=self,
		to_ent=org,
		**kwargs).delete()
	if symm:
		org.remove_org2p(self,symm=False,**kwargs)
def add_org2p(self,person,symm=True,**kwargs):
	relationship = Org2P.objects.get_or_create(
		from_ent=self,
		to_ent=person,
		**kwargs
		)
	if symm:
		person.add_p2org(self,symm=False,**kwargs)
	return relationship
def remove_org2p(self,person,symm=True,**kwargs):
	Org2P.objects.filter(
		from_ent=self,
		to_ent=person,
		**kwargs).delete()
	if symm:
		person.remove_p2org(self,symm=False,**kwargs)

#############
## Getters ##
#############
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
	Preferable to pass a string? Could also refactor for role object.
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
		kith=self.p_to_org.all().order_by('pk')
		kin=self.org_to_org.all().order_by('pk')
		return {'people':collate_relations(kith),'orgs':collate_relations(kin)}
	else: # =='person'
		kith=self.org_to_p.all().order_by('pk')
		kin=self.p_to_p.all().order_by('pk')
		return {'orgs':collate_relations(kith),'people':collate_relations(kin)}

##############

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

Org.add_org2org = add_org2org
Org.remove_org2org = remove_org2org
Org.add_org2p = add_org2p
Org.remove_org2p = remove_org2p
Org.get_relations = get_relations
Org.get_employees = get_employees
Org.get_employees_by_role = get_employees_by_role
Org.get_relations_with_type = get_relations_with_type
Org.get_relations_by_type = get_relations_by_type

