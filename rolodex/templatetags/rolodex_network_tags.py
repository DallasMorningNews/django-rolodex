from django import template
register = template.Library()

from rolodex.models import *

@register.filter
def network_length_check(nodeset,length):
	'''
	Checks if the 'nodeset' network contains more than 'length' nodes.
	'''
	net = len(nodeset['people'])+len(nodeset['orgs'])
	if net > int(len):
		return True 
	else:
		return False