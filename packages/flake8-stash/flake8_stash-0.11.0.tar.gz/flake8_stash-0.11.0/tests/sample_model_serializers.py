import rest_framework
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ALL_FIELDS, ModelSerializer


class Mixin:
    pass


class Test1Serializer(Mixin, rest_framework.serializers.ModelSerializer):
    test_field = serializers.CharField()

    class Meta:
        model = User
        fields = ALL_FIELDS


class Test2Serializer(ModelSerializer):
    test_field = serializers.CharField()

    class Meta:
        """"""

        model = User
        fields = serializers.ALL_FIELDS


class Test3Serializer(ModelSerializer):
    test_field = serializers.CharField()

    class Meta:
        model = User
        exclude = ("password",)


class Test4Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class Test5Serializer(Test1Serializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name")


class Test6Serializer(Test1Serializer):
    class Meta:
        model = User
        fields = "__all__"
