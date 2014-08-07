# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from ...processor import TzolkinProcessor
from ...libs.gregorian2tzolkin import *
from ...serializers import TzolkinSerializer


class Gregorian2Tzolkin(APIView):

    """
    Covert gregorian date in formats '%Y/%m/%d', '%Y%m%d', '%Y-%m-%d' to Longcount, Haab, and Tzolkin
    """
    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):

        if 'date' in request.QUERY_PARAMS:

            try:

                long_count = TzolkinProcessor(
                    processor=Gregorian2TzolkinProcessor(
                        gregorian=request.QUERY_PARAMS.get('date')
                    )
                ).get()

                return Response(TzolkinSerializer({
                    'long_count': long_count.long_count,
                    'haab': long_count.haab,
                    'tzolkin': long_count.tzolkin,
                    'date': long_count.gregorian
                }).data)

            except Exception as e:
                return Response(
                    {'APIError': e.message},
                )
        else:

            return Response(
                {'APIError': 'Ivalid date format'},
            )