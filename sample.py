# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models





class Contributor(models.Model):
    contributor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    credential = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    number_of_verifications = models.IntegerField(blank=True, null=True)
    number_of_contributions = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contributor'


class Datasource(models.Model):
    datasource_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    refrence_link = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        
        db_table = 'datasource'

class JuncDatasourceContributor(models.Model):
    datasource = models.OneToOneField(Datasource, models.DO_NOTHING, primary_key=True)  
    contributor = models.ForeignKey(Contributor, models.DO_NOTHING)


class Emissioncategory(models.Model):
    emission_category_id = models.AutoField(primary_key=True)
    catgory = models.CharField(max_length=255)
    sub_category = models.TextField(blank=True, null=True)
    lifecycle_activity = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'emissioncategory'


class Emissionfactor(models.Model):
    emission_factor_id = models.AutoField(primary_key=True)
    product_name = models.TextField(blank=True, null=True)
    emission_quantity = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    emission_quantity_unit = models.CharField(max_length=50, blank=True, null=True)
    pollutant = models.CharField(max_length=50, blank=True, null=True)
    co2_or_co2_equivalent = models.CharField(max_length=50, blank=True, null=True)
    additional_information = models.TextField(blank=True, null=True)
    technical_refrence = models.TextField(blank=True, null=True)
    date_recorded = models.TextField(blank=True, null=True)
    date_updated = models.TextField(blank=True, null=True)
    reliability_factor = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    sector = models.ForeignKey('Sector', models.DO_NOTHING, blank=True, null=True)
    emission_category = models.ForeignKey(Emissioncategory, on_delete=models.CASCADE, blank=True, null=True)
    data_source = models.ForeignKey(Datasource, models.DO_NOTHING, blank=True, null=True)
    geographical_scope = models.ForeignKey('Geographicalscope', models.DO_NOTHING, blank=True, null=True)
    ef_tier = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'emissionfactor'


class Geographicalscope(models.Model):
    geographical_scope_id = models.AutoField(primary_key=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'geographicalscope'


class JuncContributorEmissionfactor(models.Model):
    emission_factor = models.OneToOneField(Emissionfactor, models.DO_NOTHING, primary_key=True)  # The composite primary key (emission_factor_id, contributor_id) found, that is not supported. The first column is selected.
    contributor = models.ForeignKey(Contributor, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'junc_contributor_emissionfactor'
        unique_together = (('emission_factor', 'contributor'),)



    class Meta:
        managed = False
        db_table = 'junc_datasource_contributor'
        unique_together = (('datasource', 'contributor'),)


class Sector(models.Model):
    sector_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    geographical_scope = models.ForeignKey(Geographicalscope, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sector'
