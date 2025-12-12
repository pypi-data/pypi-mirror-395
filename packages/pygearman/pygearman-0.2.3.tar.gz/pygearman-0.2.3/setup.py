#!/usr/bin/env python

import os

from setuptools import setup


def local_file(name):
    return os.path.relpath(os.path.join(os.path.dirname(__file__), name))


SOURCE = local_file('gearman')
README = local_file('README.rst')


# Assignment to placate pyflakes. The actual version is from the exec that
# follows.
__version__ = None

with open(local_file('gearman/version.py')) as o:
    exec(o.read())

assert __version__ is not None


setup(
    name = 'pygearman',
    version = __version__,
    author = 'nerou GmbH',
    author_email = 'info@nerou.de',
    description = 'A Python 3 fork of the Gearman API - Client, worker, and admin client interfaces',
    long_description=open(README).read(),
    url = 'https://github.com/nerou42/pygearman',
    packages = ['gearman'],
    license='Apache / MIT',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
