#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
from setuptools import setup, find_packages


def get_version(package):
    '''
    Return package version as listed in `__version__` in `init.py`.
    '''
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search(
        '^__version__ = [\'"]([^\'"]+)[\'"]', init_py, re.MULTILINE
    ).group(1)


version = get_version('base/apps/tzolkin')


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    args = {'version': version}
    print('You probably want to also tag the version now:')
    print(' git tag -a release/{version} -m \'version {version}\''.format(
        **args))
    print(' git push --tags')
    sys.exit()


setup(
    name='djangorestframework-tzolkin',
    version=version,
    url='http://github.com/dimddev/django-rest-framework-tzolkin',
    license='BSD',
    description='Long Count, Haab and Tzolkin support for Django REST framework',
    author='Dim Mitar Hakini',
    author_email='dmhakini@gmail.com',
    packages=find_packages(),
    install_requires=open('requirements.txt').read().split('\n'),
    test_suite='runtests.runtests',
    classifiers=[
        'Development Status :: 1 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP'
    ]
)
