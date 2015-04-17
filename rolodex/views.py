from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render, render_to_response, HttpResponseRedirect,get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
from rolodex.models import Tag,Org,Person,P2P,Org2Org,P2Org,Org2P,P2Org_Type,P2P_Type,Org2Org_Type
from rolodex.forms import OrgForm,OrgFormSet,PersonForm,PersonFormSet,P2PForm,Org2OrgForm,P2OrgForm,Org2PForm
from datetime import datetime as dt
from operator import attrgetter
from django.db.models import Q
from itertools import chain
import json
from django.conf import settings
import networkx as nx
import pdb

'''
Employment is the only required fixture.
'''
#using first right now to get around a testing bug where there seems to be a conflict on get between fixtures
EMPLOYMENT = P2Org_Type.objects.filter(relationship_type='employment').first()


def secure(view):
	'''
	Simple decorator that checks SETTINGS.
	'''
	if settings.ROLODEX_SECURE:
		return login_required(view)
	else:
		return view


@secure
def home(request): 
	orgs = Org.objects.all()
	peeps = Person.objects.all()
	peeps = org_relate_peep(peeps)
	return render_to_response('rolodex/home.html',{'orgs':orgs,'peeps':peeps},context_instance=RequestContext(request))


############################################################################
#### ORG Views ####
###################

@secure
def new_org(request): 
	form=OrgForm(instance=Org())
	formset=OrgFormSet(instance=Org())
	if request.method == "POST":
		form = OrgForm(request.POST)
		if form.is_valid():
			org = form.save()
			org.last_edited_by = user_check(request.user)
			org.save()
			formset = OrgFormSet(request.POST,instance=org)
			if formset.is_valid():
				formset.save()
				return redirect('rolodex_org',org.slug)
			else:
				org.delete()
				form = OrgForm(request.POST)
				
	return render_to_response('rolodex/new_org.html',{'form':form,'formset':formset,},context_instance=RequestContext(request))

@secure
def edit_org(request,org_slug):
	orgNODE = Org.objects.get(slug=org_slug)
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
				orgNODE.last_edited_by = user_check(request.user)
				orgNODE.save()
				return redirect('rolodex_org',org.slug)

	return render_to_response('rolodex/new_org.html',{'form':form,'formset':formset,'orgNode':orgNODE,'edit':True},context_instance=RequestContext(request))

@permission_required('rolodex.delete_org')
def delete_org(request,org_slug):
	org = Org.objects.get(slug=org_slug)
	if request.method=="POST":
		org.delete()
		return redirect('rolodex_home')
	return render_to_response('rolodex/delete.html',{'org':org},context_instance=RequestContext(request))

@secure
def search_org(request,org_slug):
	node = Org.objects.get(slug=org_slug)
	node.employees = node.get_employees()
	node.contacts = node.org_contact.all()
	node.relations = node.get_relations_with_type()
	node.net_length = len(net_compiler(Org.objects.filter(slug=org_slug),3))
	return render_to_response('rolodex/org.html',{'node':node,},context_instance=RequestContext(request))

@secure
def org_map(request,org_slug):
	node = Org.objects.get(slug=org_slug)
	hops = int(request.GET.get('hops',3))
	return render_to_response('rolodex/orgMap.html',{'node':node,'hops':hops},context_instance=RequestContext(request))

@secure
def org_network(request,org_slug):
	network = net_compiler(Org.objects.filter(slug=org_slug),3)
	data = json.dumps(network)
	return HttpResponse(data, content_type='application/json')

@secure
def adv_org_network(request,org_slug):
	hops = int(request.GET.get('hops',3))
	network = net_compiler(Org.objects.filter(slug=org_slug),hops)
	org = Org.objects.get(slug=org_slug)
	centrality_data = adv_compile(org,hops)
	data = json.dumps({'centrality':centrality_data, 'links':network})
	return HttpResponse(data, content_type='application/json')

@secure
def new_org_relation(request,org_slug):
	saved=False
	org2orgForm = Org2OrgForm()
	org2pForm = Org2PForm()
	if request.method == "POST":
		if request.POST['formType']=='2P':
			org2pForm = Org2PForm(request.POST)
			if org2pForm.is_valid():
				fromEnt = Org.objects.get(pk=request.POST['from_ent'])
				toEnt   = Person.objects.get(pk=request.POST['to_ent'])
				relation= P2Org_Type.objects.get_or_none(relationship_type=request.POST['relation'],)
				fromEnt.add_org2p(toEnt,**{'relation':relation})
				saved=True
		else:	
			org2orgForm = Org2OrgForm(request.POST)
			if org2orgForm.is_valid():
				fromEnt = Org.objects.get(pk=request.POST['from_ent'])
				toEnt   = Org.objects.get(pk=request.POST['to_ent'])
				hierarchy = request.POST['hierarchy']
				relation= Org2Org_Type.objects.get_or_none(relationship_type=request.POST['relation'])
				fromEnt.add_org2org(toEnt,**{'relation':relation,'hierarchy':hierarchy})
				saved=True

	orgs = Org.objects.filter(~Q(slug=org_slug))
	peeps = Person.objects.all()
	peeps = org_relate_peep(peeps)
	orgNode = Org.objects.get(slug=org_slug)
	return render_to_response('rolodex/new_relation.html',{'orgNode':orgNode ,'pForm':org2pForm,'orgForm':org2orgForm,'saved':saved,'peeps':peeps,'orgs':orgs},context_instance=RequestContext(request))


############################################################################
#### PERSON Views ####
######################

@secure
def new_person(request, org_slug=None): 
	form=PersonForm()
	formset=PersonFormSet(instance=Person())
	success = False
	if request.method == "POST":
		form = PersonForm(request.POST) 
		if form.is_valid():
			person = form.save()
			person.last_edited_by = user_check(request.user)
			formset = PersonFormSet(request.POST,instance=person)
			if formset.is_valid():
				formset.save()

				#Add employment relationship
				orgNODE = Org.objects.get(slug=org_slug)
				person.add_p2org(orgNODE,**{'relation':EMPLOYMENT})
				person.save()
			
				form=PersonForm()
				formset=PersonFormSet(instance=Person())
				success = True
			else:
				person.delete()
				form = PersonForm(request.POST)
	
	primary = Org.objects.get(slug=org_slug)
	orgs = Org.objects.all()
	tags = Tag.objects.all()
	return render_to_response('rolodex/new_person.html',{'form':form,'formset':formset,'orgNode':org_slug,'orgs':orgs,'tags':tags,'primary':primary,'success':success},context_instance=RequestContext(request))

@secure
def new_person_no_org(request, org_slug=None): 
	form=PersonForm()
	formset=PersonFormSet(instance=Person())
	success = False
	if request.method == "POST":
		form = PersonForm(request.POST)
		if form.is_valid():
			person = form.save()
			person.last_edited_by = user_check(request.user)
			formset = PersonFormSet(request.POST,instance=person)
			if formset.is_valid():
				formset.save()

				person.save()

				form=PersonForm()
				formset=PersonFormSet(instance=Person())
				success = True
			else:
				person.delete()
				form = PersonForm(request.POST)
	
	orgs = Org.objects.all()
	tags = Tag.objects.all()
	return render_to_response('rolodex/new_person.html',{'form':form,'formset':formset,'orgNode':org_slug,'orgs':orgs,'tags':tags,'primary':None,'success':success},context_instance=RequestContext(request))


@secure
def edit_person(request, person_slug):
	peep = Person.objects.get(slug=person_slug)
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
				person.last_edited_by = user_check(request.user)
				person.save()
				return redirect('rolodex_person',person.slug)
	
	employer = peep.org_from_p.filter(relation=EMPLOYMENT)
	if len(employer)>0:
		primary = employer[0].to_ent
	else:
		primary = "N/A"	
	orgs = Org.objects.all()
	tags = Tag.objects.all()
	return render_to_response('rolodex/new_person.html',{'form':form,'formset':formset,'personNode':peep,'orgs':orgs,'tags':tags,'primary':primary,'edit':True},context_instance=RequestContext(request))

@permission_required('rolodex.delete_person')
def delete_person(request,person_slug):
	peep = Person.objects.get(slug=person_slug)
	if request.method=="POST":
		peep.delete()
		return redirect('rolodex_home')
	return render_to_response('rolodex/delete.html',{'peep':peep},context_instance=RequestContext(request))

@secure
def search_person(request,person_slug):
	node = Person.objects.get(slug=person_slug)
	employer = node.org_from_p.filter(relation=EMPLOYMENT)
	if len(employer)>0:
		node.primary = employer[0].to_ent.orgName
	else:
		node.primary = "N/A"
	node.contacts = node.person_contact.all()
	node.relations = node.get_relations_with_type()
	node.net_length = len(net_compiler(Person.objects.filter(slug=person_slug),3))
	return render_to_response('rolodex/person.html',{'node':node,},context_instance=RequestContext(request))

@secure
def person_map(request,person_slug):
	node = Person.objects.get(slug=person_slug)
	hops = int(request.GET.get('hops',3))
	return render_to_response('rolodex/personMap.html',{'node':node,'hops':hops},context_instance=RequestContext(request))

@secure
def person_network(request,person_slug):
	network = net_compiler(Person.objects.filter(slug=person_slug),3)
	data = json.dumps(network)
	return HttpResponse(data, content_type='application/json')

@secure
def adv_person_network(request,person_slug):
	hops = int(request.GET.get('hops',3))
	network = net_compiler(Person.objects.filter(slug=person_slug),hops)
	peep = Person.objects.get(slug=person_slug)
	centrality_data = adv_compile(peep,hops)
	data = json.dumps({'centrality':centrality_data, 'links':network})
	return HttpResponse(data, content_type='application/json')

@secure
def new_person_relation(request,person_slug):
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
				fromEnt = Person.objects.get(pk=request.POST['from_ent'])
				toEnt   = Person.objects.get(pk=request.POST['to_ent'])
				relation= P2P_Type.objects.get_or_none(relationship_type=request.POST['relation'])
				fromEnt.add_p2p(toEnt,**{'relation':relation})
				saved=True
		else:	
			p2orgForm = P2OrgForm(request.POST)
			if p2orgForm.is_valid():
				fromEnt = Person.objects.get(pk=request.POST['from_ent'])
				toEnt   = Org.objects.get(pk=request.POST['to_ent'])
				relation= P2Org_Type.objects.get_or_none(relationship_type=request.POST['relation'])
				fromEnt.add_p2org(toEnt,**{'relation':relation})
				saved=True

	orgs = Org.objects.all()
	peeps = Person.objects.filter(~Q(slug=person_slug))
	peeps = org_relate_peep(peeps)
	peepNode = Person.objects.get(slug=person_slug)
	return render_to_response('rolodex/new_relation.html',{'peepNode':peepNode,'pForm':p2pForm,'orgForm':p2orgForm,'saved':saved,'peeps':peeps,'orgs':orgs},context_instance=RequestContext(request))



@secure
def delete_relationship(request):
	'''
	Delete relationships via AJAX on entity pages.
	'''
	if request.POST:
		if request.POST['from_type']=='p':
			if request.POST['to_type'] == 'p':
				from_ent = Person.objects.get(pk=request.POST['from_ent'])
				to_ent = Person.objects.get(pk=request.POST['to_ent'])
				from_ent.remove_p2p(to_ent)
			else:
				from_ent = Person.objects.get(pk=request.POST['from_ent'])
				to_ent = Org.objects.get(pk=request.POST['to_ent'])
				from_ent.remove_p2org(to_ent)
		else:
			if request.POST['to_type'] == 'p':
				from_ent = Org.objects.get(pk=request.POST['from_ent'])
				to_ent = Person.objects.get(pk=request.POST['to_ent'])
				from_ent.remove_org2p(to_ent)
			else:
				from_ent = Org.objects.get(pk=request.POST['from_ent'])
				to_ent = Org.objects.get(pk=request.POST['to_ent'])
				from_ent.remove_org2org(to_ent)
	return HttpResponse("Done.")



#################################################################
##### GRAPH HELPER FUNCTIONS ######
###################################

def org_relate_peep(peeps):
	'''
	Helper to serialize data for search boxes.
	'''
	for peep in peeps:
		employers = peep.org_relations.filter(p_to_org__relation=EMPLOYMENT)
		if len(employers) > 0:
			peep.orgName=employers[0].orgName
			peep.orgID = employers[0].pk
		else:
			'''
			If person has no primary org relationship, or if it has been deleted, we list
			them with N/A for the purposes of the search boxes on home and relation page.
			'''
			peep.orgName="N/A"
			peep.orgID = "N/A"
	return peeps

def hierarchy(snode,tnode):
	if snode.type == 'org' and tnode.type == 'org':
		snode.hierarchy = Org2Org.objects.get(from_ent=snode.pk,to_ent=tnode.pk).hierarchy
		tnode.hierarchy = Org2Org.objects.get(from_ent=tnode.pk,to_ent=snode.pk).hierarchy
	else:
		snode.hierarchy = 'none'
		tnode.hierarchy = 'none'
	return (snode, tnode)

def get_info(n):
	class output:
		pass
	node = output()
	if n.__class__.__name__ == 'Person':
		node.name = n.firstName +" "+n.lastName
		node.type = "person"
		node.id="p"+str(n.slug)
	else:
		node.name = n.orgName
		node.type = "org"
		node.id="o"+str(n.slug)
	node.pk = n.pk
	return node

def get_relations(nodes):
	relations,node_list=[],[]
	for node in nodes: 
		snode=get_info(node)
		relations = node.get_relations()
		for r in list(chain(relations['orgs'],relations['people'])):
			tnode=get_info(r)
			snode, tnode = hierarchy(snode,tnode)
			node_list.append({ 
				"source":snode.id,
				"source_name":str(snode.name), 
				"source_type":str(snode.type),
				"source_hierarchy":str(snode.hierarchy),
				"target":tnode.id,
				"target_name":str(tnode.name),
				"target_type":str(tnode.type),
				"target_hierarchy":str(tnode.hierarchy),
				})
		relations = list(chain(relations['orgs'],relations['people']))
	relations=list(set(relations))
	return {'node_list':node_list,'relations':relations}

def net_compiler(nodes,hops=2):
	node_list=[]
	for i in range(hops):
		result = get_relations(nodes)
		nodes=result['relations']
		node_list+=result['node_list']
	#de-dup
	node_list=[dict(t) for t in set([tuple(d.items()) for d in node_list])]
	return node_list

def adv_compile(node, hops):
	'''
	Compile some basic network centrality statistics for graph.
	'''
	G = node.nx_graph(hops)
	degree = nx.degree_centrality(G)
	betweenness = nx.betweenness_centrality(G)
	closeness= nx.closeness_centrality(G) 
	data={}
	for node in degree:
		n = get_info(node)
		data[n.id] = {'degree':degree[node],
						'betweenness':betweenness[node],
						'closeness':closeness[node]}
	return data

def user_check(user):
	if user.is_authenticated():
		return user.get_username()
	else:
		return "AnonymousUser"