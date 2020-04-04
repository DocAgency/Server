from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db import models


# Create your models here.

class BaseEntity(models.Model):
    createBy = models.CharField(max_length=50)
    updateBy = models.CharField(max_length=50)
    createAt = models.DateTimeField(max_length=50)
    updateAt = models.DateTimeField(max_length=50)
    isActive = models.BooleanField(max_length=50)

    class Meta:
        abstract = True

    def baseUpdate(self, userId="1", isActive=True):
        self.updateAt = datetime.now()
        self.updateBy = userId
        self.isActive = isActive

    def baseCreate(self, userId="1", isActive=True):
        self.createAt = datetime.now()
        self.updateAt = datetime.now()
        self.updateBy = userId
        self.isActive = isActive


class Bank(BaseEntity):
    name = models.CharField(max_length=50)
    sigle = models.CharField(max_length=50)
    code = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "api_bank"
        ordering = ['name']

    def __str__(self):
        return "{}".format(self.siglep)

    # def __str__(self):
    #     return {self.sigle, self.name, self.code}

    # def __init__(self):
    #     BaseEntity.__init__(self)


class Locality(BaseEntity):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    class Meta:
        verbose_name = "api_locality"
        ordering = ['code']

    def __str__(self):
        return {self.name, self.code, self.region}

    def __init__(self):
        BaseEntity.__init__(self)


class Agency(BaseEntity):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)

    bankId = models.ForeignKey(Bank, on_delete=models.DO_NOTHING)
    localityId = models.ForeignKey(Locality, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "api_agency"
        ordering = ['code']

    def __str__(self):
        return {self.name, self.code, self.bank, self.locality}

    def __init__(self):
        BaseEntity.__init__(self)


class Category(BaseEntity):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)

    tutel = models.ForeignKey('Category', on_delete=models.DO_NOTHING, related_name='tutelId')

    class Meta:
        verbose_name = "api_category"
        ordering = ['code']

    def __str__(self):
        return [self.name, self.code, self.description, self.tutel]

    def __init__(self):
        BaseEntity.__init__(self)


class CategoryValue(BaseEntity):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)

    categoryId = models.ForeignKey(Category, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "api_category_value"
        ordering = ['code']

    def __str__(self):
        return {self.name, self.code, self.category}

    def __init__(self):
        BaseEntity.__init__(self)


class Indicator(BaseEntity):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    role = models.TextField(max_length=1000)

    categoryId = models.ForeignKey(Category, on_delete=models.DO_NOTHING, )

    class Meta:
        verbose_name = "api_indicator"
        ordering = ['code']

    def __str__(self):
        return {self.name, self.code, self.description, self.role, self.category}


class IndAgency(BaseEntity):
    data = models.IntegerField()
    type_value = models.CharField(max_length=50)
    date = models.DateTimeField(default=datetime.now)

    agencyId = models.ForeignKey(Agency, on_delete=models.DO_NOTHING, )
    indicatorId = models.ForeignKey(Indicator, on_delete=models.DO_NOTHING, )

    REQUIRED_FIELDS = ['data', 'date', 'agencyId', 'indicatorId']

    class Meta:
        verbose_name = "api_ind_agency"
        ordering = ['date']

    def __str__(self):
        return {self.date, self.data, self.type_value, self.agencyId, self.indicatorId}

    def __init__(self):
        BaseEntity.__init__(self)


class User(AbstractUser):
    username = models.CharField(blank=True, null=True, max_length=50)
    email = models.EmailField(_('email address'), unique=True)
    dob = models.DateField(null=True)
    address = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=50, null=True)
    code = models.CharField(max_length=5, null=True)
    post = models.CharField(max_length=100, null=True)

    USERNAME_FIELD = 'email' or 'username'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = "api_user"
        ordering = ['username']

    def __str__(self):
        return "{}".format(self.email)


class UserAgency(BaseEntity):
    agencyId = models.ForeignKey(Agency, on_delete=models.DO_NOTHING, )
    userId = models.ForeignKey(User, on_delete=models.DO_NOTHING, )

    class Meta:
        verbose_name = "api_user_agency"
        ordering = ['agencyId']

    def __str__(self):
        return self.agency

    def __init__(self):
        BaseEntity.__init__(self)
