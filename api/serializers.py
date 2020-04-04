from rest_framework import serializers
from api.models import User, Bank


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'email', 'first_name', 'last_name', 'password', 'dob', 'address', 'phone', 'code', 'post')
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


class BankSerializer(serializers.HyperlinkedModelSerializer):

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


class LocalitySerializer(serializers.HyperlinkedModelSerializer):
    pass


class AgencySerializer(serializers.HyperlinkedModelSerializer):
    pass


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    pass


class IndicatorSerializer(serializers.HyperlinkedModelSerializer):
    pass
