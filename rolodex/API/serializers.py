from rest_framework import serializers

from rolodex.models import Person,Org,contact,role,org_contact_role,P2P,Org2Org,P2Org,Org2P,p2p_type,org2org_type,p2org_type
from django.contrib.auth.models import User



class RoleSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = role
		fields = ('role','description')

class ContactRoleSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = org_contact_role
		fields = ('role','description')


class P2P_TypeSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = p2p_type 
		fields = ('relationship_type',)
class Org2Org_TypeSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = org2org_type 
		fields = ('relationship_type',)
class P2Org_TypeSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = p2org_type 
		fields = ('relationship_type',)


class PersonSerializer(serializers.HyperlinkedModelSerializer):
	people = serializers.HyperlinkedRelatedField(many=True, read_only=True,view_name='person-relations')
	orgs = serializers.HyperlinkedRelatedField(many=True, read_only=True,view_name='org-relations')
	person_role = serializers.HyperlinkedRelatedField(many=True, read_only=False,view_name='roles')
	class Meta:
		model = Person
		fields = ('id','firstName', 'lastName',  'position','department','gender','p_relations','org_relations','role','person_contact')

class OrgSerializer(serializers.HyperlinkedModelSerializer):
	people = serializers.HyperlinkedRelatedField(many=True, read_only=True,view_name='person-relations')
	orgs = serializers.HyperlinkedRelatedField(many=True, read_only=True,view_name='org-relations')
	class Meta:
		model = Org
		fields = ('id','orgName','org_relations','p_relations','org_contact')

class ContactSerializer(serializers.HyperlinkedModelSerializer):
	person_contact = serializers.HyperlinkedRelatedField( read_only=False,view_name='person')
	org_contact = serializers.HyperlinkedRelatedField( read_only=False,view_name='org')
	class Meta:
		model = contact
		fields = ('id','person','org','type','contact','role','notes')

class P2PSerializer(serializers.HyperlinkedModelSerializer):
	p_from_p = serializers.HyperlinkedRelatedField( read_only=False,view_name='from_person')
	p_to_p = serializers.HyperlinkedRelatedField( read_only=False,view_name='to_person')
	p2p_relation = serializers.HyperlinkedRelatedField( read_only=False,view_name='relationship_type')
	class Meta:
		model = P2P
		fields = ('id','from_ent','to_ent','relation','from_date','to_date','description')

class Org2OrgSerializer(serializers.HyperlinkedModelSerializer):
	org_from_org = serializers.HyperlinkedRelatedField( read_only=False,view_name='from_org')
	org_to_org = serializers.HyperlinkedRelatedField( read_only=False,view_name='to_org')
	org2org_relation = serializers.HyperlinkedRelatedField( read_only=False,view_name='relationship_type')
	class Meta:
		model = Org2Org
		fields = ('id','from_ent','to_ent','relation','from_date','to_date','description')

class P2OrgSerializer(serializers.HyperlinkedModelSerializer):
	org_from_p = serializers.HyperlinkedRelatedField( read_only=False,view_name='from_person')
	p_to_org = serializers.HyperlinkedRelatedField( read_only=False,view_name='to_org')
	p2org_relation = serializers.HyperlinkedRelatedField( read_only=False,view_name='relationship_type')
	class Meta:
		model = P2Org
		fields = ('id','from_ent','to_ent','relation','from_date','to_date','description')

class Org2PSerializer(serializers.HyperlinkedModelSerializer):
	p_from_org = serializers.HyperlinkedRelatedField( read_only=False,view_name='from_org')
	org_to_p = serializers.HyperlinkedRelatedField( read_only=False,view_name='to_person')
	org2p_relation = serializers.HyperlinkedRelatedField( read_only=False,view_name='relationship_type')
	class Meta:
		model = Org2P
		fields = ('id','from_ent','to_ent','relation','from_date','to_date','description')