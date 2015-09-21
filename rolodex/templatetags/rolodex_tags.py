from django import template
register = template.Library()

import os

@register.filter
def fileBaseName(string):
	return os.path.basename(string)
