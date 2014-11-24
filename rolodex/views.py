from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render, render_to_response, HttpResponseRedirect,get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
from rolodex.models import Tag, Org, Person, P2P,Org2Org,P2Org,Org2P,p2org_type,p2p_type,org2org_type
from rolodex.forms import OrgForm,OrgFormSet,PersonForm,PersonFormSet,P2PForm,Org2OrgForm,P2OrgForm,Org2PForm
from datetime import datetime as dt
from operator import attrgetter
from django.db.models import Q
from itertools import chain
import json
from django.conf import settings


EMPLOYMENT = p2org_type.objects.get(relationship_type='employment')


def secure(view):
	if settings.ROLODEX_SECURE:
		return login_required(view)
	else:
		return view

def orgRelatePeep(peeps):
	for peep in peeps:
		peep.orgName=peep.org_relations.filter(p_to_org__relation=EMPLOYMENT)[0].orgName
	return peeps

@secure
def home(request): 
	orgs = Org.objects.all()
	peeps = Person.objects.all()
	peeps = orgRelatePeep(peeps)
	return render_to_response('rolodex/home.html',{'orgs':orgs,'peeps':peeps},context_instance=RequestContext(request))

@secure
def new_org(request): 
	form=OrgForm(instance=Org())
	formset=OrgFormSet(instance=Org())
	if request.method == "POST":
		form = OrgForm(request.POST)
		if form.is_valid():
			org = form.save(commit=False)
			'''
			Because form requires pk, we fake it,
			check all other validation and then reset 
			the instance for the formset. It's a hack...
			'''
			org.pk = 1 
			formset = OrgFormSet(request.POST,instance=org)
			if formset.is_valid():
				org.pk=None
				org = form.save(commit=True)
				formset = OrgFormSet(request.POST,instance=org)
				formset.is_valid()
				formset.save()
				return redirect('rolodex_org',org.pk)

	return render_to_response('rolodex/new_org.html',{'form':form,'formset':formset,},context_instance=RequestContext(request))

@secure
def edit_org(request,orgNode):
	orgNODE = Org.objects.get(pk=orgNode)
	form=OrgForm(instance=orgNODE)
	formset=OrgFormSet(instance=orgNODE)
	formset.extra=0
	if request.method == "POST":
		form = OrgForm(request.POST,instance=orgNODE) 
		if form.is_valid():
			org = form.save()
			formset = OrgFormSet(request.POST,instance=org)
			if formset.is_valid():
				formset.save()
				return redirect('rolodex_org',orgNode)

	return render_to_response('rolodex/new_org.html',{'form':form,'formset':formset,'orgNode':orgNODE,'edit':True},context_instance=RequestContext(request))

@permission_required('rolodex.delete_org')
def delete_org(request,orgNode):
	org = Org.objects.get(pk=orgNode)
	if request.method=="POST":
		org.delete()
		return redirect('rolodex_home')
	return render_to_response('rolodex/delete.html',{'org':org},context_instance=RequestContext(request))



@secure
def new_person(request, orgNode): 
	form=PersonForm()
	formset=PersonFormSet(instance=Person())
	success = False
	if request.method == "POST":
		form = PersonForm(request.POST) 
		if form.is_valid():
			person = form.save(commit=False)
			'''
			Because form requires pk, we fake it,
			check all other validation and then reset 
			the instance for the formset. It's a hack...
			'''
			person.pk=1
			formset = PersonFormSet(request.POST,instance=person)
			if formset.is_valid():
				person.pk=None
				person = form.save(commit=True)
				formset = PersonFormSet(request.POST,instance=person)
				formset.is_valid()
				formset.save()

				#Add employment relationship
				orgNODE = Org.objects.get(id=orgNode)
				person.add_p2org(orgNODE,**{'relation':EMPLOYMENT})
				person.save()
			
				form=PersonForm()
				formset=PersonFormSet(instance=Person())
				success = True

	primary = Org.objects.get(id=orgNode)
	orgs = Org.objects.all()
	tags = Tag.objects.all()
	return render_to_response('rolodex/new_person.html',{'form':form,'formset':formset,'orgNode':orgNode,'orgs':orgs,'tags':tags,'primary':primary,'success':success},context_instance=RequestContext(request))

@secure
def edit_person(request, personNode):
	peep = Person.objects.get(pk=personNode)
	form=PersonForm(instance=peep)
	formset=PersonFormSet(instance=peep)
	formset.extra=0
	if request.method == "POST":
		form = PersonForm(request.POST,instance=peep) 
		
		if form.is_valid():
			person = form.save()
			formset = PersonFormSet(request.POST, instance=person)
			if formset.is_valid():
				formset.save()
				return redirect('rolodex_person',personNode)
		
	primary = peep.get_employer()[0]
	orgs = Org.objects.all()
	tags = Tag.objects.all()
	return render_to_response('rolodex/new_person.html',{'form':form,'formset':formset,'personNode':peep,'orgs':orgs,'tags':tags,'primary':primary,'edit':True},context_instance=RequestContext(request))

@permission_required('rolodex.delete_person')
def delete_person(request,personNode):
	peep = Person.objects.get(pk=personNode)
	if request.method=="POST":
		peep.delete()
		return redirect('rolodex_home')
	return render_to_response('rolodex/delete.html',{'peep':peep},context_instance=RequestContext(request))


@secure
def search_org(request,pNode):
	nodes = Org.objects.filter(id=pNode)
	peeps = Person.objects.filter(id=pNode)
	peeps = orgRelatePeep(peeps)
	node = nodes[0]
	node.employees = node.get_employees()
	node.contacts = node.org_contact.all()
	node.relations = node.get_relations_with_type()
	return render_to_response('rolodex/org.html',{'node':node,},context_instance=RequestContext(request))

@secure
def search_person(request,pNode):
	nodes = Person.objects.filter(id=pNode)
	node = nodes[0]
	node.primary = node.org_from_p.filter(relation=EMPLOYMENT)[0].to_ent.orgName
	node.contacts = node.person_contact.all()
	node.relations = node.get_relations_with_type()
	return render_to_response('rolodex/person.html',{'node':node,},context_instance=RequestContext(request))

@secure
def person_network(request,pNode):
	network = net_compiler(Person.objects.filter(id=pNode),3)
	data = json.dumps(network)
	return HttpResponse(data, content_type='application/json')
@secure
def org_network(request,oNode):
	network = net_compiler(Org.objects.filter(id=oNode),3)
	data = json.dumps(network)
	return HttpResponse(data, content_type='application/json')

@secure
def new_person_relation(request,Node):
	saved=False
	p2orgForm = P2OrgForm()
	p2pForm = P2PForm()
	if request.method == "POST":
		if request.POST['formType']=='2P':
			p2pForm = P2PForm(request.POST)
			if p2pForm.is_valid():
				'''
				We create the relationship via model method rather than the form
				in order to force the symetrical relationship created (so the 
				get_relations method works).
				'''
				#Create relationship via method rather than form to force symmetry
				fromEnt = Person.objects.get(pk=request.POST['from_ent'])
				toEnt   = Person.objects.get(pk=request.POST['to_ent'])
				relation= p2p_type.objects.get_or_none(relationship_type=request.POST['relation'])
				fromEnt.add_p2p(toEnt,**{'relation':relation})
				saved=True
		else:	
			p2orgForm = P2OrgForm(request.POST)
			if p2orgForm.is_valid():
				fromEnt = Person.objects.get(pk=request.POST['from_ent'])
				toEnt   = Org.objects.get(pk=request.POST['to_ent'])
				relation= p2org_type.objects.get_or_none(relationship_type=request.POST['relation'])
				fromEnt.add_p2org(toEnt,**{'relation':relation})
				saved=True

	
	orgs = Org.objects.all()
	peeps = Person.objects.filter(~Q(pk=Node))
	peeps = orgRelatePeep(peeps)
	peepNode = Person.objects.get(pk=Node)
	return render_to_response('rolodex/new_relation.html',{'peepNode':peepNode,'pForm':p2pForm,'orgForm':p2orgForm,'saved':saved,'peeps':peeps,'orgs':orgs},context_instance=RequestContext(request))

@secure
def new_org_relation(request,Node):
	saved=False
	org2orgForm = Org2OrgForm()
	org2pForm = Org2PForm()
	if request.method == "POST":
		if request.POST['formType']=='2P':
			org2pForm = Org2PForm(request.POST)
			if org2pForm.is_valid():
				fromEnt = Org.objects.get(pk=request.POST['from_ent'])
				toEnt   = Person.objects.get(pk=request.POST['to_ent'])
				relation= p2org_type.objects.get_or_none(relationship_type=request.POST['relation'])
				fromEnt.add_org2p(toEnt,**{'relation':relation})
				saved=True
		else:	
			org2orgForm = Org2OrgForm(request.POST)
			if org2orgForm.is_valid():
				fromEnt = Org.objects.get(pk=request.POST['from_ent'])
				toEnt   = Org.objects.get_or_none(pk=request.POST['to_ent'])
				relation= org2org_type.objects.get_or_none(relationship_type=request.POST['relation'])
				fromEnt.add_org2org(toEnt,**{'relation':relation})
				saved=True

	
	orgs = Org.objects.filter(~Q(pk=Node))
	peeps = Person.objects.all()
	peeps = orgRelatePeep(peeps)
	orgNode = Org.objects.get(pk=Node)
	return render_to_response('rolodex/new_relation.html',{'orgNode':orgNode ,'pForm':org2pForm,'orgForm':org2orgForm,'saved':saved,'peeps':peeps,'orgs':orgs},context_instance=RequestContext(request))


###################
## Network Funcs ##
###################
def getInfo(n):
	class output:
		pass
	node = output()
	if n.__class__.__name__ == 'Person':
		node.name = n.firstName +" "+n.lastName
		node.type = "person"
		node.id="p"+str(n.id)
	else:
		node.name = n.orgName
		node.type = "org"
		node.id="o"+str(n.id)
	return node
def getRelations(nodes):
	relations,node_list=[],[]
	for node in nodes: 
		snode=getInfo(node)
		relations = node.get_relations()
		for r in list(chain(relations['orgs'],relations['people'])):
			tnode=getInfo(r)
			node_list.append({ 
				"source":snode.id,
				"source_name":str(snode.name), 
				"source_type":str(snode.type),
				"target":tnode.id,
				"target_name":str(tnode.name),
				"target_type":str(tnode.type)
				})
		relations = list(chain(relations['orgs'],relations['people']))
	relations=list(set(relations))
	return {'node_list':node_list,'relations':relations}
def net_compiler(nodes,hops=2):
	node_list=[]
	for i in range(hops):
		result = getRelations(nodes)
		nodes=result['relations']
		node_list+=result['node_list']
	#de-dup
	node_list=[dict(t) for t in set([tuple(d.items()) for d in node_list])]
	return node_list