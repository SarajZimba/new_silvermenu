from alice_menu.utils import BaseModel
from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.text import slugify
# Create your models here.

class MenuType(BaseModel):
    title = models.CharField(max_length=255, verbose_name="MenuType Title", unique=True)
    slug = models.SlugField(verbose_name="MenuType Slug", null=True)
    description = models.TextField(
        verbose_name="MenuType Description", null=True, blank=True
    )
    def __str__(self):
        return self.title

class Menu(BaseModel):
    # item_name, group, type, price, d_exempt, restaurant/outlet, image, is_promotional, is_today-special
    item_name = models.CharField(max_length=255)
    slug = models.SlugField(verbose_name="Product Slug", null=True)
    group = models.CharField(max_length=255)   
    type = models.CharField(max_length=255)
    price = models.FloatField(default=0.0)
    outlet = models.CharField(max_length=255)
    discount_exempt = models.BooleanField(default=False)
    is_promotional = models.BooleanField(default=False)
    is_todayspecial = models.BooleanField(default=False)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    image_bytes = models.TextField(null=True, blank=True)
    menutype = models.ForeignKey(
        MenuType, on_delete=models.CASCADE, null=True, blank=True
    )
    description =models.TextField(null=True, blank=True)
    
    rating_choices = (
        (0.0, '0.0'),
        (0.5, '0.5'),
        (1.0, '1'),
        (1.5, '1.5'),
        (2.0, '2'),
        (2.5, '2.5'),
        (3.0, '3'),
        (3.5, '3.5'),
        (4.0, '4'),
        (4.5, '4.5'),
        (5.0, '5'),
    )
    rating = models.DecimalField(max_digits=2, decimal_places=1, choices=rating_choices, default=0.0, null=True, blank=True)
    promotional_price = models.FloatField(default=0.0)


    def save(self, *args, **kwargs):
        self.thumbnail = self.generate_thumbnail()

        #This is to generate the slug for sending it in the api
        self.slug = slugify(self.item_name)


        super().save(*args, **kwargs)

    def generate_thumbnail(self, thumbnail_size=(100, 100)):
        if self.thumbnail:
            image = Image.open(self.thumbnail)
            image.thumbnail(thumbnail_size)
            thumbnail_io = BytesIO()
            image.save(thumbnail_io, format='PNG')
            thumbnail_file = InMemoryUploadedFile(thumbnail_io, None, self.thumbnail.name.split('.')[0] + '_thumbnail.jpg', 'image/jpeg', thumbnail_io.tell(), None)
            thumbnail_file.seek(0)
            return thumbnail_file
        else:
            return None
        

class FlagMenu(models.Model):
    use_same_menu_for_multiple_outlet = models.BooleanField(default=True)
    autoaccept_order = models.BooleanField(default=False)

class Organization(BaseModel):
    loyalty_percentage = models.FloatField(default=0.0)
