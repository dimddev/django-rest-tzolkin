# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from django.conf import settings
#from django.views.generic import TemplateView

############################################


############################################

# client
from tzolkin.urls import tzolkin_urls

urlpatterns = patterns('',

    url(r'^API', include(tzolkin_urls)),

)

############################################

