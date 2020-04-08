# from rest_auth.app_settings import serializers
#
# from api.models import Category, CategoryValue, Indicator, Bank, Locality, Agency, IndAgency
#
#
# class BankSerializer(serializers.Serializer):
#     class Meta:
#         model = Bank
#         fields = ('name', 'code', 'sigle')
#
#
# class LocalitySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Locality
#         fields = ('name', 'code', 'region', 'country')
#
#
# class CategorySerializer(serializers.ModelSerializer):
#     # tutel = CategorySerializer(many=True, required=False)
#
#     class Meta:
#         model = Category
#         fields = ('name', 'code', 'description', 'tutel')
#
#
# class CategoryValueSerializer(serializers.ModelSerializer):
#     categoryId = CategorySerializer(many=False, required=True)
#
#     class Meta:
#         model = CategoryValue
#         fields = ('name', 'code', 'categoryId')
#
#
# class IndicatorSerializer(serializers.ModelSerializer):
#     categoryId = CategorySerializer(many=False, required=True)
#
#     class Meta:
#         model = Indicator
#         fields = ('name', 'code', 'description', 'role', 'categoryId')
#
#
# class AgencySerializer(serializers.ModelSerializer):
#     indicators = IndicatorSerializer(many=True, required=True)
#     bankId = IndicatorSerializer(many=False, required=True)
#     localityId = IndicatorSerializer(many=False, required=True)
#
#     class Meta:
#         model = Agency
#         fields = ('name', 'code', 'indicators', 'bankId', 'localityId')
#
#
# class IndAgencySerializer(serializers.ModelSerializer):
#     agencyId = AgencySerializer(many=False, required=True)
#     indicatorId = IndicatorSerializer(many=False, required=True)
#
#     class Meta:
#         model = IndAgency
#         fields = ('data', 'type_value', 'date', 'agencyId', 'indicatorId')
#
