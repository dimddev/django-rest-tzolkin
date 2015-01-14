# -*- coding: utf-8 -*-
from rest_framework import serializers


class TzolkinSerializer(serializers.Serializer):

    # pk = serializers.Field()
    long_count = serializers.CharField(required=True, max_length=14)
    haab = serializers.CharField(required=True, max_length=6)
    tzolkin = serializers.CharField(required=True, max_length=20)
    date = serializers.DateTimeField()

    def restore_object(self, attrs, instance=None):

        if instance:
            # Update existing instance
            instance.long_count = attrs.get('long_count', instance.long_count)
            instance.haab = attrs.get('haab', instance.haab)
            instance.tzlokin = attrs.get('tzolkin', instance.tzlokin)
            instance.date = attrs.get('date', instance.date)

            return instance

        # Create new instance
        return TzolkinSerializer(**attrs)
