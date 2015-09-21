from rolodex.models import Org, Person, P2P,Org2Org,P2Org,Org2P,Contact,Document
from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory



class OrgForm(ModelForm):
    class Meta:
        model = Org
        fields = ['orgName','openRecordsLaw','notes']
        widgets = {
        			'orgName': forms.TextInput(attrs={'class':'form-control','placeholder':'Name'}),
        			'openRecordsLaw': forms.Select(attrs={'class':'form-control'}),
        			'notes': forms.Textarea(attrs={'class':'form-control'}),
        		}

class PersonForm(ModelForm):
	class Meta:
		model = Person
		fields = ['lastName','firstName','role','position','department','gender','birthdate','race','ethnicity','notes']
		widgets = {
					'lastName': forms.TextInput(attrs={'class':'form-control','placeholder':'Last name'}),
					'firstName': forms.TextInput(attrs={'class':'form-control', 'placeholder':'First name'}),
					'position': forms.TextInput(attrs={'class':'form-control'}),
					'department': forms.TextInput(attrs={'class':'form-control'}),
					'gender': forms.Select(attrs={'class':'form-control'}),
					'birthdate': forms.TextInput(attrs={'class':'form-control','placeholder':'Date/year of birth'}),
					'race': forms.Select(attrs={'class':'form-control'}),
					'ethnicity': forms.Select(attrs={'class':'form-control'}),
					'role': forms.Select(attrs={'class':'form-control'}),
					'notes': forms.Textarea(attrs={'class':'form-control'}),
				}

PersonFormSet = inlineformset_factory(Person,Contact,extra=1,can_delete=True,
	exclude=(),
	widgets = {
		  'contact': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter contact'}),
          'notes': forms.Textarea(attrs={'rows':5, 'cols':35, 'class':'form-control','placeholder':'Notes'}),
          'type': forms.Select(attrs={'class':'form-control'}),
        })

OrgFormSet = inlineformset_factory(Org,Contact,extra=1,can_delete=True,
	exclude=(),
	widgets = {
		  'contact': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter contact'}),
          'notes': forms.Textarea(attrs={'rows':5, 'cols':35, 'class':'form-control','placeholder':'Notes'}),
          'type': forms.Select(attrs={'class':'form-control'}),
          'role': forms.Select(attrs={'class':'form-control role'}),
        })

class DocumentForm(ModelForm):
	class Meta:
		model = Document
		fields = '__all__'
		widgets = {
					'doc': forms.FileInput(attrs={'class': 'form-control'}),
					'link': forms.URLInput(attrs={'class': 'form-control'}),
					'notes': forms.Textarea(attrs={'rows':5, 'cols':35,'class': 'form-control'}),
				  }

########################
## Relationship Forms ##
########################
class P2PForm(ModelForm):
	class Meta:
		model = P2P
		fields = ['from_ent','to_ent','relation','from_date','to_date','description']
		widgets = {'relation': forms.Select(attrs={'class':'form-control'}),}
class P2OrgForm(ModelForm):
	class Meta:
		model = P2Org
		fields = ['from_ent','to_ent','relation','from_date','to_date','description']
		widgets = {'relation': forms.Select(attrs={'class': 'form-control'}),}
class Org2PForm(ModelForm):
	class Meta:
		model = Org2P
		fields = ['from_ent','to_ent','relation','from_date','to_date','description']
		widgets = {'relation': forms.Select(attrs={'class': 'form-control'}),}
class Org2OrgForm(ModelForm):
	class Meta:
		model = Org2Org
		fields = ['from_ent','to_ent','relation','from_date','to_date','hierarchy','description']
		widgets = {'relation': forms.Select(attrs={'class': 'form-control'}),
					'hierarchy':forms.Select(attrs={'class':'form-control'})}