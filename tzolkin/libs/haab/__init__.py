# -*- coding: utf-8 -*-
from ...libs import Tools


class Haab(Tools):

    haab_months = [
        'POP', 'WO', 'SIP', 'SOTZ',
        'SEK', 'XUL', 'YAXKIN', 'MOL',
        'CH\'EN', 'YAK', 'SAK', 'KEH', 'MAK',
        'KANKIN', 'MUWAN', 'PAX', 'KAYAB',
        'KUMKU', 'WAYEB'
    ]

    def __init__(self, *args, **kwargs):

        super(Haab, self).__init__(*args, **kwargs)

    def __get_mayan_haab_ordinar(self, month, day):
        return (month - 1) * 20 + day

    def __get_mayan_haab_epoch(self):
        return self.maya_epoch - self.__get_mayan_haab_ordinar(18, 8)

    def get_mayan_haab_from_date(self, indate):

        count = (self.get_days_from_date(indate) - self.__get_mayan_haab_epoch()) % 365

        day = count % 20
        month = (count / 20)

        return self.haab_months[month], day
