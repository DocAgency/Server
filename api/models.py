from django.db import models
from django.utils import timezone


# Create your models here.
class Bank(models.Model):
    name = models.CharField(max_length=50)
    sigle = models.CharField(max_length=50)
    code = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "article"
        ordering = ['name']

    def __str__(self):
        return self.sigle

class Locality(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    region = models.CharField(max_length=50)

    class Meta:
        verbose_name = "locality"
        ordering = ['code']

    def __str__(self):
        return self.name



class Agency(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)

    bank = models.ForeignKey(Bank, on_delete=models.DO_NOTHING)
    locality = models.ForeignKey(Locality, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "agency"
        ordering = ['code']

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)

    tutel = models.ForeignKey('Category', on_delete=models.DO_NOTHING, related_name = 'tutelId')

    class Meta:
        verbose_name = "category"
        ordering = ['code']

    def __str__(self):
        return self.name


class CategoryValue(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)

    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "category_value"
        ordering = ['code']

    def __str__(self):
        return self.name




class Indicator(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    role = models.TextField(max_length=1000)

    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING,)

    class Meta:
        verbose_name = "indicator"
        ordering = ['code']

    def __str__(self):
        return self.name


class IndicAgency(models.Model):
    data = models.IntegerField(max_length=50)
    type_value = models.CharField(max_length=50)
    date = models.DateTimeField(default=timezone.now)

    agency = models.ForeignKey(Agency, on_delete=models.DO_NOTHING,)
    indicator = models.ForeignKey(Indicator, on_delete=models.DO_NOTHING,)

    class Meta:
        verbose_name = "indic_agency"
        ordering = ['date']

    def __str__(self):
        return self.value


class User(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    userName = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    post = models.TextField(max_length=100)
    password = models.TextField(max_length=100)

    class Meta:
        verbose_name = "user"
        ordering = ['post']

    def __str__(self):
        return self.userName


class UserAgency(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.DO_NOTHING,)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING,)

    class Meta:
        verbose_name = "user_agency"
        ordering = ['agency']

    def __str__(self):
        return self.agency


