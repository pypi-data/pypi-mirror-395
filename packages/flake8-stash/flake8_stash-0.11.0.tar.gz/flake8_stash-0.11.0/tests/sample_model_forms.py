from django import forms
from django.contrib.auth.models import User
from django.forms import ALL_FIELDS, ModelForm


class Mixin:
    pass


class Test1Form(Mixin, forms.models.ModelForm):
    test_field = forms.CharField()

    class Meta:
        model = User
        fields = ALL_FIELDS


class Test2Form(ModelForm):
    test_field = forms.CharField()

    class Meta:
        """"""

        model = User
        fields = forms.ALL_FIELDS


class Test3Form(ModelForm):
    test_field = forms.CharField()

    class Meta:
        model = User
        exclude = ("password",)


class Test4Form(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"


class Test5Form(Test1Form):
    pass


class Test6Form(Test1Form):
    class Meta:
        model = User
        exclude = ("first_name",)
