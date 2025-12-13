#!/usr/bin/env python

import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


setup(name='mars',
      version='0.0.1',
      description='An eventing framework.',
      maintainer='Mourad Mourafiq',
      maintainer_email='mourad@polyaxon.com',
      author='Mourad Mourafiq',
      author_email='mourad@polyaxon.com',
      url='https://github.com/polyaxon/polyaxon-cli',
      license='MIT',
      platforms='any',
      packages=find_packages(),
      keywords=[
          'mars',
          'events',
          'webhooks',
          'async',
          'aio',
          'hooks',
          'django',
          'flask',
          'web',
          'services'
      ],
      install_requires=[
          "hestia>=0.2.0",
      ],
      classifiers=[
          'Programming Language :: Python',
          'Operating System :: OS Independent',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: Artificial Intelligence'
      ],
      tests_require=['pytest'],
      cmdclass={'test': PyTest})
