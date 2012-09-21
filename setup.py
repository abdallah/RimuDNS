#!/usr/bin/env python
# -*- encoding: utf-8 -*-
__author__ = "Abdallah Deeb <abdallah@deeb.me>"
import os
from setuptools import setup, find_packages
NAME = "rimudns"
GITHUB_URL = "https://github.com/abdallah/%s" % (NAME)
DESCRIPTION = "Python interface to RimuHosting/Zonomi DNS "

VERSION = "0.0.0"


def read(fname):
    full_path = os.path.join(os.path.dirname(__file__), fname)
    if os.path.exists(fname):
        return open(full_path).read()
    else:
        return ""

try:
    from rimudns.consts import VERSION
except ImportError:
    for line in read('rimudns/consts.py').split('\n'):
        if line.startswith('VERSION'):
            VERSION = \
                line.split('=')[1].replace('"', '').replace("'", '').strip()
requirements = []

setup(name=NAME,
      version=VERSION,
      download_url="%s/zipball/%s" % (GITHUB_URL, VERSION),
      description=DESCRIPTION,
      install_requires=requirements,
      author='Abdallah Deeb',
      author_email='abdallah@deeb.me',
      url=GITHUB_URL,
      long_description=read('README.md'),
      license='GPLv3',
      include_package_data=True,
      zip_safe=False,
      packages=find_packages(exclude=['tests', 'debian']),
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Distributed Computing',
        'Topic :: Utilities',
        ],
      )