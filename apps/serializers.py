from rest_framework import serializers
from .models import Driver, Car, Fine


class DriverSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    cars = serializers.SerializerMethodField()

    class Meta:
        model = Driver
        fields = ['id', 'first_name', 'last_name', 'full_name', 'cars']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    def get_cars(self, obj):
        return [ car.brand for car in obj.cars.all()]


class CarSerializer(serializers.ModelSerializer):
    driver_name = serializers.StringRelatedField(source="driver")
    fines = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = ['id', 'brand', 'license_plate', 'driver']

    def get_fines(self, obj):
        return [ f"{fine.date} - ${fine.amount}" for fine in obj.fines.all() if fine.amount != 0 ]



class FineSerializer(serializers.ModelSerializer):
    car_brand = serializers.StringRelatedField(source="car")

    class Meta:
        model = Fine
        fields = ['id', 'amount', 'date', 'car', 'car_brand']
        read_only_fields = ['date', 'amount', 'car_brand']
