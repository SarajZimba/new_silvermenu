from alice_menu.utils import BaseModel
from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.text import slugify
# Create your models here.

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
        

