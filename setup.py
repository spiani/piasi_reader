#!/usr/bin/env python

from distutils.core import setup

setup(name='piasi_reader',
      version='0.9.3',
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
