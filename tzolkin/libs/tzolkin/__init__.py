# -*- coding: utf-8 -*-
#from base.apps.shared.tzolkin1.libs import Tools
from ...libs import Tools


class Tzolkin(Tools):

    sels = {

        'maya_name': (

            'IMIX', 'IK', 'AKBAL', 'KAN',
            'CHICCHAN', 'CIMI', 'MANIK', 'LAMAT',
            'MULAC', 'OC', 'CHUEN', 'EB',
            'BEN', 'IX', 'MEN', 'CIB',
            'CABAN', 'ETZNAB', 'CAUAC', 'AHAU'

        ),

        'eng_name': (

            'Dragon', 'Wind', 'Night', 'Seed',
            'Serpent', 'World brigder', 'Hand', 'Star',
            'Moon', 'Dog', 'Monkey', 'Human',
            'Sky walker', 'Wizard', 'Eagel', 'Warrior',
            'Earth', 'Mirror', 'Storm', 'Sun'

        ),
    }

    __lang = 'maya'

    def __init__(self, *args, **kwargs):

        super(Tzolkin, self).__init__(*args, **kwargs)

        if 'lang' in kwargs:
            self.__lang = kwargs['lang']

    def __get_mayan_tzolkin_ordinar(self, tone, seal):
        return (tone - 1 + 39 * (tone - seal)) % 260

    def __get_mayan_tzolkin_epoch(self):
        return self.maya_epoch - self.__get_mayan_tzolkin_ordinar(4, 20)

    def __amod(self, x, y):
        return (y + x % (-y))

    def get_mayan_tzolkin_from_date(self, indate):

        count = self.get_days_from_date(indate) - self.__get_mayan_tzolkin_epoch() + 1
        tone = self.__amod(count, 13)
        seal = self.__amod(count, 20)

        if self.__lang == 'maya':
            return tone, self.sels['maya_name'][seal - 1]

        elif self.__lang == 'eng':
            return tone, self.sels['eng_name'][seal - 1]
