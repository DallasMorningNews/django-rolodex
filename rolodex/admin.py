from django.contrib import admin
from rolodex.models import openRecordsLaw,role,p2p_type,org2org_type,p2org_type,Tag,contact,Person,Org,org_contact_role



class ContactInline(admin.StackedInline):
	model = contact
	extra = 0

class POAdmin(admin.ModelAdmin):
	inlines = [ContactInline,]

admin.site.register(openRecordsLaw)
admin.site.register(role)
admin.site.register(org_contact_role)
admin.site.register(p2p_type)
admin.site.register(org2org_type)
admin.site.register(p2org_type)
admin.site.register(Tag)

admin.site.register(Person,POAdmin)
admin.site.register(Org,POAdmin)