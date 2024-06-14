
from rest_framework import viewsets,status,serializers,filters
from rest_framework.response import Response
from .models import *
from .serializer import *
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ContributorFilter,GeographicalScopeFilter

from rest_framework.exceptions import ValidationError
from django.core.cache import cache

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializer import UserRegisterSerializer
from .serializer import UserLoginSerializer


class ContributorViewSet(viewsets.ModelViewSet):
    queryset=Contributor.objects.all().order_by('contributor_id') #gets all the contributor entries from the database 
    print(queryset.query)
    serializer_class=ContributorSerializer
    filter_backends=[DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_class=ContributorFilter
    search_fields=['name','organization']
    ordering_fields=['number_of_verifications','number_of_contribution']

    
    def list(self,request):
        try:
            #response = cache.get('ContributorViewSet')

            #if not response:
                # Getting the queryset for the viewset
                queryset=self.get_queryset()  #treturns he queryset defined in the viewset i.e [Contributor.objects.all()] i.e retrieve entire instance of the model
           
                #searilizing  the queryset into format suitable for jason output
                serializer =self.get_serializer(queryset,many=True)
                response = Response({'status': 'contributor list success', 'data':serializer.data},
                             status=status.HTTP_200_OK)
                #cache.set('ContributorViewSet', serializer.data)
                return response

            #return Response({'status': 'contributor list success', 'data':response},
             #                status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'status':'list failed','message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
        
    def retrieve(self, request, pk=None):
        try:
            # get_object uses the pk to retrieve the instance
            instance=self.get_object() #it retrieves the single instance of the model
            serializer=self.get_serializer(instance) #serialize the instance
            return(Response({
            'status': 'retrieve success ',
            'data': serializer.data
            },status=status.HTTP_200_OK))
        
        except Exception as e :
            return(Response(
                {
                    'message':'retrieve failed',
                    'status': str(e)
                }
            ))
   
    def create(self,request):
         
         try:
            #Initialize the serializer with the request data
            serializer=self.get_serializer(data=request.data)
            
            #validate the data and raise exception if it is not valid 
            serializer.is_valid(raise_exception=True) 
            self.perform_create(serializer) # save the validate data 

            #queryset=self.get_queryset() 
            #cacheSerializer=self.get_serializer(queryset,many=True)
            #cache.set('ContributorViewSet', cacheSerializer.data)

            return Response({
                'message':'Contributor created successfully',
                'data':serializer.data
            },status=status.HTTP_201_CREATED)
         
         except serializers.ValidationError as e:
            return(Response({'status':'create validation error contributor','message': e.detail },
                            status=status.HTTP_400_BAD_REQUEST))
         except Exception as e:
            # Handle all other errors
            return Response({
                "status": "Contributor Creation failed",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
           
    def update (self,request,pk=None):
        try:
            instance =self.get_object() #select the instance need to be updated 

            # Initialize the serializer with the instance and the request data
            serializer=self.get_serializer(instance, data=request.data, partial=False)
            # Validate the data and raise an exception if invalid
            serializer.is_valid(raise_exception=True)  
            # Save the valid data using perform_update
            self.perform_update(serializer)

            #queryset=self.get_queryset() 
            #cacheSerializer=self.get_serializer(queryset,many=True)
            #cache.set('ContributorViewSet', cacheSerializer.data)

            return Response({'message': 'contriutor updated successfully','data':serializer.data},
                            status=status.HTTP_200_OK)
        
        except serializers.ValidationError as e:
            return(
                Response({
                    'status':'update validation error',
                    'message':e.detail
                }, status=status.HTTP_400_BAD_REQUEST)
            )
        except Exception as e:
            return(
                Response(
                    {
                        'status': 'update failed',
                        'message':str(e)
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            )
   
    def partial_update(self,request,pk=None):
        try:
            instance=self.get_object()
            serializer=self.get_serializer(instance,data=request.data,partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            #queryset=self.get_queryset() 
            #cacheSerializer=self.get_serializer(queryset,many=True)
            #cache.set('ContributorViewSet', cacheSerializer.data)

            return (
                Response(
                    {
                        'status':'partial update successful ',
                        'data':serializer.data
                    },status=status.HTTP_200_OK
                )
            )
        except serializers.ValidationError as e:
            return (Response({
                'status': 'validation error',
                'message':e.detail
            },
            status=status.HTTP_400_BAD_REQUEST  
            ))
        except Exception as e:
            return Response(
                {
                    'status':'partial update failed',
                    'message': str(e)
                },status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def destroy(self, request,pk=None):
        try:
            instance =self.get_object()
            self.perform_destroy(instance)

            #queryset=self.get_queryset() 
            #cacheSerializer=self.get_serializer(queryset,many=True)
            #cache.set('ContributorViewSet', cacheSerializer.data)

            return(Response({

                'status':'contributor deleted successfully'
            },status=status.HTTP_204_NO_CONTENT
            ))
        except Exception as e:
            return(Response(
                {
                    'status':" contributor data deletion failed",
                    'message':str(e)
                },status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ))

class DataSourceViewSet(viewsets.ModelViewSet):
    queryset=Datasource.objects.all().order_by('data_sourceid')
    serializer_class=DatasourceSerializer 
    
    def list(self,request):
        try:
            queryset=self.get_queryset()
            serializer=self.get_serializer(queryset, many=True)
            return(Response(
                {
                    'status':'dtata source list success',
                    'data': serializer.data
                },
                status=status.HTTP_200_OK   
            ))
        except Exception as e :
            return (
                Response(
                    {
                        'message': 'getting list failed',
                        'status': str(e)

                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            )
        
    def retrieve(self,request,pk=None):
        try:
            instance =self.get_object()
            serializer=self.get_serializer(instance)
            return(
                Response(
                    {
                        'messsage': 'retrieve success',
                        'status': serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            )
        except Exception as e :
            return(
                Response(
                    {
                        'message':'retrieve failed',
                        'status': str(e)

                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            )

    def create(self,request):
        try:
            serializer=self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception= True)
            self.perform_create(serializer)
            return(
                Response(
                    {
                        'message':'data create successful',
                        'data':serializer.data
                    },status=status.HTTP_201_CREATED
                )
            )
        except serializers.ValidationError as e:
            return(
                Response(
                    {
                        'status':'validation error',
                        'status':e.detail
                    }, status=status.HTTP_400_BAD_REQUEST
                )
            )
        except Exception as e :
            return(
                Response(
                    {
                        'message':'datasource creatiion failed',
                        'status': str(e)

                    },status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            )
    
    def update(self,request,pk=None):
        try:
            instance=self.get_object()
            serializer=self.get_serializer(instance, data=request.data, partial=False)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return(
                Response(
                    {
                        'message': 'datasource update successful',
                        'data':serializer.data
                    }, status=status.HTTP_200_OK
                )
            )
        except serializers.ValidationError as e :
            return(
                Response(
                    {
                        'status':' validation error ',
                        'message':e.detail
                    },status=status.HTTP_400_BAD_REQUEST
                )
            )
        except Exception as e :
            return(
                Response(
                    {
                        'message': 'update failed',
                        'status': str(e)
                    },status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            )

    def partial_update(self,request, pk=None):
        try:
            instance=self.get_object()
            serializer=self.get_serializer(instance,data=request.data,partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(
                        {
                        'status':'partial update successful ',
                        'data':serializer.data
                        },status=status.HTTP_200_OK
                    )
            
        except serializers.ValidationError as e:
            return  Response({
                'status': 'validation error',
                'message':e.detail
            },
            status=status.HTTP_400_BAD_REQUEST  
            )
        except Exception as e:
            return Response(
                {
                    'status':'partial update failed',
                    'message': str(e)
                },status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request,pk=None):
        try:
            instance =self.get_object()
            self.perform_destroy(instance)
            return(Response({

                'status':'contributor deleted successfully'
            },status=status.HTTP_204_NO_CONTENT
            ))
        except Exception as e:
            return(Response(
                {
                    'status':" contributor data deletion failed",
                    'message':str(e)
                },status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ))

class GeographicalScopelViewSet(viewsets.ModelViewSet):
    queryset=GeographicalScope.objects.all().order_by('geographical_scope_id')
    serializer_class=GeographicalScopeSerializer
    filter_backends=[DjangoFilterBackend,filters.SearchFilter]
    filterset_class=GeographicalScopeFilter
    search_fields=['region','country','city','district']

    def list(self,request):
        try:
            # Getting the queryset for the viewset
            queryset=self.get_queryset()  #treturns he queryset defined in the viewset i.e [Contributor.objects.all()] i.e retrieve entire instance of the model
           
            #searilizing  the queryset into format suitable for jason output
            serializer =self.get_serializer(queryset,many=True)
            return Response({'status': 'geographical list success', 'data':serializer.data},
                             status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'status':'list failed','message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
        
    def retrieve(self, request, pk=None):
        try:
            # get_object uses the pk to retrieve the instance
            instance=self.get_object() #it retrieves the single instance of the model
            serializer=self.get_serializer(instance) #serialize the instance
            return(Response({
            'status': 'retrieve success ',
            'data': serializer.data
            },status=status.HTTP_200_OK))
        
        except Exception as e :
            return(Response(
                {
                    'message':'retrieve failed',
                    'status': str(e)
                }
            ))
   
    def create(self,request):
         
         try:
            #Initialize the serializer with the request data
            serializer=self.get_serializer(data=request.data)
            
            #validate the data and raise exception if it is not valid 
            serializer.is_valid(raise_exception=True) 
            self.perform_create(serializer) # save the validate data 
            return Response({
                'message':'Geographical created successfully',
                'data':serializer.data
            },status=status.HTTP_201_CREATED)
         
         except serializers.ValidationError as e:
            return(Response({'status':' validation error','message': e.detail },
                            status=status.HTTP_400_BAD_REQUEST))
         except Exception as e:
            # Handle all other errors
            return Response({
                "status": "Geographical Creation failed",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
           
    def update (self,request,pk=None):
        try:
            instance =self.get_object() #select the instance need to be updated 

            # Initialize the serializer with the instance and the request data
            serializer=self.get_serializer(instance, data=request.data, partial=False)
            # Validate the data and raise an exception if invalid
            serializer.is_valid(raise_exception=True)  
            # Save the valid data using perform_update
            self.perform_update(serializer)
            return Response({'message': ' updated successfully','data':serializer.data},
                            status=status.HTTP_200_OK)
        
        except serializers.ValidationError as e:
            return(
                Response({
                    'status':'update validation error',
                    'message':e.detail
                }, status=status.HTTP_400_BAD_REQUEST)
            )
        except Exception as e:
            return(
                Response(
                    {
                        'status': 'update failed',
                        'message':str(e)
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            )
   
    def partial_update(self,request,pk=None):
        try:
            instance=self.get_object()
            serializer=self.get_serializer(instance,data=request.data,partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return (
                Response(
                    {
                        'status':'partial update successful ',
                        'data':serializer.data
                    },status=status.HTTP_200_OK
                )
            )
        except serializers.ValidationError as e:
            return (Response({
                'status': 'validation error',
                'message':e.detail
            },
            status=status.HTTP_400_BAD_REQUEST  
            ))
        except Exception as e:
            return Response(
                {
                    'status':'partial update failed',
                    'message': str(e)
                },status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def destroy(self, request,pk=None):
        try:
            instance =self.get_object()
            self.perform_destroy(instance)
            return(Response({

                'status':'geographicalscope deleted successfully'
            },status=status.HTTP_204_NO_CONTENT
            ))
        except Exception as e:
            return(Response(
                {
                    'status':" deletion failed",
                    'message':str(e)
                },status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ))

class SectorViewSet(viewsets.ModelViewSet):
    queryset=Sector.objects.all().order_by('sector_id')
    serializer_class=SectorSerializer

    def list(self,request):
        try:
            queryset=self.get_queryset()
            serializer=self.get_serializer(queryset,many=True)
            return Response(
                {
                    'status':'List successfull',
                    'data':serializer.data
                },status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'status':'getting list failed ',
                    'message':str(e)
                },status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
 
    def retrieve(self,request,pk=None):

        try:
            instance=self.get_object()
            serializer=self.get_serializer(instance)
            return(
                Response(
                    {
                        'messsage': 'retrieve success',
                        'status': serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            )
        except Exception as e :
            return(
                Response(
                    {
                        'message':'retrieve failed',
                        'status': str(e)

                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            )
   
    def create(self, request):
        try:
            serializer=self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(
                {
                    'status': 'sector created successfully',
                    'data':serializer.data
                }, status=status.HTTP_201_CREATED
            )
        except serializers.ValidationError as e :
            return Response(
                {
                    'status':'validation error',
                    'message': e.detail
                }, status= status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response (
                {
                    'status':'list creation failed',
                    'message':str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self,request,pk=None):
        try:
            instance=self.get_object()
            serializer=self.get_serializer(instance, data=request.data,partial=False)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(
                 {
                        'message': 'datasource update successful',
                        'data':serializer.data
                    }, status=status.HTTP_200_OK
            )
        except serializers.ValidationError as e: 
            return Response (
                 {
                        'status':' validation error ',
                        'message':e.detail
                    },status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e :
            return Response (
                 {
                    'message': 'update failed',
                    'status': str(e)
                },status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def partial_update(self,request, pk=None):
        try:
            instance=self.get_object()
            serializer=self.get_serializer(instance,data=request.data,partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return (
                    Response(
                        {
                            'status':'partial update successful ',
                            'data':serializer.data
                        },status=status.HTTP_200_OK
                    )
            )
        except serializers.ValidationError as e:
            return (Response({
                'status': 'validation error',
                'message':e.detail
            },
            status=status.HTTP_400_BAD_REQUEST  
            ))
        except Exception as e:
            return Response(
                {
                    'status':'partial update failed',
                    'message': str(e)
                },status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self,request,pk=None):
        try:
            instance=self.get_object()
            self.perform_destroy(instance)
            return(Response({

                'status':'contributor deleted successfully'
            },status=status.HTTP_204_NO_CONTENT
            ))
        except Exception as e:
            return Response(
                {
                    'status':" contributor data deletion failed",
                    'message':str(e)
                },status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class EmissionCategoryViewSet(viewsets.ModelViewSet):
    queryset=EmissionCategory.objects.all().order_by('emission_category_id')
    serializer_class=EmissionCategorySerializer

    def list(self,request):
        try:
            queryset=self.get_queryset()
            serializer=self.get_serializer(queryset, many=True)
            return Response(
                {
                    'status':'List successfull',
                    'data':serializer.data
                },status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'status':'getting list failed ',
                    'message':str(e)
                },status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
   
    def retrieve(self,request,pk=None):
        try:
            instance=self.get_object()
            serializer=self.get_serializer(instance)
            return Response(
                {
                    'status':'retrieve successfull',
                    'data':serializer.data
                },status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'status':'retrirve failed ',
                    'message':str(e)
                },status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def create(self,request):
        try:
            serializer=self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(
                {
                    'status':'emission category create successful',
                    'data':serializer.data
                }, status=status.HTTP_201_CREATED
            )
        
        except serializers.ValidationError as e:
            return Response(
                {
                    'status':'validation error',
                    'message': e.detail
                },status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response (
                {
                    'status':'emission category create failed',
                    'message': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def update(self,request,pk=None):
        try:
            instance=self.get_object()
            serializer=self.get_serializer(instance,data=request.data, partial=False)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response (
                 {
                        'message': 'update successful',
                        'data':serializer.data
                    }, status=status.HTTP_200_OK
            )
        except serializers.ValidationError as e: 
            return Response (
                 {
                        'status':' validation error ',
                        'message':e.detail
                    },status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e :
            return Response (
                 {
                    'message': 'update failed',
                    'status': str(e)
                },status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def partial_update(self,request,pk=None):
        try:
            instance=self.get_object()
            serializer=self.get_serializer(instance,data=request.data,partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return (
                    Response(
                        {
                            'status':'partial update successful ',
                            'data':serializer.data
                        },status=status.HTTP_200_OK
                    )
            )
        except serializers.ValidationError as e:
            return (Response({
                'status': 'validation error',
                'message':e.detail
            },
            status=status.HTTP_400_BAD_REQUEST  
            ))
        except Exception as e:
            return Response(
                {
                    'status':'partial update failed',
                    'message': str(e)
                },status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self,request,pk=None):
        try:
            instance=self.get_object()
            self.perform_destroy(instance)
            return Response({

                'status':'contributor deleted successfully'
            },status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                {
                    'status':" contributor data deletion failed",
                    'message':str(e)
                },status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class EmissionFactorViewSet(viewsets.ModelViewSet):
    queryset=EmissionFactor.objects.all().order_by('emission_factor_id')
    serializer_class=EmissionFactorSerializer
   
    def list(self,request):
        try:
            queryset=self.get_queryset()
            serializer=self.get_serializer(queryset, many=True)
            return Response(
                {
                    'status':'List successfull',
                    'data':serializer.data
                },status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'status':'getting list failed ',
                    'message':str(e)
                },status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
   
    def retrieve(self,request,pk=None):
        try:
            instance=self.get_object()
            serializer=self.get_serializer(instance)
            return Response(
                {
                    'status':'retrieve successfull',
                    'data':serializer.data
                },status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'status':'retrirve failed ',
                    'message':str(e)
                },status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def create(self,request):
        try:
            serializer=self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(
                {
                    'status':'emission factor create successful',
                    'data':serializer.data
                }, status=status.HTTP_201_CREATED
            )
        
        except serializers.ValidationError as e:
            return Response(
                {
                    'status':'validation error',
                    'message': e.detail
                },status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response (
                {
                    'status':'emission factor create failed',
                    'message': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def update(self,request,pk=None):
        try:
            instance=self.get_object()
            serializer=self.get_serializer(instance,data=request.data, partial=False)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response (
                 {
                        'message': 'update successful',
                        'data':serializer.data
                    }, status=status.HTTP_200_OK
            )
        except serializers.ValidationError as e: 
            return Response (
                 {
                        'status':' validation error ',
                        'message':e.detail
                    },status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e :
            return Response (
                 {
                    'message': 'update failed',
                    'status': str(e)
                },status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def partial_update(self,request,pk=None):
        try:
            instance=self.get_object()
            serializer=self.get_serializer(instance,data=request.data,partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return (
                    Response(
                        {
                            'status':'partial update successful ',
                            'data':serializer.data
                        },status=status.HTTP_200_OK
                    )
            )
        except serializers.ValidationError as e:
            return (Response({
                'status': 'validation error',
                'message':e.detail
            },
            status=status.HTTP_400_BAD_REQUEST  
            ))
        except Exception as e:
            return Response(
                {
                    'status':'partial update failed',
                    'message': str(e)
                },status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self,request,pk=None):
        try:
            instance=self.get_object()
            self.perform_destroy(instance)
            return Response (
                {
                    'status':'delete successful'
                }, status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                {
                    'status':'deletion failes',
                    'message':str(e)
                }, status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @action(methods=['post'],detail=False,url_name='bulk-upload-emission-factors',url_path='bulk-upload')
    
    def bulk_upload(self,request,*args,**kwargs):
        try:
            if not isinstance(request.data,list):
                return Response({'error':'list is expected '},status=status.HTTP_400_BAD_REQUEST)
            serializer=self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            emission_factors=[EmissionFactor(**item)for item in serializer.validated_data]
            EmissionFactor.objects.bulk_create(emission_factors)
            return Response({
                'message':'emission created successfully',
                'data':serializer.data
            },status=status.HTTP_201_CREATED)
        
        except serializers.ValidationError as e:
            return Response({
                'status':'validation error',
                'message':e.detail
            },status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {
                    'status':'bulk emission factor creation failed',
                    'message':str(e)
                }
            )

            
        

class JunctionContributorEmissionfactorViewSet(viewsets.ModelViewSet):
    queryset=JunctionContributorEmissionfactor.objects.all()
    serializer_class=JunctionContributorEmissionfactorSerializer
    
    


class UserLoginAPIView(APIView):
    def post(self, request, *args, **kargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            response = {
                "username": {
                    "detail": "User Doesnot exist!"
                }
            }
            if User.objects.filter(username=request.data['username']).exists():
                user = User.objects.get(username=request.data['username'])
                token, created = Token.objects.get_or_create(user=user)
                response = {
                    'success': True,
                    'username': user.username,
                    'email': user.email,
                    'token': token.key
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterAPIView(APIView):
    def post(self, request, *args, **kargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'success': True,
                'user': serializer.data,
                'token': Token.objects.get(user=User.objects.get(username=serializer.data['username'])).key
            }
            return Response(response, status=status.HTTP_200_OK)
        raise ValidationError(
            serializer.errors, code=status.HTTP_406_NOT_ACCEPTABLE)


class UserLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({"success": True, "detail": "Logged out!"}, status=status.HTTP_200_OK)













    



    



        







        
















    



    



        







        