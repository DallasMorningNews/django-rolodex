from rest_framework import serializers

from rolodex.models import Person,Org,Contact,PersonRole,OrgContactRole,P2P,Org2Org,P2Org,Org2P,P2P_Type,Org2Org_Type,P2Org_Type
from django.contrib.auth.models import User



class RoleSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = PersonRole
		fields = ('role','description')

class ContactRoleSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = OrgContactRole
		fields = ('role','description')


class P2P_TypeSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = P2P_Type 
		fields = ('relationship_type',)
class Org2Org_TypeSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Org2Org_Type 
		fields = ('relationship_type',)
class P2Org_TypeSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = P2Org_Type 
		fields = ('relationship_type',)


class PersonSerializer(serializers.HyperlinkedModelSerializer):
	# people = serializers.HyperlinkedRelatedField(many=True, read_only=True,view_name='p_relations')
	# orgs = serializers.HyperlinkedRelatedField(many=True, read_only=True,view_name='org_relations')
	# person_role = serializers.HyperlinkedRelatedField(many=True, read_only=False,view_name='role',queryset=PersonRole.objects.all())
	class Meta:
		model = Person
		fields = ('slug','firstName', 'lastName','position','department','gender','role','person_contact','org_relations','p_relations')

class OrgSerializer(serializers.HyperlinkedModelSerializer):
	# people = serializers.HyperlinkedRelatedField(many=True, read_only=True,view_name='person-relations')
	# orgs = serializers.HyperlinkedRelatedField(many=True, read_only=True,view_name='org-relations')
	class Meta:
		model = Org
		fields = ('slug','orgName','org_relations','p_relations','org_contact')

class ContactSerializer(serializers.HyperlinkedModelSerializer):
	# person_contact = serializers.HyperlinkedRelatedField( read_only=False,view_name='person',queryset=Person.objects.all())
	# org_contact = serializers.HyperlinkedRelatedField( read_only=False,view_name='org',queryset=Org.objects.all())
	class Meta:
		model = Contact
		fields = ('id','person','org','type','contact','role','notes')

class P2PSerializer(serializers.HyperlinkedModelSerializer):
	# p_from_p = serializers.HyperlinkedRelatedField( read_only=False,view_name='from_person',queryset=Person.objects.all())
	# p_to_p = serializers.HyperlinkedRelatedField( read_only=False,view_name='to_person',queryset=Person.objects.all())
	# p2p_relation = serializers.HyperlinkedRelatedField( read_only=False,view_name='relationship_type',queryset=P2P_Type.objects.all())
	class Meta:
		model = P2P
		fields = ('id','from_ent','to_ent','relation','from_date','to_date','description')

class Org2OrgSerializer(serializers.HyperlinkedModelSerializer):
	# org_from_org = serializers.HyperlinkedRelatedField( read_only=False,view_name='from_org',queryset=Org.objects.all())
	# org_to_org = serializers.HyperlinkedRelatedField( read_only=False,view_name='to_org',queryset=Org.objects.all())
	# org2org_relation = serializers.HyperlinkedRelatedField( read_only=False,view_name='relationship_type',queryset=Org2Org_Type.objects.all())
	class Meta:
		model = Org2Org
		fields = ('id','from_ent','to_ent','relation','from_date','to_date','description')

class P2OrgSerializer(serializers.HyperlinkedModelSerializer):
	# org_from_p = serializers.HyperlinkedRelatedField( read_only=False,view_name='from_person',queryset=Person.objects.all())
	# p_to_org = serializers.HyperlinkedRelatedField( read_only=False,view_name='to_org',queryset=Org.objects.all())
	# p2org_relation = serializers.HyperlinkedRelatedField( read_only=False,view_name='relationship_type',queryset=P2Org_Type.objects.all())
	class Meta:
		model = P2Org
		fields = ('id','from_ent','to_ent','relation','from_date','to_date','description')

class Org2PSerializer(serializers.HyperlinkedModelSerializer):
	# p_from_org = serializers.HyperlinkedRelatedField( read_only=False,view_name='from_org',queryset=Org.objects.all())
	# org_to_p = serializers.HyperlinkedRelatedField( read_only=False,view_name='to_person',queryset=Person.objects.all())
	# org2p_relation = serializers.HyperlinkedRelatedField( read_only=False,view_name='relationship_type',queryset=P2Org_Type.objects.all())
	class Meta:
		model = Org2P
		fields = ('id','from_ent','to_ent','relation','from_date','to_date','description')