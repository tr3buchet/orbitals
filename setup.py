#!/usr/bin/python
#
# Copyright 2012 Trey Morris
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import os
from setuptools import setup, find_packages
#from orbitals import orbitals


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='orbitals',
#    version=orbitals.__version__,
    author='Trey Morris',
    author_email='trey@treymorris.com',
    description='gevent threaded test runner using novaclient and supernova',
    long_description=read('README'),
    install_requires=['python-novaclient', 'supernova', 'gevent'],
    packages=find_packages(),
    url='https://github.com/tr3buchet/orbitals',
    entry_points={
        'console_scripts': [
            'orbitals = orbitals.executable:run_orbitals']})

#from setuptools import setup
#from orbitals import orbitals
#
#
#setup(
#    name='orbitals',
#    author='Trey Morris',
#    author_email='treyemorris@gmail.com',
#    description='threaded test runner using python-novaclient and supernova',
#    install_requires=['keyring'],
#    packages=['orbitals'],
#    url='https://github.com/tr3buchet/orbitals',
#    entry_points={
#        'console_scripts': [
#            'orbitals = orbitals.executable:run_orbitals'],
#        }
#    )
