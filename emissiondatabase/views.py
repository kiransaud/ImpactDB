from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from .models import *
from .serializer import *
from rest_framework.decorators import action, api_view


class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all().order_by("contributor_id")
    serializer_class = ContributorSerializer

    def list(self, request):
        try:
            # Getting the queryset for the viewset
            queryset = (
                self.get_queryset()
            )  # treturns he queryset defined in the viewset i.e [Contributor.objects.all()] i.e retrieve entire instance of the model

            # searilizing  the queryset into format suitable for jason output
            serializer = self.get_serializer(queryset, many=True)
            return Response(
                {"status": "contributor list success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"status": "list failed", "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def retrieve(self, request, pk=None):
        try:
            # get_object uses the pk to retrieve the instance
            instance = (
                self.get_object()
            )  # it retrieves the single instance of the model
            serializer = self.get_serializer(instance)  # serialize the instance
            return Response(
                {"status": "retrieve success ", "data": serializer.data},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response({"message": "retrieve failed", "status": str(e)})

    def create(self, request):
        try:
            # Initialize the serializer with the request data
            serializer = self.get_serializer(data=request.data)

            # validate the data and raise exception if it is not valid
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)  # save the validate data
            return Response(
                {
                    "message": "Contributor created successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        except serializers.ValidationError as e:
            return Response(
                {"status": "create validation error contributor", "message": e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            # Handle all other errors
            return Response(
                {"status": "Contributor Creation failed", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, pk=None):
        try:
            instance = self.get_object()  # select the instance need to be updated

            # Initialize the serializer with the instance and the request data
            serializer = self.get_serializer(instance, data=request.data, partial=False)
            # Validate the data and raise an exception if invalid
            serializer.is_valid(raise_exception=True)
            # Save the valid data using perform_update
            self.perform_update(serializer)
            return Response(
                {"message": "contriutor updated successfully", "data": serializer.data},
                status=status.HTTP_200_OK,
            )

        except serializers.ValidationError as e:
            return Response(
                {"status": "update validation error", "message": e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"status": "update failed", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def partial_update(self, request, pk=None):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(
                {"status": "partial update successful ", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except serializers.ValidationError as e:
            return Response(
                {"status": "validation error", "message": e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"status": "partial update failed", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, pk=None):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(
                {"status": "contributor deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            return Response(
                {"status": " contributor data deletion failed", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DataSourceViewSet(viewsets.ModelViewSet):
    queryset = Datasource.objects.all().order_by("data_sourceid")
    serializer_class = DatasourceSerializer

    def list(self, request):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(
                {"status": "dtata source list success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"message": "getting list failed", "status": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, pk=None):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(
                {"messsage": "retrieve success", "status": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"message": "retrieve failed", "status": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(
                {"message": "data create successful", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        except serializers.ValidationError as e:
            return Response(
                {"status": "validation error", "status": e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"message": "datasource creatiion failed", "status": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, pk=None):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=False)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(
                {"message": "datasource update successful", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except serializers.ValidationError as e:
            return Response(
                {"status": " validation error ", "message": e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"message": "update failed", "status": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def partial_update(self, request, pk=None):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(
                {"status": "partial update successful ", "data": serializer.data},
                status=status.HTTP_200_OK,
            )

        except serializers.ValidationError as e:
            return Response(
                {"status": "validation error", "message": e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"status": "partial update failed", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, pk=None):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(
                {"status": "contributor deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            return Response(
                {"status": " contributor data deletion failed", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GeographicalScopelViewSet(viewsets.ModelViewSet):
    queryset = GeographicalScope.objects.all().order_by("geographical_scope_id")
    serializer_class = GeographicalScopeSerializer

    def list(self, request):
        try:
            # Getting the queryset for the viewset
            queryset = (
                self.get_queryset()
            )  # treturns he queryset defined in the viewset i.e [Contributor.objects.all()] i.e retrieve entire instance of the model

            # searilizing  the queryset into format suitable for jason output
            serializer = self.get_serializer(queryset, many=True)
            return Response(
                {"status": "geographical list success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"status": "list failed", "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def retrieve(self, request, pk=None):
        try:
            # get_object uses the pk to retrieve the instance
            instance = (
                self.get_object()
            )  # it retrieves the single instance of the model
            serializer = self.get_serializer(instance)  # serialize the instance
            return Response(
                {"status": "retrieve success ", "data": serializer.data},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response({"message": "retrieve failed", "status": str(e)})

    def create(self, request):
        try:
            # Initialize the serializer with the request data
            serializer = self.get_serializer(data=request.data)

            # validate the data and raise exception if it is not valid
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)  # save the validate data
            return Response(
                {
                    "message": "Geographical created successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        except serializers.ValidationError as e:
            return Response(
                {"status": " validation error", "message": e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            # Handle all other errors
            return Response(
                {"status": "Geographical Creation failed", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, pk=None):
        try:
            instance = self.get_object()  # select the instance need to be updated

            # Initialize the serializer with the instance and the request data
            serializer = self.get_serializer(instance, data=request.data, partial=False)
            # Validate the data and raise an exception if invalid
            serializer.is_valid(raise_exception=True)
            # Save the valid data using perform_update
            self.perform_update(serializer)
            return Response(
                {"message": " updated successfully", "data": serializer.data},
                status=status.HTTP_200_OK,
            )

        except serializers.ValidationError as e:
            return Response(
                {"status": "update validation error", "message": e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"status": "update failed", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def partial_update(self, request, pk=None):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(
                {"status": "partial update successful ", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except serializers.ValidationError as e:
            return Response(
                {"status": "validation error", "message": e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"status": "partial update failed", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, pk=None):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(
                {"status": "geographicalscope deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            return Response(
                {"status": " deletion failed", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class SectorViewSet(viewsets.ModelViewSet):
    queryset = Sector.objects.all().order_by("sector_id")
    serializer_class = SectorSerializer

    def list(self, request):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(
                {"status": "List successfull", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"status": "getting list failed ", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, pk=None):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(
                {"messsage": "retrieve success", "status": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"message": "retrieve failed", "status": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(
                {"status": "sector created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        except serializers.ValidationError as e:
            return Response(
                {"status": "validation error", "message": e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"status": "list creation failed", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, pk=None):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=False)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(
                {"message": "datasource update successful", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except serializers.ValidationError as e:
            return Response(
                {"status": " validation error ", "message": e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"message": "update failed", "status": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def partial_update(self, request, pk=None):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(
                {"status": "partial update successful ", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except serializers.ValidationError as e:
            return Response(
                {"status": "validation error", "message": e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"status": "partial update failed", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, pk=None):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(
                {"status": "contributor deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            return Response(
                {"status": " contributor data deletion failed", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class EmissionCategoryViewSet(viewsets.ModelViewSet):
    queryset = EmissionCategory.objects.all().order_by("emission_category_id")
    serializer_class = EmissionCategorySerializer

    def list(self, request):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(
                {"status": "List successfull", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"status": "getting list failed ", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, pk=None):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(
                {"status": "retrieve successfull", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"status": "retrirve failed ", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(
                {
                    "status": "emission category create successful",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        except serializers.ValidationError as e:
            return Response(
                {"status": "validation error", "message": e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"status": "emission category create failed", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, pk=None):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=False)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(
                {"message": "update successful", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except serializers.ValidationError as e:
            return Response(
                {"status": " validation error ", "message": e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"message": "update failed", "status": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def partial_update(self, request, pk=None):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(
                {"status": "partial update successful ", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except serializers.ValidationError as e:
            return Response(
                {"status": "validation error", "message": e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"status": "partial update failed", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, pk=None):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(
                {"status": "contributor deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            return Response(
                {"status": " contributor data deletion failed", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class EmissionFactorViewSet(viewsets.ModelViewSet):
    queryset = EmissionFactor.objects.all().order_by("emission_factor_id")
    serializer_class = EmissionFactorSerializer

    def list(self, request):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(
                {"status": "List successfull", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"status": "getting list failed ", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, pk=None):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(
                {"status": "retrieve successfull", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"status": "retrirve failed ", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(
                {
                    "status": "emission factor create successful",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        except serializers.ValidationError as e:
            return Response(
                {"status": "validation error", "message": e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"status": "emission factor create failed", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, pk=None):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=False)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(
                {"message": "update successful", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except serializers.ValidationError as e:
            return Response(
                {"status": " validation error ", "message": e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"message": "update failed", "status": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def partial_update(self, request, pk=None):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(
                {"status": "partial update successful ", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except serializers.ValidationError as e:
            return Response(
                {"status": "validation error", "message": e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"status": "partial update failed", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, pk=None):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(
                {"status": "delete successful"}, status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                {"status": "deletion failes", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(
        methods=["post"],
        detail=False,
        url_name="bulk-upload-emission-factors",
        url_path="bulk-upload",
    )
    def bulk_upload(self, request, *args, **kwargs):
        try:
            if not isinstance(request.data, list):
                return Response(
                    {"error": "list is expected "}, status=status.HTTP_400_BAD_REQUEST
                )
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            emission_factors = [
                EmissionFactor(**item) for item in serializer.validated_data
            ]
            EmissionFactor.objects.bulk_create(emission_factors)
            return Response(
                {"message": "emission created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )

        except serializers.ValidationError as e:
            return Response(
                {"status": "validation error", "message": e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"status": "bulk emission factor creation failed", "message": str(e)}
            )


class JunctionContributorEmissionfactorViewSet(viewsets.ModelViewSet):
    queryset = JunctionContributorEmissionfactor.objects.all()
    serializer_class = JunctionContributorEmissionfactorSerializer


@api_view(["GET"])
def Filter_emission_Category_factor(request, category_name=None):

    if category_name is not None:
        try:
            category = EmissionCategory.objects.get(category=category_name)
            emission_factors = EmissionFactor.objects.filter(emissioncategory=category)
            serializer = EmissionFactorSerializer(emission_factors, many=True)
            return Response(serializer.data)
        except EmissionCategory.DoesNotExist:
            return Response(
                {"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND
            )
    else:
        return Response(
            {"error": "Category parameter is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )
