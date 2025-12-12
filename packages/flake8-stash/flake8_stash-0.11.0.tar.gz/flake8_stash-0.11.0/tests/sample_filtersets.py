from django.contrib.auth.models import User
from django_filters import constants, rest_framework as filters
from django_filters.constants import ALL_FIELDS
from django_filters.rest_framework import FilterSet


class Mixin:
    pass


class Test1FilterSet(Mixin, filters.FilterSet):
    test_field = filters.CharFilter()

    class Meta:
        model = User
        fields = ALL_FIELDS


class Test2FilterSet(FilterSet):
    test_field = filters.CharFilter()

    class Meta:
        """"""

        model = User
        fields = constants.ALL_FIELDS


class Test3FilterSet(FilterSet):
    test_field = filters.CharFilter()

    class Meta:
        model = User
        exclude = ("password",)


class Test4FilterSet(filters.FilterSet):
    class Meta:
        model = User
        fields = "__all__"


class Test5FilterSet(Test1FilterSet):
    class Meta:
        model = User
        fields = ("first_name", "last_name")


class Test6FilterSet(Test1FilterSet):
    pass
