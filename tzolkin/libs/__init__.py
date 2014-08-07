# -*- coding: utf-8 -*-
import datetime
from calendar import isleap


class Tools(object):

    __long_count = False

    # The starting epoch of the long count, according to the Goodman-Martinez-Thompson correlation,
    # is taken as Monday, August 11, −3113 (Gregorian). This date equals September 6, 3114 B.C.E. (Julian),
    # which was (at noon) JD 584,283, that is, R.D. −1,137,142
    maya_epoch = -1137142

    months = [
        31, 28, 31,
        30, 31, 30,
        31, 31, 30,
        31, 30, 31
    ]

    def __init__(self, *args, **kwargs):

        super(Tools, self).__init__()

        if 'long_count' in kwargs:
            # print 'in Tools %s' % kwargs['long_count']
            self.__long_count = kwargs['long_count']

    def check_for_zero_day(self, long_count=None):

        long_count = long_count or self.__long_count

        try:
            if int(long_count.baktun) == 7 and \
                int(long_count.katun) == 17 and \
                int(long_count.tun) == 18 and \
                int(long_count.uinal) == 13 and \
                int(long_count.kin) == 2:
                    return True

            else:

                return False
        except Exception as e:
            raise Exception(e.message)

    def check_for_first_day(self, long_count=None):

        long_count = long_count or self.__long_count

        try:

            if int(long_count.baktun) == 7 and \
                int(long_count.katun) == 17 and \
                int(long_count.tun) == 18 and \
                int(long_count.uinal) == 13 and \
                int(long_count.kin) == 3:

                    return True
            else:
                return False

        except Exception as e:
            raise Exception(e.message)

    def check_for_leap_year(self, year):
        return isleap(year)

    def get_days_from_date(self, div):

        days = 0

        if div is None or div is False:
            raise Exception('incorrect paramenter div: %s' % div)

        while(div.year > 0):
            # stop loop
            if div.year == 1 and div.month == 1 and div.day == 1:
                return days or days + 1

            if not self.check_for_leap_year(div.year):

                try:

                    div -= datetime.timedelta(days=sum(self.months))
                    days += sum(self.months)
                    #print (('N - %s' % div))

                except OverflowError:

                    month_days = sum(self.months[0:div.month - 1])
                    total = month_days + div.day
                    div -= datetime.timedelta(days=total - 1)
                    days += total

            else:
                days += sum(self.months) + 1
                try:
                    div -= datetime.timedelta(days=sum(self.months) + 1)
                    #print (('L - %s' % div))

                except OverflowError as e:
                    raise Exception(e.message)