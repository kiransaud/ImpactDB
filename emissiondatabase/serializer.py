from rest_framework import serializers
from .models import EmissionCategory,EmissionFactor,JunctionContributorEmissionfactor,GeographicalScope,Sector,Contributor,Datasource

class EmissionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=EmissionCategory
        fields='__all__'
       
        

class EmissionFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model=EmissionFactor
        fields='__all__'

class JunctionContributorEmissionfactorSerializer(serializers.ModelSerializer):
    class Meta:
        model=JunctionContributorEmissionfactor
        fields='__all__'

class GeographicalScopeSerializer(serializers.ModelSerializer):
    class Meta:
        model=GeographicalScope
        fields='__all__'
        
class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Sector
        fields='__all__'

    def validate(self,data):
        if data['date_recorded']> data['date_updated']:
            raise serializers.ValidationError("date updated must be after recorded date ")
        return data


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Contributor
        fields='__all__'

class DatasourceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Datasource
        fields='__all__'
