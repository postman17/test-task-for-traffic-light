from rest_framework import serializers

from accounts.models import (
    Client,
    AdditionalPhone,
    AdditionalEmail,
    SocialNetwork,
    Url,
    Department,
)


class AdditionalPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalPhone
        fields = ('phone',)


class AdditionalEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalEmail
        fields = ('email',)


class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = ('url',)


class SocialNetworkSerializer(serializers.ModelSerializer):
    vk = UrlSerializer(many=True)
    fb = UrlSerializer(many=True)

    class Meta:
        model = SocialNetwork
        fields = (
            'vk',
            'fb',
            'ok',
            'instagram',
            'telegram',
            'whatsapp',
            'viber',
        )


class ClientSerializer(serializers.ModelSerializer):
    additional_phones = AdditionalPhoneSerializer(many=True)
    additional_emails = AdditionalEmailSerializer(many=True)
    social_networks = SocialNetworkSerializer()

    class Meta:
        model = Client
        fields = (
            'id',
            'username',
            'phone',
            'first_name',
            'last_name',
            'middle_name',
            'created_at',
            'updated_at',
            'status_changed_at',
            'is_active',
            'type',
            'gender',
            'timezone',
            'additional_phones',
            'additional_emails',
            'social_networks',
        )


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name', 'children')

    def get_fields(self):
        fields = super().get_fields()
        fields['children'] = DepartmentSerializer(many=True)
        return fields
