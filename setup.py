#! /usr/bin/env python

DESCRIPTION = "Probabilistic Programming Forecasting for COVID-19 Cases"
LONG_DESCRIPTION = """\
Coronacast provides a simple interface for performing time-series forecasting
for COVID-19 cases using bayesian models.
"""

DISTNAME = 'Coronacaster'
MAINTAINER = 'Mikko Kotila'
MAINTAINER_EMAIL = 'mailme@mikkokotila.com'
URL = 'http://autonom.io'
LICENSE = 'MIT'
DOWNLOAD_URL = 'https://github.com/autonomio/coronacast/'
VERSION = '0.0.1'

try:
    from setuptools import setup
    _has_setuptools = True
except ImportError:
    from distutils.core import setup

install_requires = ['pymc3',
                    'matplotlib',
                    'pandas',
                    'numpy']

if __name__ == "__main__":

    setup(name=DISTNAME,
          author=MAINTAINER,
          author_email=MAINTAINER_EMAIL,
          maintainer=MAINTAINER,
          maintainer_email=MAINTAINER_EMAIL,
          description=DESCRIPTION,
          long_description=LONG_DESCRIPTION,
          license=LICENSE,
          url=URL,
          version=VERSION,
          download_url=DOWNLOAD_URL,
          install_requires=install_requires,
          packages=['coronacaster'],

          classifiers=['Intended Audience :: Science/Research',
                       'Programming Language :: Python :: 3.6',
                       'Programming Language :: Python :: 3.7',
                       'Programming Language :: Python :: 3.8',
                       'License :: OSI Approved :: MIT License',
                       'Topic :: Scientific/Engineering :: Human Machine Interfaces',
                       'Topic :: Scientific/Engineering :: Mathematics',
                       'Operating System :: POSIX',
                       'Operating System :: Unix',
                       'Operating System :: MacOS',
                       'Operating System :: Microsoft :: Windows :: Windows 10'])