from rest_framework import serializers


class BusinessLocationESSerializer(serializers.Serializer):
    location_name = serializers.CharField()
    manager_name = serializers.CharField()
    location_email = serializers.CharField()
    dispensary = serializers.BooleanField()
    delivery = serializers.BooleanField()
    grow_house = serializers.BooleanField()
    delivery_radius = serializers.FloatField()
    street1 = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField()
    zip_code = serializers.CharField()
    lat = serializers.FloatField()
    lng = serializers.FloatField()
    location_raw = serializers.CharField()
    phone = serializers.CharField()
    ext = serializers.CharField()
    removed_date = serializers.DateTimeField()
    created_date = serializers.DateTimeField()
    mon_open = serializers.TimeField(format='%I:%M %p', input_formats=['%I:%M %p'], allow_null=True)
    mon_close = serializers.TimeField(format='%I:%M %p', input_formats=['%I:%M %p'], allow_null=True)
    tue_open = serializers.TimeField(format='%I:%M %p', input_formats=['%I:%M %p'], allow_null=True)
    tue_close = serializers.TimeField(format='%I:%M %p', input_formats=['%I:%M %p'], allow_null=True)
    wed_open = serializers.TimeField(format='%I:%M %p', input_formats=['%I:%M %p'], allow_null=True)
    wed_close = serializers.TimeField(format='%I:%M %p', input_formats=['%I:%M %p'], allow_null=True)
    thu_open = serializers.TimeField(format='%I:%M %p', input_formats=['%I:%M %p'], allow_null=True)
    thu_close = serializers.TimeField(format='%I:%M %p', input_formats=['%I:%M %p'], allow_null=True)
    fri_open = serializers.TimeField(format='%I:%M %p', input_formats=['%I:%M %p'], allow_null=True)
    fri_close = serializers.TimeField(format='%I:%M %p', input_formats=['%I:%M %p'], allow_null=True)
    sat_open = serializers.TimeField(format='%I:%M %p', input_formats=['%I:%M %p'], allow_null=True)
    sat_close = serializers.TimeField(format='%I:%M %p', input_formats=['%I:%M %p'], allow_null=True)
    sun_open = serializers.TimeField(format='%I:%M %p', input_formats=['%I:%M %p'], allow_null=True)
    sun_close = serializers.TimeField(format='%I:%M %p', input_formats=['%I:%M %p'], allow_null=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class MenuItemESSerializer(serializers.Serializer):
    price_gram = serializers.FloatField()
    price_eighth = serializers.FloatField()
    price_quarter = serializers.FloatField()
    price_half = serializers.FloatField()
    in_stock = serializers.BooleanField()
    removed_date = serializers.DateTimeField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass