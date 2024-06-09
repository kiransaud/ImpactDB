from venv import logger
import django_filters
from .models import Contributor,GeographicalScope
import logging

class ContributorFilter(django_filters.FilterSet):
    class Meta:
        model=Contributor
        fields={
            'name':['exact', 'icontains'],
            'organization':['iexact','icontains']
        }
class GeographicalScopeFilter(django_filters.FilterSet):
    class Meta:
        model=GeographicalScope
        fields={
            'region':['iexact','icontains']
        }