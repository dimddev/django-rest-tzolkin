# -*- coding: utf-8 -*-

import datetime
from calendar import *
from datetime import date
import re

from ...libs import Tools
from ...libs.haab import Haab
from ...libs.tzolkin import Tzolkin as TzolkinCalc


class Tzolkin2GregorianResult(object):

    def __init__(self):
        pass


class Tzolkin2GregorianProcessor(Tools):

    def __init__(self, *args, **kwargs):

        if 'long_count' in kwargs:
            self.setLongCount(kwargs['long_count'])
            kwargs['long_count'] = self.getLongCount()

        else:
            raise Exception('long_count parameter is not present')

        super(Tzolkin2GregorianProcessor, self).__init__(*args, **kwargs)

    def check_long_count_date(self, check_date):

        pattern = '^(\d{1,2}\.){1,4}(\d{1,2})$'
        result = re.match(pattern, check_date)

        if result is not None:
            return result.group()

        return False

    def setLongCount(self, long_count):

        if self.check_long_count_date(long_count):

            prepared_date = dict(list(zip(
                ['baktun', 'katun', 'tun', 'uinal', 'kin'],
                long_count.split('.'),
            )))

            long_count = Tzolkin2GregorianResult()
            long_count.baktun = prepared_date['baktun']
            long_count.katun = prepared_date['katun']
            long_count.tun = prepared_date['tun']
            long_count.uinal = prepared_date['uinal']
            long_count.kin = prepared_date['kin']

            self.__long_count = long_count

        else:
            raise Exception('Incorrect data format')

    def getLongCount(self):
        return self.__long_count

    def get_days_from_long_count(self):

        long_count = self.getLongCount()

        return self.maya_epoch + int(long_count.baktun) * 144000 + \
            int(long_count.katun) * 7200 + int(long_count.tun) * 360 + \
            int(long_count.uinal) * 20 + int(long_count.kin)

    def process(self):

        div = None

        step = datetime.timedelta(
            days=self.get_days_from_long_count()
        )

        result = self.getLongCount()

        result.long_count = '%s.%s.%s.%s.%s' % (
            result.baktun,
            result.katun,
            result.tun,
            result.uinal,
            result.kin
        )

        # return today
        if step.days == self.get_days_from_date(date.today()):

            result.gregorian = datetime.datetime.now()

            result.haab = Haab(
                long_count=result
            ).get_mayan_haab_from_date(result.gregorian)

            result.tzolkin = TzolkinCalc(
                long_count=result
            ).get_mayan_tzolkin_from_date(result.gregorian)

            result.gregorian = result.gregorian.date()

            return result

        # return our zero day 7.17.18.13.2
        if self.check_for_zero_day(self.getLongCount()) is True:
            raise Exception('supported date range: 0001-01-01 - xxxx-xx-xx')

        # return our first day 7.17.18.13.3 eg 0001-01-01
        if self.check_for_first_day(self.getLongCount()) is True:

            result.gregorian = datetime.datetime(1, 1, 1)

            result.haab = Haab(
                long_count=result
            ).get_mayan_haab_from_date(result.gregorian)

            result.tzolkin = TzolkinCalc(
                long_count=result
            ).get_mayan_tzolkin_from_date(result.gregorian)

            result.gregorian = result.gregorian.date()

            return result

        # past and futured date
        try:
            # if today > step

            if step != datetime.timedelta(days=0):

                isPast = True
                div = date.today() - step

                # yesterday fix
                if div.year == 1 and div.month == 1 and div.day == 1:
                    div -= datetime.timedelta(days=1)

        except OverflowError:

            # if today < step
            isPast = False
            step_plus = step.days - self.get_days_from_date(date.today())
            div = date.today() + datetime.timedelta(days=step_plus)

        if div is not None:

            try:
                days_in_past = self.get_days_from_date(div)
                #print 'past day %s' % days_in_past

            except Exception as e:
                raise Exception(e.message)

            if isPast:

                if self.get_days_from_date(datetime.datetime.now()) > days_in_past:
                    result.gregorian = datetime.datetime.now() - datetime.timedelta(days=days_in_past)

            else:
                result.gregorian = datetime.datetime.now() + datetime.timedelta(days=step_plus)

            try:
                result.haab = Haab(
                    long_count=result
                ).get_mayan_haab_from_date(result.gregorian)

                result.tzolkin = TzolkinCalc(
                    long_count=result
                ).get_mayan_tzolkin_from_date(result.gregorian)

                result.gregorian = result.gregorian.date()

                return result

            except Exception as e:
                raise Exception(e.message)

        else:
            raise Exception('div is none')
