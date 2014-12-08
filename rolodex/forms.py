from rolodex.models import Org, Person, P2P,Org2Org,P2Org,Org2P,Contact
from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory



class OrgForm(ModelForm):
    class Meta:
        model = Org
        fields = ['orgName','openRecordsLaw','notes']

class PersonForm(ModelForm):
	class Meta:
		model = Person
		fields = ['lastName','firstName','role','position','department','gender','notes']

PersonFormSet = inlineformset_factory(Person,Contact,extra=1,can_delete=True,
	widgets = {
          'notes': forms.Textarea(attrs={'rows':1, 'cols':40}),
        })

OrgFormSet = inlineformset_factory(Org,Contact,extra=1,can_delete=True,
	widgets = {
          'notes': forms.Textarea(attrs={'rows':1, 'cols':40}),
        })
########################
## Relationship Forms ##
########################
class P2PForm(ModelForm):
	class Meta:
		model = P2P
		fields = ['from_ent','to_ent','relation','from_date','to_date','description']
class P2OrgForm(ModelForm):
	class Meta:
		model = P2Org
		fields = ['from_ent','to_ent','relation','from_date','to_date','description']
class Org2PForm(ModelForm):
	class Meta:
		model = Org2P
		fields = ['from_ent','to_ent','relation','from_date','to_date','description']
class Org2OrgForm(ModelForm):
	class Meta:
		model = Org2Org
		fields = ['from_ent','to_ent','relation','from_date','to_date','hierarchy','description']