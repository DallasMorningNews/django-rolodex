from rest_framework import viewsets
from rest_framework.decorators import api_view
from rolodex.API import serializers
from rolodex.models import Person,Org,contact,role,org_contact_role,P2P,Org2Org,P2Org,Org2P,p2p_type,org2org_type,p2org_type
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class RoleViewSet(viewsets.ModelViewSet):
	queryset = role.objects.all()
	serializer_class = serializers.RoleSerializer

class ContactRoleViewSet(viewsets.ModelViewSet):
	queryset = org_contact_role.objects.all()
	serializer_class = serializers.ContactRoleSerializer


class P2P_TypeViewSet(viewsets.ModelViewSet):
	queryset = p2p_type.objects.all()
	serializer_class = serializers.P2P_TypeSerializer
class Org2Org_TypeViewSet(viewsets.ModelViewSet):
	queryset = org2org_type.objects.all()
	serializer_class = serializers.Org2Org_TypeSerializer
class P2Org_TypeViewSet(viewsets.ModelViewSet):
	queryset = p2org_type.objects.all()
	serializer_class = serializers.P2Org_TypeSerializer


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all().order_by('id')
    serializer_class = serializers.PersonSerializer

class OrgViewSet(viewsets.ModelViewSet):
	queryset = Org.objects.all().order_by('id')
	serializer_class = serializers.OrgSerializer

class ContactViewSet(viewsets.ModelViewSet):
	queryset = contact.objects.all().order_by('id')
	serializer_class = serializers.ContactSerializer

class P2PViewSet(viewsets.ModelViewSet):
	queryset = P2P.objects.all().order_by('id')
	serializer_class = serializers.P2PSerializer

class Org2OrgViewSet(viewsets.ModelViewSet):
	queryset = Org2Org.objects.all().order_by('id')
	serializer_class = serializers.Org2OrgSerializer

class Org2PViewSet(viewsets.ModelViewSet):
	queryset = Org2P.objects.all().order_by('id')
	serializer_class = serializers.Org2PSerializer

class P2OrgViewSet(viewsets.ModelViewSet):
	queryset = P2Org.objects.all().order_by('id')
	serializer_class = serializers.P2OrgSerializer


class GetEmployees(APIView):
	model = Person
	queryset = Person.objects.all()
	'''
	Get all an orgs empoyees.
	'''
	def get(self,request,pk):
		org = get_object_or_404(Org,pk=pk)
		employees = org.get_employees()
		serializer = serializers.PersonSerializer(employees,many=True,context={'request': request})
		return Response(serializer.data)
