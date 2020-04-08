from django.conf.urls import url, include
from .views import IndAgencyView

urlpatterns = [
    url('data/', IndAgencyView.as_view()),
]