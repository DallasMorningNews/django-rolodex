from django import template
register = template.Library()

import os
import re

@register.filter
def fileBaseName(string):
	return re.sub(r'(.+)\?.+','\\1',os.path.basename(string))
