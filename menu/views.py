
from django.urls import reverse_lazy
from .models import MenuType
from .forms import MenuTypeForm
from user.permission import IsAdminMixin, SearchMixin
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    View,
    TemplateView,

)

from alice_menu.utils import DeleteMixin


class MenuTypeMixin(IsAdminMixin):
    model = MenuType
    form_class = MenuTypeForm
    paginate_by = 50    
    queryset = MenuType.objects.filter(status=True, is_deleted=False)
    success_url = reverse_lazy("menu_type_list")
    search_lookup_fields = [
        "title",
        "description",
    ]


class MenuTypeList(MenuTypeMixin, ListView):
    template_name = "menutype/menutype-list.html"
    queryset = MenuType.objects.filter(status=True, is_deleted=False)


class MenuTypeDetail(MenuTypeMixin, DetailView):
    template_name = "menutype/menutype-list.html"


class MenuTypeCreate(MenuTypeMixin, CreateView):
    template_name = "create.html"


class MenuTypeUpdate(MenuTypeMixin, UpdateView):
    template_name = "update.html"


class MenuTypeDelete(MenuTypeMixin, DeleteMixin, View):
    pass


from django.views.generic import ListView
from .models import Menu, MenuType
from itertools import chain
from django.db.models import Q


# class MenuList(ListView):
# class MenuList(ListView, IsAdminMixin):
# class MenuList(ListView):
#     template_name = "menu/menu_list.html"
#     context_object_name = "grouped_menus"  # Rename context variable

#     def get_queryset(self):
#         # Fetch all products with specific filters
#         queryset = Menu.objects.filter(status=True, is_deleted=False)
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
        
#         # Fetch all BudClass objects
#         budclasses = MenuType.objects.all()

#         # If a search query is provided, filter products based on the query
#         search_query = self.request.GET.get("q")
#         if search_query:
#             queryset = Menu.objects.filter(Q(title__icontains=search_query, status=True, is_deleted=False)|Q(budclass__title__icontains=search_query, status=True, is_deleted=False)|Q(category__title__icontains=search_query, status=True, is_deleted=False))
#             grouped_products = [(budclass.title, queryset.filter(budclass=budclass)) for budclass in budclasses]
#         else:
#             # Create a list of tuples with BudClass title and associated products
#             grouped_products = [(budclass.title, budclass.product_set.filter(status=True, is_deleted=False)) for budclass in budclasses]
        
#         # Pass the grouped products to the template
#         context[self.context_object_name] = grouped_products
        
#         return context


    
from .forms import MenuForm


class MenuMixin(IsAdminMixin):
    model = Menu
    form_class = MenuForm
    paginate_by = 50
    queryset = Menu.objects.filter(status=True, is_deleted=False)
    success_url = reverse_lazy("menu_list")
    search_lookup_fields = [
        "item_name",
        "description",
    ]

class MenuList(MenuMixin, ListView):
    template_name = "menu/menu-list.html"
    queryset = Menu.objects.filter(status=True, is_deleted=False)

class MenuDetail(MenuMixin, DetailView):
    template_name = "menu/menu-detail.html"


class MenuCreate(MenuMixin, CreateView):
    template_name = "menu/menu-create.html"


# class MenuUpdate(MenuMixin, UpdateView):
#     template_name = "menu/menu_update.html"

#     def form_valid(self, form):
#         updated_name = form.data.get('title')
#         menu_id = form.initial.get('id')
#         initial_name = form.initial.get('title')
#         # update_subledger_after_updating_menu(menu_id=menu_id, initial_name=initial_name, updated_name=updated_name)
#         return super().form_valid(form)

class MenuUpdate(MenuMixin, UpdateView):
    template_name = "update.html"
    

class MenuDelete(MenuMixin, DeleteMixin, View):
    pass

from django.conf import settings
from django.db import IntegrityError
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from openpyxl import load_workbook
from .models import Menu, MenuType
from urllib.parse import urlparse, urlunparse
import requests
from django.core.files.base import ContentFile

class MenuUpload(View):

    def post(self, request):
        file = request.FILES['file']
        wb = load_workbook(file)

        excel_data = list()
        # for sheet in wb.worksheets:
        #     for row in sheet.iter_rows():

        #         row_data = list()
        #         for cell in row:
        #             row_data.append(cell.value)
        #         excel_data.append(row_data)

        for sheet in wb.worksheets:
            for row_index, row in enumerate(sheet.iter_rows(), start=1):
                # Skip the first row (index 0) which contains column headers
                if row_index == 1:
                    continue

                row_data = list()
                for cell in row:
                    row_data.append(cell.value)
                excel_data.append(row_data)

        product_create_error = []
        for data in excel_data:
            if not all(data):
                continue
            title = data[0].strip()
            category_name = data[1].strip().lower()
            price = data[2]
            budclass_name = str(data[2]).strip() if isinstance(data[2], str) else str(data[2]) + " Shelf"
            description = str(data[4]).strip() if isinstance(data[4], str) else str(data[4])
            image = data[3]
            parsed_url = urlparse(str(image))
            image_without_query = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', '', ''))

            response = requests.get(image_without_query)

            if MenuType.objects.filter(title__iexact=category_name).exists():
                category = MenuType.objects.get(title__iexact=category_name)
            else:
                try:
                    category = MenuType.objects.create(title=category_name)
                except IntegrityError:
                    category = MenuType.objects.get(title__iexact=category_name)

            if response.status_code == 200:
                image_content = ContentFile(response.content)        
                product = Menu(
                    category=category,
                    title=title,
                    price=price,
                    description=description

                )
                # product.is_taxable = True if data[3].strip().lower() == "yes" else False  # Assuming the 4th column is for is_taxable
                product.image.save(f"{title}_image.png", image_content, save=True)
                try:
                    product.save()
                except Exception as e:
                    print(e)
                    product_create_error.append(product.title)
            else:
                print(f"Failed to download image from {image_without_query}")

        if product_create_error:
            messages.error(request, f"Error creating menus \n {product_create_error}", extra_tags='danger')
            return redirect(reverse_lazy('product_list'))

        messages.success(request, "Menus uploaded successfully", extra_tags='success')
        return redirect(reverse_lazy('menu_list'))
    
from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = "index.html"