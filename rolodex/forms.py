from rolodex.models import Org, Person, P2P,Org2Org,P2Org,Org2P,contact
from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory



class OrgForm(ModelForm):
    class Meta:
        model = Org
        fields = ['orgName','openRecordsLaw']

class PersonForm(ModelForm):
	class Meta:
		model = Person
		fields = ['lastName','firstName','role','position','department','gender']

PersonFormSet = inlineformset_factory(Person,contact,extra=1,can_delete=True,
	widgets = {
          'notes': forms.Textarea(attrs={'rows':1, 'cols':40}),
        })

OrgFormSet = inlineformset_factory(Org,contact,extra=1,can_delete=True,
	widgets = {
          'notes': forms.Textarea(attrs={'rows':1, 'cols':40}),
        })
########################
## Relationship Forms ##
########################
class P2PForm(ModelForm):
	class Meta:
		model = P2P
class P2OrgForm(ModelForm):
	class Meta:
		model = P2Org
class Org2PForm(ModelForm):
	class Meta:
		model = Org2P
class Org2OrgForm(ModelForm):
	class Meta:
		model = Org2Org