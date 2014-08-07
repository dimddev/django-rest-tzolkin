# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
import datetime
#from rest_framework import status
#from django.utils import unittest
from django.test import SimpleTestCase
from django.test.client import Client

from .libs import Tools
from .libs.haab import Haab
from .libs.tzolkin import Tzolkin
from .libs.tzolkin2gregorian import Tzolkin2GregorianProcessor
from .libs.gregorian2tzolkin import Gregorian2TzolkinProcessor


class TzolkinToolsTests(SimpleTestCase):

    tzolkin_date = [
        '13.0.0.0.0',
        '7.17.18.15.3',
        '7.17.18.14.15',
        '13.0.1.10.0'
    ]

    zero_date = ['7.17.18.13.2']
    first_date = '7.17.18.13.3'

    # check Tools methods
    def __check_for_non_zero_day(self, long_count):
        tgp = Tzolkin2GregorianProcessor(long_count=long_count)
        tools = Tools()
        self.assertFalse(tools.check_for_zero_day(long_count=tgp.getLongCount()), False)

    def test_check_for_zero_day_result_false(self):
        for tz in self.tzolkin_date:
            self.__check_for_non_zero_day(tz)

    def __check_for_zero_day(self, long_count):
        tgp = Tzolkin2GregorianProcessor(long_count=long_count)
        tools = Tools()
        self.assertTrue(tools.check_for_zero_day(long_count=tgp.getLongCount()), True)

    def test_check_for_zero_day_result_true(self):
        for tz in self.zero_date:
            self.__check_for_zero_day(tz)

    def __check_for_first_day(self, first_day):
        tgp = Tzolkin2GregorianProcessor(long_count=first_day)
        tools = Tools()
        self.assertTrue(tools.check_for_first_day(long_count=tgp.getLongCount()), True)

    def test_check_for_first_day_result_true(self):
        self.__check_for_first_day(self.first_date)

    def test_check_for_zero_day_all_result_true(self):
        tgp = Tzolkin2GregorianProcessor(long_count=self.zero_date[0])
        self.assertTrue(tgp.check_for_zero_day(), True)

    def test_check_for_zero_day_all_result_false(self):
        tgp = Tzolkin2GregorianProcessor(long_count=self.first_date)
        self.assertFalse(tgp.check_for_zero_day(), False)

    def test_check_for_first_day_all_result_true(self):
        tgp = Tzolkin2GregorianProcessor(long_count=self.first_date)
        self.assertTrue(tgp.check_for_first_day(), True)

    def test_check_for_first_day_all_result_false(self):
        tgp = Tzolkin2GregorianProcessor(long_count=self.zero_date[0])
        self.assertFalse(tgp.check_for_first_day(), False)

    def test_check_for_leap_year(self):
        tools = Tools()
        self.assertTrue(tools.check_for_leap_year(2012), True)
        self.assertFalse(tools.check_for_leap_year(2013), False)

    def test_get_days_from_date_first_day(self):
        tools = Tools()
        self.assertEqual(tools.get_days_from_date(datetime.datetime(1, 1, 1)), 1)

    def test_get_days_from_date_20121221(self):
        tools = Tools()
        self.assertEqual(tools.get_days_from_date(datetime.datetime(2012, 12, 21)), 734858)

    def test_get_days_from_date_40221221(self):
        tools = Tools()
        self.assertEqual(tools.get_days_from_date(datetime.datetime(4022, 12, 21)), 1468995)


class TzolkinHaabTests(SimpleTestCase):

    def __test_get_mayan_haab_from_long(self, check_date, result):
        tgp = Tzolkin2GregorianProcessor(long_count=check_date)
        result = tgp.process()
        haab = Haab(long_count=result)
        self.assertEqual(haab.get_mayan_haab_from_date(result.gregorian), result.haab)

    def test_get_mayan_haab_from_date_13_0_0_0_0(self):
        check_date = '13.0.0.0.0'
        result = ('KANKIN', 3)
        self.__test_get_mayan_haab_from_long(check_date, result)

    def test_get_mayan_haab_from_date_7_17_18_13_3(self):
        check_date = '7.17.18.13.3'
        result = ('MOL', 11)
        self.__test_get_mayan_haab_from_long(check_date, result)

    def test_get_mayan_haab_from_date_13_10_13_10_13(self):
        check_date = '13.10.13.10.13'
        result = ('MOL', 1)
        self.__test_get_mayan_haab_from_long(check_date, result)

    def __test_get_mayan_haab_from_date(self, check_dates, result):

        for check_date in check_dates:
            tgp = Gregorian2TzolkinProcessor(gregorian=check_date)
            result = tgp.process()
            haab = Haab(long_count=result)
            self.assertEqual(haab.get_mayan_haab_from_date(result.gregorian), result.haab)

    def test_get_mayan_haab_from_date_20121221(self):
        check_dates = ['20121221', '2012/12/21', '2012-12-21']
        result = ('KANKIN', 3)
        self.__test_get_mayan_haab_from_date(check_dates, result)

    def test_get_mayan_haab_from_date_00010101(self):
        check_dates = ['00010101', '0001/01/01', '0001-01-01']
        result = ('MOL', 1)
        self.__test_get_mayan_haab_from_date(check_dates, result)


class TzolkinTzolkinTests(SimpleTestCase):

    def __test_get_mayan_tzolkin_from_long(self, check_date, check_result):

        tgp = Tzolkin2GregorianProcessor(long_count=check_date)
        result = tgp.process()
        tz = Tzolkin(long_count=result)
        self.assertEqual(tz.get_mayan_tzolkin_from_date(result.gregorian), check_result)

    def __test_get_mayan_tzolkin_from_date(self, check_date, check_result):

        tgp = Gregorian2TzolkinProcessor(gregorian=check_date)
        result = tgp.process()
        tz = Tzolkin(long_count=result)
        self.assertEqual(tz.get_mayan_tzolkin_from_date(result.gregorian), check_result)

    def test_get_mayan_tzolkin_from_date_13_0_0_0_0(self):

        check_date = '13.0.0.0.0'
        result = (4, 'AHAU')
        self.__test_get_mayan_tzolkin_from_long(check_date, result)

    def test_get_mayan_tzolkin_from_date_7_17_18_13_3(self):

        check_date = '7.17.18.13.3'
        result = (11, 'AKBAL')
        self.__test_get_mayan_tzolkin_from_long(check_date, result)

    def test_get_mayan_haab_from_date_13_10_13_10_13(self):
        check_date = '13.10.13.10.13'
        result = (2, 'BEN')
        self.__test_get_mayan_tzolkin_from_long(check_date, result)

    def test_get_mayan_tzolkin_from_date_20121221(self):

        check_date = '20121221'
        result = (4, 'AHAU')
        self.__test_get_mayan_tzolkin_from_date(check_date, result)

    def test_get_mayan_tzolkin_from_date_00010101(self):

        check_date = '00010101'
        result = (11, 'AKBAL')
        self.__test_get_mayan_tzolkin_from_date(check_date, result)

    def test_get_mayan_haab_from_date_22230702(self):
        check_date = '22230702'
        result = (2, 'BEN')
        self.__test_get_mayan_tzolkin_from_date(check_date, result)


class TzolkinRestAPIConfig():

    # define some test values

    ####################################

    first_day_long = {'date': '7.17.18.13.3'}

    first_day_result_long = {
        "long_count": "7.17.18.13.3",
        "haab": ["MOL", 11],
        "tzolkin": [11, "AKBAL"],
        "date": "0001-01-01"
    }

    ####################################

    end_of_baktun_long = {'date': '13.0.0.0.0'}

    end_of_baktun_result_long = {
        "long_count": "13.0.0.0.0",
        "haab": ["KANKIN", 3],
        "tzolkin": [4, "AHAU"],
        "date": "2012-12-21"
    }

    ####################################

    future_day_long = {'date': '13.10.13.10.13'}

    future_day_result_long = {
        "long_count": "13.10.13.10.13",
        "haab": ["MOL", 1],
        "tzolkin": [2, "BEN"],
        "date": "2223-07-02"
    }

    # gregorian

    ####################################

    first_day_gregorian = {'date': '00010101'}

    first_day_gregorian_result = {
        "long_count": "7.17.18.13.3",
        "haab": ["MOL", 11],
        "tzolkin": [11, "AKBAL"],
        "date": "0001-01-01"
    }

    ####################################

    end_of_baktun_gregorian = {'date': '20121221'}

    end_of_baktun_result_gregorian = {
        "long_count": "13.0.0.0.0",
        "haab": ["KANKIN", 3],
        "tzolkin": [4, "AHAU"],
        "date": "2012-12-21"
    }

    ####################################

    future_day_gregorian = {'date': '2223-7-2'}

    future_day_result_gregorian = {
        "long_count": "13.10.13.10.13",
        "haab": ["MOL", 1],
        "tzolkin": [2, "BEN"],
        "date": "2223-07-02"
    }


class Tzolkin2GregorianRestAPITests(SimpleTestCase, TzolkinRestAPIConfig):

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
    
    def __test_tzolkin2gregorian(self, query, result):

        url = reverse('api-tzolkin2gregorian')
        response = self.client.get(url, query, format='json')
        response.data['date'] = str(response.data['date'])

        self.assertEqual(response.data, result)

    def test_tzolkin2gregorian_71718133(self):

        self.__test_tzolkin2gregorian(
            self.first_day_long,
            self.first_day_result_long
        )

    def test_tzolkin2gregorian_1300000(self):

        self.__test_tzolkin2gregorian(
            self.end_of_baktun_long,
            self.end_of_baktun_result_long
        )

    def test_tzolkin2gregorian_1310131013(self):

        self.__test_tzolkin2gregorian(
            self.future_day_long,
            self.future_day_result_long
        )


class Gregorian2TzolkinRestAPITests(SimpleTestCase, TzolkinRestAPIConfig):

    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def __test_gregorian2tzolkin(self, query, result):

        url = reverse('api-gregorian2tzolkin')
        response = self.client.get(url, query, format='json')
        response.data['date'] = str(response.data['date'])
        self.assertEqual(response.data, result)

    def test_gregorian2tzolkin_00010101(self):

        self.__test_gregorian2tzolkin(
            self.first_day_gregorian,
            self.first_day_gregorian_result
        )

    def test_gregorian2tzolkin_20121221(self):

        self.__test_gregorian2tzolkin(
            self.end_of_baktun_gregorian,
            self.end_of_baktun_result_gregorian
        )

    def test_gregorian2tzolkin_22230702(self):

        self.__test_gregorian2tzolkin(
            self.future_day_gregorian,
            self.future_day_result_gregorian
        )


class CombineRestAPITests(SimpleTestCase, TzolkinRestAPIConfig):

    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_tzolkin2gregorian(self):
        url = reverse('api-tzolkin2gregorian')
        url1 = reverse('api-gregorian2tzolkin')
        tzolkin = self.client.get(url, self.future_day_long, format='json')
        gregor = self.client.get(url1, {'date': tzolkin.data['date']}, format='json')
        self.assertEqual(tzolkin.data, gregor.data)

    def test_gregorian2tzolkin(self):
        url = reverse('api-tzolkin2gregorian')
        url1 = reverse('api-gregorian2tzolkin')
        gregor = self.client.get(url1, {'date': '20121221'}, format='json')
        tzolkin = self.client.get(url, {'date': gregor.data['long_count']}, format='json')
        self.assertEqual(tzolkin.data, gregor.data)
