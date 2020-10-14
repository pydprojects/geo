from rest_framework import serializers

from .models import Balance


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = '__all__'

    def create(self, validated_data):
        user_id = validated_data.get('user_id')
        points = validated_data.get('points')
        description = validated_data.get('description')

        balance = Balance.objects.create(user_id=user_id, points=points, description=description)

        return balance
