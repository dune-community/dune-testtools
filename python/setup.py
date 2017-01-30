#!/usr/bin/env python

import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


def dune_testtools_scripts():
    return ['./scripts/dune_metaini_analysis.py',
            './scripts/dune_expand_metaini.py',
            './scripts/dune_extract_static.py',
            './scripts/dune_has_static_section.py',
            './wrapper/dune_convergencetest.py',
            './wrapper/dune_execute.py',
            './wrapper/dune_execute_parallel.py',
            './wrapper/dune_vtkcompare.py',
            './wrapper/dune_outputtreecompare.py']


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(name='dune.testtools',
      version='2.4',
      namespace_packages=['dune'],
      description='Python testtools for systemtesting in Dune',
      author='Dominic Kempf <dominic.kempf@iwr.uni-heidelberg.de>, Timo Koch <timo.koch@iws.uni-stuttgart.de>',
      author_email='no_mailinglist_yet@dune-testtools.de',
      url='http://conan2.iwr.uni-heidelberg.de/git/quality/dune-testtools',
      packages=['dune.testtools', 'dune.testtools.wrapper'],
      install_requires=['dune.common', 'pyparsing>=2.1.10', 'six>=1.4.1'],
      tests_require=['pytest'],
      cmdclass={'test': PyTest},
      scripts=dune_testtools_scripts())
