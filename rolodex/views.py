from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.db import connection
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from rolodex.models import Org, Person, Org2Org, P2Org_Type, P2P_Type, Org2Org_Type, SearchLog, Document
from rolodex.forms import OrgForm, OrgFormSet, PersonForm, PersonFormSet, P2PForm, Org2OrgForm, P2OrgForm, Org2PForm, DocumentForm
from datetime import date, timedelta
from itertools import chain
import json
from taggit.models import Tag
import networkx as nx

'''
Employment is the only required fixture.
'''

if 'rolodex_p2org' in connection.introspection.table_names():
	# using first right now to get around a testing bug where there seems to be a conflict on get between fixtures
	EMPLOYMENT = P2Org_Type.objects.filter(relationship_type='employment').first()
else:
	EMPLOYMENT = None


# timedelta for search activity calendar
minus_time = timedelta(days=-365 / 2)


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
	return render_to_response('rolodex/home.html', {}, context_instance=RequestContext(request))


############################################################################
# ORG Views #
#############

@secure
def new_org(request):
	form = OrgForm(instance=Org())
	formset = OrgFormSet(instance=Org())
	if request.method == "POST":
		form = OrgForm(request.POST)
		if form.is_valid():
			org = form.save()
			org.last_edited_by = user_check(request.user)
			org.save()
			formset = OrgFormSet(request.POST, instance=org)
			if formset.is_valid():
				formset.save()
				return redirect('rolodex_org', org.slug)
			else:
				org.delete()
				form = OrgForm(request.POST)
	return render_to_response('rolodex/new_org.html', {'form': form, 'formset': formset, }, context_instance=RequestContext(request))


@secure
def edit_org(request, org_slug):
	org_node = Org.objects.get(slug=org_slug)
	form = OrgForm(instance=org_node)
	formset = OrgFormSet(instance=org_node)
	formset.extra = 0
	if request.method == "POST":
		form = OrgForm(request.POST, instance=org_node)
		if form.is_valid():
			org = form.save()
			formset = OrgFormSet(request.POST, instance=org)
			if formset.is_valid():
				formset.save()
				org_node.last_edited_by = user_check(request.user)
				org_node.save()
				return redirect('rolodex_org', org.slug)

	return render_to_response('rolodex/new_org.html', {'form': form, 'formset': formset, 'orgNode': org_node, 'edit': True}, context_instance=RequestContext(request))


@permission_required('rolodex.delete_org')
def delete_org(request, org_slug):
	org = Org.objects.get(slug=org_slug)
	if request.method == "POST":
		org.delete()
		return redirect('rolodex_home')
	return render_to_response('rolodex/delete.html', {'org': org}, context_instance=RequestContext(request))


@secure
def search_org(request, org_slug):
	node = Org.objects.get(slug=org_slug)
	node.employees = node.get_employees()
	node.contacts = node.org_contact.all()
	node.relations = node.get_relations_with_type()
	node.net_length = len(net_compiler(Org.objects.filter(slug=org_slug), 3))
	# log the search
	logger(user=request.user, org=node)
	searches = SearchLog.objects.filter(org=node, datestamp__gt=date.today() - timedelta(days=365)).order_by('-datestamp')
	node.searches = [{'date': s.datestamp.strftime("%Y-%m-%d"), 'user': s.user} for s in searches]
	node.calendar = json.dumps(node.searches)
	node.documents = Document.objects.filter(org=node)
	node.tags = node.tags.all()
	tags = Tag.objects.all()
	return render_to_response('rolodex/org.html', {'node': node, 'tags': tags, }, context_instance=RequestContext(request))


@secure
def org_map(request, org_slug):
	node = Org.objects.get(slug=org_slug)
	hops = int(request.GET.get('hops', 3))
	return render_to_response('rolodex/orgMap.html', {'node': node, 'hops': hops}, context_instance=RequestContext(request))


@secure
def org_network(request, org_slug):
	network = net_compiler(Org.objects.filter(slug=org_slug), 3)
	data = json.dumps(network)
	return HttpResponse(data, content_type='application/json')


@secure
def adv_org_network(request, org_slug):
	hops = int(request.GET.get('hops', 3))
	network = net_compiler(Org.objects.filter(slug=org_slug), hops)
	org = Org.objects.get(slug=org_slug)
	centrality_data = adv_compile(org, hops)
	data = json.dumps({'centrality': centrality_data, 'links': network})
	return HttpResponse(data, content_type='application/json')


@secure
def new_org_relation(request, org_slug):
	saved = False
	org2org_form = Org2OrgForm()
	org2p_form = Org2PForm()
	if request.method == "POST":
		if request.POST['formType'] == '2P':
			org2p_form = Org2PForm(request.POST)
			if org2p_form.is_valid():
				from_ent = Org.objects.get(pk=request.POST['from_ent'])
				to_ent = Person.objects.get(pk=request.POST['to_ent'])
				relation = P2Org_Type.objects.get_or_none(relationship_type=request.POST['relation'],)
				from_ent.add_org2p(to_ent, **{'relation': relation})
				saved = True
		else:
			org2org_form = Org2OrgForm(request.POST)
			if org2org_form.is_valid():
				from_ent = Org.objects.get(pk=request.POST['from_ent'])
				to_ent = Org.objects.get(pk=request.POST['to_ent'])
				hierarchy = request.POST['hierarchy']
				relation = Org2Org_Type.objects.get_or_none(relationship_type=request.POST['relation'])
				from_ent.add_org2org(to_ent, **{'relation': relation, 'hierarchy': hierarchy})
				saved = True
	org_node = Org.objects.get(slug=org_slug)
	return render_to_response('rolodex/new_relation.html', {'orgNode': org_node, 'pForm': org2p_form, 'orgForm': org2org_form, 'saved': saved}, context_instance=RequestContext(request))


@secure
def new_org_doc(request, org_slug=None):
	if request.method == "POST":
		doc_form = DocumentForm(request.POST, request.FILES)
		if doc_form.is_valid():
			doc_form.save()
			return redirect('rolodex_org', org_slug)
		else:
			node = Person.objects.get(pk=request.POST['org'])
	else:
		node = Org.objects.get(slug=org_slug)
		doc_form = DocumentForm(initial={'org': node})
	return render_to_response('rolodex/new_doc.html', {'node': node, 'entity': 'org', 'docForm': doc_form}, context_instance=RequestContext(request))


############################################################################
# PERSON Views #
################

@secure
def new_person(request, org_slug=None):
	form = PersonForm()
	formset = PersonFormSet(instance=Person())
	success = False
	if request.method == "POST":
		form = PersonForm(request.POST)
		if form.is_valid():
			person = form.save()
			person.last_edited_by = user_check(request.user)
			formset = PersonFormSet(request.POST, instance=person)
			if formset.is_valid():
				formset.save()

				# Add employment relationship
				org_node = Org.objects.get(slug=org_slug)
				person.add_p2org(org_node, **{'relation': EMPLOYMENT})
				person.save()

				form = PersonForm()
				formset = PersonFormSet(instance=Person())
				success = True
			else:
				person.delete()
				form = PersonForm(request.POST)

	primary = Org.objects.get(slug=org_slug)
	return render_to_response('rolodex/new_person.html', {'form': form, 'formset': formset, 'orgNode': org_slug, 'primary': primary, 'success': success}, context_instance=RequestContext(request))


@secure
def new_person_no_org(request, org_slug=None):
	form = PersonForm()
	formset = PersonFormSet(instance=Person())
	success = False
	if request.method == "POST":
		form = PersonForm(request.POST)
		if form.is_valid():
			person = form.save()
			person.last_edited_by = user_check(request.user)
			formset = PersonFormSet(request.POST, instance=person)
			if formset.is_valid():
				formset.save()

				person.save()

				form = PersonForm()
				formset = PersonFormSet(instance=Person())
				success = True
			else:
				person.delete()
				form = PersonForm(request.POST)
	return render_to_response('rolodex/new_person.html', {'form': form, 'formset': formset, 'orgNode': org_slug, 'primary': None, 'success': success}, context_instance=RequestContext(request))


@secure
def edit_person(request, person_slug):
	peep = Person.objects.get(slug=person_slug)
	form = PersonForm(instance=peep)
	formset = PersonFormSet(instance=peep)
	formset.extra = 0
	if request.method == "POST":
		form = PersonForm(request.POST, instance=peep)

		if form.is_valid():
			person = form.save()
			formset = PersonFormSet(request.POST, instance=person)
			if formset.is_valid():
				formset.save()
				person.last_edited_by = user_check(request.user)
				person.save()
				return redirect('rolodex_person', person.slug)

	employer = peep.org_from_p.filter(relation=EMPLOYMENT)
	if len(employer) > 0:
		primary = employer[0].to_ent
	else:
		primary = "N/A"
	return render_to_response('rolodex/new_person.html', {'form': form, 'formset': formset, 'personNode': peep, 'primary': primary, 'edit': True}, context_instance=RequestContext(request))


@permission_required('rolodex.delete_person')
def delete_person(request, person_slug):
	peep = Person.objects.get(slug=person_slug)
	if request.method == "POST":
		peep.delete()
		return redirect('rolodex_home')
	return render_to_response('rolodex/delete.html', {'peep': peep}, context_instance=RequestContext(request))


@secure
def search_person(request, person_slug):
	node = Person.objects.get(slug=person_slug)
	employer = node.org_from_p.filter(relation=EMPLOYMENT)
	if len(employer) > 0:
		node.primary = employer[0].to_ent.orgName
	else:
		node.primary = "N/A"
	node.contacts = node.person_contact.all()
	node.relations = node.get_relations_with_type()
	node.net_length = len(net_compiler(Person.objects.filter(slug=person_slug), 3))
	# log the search
	logger(user=request.user, person=node)
	searches = SearchLog.objects.filter(person=node, datestamp__gt=date.today() - timedelta(days=365)).order_by('-datestamp')
	node.searches = [{'date': s.datestamp.strftime("%Y-%m-%d"), 'user': s.user} for s in searches]
	node.calendar = json.dumps(node.searches)
	node.documents = Document.objects.filter(person=node)
	node.tags = node.tags.all()
	tags = Tag.objects.all()
	return render_to_response('rolodex/person.html', {'node': node, 'tags': tags, }, context_instance=RequestContext(request))


@secure
def person_map(request, person_slug):
	node = Person.objects.get(slug=person_slug)
	hops = int(request.GET.get('hops', 3))
	return render_to_response('rolodex/personMap.html', {'node': node, 'hops': hops}, context_instance=RequestContext(request))


@secure
def person_network(request, person_slug):
	network = net_compiler(Person.objects.filter(slug=person_slug), 3)
	data = json.dumps(network)
	return HttpResponse(data, content_type='application/json')


@secure
def adv_person_network(request, person_slug):
	hops = int(request.GET.get('hops', 3))
	network = net_compiler(Person.objects.filter(slug=person_slug), hops)
	peep = Person.objects.get(slug=person_slug)
	centrality_data = adv_compile(peep, hops)
	data = json.dumps({'centrality': centrality_data, 'links': network})
	return HttpResponse(data, content_type='application/json')


@secure
def new_person_relation(request, person_slug):
	saved = False
	p2org_form = P2OrgForm()
	p2p_form = P2PForm()
	if request.method == "POST":
		if request.POST['formType'] == '2P':
			p2p_form = P2PForm(request.POST)
			if p2p_form.is_valid():
				'''
				We create the relationship via model method rather than the form
				in order to force the symetrical relationship created (so the
				get_relations method works).
				'''
				from_ent = Person.objects.get(pk=request.POST['from_ent'])
				to_ent = Person.objects.get(pk=request.POST['to_ent'])
				relation = P2P_Type.objects.get_or_none(relationship_type=request.POST['relation'])
				from_ent.add_p2p(to_ent, **{'relation': relation})
				saved = True
		else:
			p2org_form = P2OrgForm(request.POST)
			if p2org_form.is_valid():
				from_ent = Person.objects.get(pk=request.POST['from_ent'])
				to_ent = Org.objects.get(pk=request.POST['to_ent'])
				relation = P2Org_Type.objects.get_or_none(relationship_type=request.POST['relation'])
				from_ent.add_p2org(to_ent, **{'relation': relation})
				saved = True
	peep_node = Person.objects.get(slug=person_slug)
	return render_to_response('rolodex/new_relation.html', {'peepNode': peep_node, 'pForm': p2p_form, 'orgForm': p2org_form, 'saved': saved}, context_instance=RequestContext(request))


@secure
def new_person_doc(request, person_slug=None):
	if request.method == "POST":
		print(request.FILES)
		doc_form = DocumentForm(request.POST, request.FILES)
		if doc_form.is_valid():
			doc_form.save()
			return redirect('rolodex_person', person_slug)
		else:
			node = Person.objects.get(pk=request.POST['person'])
	else:
		node = Person.objects.get(slug=person_slug)
		doc_form = DocumentForm(initial={'person': node})
	return render_to_response('rolodex/new_doc.html', {'node': node, 'entity': 'person', 'docForm': doc_form}, context_instance=RequestContext(request))


@secure
def delete_relationship(request):
	'''
	Delete relationships via AJAX on entity pages.
	'''
	if request.POST:
		if request.POST['from_type'] == 'p':
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


@secure
def delete_doc(request):
	if request.POST:
		doc = Document.objects.get(pk=request.POST['id'])
		doc.delete()
		return HttpResponse("Done.")


@secure
def add_tag(request):
	if request.POST:
		if request.POST['entity'] == 'person':
			p = Person.objects.get(pk=request.POST['pk'])
			p.tags.add(request.POST['tag'])
		else:
			o = Org.objects.get(pk=request.POST['pk'])
			o.tags.add(request.POST['tag'])
		return HttpResponse("Done.")


@secure
def remove_tag(request):
	if request.POST:
		if request.POST['entity'] == 'person':
			p = Person.objects.get(pk=request.POST['pk'])
			p.tags.remove(request.POST['tag'])
		else:
			o = Org.objects.get(pk=request.POST['pk'])
			o.tags.remove(request.POST['tag'])
		return HttpResponse("Done.")


@secure
def search_tag(request, tag_name=None):
	tag = {}
	tag['name'] = tag_name
	tag['peeps'] = Person.objects.filter(tags__name=tag_name)
	tag['orgs'] = Org.objects.filter(tags__name=tag_name)
	tag['all_tags'] = Tag.objects.all()
	return render_to_response('rolodex/tag_search.html', {'tag': tag, }, context_instance=RequestContext(request))

#################################################################
# SELECT SEARCH FUNCTIONS #
###########################
# AJAX search for bloodhound/typeahead and selectize


@csrf_exempt
def entity_remote_search(request):
	q = request.GET.get('q', '')
	peeps = Person.objects.filter(Q(lastName__icontains=q) | Q(firstName__icontains=q))
	orgs = Org.objects.filter(orgName__icontains=q)
	response = [
		{
			'url': reverse(search_person, args=[p.slug]),
			'name': "%s, %s" % (p.lastName, p.firstName)
		} for p in peeps
	] + [
		{
			'url': reverse(search_org, args=[o.slug]),
			'name': o.orgName
		} for o in orgs
	]
	return JsonResponse(response, safe=False)


@csrf_exempt
def person_remote_search(request):
	q = request.GET.get('q', '')
	ignore = request.GET.get('ignore', None)  # On adding relations, we want to exclude the node itself
	peeps = Person.objects.filter(
		Q(lastName__icontains=q) |
		Q(firstName__icontains=q) |
		Q(role__role__icontains=q) |
		reduce(lambda x, y: x | y, [Q(orgs__orgName__contains=letter) for letter in q])
	).exclude(pk=ignore)  # Search firstName, lastName, role and org relations
	response = [
		{
			'pk': p.pk,
			'p-url': reverse(search_person, args=[p.slug]),
			'name': "%s, %s" % (p.lastName, p.firstName),
			'role': p.role.role if hasattr(p.role, 'role') else '',
			'org': p.orgName
		} for p in org_relate_peep(peeps)
	]
	return JsonResponse(response, safe=False)


@csrf_exempt
def org_remote_search(request):
	q = request.GET.get('q', '')
	ignore = request.GET.get('ignore', None)
	orgs = Org.objects.filter(orgName__icontains=q).exclude(pk=ignore)
	response = [
		{
			'pk': o.pk,
			'org-url': reverse(search_org, args=[o.slug]),
			'new-p-url': reverse(new_person, args=[o.slug]),
			'name': o.orgName
		} for o in orgs
	]
	return JsonResponse(response, safe=False)


#################################################################
# GRAPH HELPER FUNCTIONS #
##########################


def org_relate_peep(peeps):
	'''
	Helper to serialize data for search boxes.
	'''
	for peep in peeps:
		employers = peep.org_relations.filter(p_to_org__relation=EMPLOYMENT)
		if len(employers) > 0:
			peep.orgName = employers[0].orgName
			peep.orgID = employers[0].pk
		else:
			'''
			If person has no primary org relationship, or if it has been deleted, we list
			them with N/A for the purposes of the search boxes on home and relation page.
			'''
			peep.orgName = "N/A"
			peep.orgID = "N/A"
	return peeps


def hierarchy(snode, tnode):
	if snode.type == 'org' and tnode.type == 'org':
		snode.hierarchy = Org2Org.objects.get(from_ent=snode.pk, to_ent=tnode.pk).hierarchy
		tnode.hierarchy = Org2Org.objects.get(from_ent=tnode.pk, to_ent=snode.pk).hierarchy
	else:
		snode.hierarchy = 'none'
		tnode.hierarchy = 'none'
	return (snode, tnode)


def get_info(n):
	class Output:
		pass
	node = Output()
	if n.__class__.__name__ == 'Person':
		node.name = n.firstName + " " + n.lastName
		node.type = "person"
		node.id = "p" + str(n.slug)
	else:
		node.name = n.orgName
		node.type = "org"
		node.id = "o" + str(n.slug)
	node.pk = n.pk
	return node


def get_relations(nodes):
	relations, node_list = [], []
	for node in nodes:
		snode = get_info(node)
		relations = node.get_relations()
		for r in list(chain(relations['orgs'], relations['people'])):
			tnode = get_info(r)
			snode, tnode = hierarchy(snode, tnode)
			node_list.append({
				"source": snode.id,
				"source_name": str(snode.name),
				"source_type": str(snode.type),
				"source_hierarchy": str(snode.hierarchy),
				"target": tnode.id,
				"target_name": str(tnode.name),
				"target_type": str(tnode.type),
				"target_hierarchy": str(tnode.hierarchy),
			})
		relations = list(chain(relations['orgs'], relations['people']))
	relations = list(set(relations))
	return {'node_list': node_list, 'relations': relations}


def net_compiler(nodes, hops=2):
	node_list = []
	for i in range(hops):
		result = get_relations(nodes)
		nodes = result['relations']
		node_list += result['node_list']
	# de-dup
	node_list = [dict(t) for t in set([tuple(d.items()) for d in node_list])]
	return node_list


def adv_compile(node, hops):
	'''
	Compile some basic network centrality statistics for graph.
	'''
	graph = node.nx_graph(hops)
	degree = nx.degree_centrality(graph)
	betweenness = nx.betweenness_centrality(graph)
	closeness = nx.closeness_centrality(graph)
	data = {}
	for node in degree:
		n = get_info(node)
		data[n.id] = {
			'degree': degree[node],
			'betweenness': betweenness[node],
			'closeness': closeness[node],
		}
	return data


def user_check(user):
	if user.is_authenticated():
		return user.get_username()
	else:
		return "AnonymousUser"


def logger(user, person=None, org=None):
	user = user_check(user)
	if person:
		if not SearchLog.objects.filter(person=person, user=user, datestamp=date.today()).exists():
			SearchLog.objects.create(person=person, user=user)
	if org:
		if not SearchLog.objects.filter(org=org, user=user, datestamp=date.today()).exists():
			SearchLog.objects.create(org=org, user=user)
