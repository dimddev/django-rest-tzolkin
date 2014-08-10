=============================

Django Rest API for convert Mesoamerican Long Count calendar `<http://en.wikipedia.org/wiki/Mesoamerican_Long_Count_calendar>`_ 
to Gregorian `<http://en.wikipedia.org/wiki/Gregorian_calendar>`_ dates

Installation
------------

Install using ``pip``:

.. code-block:: bash

    $ pip install django-rest-tzolkin

...or clone the project from github:

.. code-block:: bash

    $ git clone https://github.com/dimddev/django-rest-tzolkin

Django and Django-Rest-Framework are required packages


Config
------

put url(r'^API', include('tzolkin.urls')) into your urls.py

start/ or restart your test server

Usage
-----

Tzolkin2Gregorian Converter means that will convert long count date in format baktun.katun.tun.uinal.kin (13.0.0.0.0) to gregorian date 2012-12-21 (Y-m-d)
 
example url and long count:
http://your_test_ip/API/v1/ancient/calendars/mayan/tzolkin2gregorian?date=13.0.0.0.0
JSON result

Gregorian2Tzolkin Converter means that will convert gregorian date 2012-12-21 (Y-m-d) (supported formats are Y/m/d, Y-m-d, Ymd) to Long count 13.0.0.0.0,
includind Haab date and of course The Tzolkin or Sacred Mayan Calendar


example url and gregorian date in format Ymd
http://your_test_ip/API/v1/ancient/calendars/mayan/gregorian2tzolkin?date=20011012
JSON result

So that's all, have fun with The Tzolkin or Sacred Mayan Calendar : )
