from django.contrib import admin
from rolodex.models import OpenRecordsLaw,PersonRole,P2P_Type,Org2Org_Type,P2Org_Type,Tag,Contact,Person,Org,OrgContactRole



class ContactInline(admin.StackedInline):
	model = Contact
	extra = 0

class POAdmin(admin.ModelAdmin):
	inlines = [ContactInline,]

admin.site.register(OpenRecordsLaw)
admin.site.register(PersonRole)
admin.site.register(OrgContactRole)
admin.site.register(P2P_Type)
admin.site.register(Org2Org_Type)
admin.site.register(P2Org_Type)
admin.site.register(Tag)

admin.site.register(Person,POAdmin)
admin.site.register(Org,POAdmin)