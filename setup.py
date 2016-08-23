#!/usr/bin/env python

from distutils.core import setup

from __version import version

version_str = '{}.{}.{}'.format(version[0], version[1], version[2])

setup(name='piasi_reader',
      version=version_str,
      description='A library to read the native IASI L1C files',
      author='Stefano Piani',
      author_email='stefano.piani@exact-lab.it',
      package_dir={'piasi_reader': ''},
      packages=['piasi_reader', 'piasi_reader.records'],
      classifiers=[
          'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          ]
     )
