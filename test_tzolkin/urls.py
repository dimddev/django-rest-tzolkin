# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include

urlpatterns = patterns('',

    url(r'^API', include('tzolkin.urls')),

)

