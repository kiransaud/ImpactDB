from django.contrib import admin
from .models import EmissionCategory,EmissionFactor,JunctionContributorEmissionfactor,Sector,GeographicalScope,Contributor,Datasource

admin.site.register(EmissionCategory)
# admin.site.register(EmissionFactor)
admin.site.register(JunctionContributorEmissionfactor)
admin.site.register(Sector)
admin.site.register(GeographicalScope)
admin.site.register(Contributor)
admin.site.register(Datasource)

admin.site.register(EmissionFactor)
