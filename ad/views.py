from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from ad.models import Ads
from ad.serializers import AdsSerializer


class AdsViewSet(CreateAPIView,
                 UpdateAPIView,
                 RetrieveAPIView,
                 GenericViewSet):
    serializer_class = AdsSerializer
    queryset = Ads.objects.all()

    @swagger_auto_schema(request_body=AdsSerializer,
                         operation_description="Criação de um novo anúncio.",
                         responses={
                             status.HTTP_201_CREATED: AdsSerializer,
                             status.HTTP_404_NOT_FOUND: 'Anúncio não encontrado.',
                             status.HTTP_400_BAD_REQUEST: 'Lista de erros de cadastramento do anúncio.'
                         })
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except TypeError as _error:
            return Response({'error': 'Error interno'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(operation_description="Lista de todos os anúncios.",
                         responses={
                             status.HTTP_200_OK: AdsSerializer(many=True)
                         })
    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))

    @swagger_auto_schema(operation_description="Retorna um anúncio a partir de seu UUID.",
                         responses={
                             status.HTTP_200_OK: AdsSerializer,
                             status.HTTP_404_NOT_FOUND: 'Anúncio não encontrada.'
                         })
    def retrieve(self, request, pk, **kwargs):
        item = self.get_object()
        serializer = self.get_serializer(item)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description="Atualiza um anúncio a partir de seu UUID.",
                         responses={
                             status.HTTP_202_ACCEPTED: AdsSerializer,
                             status.HTTP_400_BAD_REQUEST: 'Erro durante a atualização do anúncio.',
                             status.HTTP_404_NOT_FOUND: 'Anúncio não encontrada.'
                         })
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_202_ACCEPTED)

    @swagger_auto_schema(operation_description="Atualiza apenas alguns campos do anúncio.",
                         responses={
                             status.HTTP_202_ACCEPTED: AdsSerializer,
                             status.HTTP_400_BAD_REQUEST: 'Erro durante 1a atualização do anúncio.',
                             status.HTTP_404_NOT_FOUND: 'Anúncio não encontrada.'
                         })
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_202_ACCEPTED)
