from abc import ABC

from rest_framework import serializers
from api.models import User, Bank, Agency, Indicator, IndAgency, Category, UserAgency, Locality


class BankSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bank
        fields = ('url', 'id', 'name', 'sigle', 'code')

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.code = validated_data.get('code', instance.code)
        instance.sigle = validated_data.get('sigle', instance.sigle)
        instance.name = validated_data.get('name', instance.name)
        instance.baseUpdate(self)
        instance.save()

        return instance

    def create(self, validated_data):
        bank = Bank(**validated_data)
        bank.baseCreate(self)
        bank.save()
        return bank


class LocalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Locality
        fields = '__all__'


class IndAgencySerializer(serializers.ModelSerializer):

    class Meta:
        model = IndAgency
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'code', 'description', 'tutel', 'isActive')


class IndicatorSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Indicator
        fields = '__all__'
        # fields = ('name', 'code', 'description',
        #           'role', 'category', 'isActive', 'type_value', 'datee', 'value')


class AgencySerializer(serializers.ModelSerializer):
    indicators = IndicatorSerializer(many=True, read_only=True)

    class Meta:
        model = Agency
        fields = ('name', 'code', 'indicators', 'isActive')
        depth = 1


class UserAgencySerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAgency
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    agency = AgencySerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'first_name', 'last_name',
                  'password', 'dob', 'address', 'phone', 'code', 'post', 'agency')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance


class Data_per_dateSerializer(serializers.Serializer):
    period = serializers.CharField(200)
    data = serializers.IntegerField()


class BankMarketSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=200)
    total = serializers.IntegerField()
    rang = serializers.IntegerField()
    avg = serializers.FloatField()
    ecart_type = serializers.FloatField()
    data_per_date = Data_per_dateSerializer(required=True)




