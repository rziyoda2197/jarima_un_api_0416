# views.py
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Driver, Car, Fine
from .serializers import DriverSerializer, CarSerializer, FineSerializer


class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.prefetch_related('cars').all()
    serializer_class = DriverSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['first_name', 'last_name']

    @action(detail=True, methods=['get'], url_path='cars')
    def cars(self, request, pk=None):
        """Haydovchining barcha mashinalari"""
        driver = self.get_object()
        cars = driver.cars.all()
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='fines')
    def fines(self, request, pk=None):
        """Haydovchiga tegishli barcha jarimalar"""
        driver = self.get_object()
        fines = Fine.objects.filter(car__driver=driver)
        serializer = FineSerializer(fines, many=True)
        return Response(serializer.data)


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.select_related('driver').prefetch_related('fines').all()
    serializer_class = CarSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['driver']
    search_fields = ['brand', 'license_plate']

    @action(detail=True, methods=['get'], url_path='fines')
    def fines(self, request, pk=None):
        """Mashinaning barcha jarimalari"""
        car = self.get_object()
        fines = car.fines.all()
        serializer = FineSerializer(fines, many=True)
        return Response(serializer.data)


class FineViewSet(viewsets.ModelViewSet):
    queryset = Fine.objects.select_related('car__driver').all()
    serializer_class = FineSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['car']
    ordering_fields = ['date', 'amount']
