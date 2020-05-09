from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework import viewsets, status
from rest_framework.response import Response
from api.models import User, Bank, Agency, Indicator, Locality, IndAgency, Category, CategoryValue
from rest_framework.decorators import APIView
from django.db.models import Prefetch, Q
import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Avg, Count, Sum
from api.serializers import UserSerializer, BankSerializer, AgencySerializer, CategorySerializer, IndAgencySerializer, \
    UserAgencySerializer, LocalitySerializer, BankMarketSerializer
from django.shortcuts import get_object_or_404
import pandas as pd
from django.http import HttpResponseForbidden
import json
from django.db.models.query import QuerySet

# Create your views here.
from api.view_model import BankMarketViewModel, Data_per_date


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BankViewSet(viewsets.ModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer


class RegisterUser(APIView):
    def post(self, request):
        serializer = UserSerializer(
            data=request.data, context={'request': request})
        data = {}
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors)


class AgenciesList(APIView):
    def get(self, request):
        agencies = Agency.objects.all()
        serializer = AgencySerializer(
            agencies, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegionList(APIView):
    def get(self, request):
        regions = Locality.objects.raw(
            'SELECT * FROM api_locality GROUP BY region')
        serializer = LocalitySerializer(
            regions, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class LocalityList(APIView):
    def get(self, request):
        localities = Locality.objects.all()
        serializer = LocalitySerializer(
            localities, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class getUserAgency(APIView):
    def get(self, request):
        email = request.data['email']
        user = get_object_or_404(User, email=email)
        if user.post == "Administrateur":
            agencies = Agency.objects.all()
            serializer = AgencySerializer(
                agencies, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif user.post == "da":
            return Response(UserSerializer(user, context={'request': request}).data['agency'],
                            status=status.HTTP_200_OK)
        else:
            agencies = Agency.objects.all()
            serializer = AgencySerializer(
                agencies, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)


def get_month_list(start, end):
    months = set()
    start_date = datetime.datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end, '%Y-%m-%d')

    if start_date > end_date:
        pass
    else:
        num_month = (end_date - start_date) // 30
        nb_loops = (num_month.days + 1)
        for x in range(1, nb_loops):
            month = start_date + relativedelta(months=x)
            month_format = datetime.datetime.strftime(month, '%Y-%m-%d')
            months.add(month_format)
    return months


def get_bank_market_qs(localityId, agencyId, categoryId):
    if localityId is None and agencyId is None and categoryId is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    locality_qs = Locality.objects.get(id=localityId)
    agency_qs = Agency.objects.select_related().filter(Q(locality=locality_qs))
    category_qs = Category.objects.get(pk=1)
    indicator_qs = Indicator.objects.select_related().filter(category__exact=category_qs)
    indicator_agency_qs = IndAgency.objects.select_related().filter(
        Q(agency__in=agency_qs) & Q(indicator__in=indicator_qs))

    return indicator_agency_qs


def avg(tableau):
    return sum(tableau, 0.0) / len(tableau)


def variance(tableau):
    m = avg(tableau)
    return avg([(x - m) ** 2 for x in tableau])


def ecart_type(tableau):
    return variance(tableau) ** 0.5


class Diagnostics(APIView):
    def post(self, request):
        start = request.data['from']
        end = request.data['to']
        localityId = request.data['localityId']
        agencyId = request.data['agencyId']
        categoryId = request.data['categoryId']
        results = list(BankMarketViewModel)
        banks = Bank.objects.all()
        responses = set()

        months_list = get_month_list(start, end)
        indicator_agency_qs = get_bank_market_qs(localityId, agencyId, categoryId)
        if indicator_agency_qs is None and months_list is None:
            return Response({'msg': "Indicators List is empty", 'success': False},
                            status=status.HTTP_204_NO_CONTENT)

        for bank in banks:
            data_per_dates = list(Data_per_date)
            bank_data = []
            bank_total = 0
            bank_indicators = indicator_agency_qs.filter(agency__bank__exact=bank)
            if bank_indicators is None:
                data_per_date = Data_per_date('No period', 0)
                result = BankMarketViewModel(id=bank.id, name=bank.name, total=0, rang=0, avg=0, ecart_type=0,
                                             data_per_date=data_per_date)
                results.add(result)
                continue

            for x in months_list:
                year = x[0:4]
                mont = x[5:7]
                final_qs = bank_indicators.filter(Q(date_operation__month__exact=int(mont)) &
                                                  Q(date_operation__year__exact=int(year)))
                if final_qs.count() == 0:
                    continue
                data_aggregate_per_bank = final_qs.values('bank__id', 'bank__name', 'bank__sigle') \
                    .order_by('bank__id') \
                    .annotate(total=Sum('data')) \
                    .first()
                bank_data.append(data_aggregate_per_bank.total)
                # bank_total += data_aggregate_per_bank.total
                data_per_date = Data_per_date(period=x, data=data_aggregate_per_bank.total)
                data_per_dates.add(data_per_date)

            # lenght = data_per_dates.count()
            # avg = bank_total / lenght
            bank_total = sum(bank_data)
            avg = avg(bank_data)
            ecart_type = ecart_type(bank_data)
            response = BankMarketViewModel(id=bank.id, name=bank.name, total=bank_total, avg=avg,
                                           ecart_type=ecart_type, data_per_date=data_per_dates)

            responses.add(response)

            data_avg_per_dates = list(Data_per_date)
            data_evol_per_dates = list(Data_per_date)
            data_afb_evol_per_dates = list(Data_per_date)
            data_evol_months = []
            data_afb_evol_months = []
            i = 0

        for x in months_list:

            year = x[0:4]
            mont = x[5:7]
            other_qs = bank_indicators.filter(Q(date_operation__month__exact=int(mont)) &
                                              Q(date_operation__year__exact=int(year)))

            if other_qs.count() == 0:
                continue
            data_aggregate_per_bank = other_qs.values('agency') \
                .order_by('agencyId') \
                .annotate(total=Sum('data')) \
                .first()

            data_evol_months.append(data_aggregate_per_bank.total)
            data_avg_per_date = Data_per_date(period=x, data=data_aggregate_per_bank.total)
            data_avg_per_dates.append(data_avg_per_date)
            if i > 0:
                diff = data_evol_months[i-1] - data_evol_months[i]
                data_evol_per_date = Data_per_date(period=x, data=diff)
                data_evol_per_dates.append(data_evol_per_date)

            afb_qs = other_qs.filter(bank__sigle__exact='AFB')
            if afb_qs.count() == 0:
                continue
            data_afb_aggregate_per_bank = other_qs.values('agency') \
                .order_by('agencyId') \
                .annotate(total=Sum('data')) \
                .first()
            data_afb_evol_months.append(data_afb_aggregate_per_bank.total)
            data_afb_per_date = Data_per_date(period=x, data=data_aggregate_per_bank.total)
            data_afb_evol_per_dates.append(data_per_date)
            if i > 0:
                diff_afb = data_afb_evol_months[i - 1] - data_evol_months[i]
                data_afb_evol_per_date = Data_per_date(period=x, data=diff_afb)
                data_afb_evol_per_dates.append(data_afb_evol_per_date)
            result_avg = BankMarketViewModel(id=0, name='Moyenne', data_per_date=data_avg_per_dates)
            result_evol = BankMarketViewModel(id=0, name='Evolution', data_per_date=data_evol_per_date)
            result_afb_evol = BankMarketViewModel(id=0, name='Evolution AFB', data_per_date=data_afb_evol_per_dates)
            responses.add(result_avg, result_evol, result_afb_evol)
        serializer = BankMarketSerializer(results, many=True)
        return Response({'data': serializer.data, 'msg': "Operation Ok", 'success': False}, status=status.HTTP_200_OK)




class Diagnostic_ressource_structuration(APIView):
    def post(self, request):
        start = request.data['from']
        end = request.data['to']
        localityId = request.data['localityId']
        agencyId = request.data['agencyId']

        if localityId is None and agencyId is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        locality_qs = Locality.objects.get(id=localityId)
        agency_qs = Agency.objects.select_related().filter(Q(locality=locality_qs))
        category_qs = Category.objects.get(pk=1)
        indicator_qs = Indicator.objects.select_related().filter(category__exact=category_qs)
        indicator_agency_qs = IndAgency.objects.select_related().filter(
            Q(agency__in=agency_qs) & Q(indicator__in=indicator_qs))
        months_list = get_month_list(start, end)
        results = list(BankMarketViewModel)
        print(months_list)
        for x in months_list:
            year = x[0:4]
            mont = x[5:7]
            final_qs = indicator_agency_qs.filter(Q(date_operation__month__exact=int(mont)) &
                                                  Q(date_operation__year__exact=int(year)))
            if final_qs.count() == 0:
                return Response({'msg': "Indicators List is empty", 'success': False},
                                status=status.HTTP_204_NO_CONTENT)
            data_aggregate_per_bank = final_qs.values('bank__id', 'bank__name', 'bank__sigle') \
                .order_by('bank__id') \
                .annotate(total=Sum('data'))

            for item in data_aggregate_per_bank:
                vm = BankMarketViewModel(id=item.bank__id, name=item.bank__name, total=item.total)
                results.add(vm)

            serializer = BankMarketSerializer(results, many=True)
        return Response({'data': serializer.data, 'msg': "Operation Ok", 'success': False}, status=status.HTTP_200_OK)

        # for x in months_list:
        #     year = x[0:4]
        #     mont = x[5:7]
        #     final_qs = indicator_agency_qs.filter(Q(date_operation__month__exact=int(mont)) &
        #                                           Q(date_operation__year__exact=int(year)))
        #     if final_qs.count() == 0:
        #         return Response({'msg': "Indicators List is empty", 'success': False},
        #                         status=status.HTTP_204_NO_CONTENT)
        #
        #     data_aggregate_per_bank = final_qs.values('bank__id', 'bank__name', 'bank__sigle') \
        #         .order_by('bank__id') \
        #         .annotate(total=Sum('data'))
        #
        #     for item in data_aggregate_per_bank:
        #         vm = BankMarketViewModel(id=item.bank__id, name=item.bank__name, total=item.total)
        #         results.add(vm)
        #
        #     serializer = BankMarketSerializer(results, many=True)
        # return Response({'data': serializer.data, 'msg': "Operation Ok", 'success': False}, status=status.HTTP_200_OK)

class Diagnostic_reemplois_structuration(APIView):
    pass


class Diagnostic_organisation_analyse_RH(APIView):
    pass


class Diagnostic_organisation_analyse_EQ(APIView):
    pass


class Diagnostic_organisation_analyse_ESP(APIView):
    pass


class Diagnostic_operation_guichet_AC(APIView):
    pass


class MarcheBancaire(APIView):
    def post(self, request):

        # get the range of the months and year
        # 2019-03-01
        start = request.data['from']

        # endYear, endMonth, endDate = request.data['to'].split('-')
        end = request.data['to']

        # get the locality Id
        localityId = request.data['localityId']
        # locality = Locality.objects.filter(id=localityId).values()

        # get the agency Id
        agencyId = request.data['agencyId']

        # Predifined indicators list depot for analyse du marche
        # IndicatorsId = ['Id1', 'Id2', 'Id3', 'Id4']
        # or categories ID for Marcher Bancaire
        categoriesId = ['1', '2']

        # Get the agency first, then all the indicators from the range within the month range.
        prefetch_qs = Indicator.objects.filter(
            category_id__in=categoriesId, date__gte=start, date__lte=end)
        AfbAgencies = Agency.objects.filter(
            id=agencyId).prefetch_related(Prefetch("indicators", queryset=prefetch_qs))
        serializer = AgencySerializer(
            AfbAgencies, many=True, context={'request': request})

        otherAgencies = Agency.objects.filter(
            locality_id=localityId).exclude(bank_id=1).prefetch_related(Prefetch("indicators", queryset=prefetch_qs))
        serializer2 = AgencySerializer(
            otherAgencies, many=True, context={'request': request})

        df = pd.DataFrame.from_records(
            serializer.data[0]['indicators'])

        for agency in serializer2.data:
            if agency['indicators']:
                df2 = pd.DataFrame.from_records(agency['indicators'])

        avgByMonthAFB = df.groupby(['date']).mean().groupby('date')[
            'value'].mean()
        ecartTypeAFB = df.groupby(['date'])['value'].std()
        avgByMonthAFB.loc["Total"] = avgByMonthAFB.sum()

        avgByMonthOthers = df2.groupby(['date']).mean().groupby('date')[
            'value'].mean()
        ecartTypeOthers = df2.groupby(['date'])['value'].std()
        avgByMonthOthers.loc["Total"] = avgByMonthOthers.sum()

        # frames = [df, df2]
        # result = pd.concat(frames)
        print(avgByMonthAFB)
        print(ecartTypeAFB)
        print(avgByMonthOthers)
        print(ecartTypeOthers)
        return Response((
            {'agencies AFB': serializer.data, 'avgByMonthAFB': avgByMonthAFB, 'ecartType AFB': ecartTypeAFB,
             'agenciesOthers': serializer2.data, 'avgByMonthOthers': avgByMonthOthers,
             'ecartTypeOthers': ecartTypeOthers}), status=status.HTTP_200_OK)
