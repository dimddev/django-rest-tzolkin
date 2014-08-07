# -*- coding: utf-8 -*-


class TzolkinProcessor(object):

    __processor = False

    def __init__(self, *args, **kwargs):

        if 'processor' in kwargs:
            self.__processor = kwargs['processor']

        else:
            raise Exception('processor keyword is not defined')

        super(TzolkinProcessor, self).__init__()

    def get(self):

        try:
            return self.__processor.process()

        except Exception as e:
            raise Exception(e.message)