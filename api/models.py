from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db import models
from datetime import date


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
        return "{}".format(self.sigle)

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
        return self.name

    # def __init__(self):
    #     BaseEntity.__init__(self)


class Category(BaseEntity):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)

    parent = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='children', null=True)

    class Meta:
        verbose_name = "api_category"
        ordering = ['code']

    def __str__(self):
        return self.name

    # def __init__(self):
    #     BaseEntity.__init__(self)


class CategoryValue(BaseEntity):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)

    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='categoriesvalue', default=None, null=True)

    class Meta:
        verbose_name = "api_category_value"
        ordering = ['code']

    def __str__(self):
        return self.name

    # def __init__(self):
    #     BaseEntity.__init__(self)


class Indicator(BaseEntity):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    description = models.TextField(max_length=1000, default='-')
    role = models.TextField(max_length=1000, default='-')
    type_value = models.CharField(max_length=50, default='int')
    date = models.DateField(default=date.today)
    value = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='indicators', null=True)

    class Meta:
        verbose_name = "api_indicator"
        ordering = ['code']

    def __str__(self):
        return self.name


class Agency(BaseEntity):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)

    indicators = models.ManyToManyField(Indicator, through='IndAgency', related_name='agency')
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='agency', null=True)
    locality = models.ForeignKey(Locality, on_delete=models.CASCADE, related_name='agency', null=True)

    class Meta:
        verbose_name = "api_agency"
        ordering = ['id']

    def __str__(self):
        return self.name

    # def __init__(self):
    #     BaseEntity.__init__(self)


class IndAgency(BaseEntity):
    data = models.IntegerField()
    type_value = models.CharField(max_length=50)
    date_operation = models.DateField(default=date.today)

    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='indicagency', null=True)
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE, related_name='indicagency', null=True)

    REQUIRED_FIELDS = ['data', 'date', 'agency_id', 'indicator_id']

    class Meta:
        verbose_name = "api_ind_agency"
        ordering = ['date_operation']

    def __str__(self):
        return self.type_value

    # def __init__(self):
    #     BaseEntity.__init__(self)


class User(AbstractUser):
    username = models.CharField(blank=True, null=True, max_length=50)
    email = models.EmailField(_('email address'), unique=True)
    dob = models.DateField(null=True)
    address = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=50, null=True)
    code = models.CharField(max_length=5, null=True)
    post = models.CharField(max_length=100, null=True)

    agency = models.ManyToManyField(Agency, through='UserAgency', related_name='user')

    USERNAME_FIELD = 'email' or 'username'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = "api_user"
        ordering = ['username']

    def __str__(self):
        return "{}".format(self.email)


class UserAgency(BaseEntity):

    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='useragency')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='useragency')

    class Meta:
        verbose_name = "api_user_agency"
        ordering = ['agency']

    def __str__(self):
        return self.agency.name

    # def __init__(self):
    #     BaseEntity.__init__(self)
