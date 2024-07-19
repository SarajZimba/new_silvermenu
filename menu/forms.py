from django import forms

from .models import Menu, MenuType
from alice_menu.forms import BaseForm

class MenuTypeForm(BaseForm, forms.ModelForm):
    class Meta:
        model = MenuType
        fields = "__all__"
        exclude = [
            "is_deleted",
            "status",
            "deleted_at",
            "sorting_order",
            "slug",
            "is_featured",
        ]


class MenuForm(BaseForm, forms.ModelForm):
    # branch = forms.ModelChoiceField(queryset=Branch.objects.all(), required=False)
    # branch_quantity = forms.IntegerField(required=False)

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

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields["price"].label = "Selling Price"
    #     self.fields["category"].label = "StrainType"
    #     self.fields["description"].widget = forms.Textarea(attrs={"rows": 3, "class": "form-select"})

    #     if self.instance.id:
    #         # Show the 'reason' field when updating an existing product
    #         self.fields["reason"].widget = forms.Textarea(attrs={"rows": 3, "class": "form-select"})
    #     else:
    #         # Exclude the 'reason' field when creating a new product
    #         del self.fields["reason"]

    # def clean(self):
    #     cleaned_data = super().clean()

    #     is_taxable = cleaned_data.get('is_taxable')
    #     taxbracket = cleaned_data.get('taxbracket')

    #     if is_taxable == True:
    #         if taxbracket is None:
    #             raise forms.ValidationError("Taxable Products must have a taxbracket")

    #     return cleaned_data

    # def save(self, commit=True):
    #     product = super().save(commit=commit)
    #     if self.cleaned_data.get('branch') and self.cleaned_data.get('branch_quantity'):

    #         branch = self.cleaned_data['branch']
    #         branch_quantity = self.cleaned_data['branch_quantity']

    #         branch_stock = BranchStock(product=product, branch=branch, quantity=branch_quantity)
    #         branch_stock.save()

    #     return product