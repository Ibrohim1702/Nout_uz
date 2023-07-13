from django.db import models

# Create your models here.
from django.utils.text import slugify


class Log(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    messages = models.JSONField(default={"state": 0})

    def __str__(self):
        return self.user_id


class TgUser(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=56, null=True)
    first_name = models.CharField(max_length=128, null=True)
    name = models.CharField(max_length=128, null=True)
    # last_name = models.CharField(max_length=128, null=True)
    phone_number = models.CharField(max_length=15, null=True)
    til = models.CharField(max_length=20, null=True)

    def __str__(self):
        return f"{self.user_id} {self.username} {self.name}"


class Category(models.Model):
    content = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)

    def __str__(self):
        return self.content


class Brands(models.Model):
    content = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)

    def __str__(self):
        return self.content


class Product(models.Model):
    name = models.CharField(max_length=128, null=True, blank=True)
    img = models.ImageField()
    manitor = models.CharField(max_length=128, null=True, blank=True)
    cpu = models.CharField(max_length=128, null=True, blank=True)
    gpu = models.CharField(max_length=128, null=True, blank=True)
    ram = models.CharField(max_length=128, null=True, blank=True)
    hard = models.CharField(max_length=128, null=True, blank=True)
    price = models.CharField(max_length=128)
    ctg = models.ForeignKey(Category, models.SET_NULL, null=True)
    brds = models.ForeignKey(Brands, models.SET_NULL, null=True)
    short_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Savat(models.Model):
    user_id = models.BigIntegerField()
    slug = models.SlugField(max_length=128, null=True)
    product = models.CharField(max_length=256)
    amount = models.IntegerField(null=True)
    priceproduct = models.CharField(max_length=128, null=True)
    summ = models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product)

        return super(Savat, self).save(*args, **kwargs)

    def __str__(self):
        return self.product
