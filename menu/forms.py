from django import forms

from .models import Menu, MenuType
from alice_menu.forms import BaseForm



class MenuForm(BaseForm, forms.ModelForm):

    class Meta:
        model = Menu
        fields = "__all__"
        exclude = [
            "is_deleted",
            "status",
            "deleted_at",
            "sorting_order",
            "slug",
            "is_featured",
        ]


class MenuTypeForm(BaseForm, forms.ModelForm):

    class Meta:
        model = MenuType
        fields = "__all__"
        exclude = [
            "is_deleted",
            "deleted_at",
            "sorting_order",
            "slug",
            "is_featured",
        ]

from menu.models import Organization

class OrganizationForm(BaseForm, forms.ModelForm):
    class Meta:
        model = Organization
        fields = '__all__'
        exclude = [
            "is_deleted",
            "deleted_at",
            "sorting_order",
            "slug",
            "is_featured"
        ]
        
