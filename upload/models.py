from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=1000)
    photo = models.CharField(max_length=1000)
    parent = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True, blank=True)
    url = models.CharField(max_length=200)


class Urls(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    url = models.CharField(max_length=500)
    done = models.BooleanField(default=False)


class Product(models.Model):
    title = models.CharField(max_length=1000)
    price = models.CharField(max_length=1000)
    vendor_code = models.CharField(max_length=50)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    images = models.CharField(max_length=200)
    company = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    manufacturer_logo = models.CharField(max_length=300, null=True, blank=True)
    manufacturer_code = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField()
