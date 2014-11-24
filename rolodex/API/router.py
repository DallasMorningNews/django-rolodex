from rest_framework import routers

from rolodex.API import views

router = routers.DefaultRouter()
router.register(r'roles', views.RoleViewSet)
router.register(r'contact-roles', views.ContactRoleViewSet)
router.register(r'contacts', views.ContactViewSet)
router.register(r'people', views.PersonViewSet)
router.register(r'orgs', views.OrgViewSet)
router.register(r'relationships/person_to_person', views.P2PViewSet)
router.register(r'relationships/org_to_org', views.Org2OrgViewSet)
router.register(r'relationships/org_to_person', views.Org2PViewSet)
router.register(r'relationships/person_to_org', views.P2OrgViewSet)
router.register(r'relationships/types/person_to_person',views.P2P_TypeViewSet)
router.register(r'relationships/types/org_to_org',views.Org2Org_TypeViewSet)
router.register(r'relationships/types/person_to_org',views.P2Org_TypeViewSet)