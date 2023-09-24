from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from property.models import Property
from property.serializers import PropertySerializer


class PropertyViewSet(CreateAPIView,
                      UpdateAPIView,
                      RetrieveAPIView,
                      DestroyAPIView,
                      GenericViewSet):
    serializer_class = PropertySerializer
    queryset = Property.objects.all().order_by('-created_at')

    @swagger_auto_schema(request_body=PropertySerializer,
                         operation_description="Criação de um novo imóvel.",
                         responses={
                             status.HTTP_201_CREATED: PropertySerializer,
                             status.HTTP_404_NOT_FOUND: 'Imóvel não encontrado.',
                             status.HTTP_400_BAD_REQUEST: 'Lista de erros de cadastramento do imóvel.'
                         })
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except TypeError as _error:
            return Response({'error': 'Error interno'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(operation_description="Lista de todos os imóveis",
                         responses={
                             status.HTTP_200_OK: PropertySerializer(many=True)
                         })
    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))

    @swagger_auto_schema(operation_description="Retorna um imóvel a partir de seu UUID.",
                         responses={
                             status.HTTP_200_OK: PropertySerializer(many=True),
                             status.HTTP_404_NOT_FOUND: 'Imóvel não encontrado.'
                         })
    def retrieve(self, request, pk):
        item = self.get_object()
        serializer = self.get_serializer(item)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description="Apagar um imóvel.",
                         responses={
                             status.HTTP_204_NO_CONTENT: 'Imóvel apagado com sucesso.',
                             status.HTTP_404_NOT_FOUND: 'Imóvel não encontrado.'
                         })
    def destroy(self, request, pk):
        item = self.get_object()
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(operation_description="Atualiza um imóvel a partir de seu UUID.",
                         responses={
                             status.HTTP_202_ACCEPTED: PropertySerializer,
                             status.HTTP_400_BAD_REQUEST: 'Erro durante a atualização do imóvel.',
                             status.HTTP_404_NOT_FOUND: 'Imóvel não encontrada.'
                         })
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_202_ACCEPTED)

    @swagger_auto_schema(operation_description="Atualiza apenas alguns campos do imóvel.",
                         responses={
                             status.HTTP_202_ACCEPTED: PropertySerializer,
                             status.HTTP_400_BAD_REQUEST: 'Erro durante 1a atualização do imóvel.',
                             status.HTTP_404_NOT_FOUND: 'Imóvel não encontrada.'
                         })
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_202_ACCEPTED)
