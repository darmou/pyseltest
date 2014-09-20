# Copyright 2014 Andrew Magee.
# Distributed under the GPL v3 licence: http://www.gnu.org/licenses/gpl-3.0.html

"""
This file is part of pyseltest.

pyseltest is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyseltest is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pyseltest.  If not, see <http://www.gnu.org/licenses/>.
"""

from setuptools import setup

setup(
    name='pyseltest',
    version='0.1',
    description='Py.test Selenium helpers',
    url='http://bitbucket.org/amagee/pyseltest',
    author='Andrew Magee',
    author_email='amagee@gmail.com',
    license='GPL v3',
    packages=['pyseltest'],
    zip_safe=False
)
