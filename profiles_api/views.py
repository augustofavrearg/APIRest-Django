from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import status, filters
from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from profiles_api import serializers, models, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class HelloApiView(APIView):
    """ API VIEW de prueba"""

    
    serializer_class = serializers.HelloSerializers

    def get(self, request, format = None):

        """ retornar lista de caracteristicas de API VIEW"""
                
        an_apiview = [
            'usamos metodos HTTP como funciones (put, delete, patch, get post)',
            'es similar a una vista tradicional de Django',
            'nos da un mayor control sobre la logica de nuestra aplicacion',
            'Esta mapeado manualmente a los URLs',
        ]

        return Response({'message':'Hello', 'an_apiview': an_apiview})

    def post(self, request):
        """crea un mensaje con nuestro nombre """
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message':message})
        else:  
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST 
            )
    
    def put (self, request, pk=None):
        """ put actualiza un objeto"""
        return Response({'method':'PUT'})
        
    def patch (self, request, pk=None):
        """ patch actualiza parcialmente un objeto"""
        return Response({'method':'PATCH'})


    def delete (self, request, pk=None):
        """ delete borra un objeto"""
        return Response({'method':'DELETE'})


class HelloViewSet(viewsets.ViewSet):
    """Test API View Set"""

    serializer_class = serializers.HelloSerializers

    def list(self, request): 
        """retornar mensaje de Hola mundo"""

        a_viewset = [
            'usa acciones (list, create, retrieve, update, partial_update)',
            'automaticamente mapea a los URLs usando Routers'
            'provee mas funcionalidad con menos codigo',
        ]

        return Response({'message':'Hola', 'a_viewset': a_viewset})

    def create(self, request):
        """Crear nuevo mensaje de Hola Mundo"""

        serializers = self.serializer_class(data = request.data)

        if serializers.is_valid():
            name = serializers.validated_data.get("name")
            message = f"Hola {name}"
            return Response({'message': message})
        else:
            return Response(
                serializers.errors,
                status = status.HTTP_400_BAD_REQUEST
            )
    
    def retrieve(self, request, pk=None):
        """obtiene un objeto y su id"""

        return Response({'http_method':'GET'})
    
    def update(self, request, pk=None):
        """Actualiza un objeto """

        return Response({'http_method':'PUT'})

    def partial_update(self, request, pk=None):
        """Actualiza parcialmente un objeto"""
        return Response({'http_method':'PATCH'})

    def destroy(self, request, pk=None):
        """Destruye un objeto"""
        return Response({'http_method':'DELETE'})

class UserProfileViewset(viewsets.ModelViewSet):
    """Crear y actualizar perfiles"""

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfiles.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)

class UserLoginApiView(ObtainAuthToken):
    """Crea tokens de authenticacion de usuario"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Maneja el crear leer y actualizar el ProfileFeed"""    
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (
        permissions.UpdateOwnStatus, 
        IsAuthenticatedOrReadOnly
    )

    def perform_create(self, serializer):
        """Setear el perfil de usuario para el usuario que esta logueado"""
        serializer.save(user_profile = self.request.user)

