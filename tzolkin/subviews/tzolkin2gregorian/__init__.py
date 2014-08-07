# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from ...processor import TzolkinProcessor
from ...libs.tzolkin2gregorian import *
from ...serializers import TzolkinSerializer


class Tzolkin2Gregorian(APIView):

    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):

        if 'date' in request.QUERY_PARAMS:

            try:

                result_date = TzolkinProcessor(
                    processor=Tzolkin2GregorianProcessor(
                        long_count=request.QUERY_PARAMS.get('date')
                    )
                ).get()

                if result_date.gregorian is False or result_date.gregorian is None:

                    return Response(
                        {'APIError': 'Ivalid date format or invalid date'},
                    )

                return Response(TzolkinSerializer({

                    'long_count': result_date.long_count,
                    'haab': result_date.haab,
                    'tzolkin': result_date.tzolkin,
                    'date': result_date.gregorian

                }).data)

            except Exception as e:

                return Response(
                    {'APIError': e.message},
                )

        else:

            return Response(
                {'APIError': 'Ivalid date format'},
            )
