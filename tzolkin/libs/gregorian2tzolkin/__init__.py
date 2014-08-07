# -*- coding: utf-8 -*-

import datetime
from calendar import *

from ...libs import Tools
from ...libs.haab import Haab
from ...libs.tzolkin import Tzolkin as TzolkinCalc


class Gregorian2TzolkinResult(object):

    def __init__(self):
        pass


class Gregorian2TzolkinProcessor(Tools):

    __gregorian = False

    allowed_date_format = ['%Y/%m/%d', '%Y%m%d', '%Y-%m-%d']

    def __init__(self, *args, **kwargs):

        super(Gregorian2TzolkinProcessor, self).__init__(*args, **kwargs)

        if 'gregorian' in kwargs:
            self.setGregorian(kwargs['gregorian'])

    def setGregorian(self, indate):

        for allowed_format in self.allowed_date_format:

            try:

                calc_date = datetime.datetime.strptime(
                    indate,
                    allowed_format
                ).date()

                self.__gregorian = calc_date

            except Exception:
                pass

        if self.__gregorian is False:
            raise Exception('Invalid input format: %s' % indate)

    def getGregorian(self):
        return self.__gregorian

    def gregorian2tzolkin(self):

        long_count = int(self.get_days_from_date(self.getGregorian())) - self.maya_epoch
        baktun = long_count / 144000
        day_of_baktun = long_count % 144000
        katun = day_of_baktun / 7200
        day_of_katun = day_of_baktun % 7200
        tun = day_of_katun / 360
        day_of_tun = day_of_katun % 360
        uinal = day_of_tun / 20
        kin = day_of_tun % 20

        return baktun, katun, tun, uinal, kin

    def process(self):

        result = Gregorian2TzolkinResult()
        result.baktun, result.katun, result.tun, result.uinal, result.kin = self.gregorian2tzolkin()
        result.gregorian = self.getGregorian()

        try:

            result.long_count = '%d.%d.%d.%d.%d' % (
                result.baktun,
                result.katun,
                result.tun,
                result.uinal,
                result.kin
            )

            result.haab = Haab(
                long_count=result
            ).get_mayan_haab_from_date(self.getGregorian())

            result.tzolkin = TzolkinCalc(
                long_count=result
            ).get_mayan_tzolkin_from_date(self.getGregorian())

            return result

        except Exception as e:

            raise Exception(e.message)
