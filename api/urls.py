from django.conf.urls import url, include
from rest_framework import routers
from api.views import UserViewSet, BankViewSet, AgenciesList, MarcheBancaire, getUserAgency, RegisterUser, RegionList, LocalityList, Diagnostics

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'banks', BankViewSet)

#  this is a list of url to manage authentication
# /login/ [name='login']
# /logout/ [name='logout']
# /password_change/ [name='password_change']
# /password_change/done/ [name='password_change_done']
# /password_reset/ [name='password_reset']
# /password_reset/done/ [name='password_reset_done']
# /reset/<uidb64>/<token>/ [name='password_reset_confirm']
# /reset/done/ [name='password_reset_complete']

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_auth.urls')),
    url(r'^register/', RegisterUser.as_view()),
    url(r'^agencies/', AgenciesList.as_view()),
    url(r'^regions/', RegionList.as_view()),
    url(r'^localites/', LocalityList.as_view()),
    url(r'^user/agency/', getUserAgency.as_view()),
    url(r'^marche-bancaire/', MarcheBancaire.as_view()),
    url(r'^diagnostique/', Diagnostics.as_view()),
]
