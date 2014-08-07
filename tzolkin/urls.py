# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from .views import Gregorian2Tzolkin
from .views import Tzolkin2Gregorian

urlpatterns = patterns('',
    url(r'^/v1/ancient/calendars/mayan/gregorian2tzolkin', Gregorian2Tzolkin.as_view(), name='api-gregorian2tzolkin'),
    url(r'^/v1/ancient/calendars/mayan/tzolkin2gregorian', Tzolkin2Gregorian.as_view(), name='api-tzolkin2gregorian')
)
