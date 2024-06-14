from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ContributorViewSet,
    SectorViewSet,
    EmissionCategoryViewSet,
    EmissionFactorViewSet,
    GeographicalScopelViewSet,
    DataSourceViewSet,
    JunctionContributorEmissionfactorViewSet,
    Filter_emission_Category_factor,
)

router = DefaultRouter()
router.register(r"contributor", ContributorViewSet, basename="contributor")
router.register(r"sector", SectorViewSet, basename="sector")
router.register(
    r"emissioncategory", EmissionCategoryViewSet, basename="emissiocategory"
)
router.register(r"emissionfactor", EmissionFactorViewSet, basename="emissionfactor")
router.register(
    r"geographicalscope", GeographicalScopelViewSet, basename="geographicalscope"
)
router.register(r"datasource", DataSourceViewSet, basename="datasource")
router.register(
    r"juncContribEmit", JunctionContributorEmissionfactorViewSet, basename="junction"
)


urlpatterns = [
    path("", include(router.urls)),
    path('filter-emissioncategory/<str:category_name>/',Filter_emission_Category_factor,name='EmissionSearchFilter'),
]
