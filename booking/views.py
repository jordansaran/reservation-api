import logging

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from booking.models import Booking
from booking.serializers import BookingSerializer


class BookingViewSet(CreateAPIView, RetrieveAPIView, DestroyAPIView, GenericViewSet):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()

    @swagger_auto_schema(request_body=BookingSerializer,
                         operation_description="Criação de uma nova reserva.",
                         responses={
                             status.HTTP_201_CREATED: BookingSerializer,
                             status.HTTP_404_NOT_FOUND: 'Reserva não encontrada.',
                             status.HTTP_400_BAD_REQUEST: 'Lista de erros de cadastramento da reserva.'
                         })
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except TypeError as _error:
            logging.error(_error)
            return Response({'error': 'Error interno'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(operation_description="Lista de todas reservas",
                         responses={
                             status.HTTP_200_OK: BookingSerializer(many=True)
                         })
    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))

    @swagger_auto_schema(operation_description="Retorna uma reserva a partir de seu UUID.",
                         responses={status.HTTP_200_OK: BookingSerializer(many=True),
                                    status.HTTP_404_NOT_FOUND: 'Reserva não encontrada.'
                                    })
    def retrieve(self, request, pk, **kwargs):
        item = self.get_object()
        serializer = self.get_serializer(item)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description="Apagar uma reserva.",
                         responses={
                             status.HTTP_204_NO_CONTENT: 'Reserva apagada com sucesso.',
                             status.HTTP_404_NOT_FOUND: 'Reserva não encontrado.'
                         })
    def destroy(self, request, pk, **kwargs):
        item = self.get_object()
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
