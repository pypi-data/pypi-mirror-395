from rest_framework import serializers


class ActivitySerializer(serializers.ModelSerializer):
    """ """

    class Meta:
        fields = [
            "id",
        ]
