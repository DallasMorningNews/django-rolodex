
from rolodex.models import Person, Org
from rolodex.views import org_relate_peep
def modal_context(request):
	modal_peeps = Person.objects.all()
	modal_orgs = Org.objects.all()
	modal_peeps = org_relate_peep(modal_peeps)
	return {'modal_peeps':modal_peeps,'modal_orgs':modal_orgs,}