from django.conf.urls import patterns, url, include
from rolodex import views, API
from rolodex.API import router, views as APIviews



urlpatterns = patterns('',
    url(r'^$', views.home, name='rolodex_home'),
    url(r'^org/(.+)/$',views.search_org,name='rolodex_org'),
    url(r'^person/(.+)/$',views.search_person,name='rolodex_person'),

    #Entity maintenance
    url(r'^add-person/(.+)/$',views.new_person,name='rolodex_new_person'),
    url(r'^add-person/$',views.new_person_no_org,name='rolodex_new_person_no_org'),
    url(r'^edit-person/(.+)/$',views.edit_person,name='rolodex_edit_person'),
    url(r'^delete-person/(.+)/$',views.delete_person,name='rolodex_delete_person'),
    url(r'^add-org/$',views.new_org,name='rolodex_new_org'),
    url(r'^edit-org/(.+)/$',views.edit_org,name='rolodex_edit_org'),
    url(r'^delete-org/(.+)/$',views.delete_org,name='rolodex_delete_org'),
    
    #Relationship maintenance
    url(r'^add-relationship/org/(.+)/$',views.new_org_relation,name='rolodex_new_org_relation'),
    url(r'^add-relationship/person/(.+)/$',views.new_person_relation,name='rolodex_new_person_relation'),
    url(r'^delete-relationship/$',views.delete_relationship,name='rolodex_delete_relation'),


    #network graphs
    url(r'^person-map/(.+)/$',views.person_map,name='rolodex_person_map'),
    url(r'^org-map/(.+)/$',views.org_map,name='rolodex_org_map'),
    url(r'^person-network/(.+)/$',views.person_network,name='rolodex_person_network'),
    url(r'^org-network/(.+)/$',views.org_network,name='rolodex_org_network'),
    url(r'^person-network-advanced/person/(.+)/$',views.adv_person_network,name='rolodex_adv_person_network'),
    url(r'^org-network-advanced/org/(.+)/$',views.adv_org_network,name='rolodex_adv_org_network'),
    
    #api
    url(r'^api/',include(router.router.urls)),
    url(r'^api/employees/([0-9]+)/$',APIviews.GetEmployees.as_view())
)

'''
    Work on more API calls to match model methods (though some model funcs 
        are passed strings and others objects...)
'''