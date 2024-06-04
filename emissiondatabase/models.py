from django.db import models

class  Contributor(models.Model):
    contributor_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255,blank=False,null=False)
    credential=models.CharField(max_length=255,blank=False,null=False)
    organization=models.CharField(max_length=255,blank=False,null=False)
    number_of_verifications=models.IntegerField(blank=True,null=True)
    number_of_contribution=models.IntegerField(blank=True,null=True)

    class Meta:
        db_table = 'contributor'
       

class Datasource(models.Model):
    data_sourceid=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255,blank=False,null=False)
    description=models.TextField(blank=True)
    reference_link=models.URLField(max_length=255,blank=True,null=True)
    contributors=models.ManyToManyField(Contributor,related_name='datasource')

    class Meta:
        db_table='datasource'
        


class GeographicalScope(models.Model):
    geographical_scope_id=models.AutoField(primary_key=True)
    region =models.CharField( max_length=50,blank=False,null=False)
    contry=models.CharField(max_length=50,blank=True,null=True)
    city=models.CharField( max_length=50,blank=True,)
    district=models.CharField( max_length=50, blank=True,null=True)
    class Meta:
        db_table='geographicalscope'

class Sector(models.Model):
    sector_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=250,blank=False,null=False)
    description=models.TextField(blank=False,null=False)
    geographic_scope=models.ForeignKey(GeographicalScope, on_delete=models.CASCADE,related_name='sectors')
    class Meta:
        db_table='sector'

class EmissionCategory(models.Model):
    emission_category_id=models.AutoField(primary_key=True)
    category=models.CharField( max_length=255,blank=False,null=False)
    sub_category=models.TextField(blank=True,null=True)
    lifecycle_activity=models.TextField(blank=True,null=True)

    class Meta:
        db_table='emissioncategory'





class EmissionFactor(models.Model):
    emission_factor_id=models.AutoField(primary_key=True)
    product_name=models.TextField( blank=True,null=True)
    additional_information=models.TextField(blank=True,null=True)
    emission_quantity=models.DecimalField( max_digits=10, decimal_places=2,blank=True)
    emission_quantity_units=models.CharField(max_length=50,blank=True,null=True)
    pollutant=models.CharField( max_length=50,blank=False,null=False)
    co2_or_co2_equivalent = models.CharField(max_length=50, blank=True, null=True)
    technical_refrence = models.TextField(blank=True, null=True)
    date_recorded=models.DateField(auto_now_add=True,blank=True,null=True)
    date_updated=models.DateField(auto_now=True,blank=True,null=True)
    reliability_factor=models.DecimalField(max_digits=16,decimal_places=2,blank=True,null=True)
    sector=models.ForeignKey( Sector,on_delete=models.CASCADE,related_name='emissionfactors_sector')
    emissioncategory=models.ForeignKey(EmissionCategory,on_delete=models.CASCADE,related_name='emissionfactors_category')
    datasource=models.ForeignKey (Datasource,on_delete=models.CASCADE,related_name='emissionfactors_source')
    geographicalscope=models.ForeignKey(GeographicalScope,on_delete=models.CASCADE,related_name='emissionfactors_geography')
    ef_tier=models.CharField(max_length=50,blank=True,null=True)

    class Meta:
        db_table='emissionfactor'

class JunctionContributorEmissionfactor(models.Model):
    emissionfactor=models.ForeignKey(EmissionFactor,on_delete=models.CASCADE)
    contributor=models.ForeignKey(Contributor,on_delete=models.CASCADE)
    class Meta:
        db_table = 'junction_contributor_emissionfactor'
        unique_together=(('emissionfactor','contributor'))


    
