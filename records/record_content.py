"""
Piasi-reader: a library to read and convert the native IASI L1C files
Copyright (C) 2015  Stefano Piani

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 3.0 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
"""

from sys import version_info

# Get python major version
py_version = int(version_info[0])

if py_version < 3:
    class uninterpreted_content(str):
        @property
        def interpreted(self):
            return False

        @property
        def raw(self):
            return self
else:
    class uninterpreted_content(bytes):
        @property
        def interpreted(self):
            return False

        @property
        def raw(self):
            return self

class interpreted_content(object):
    @property
    def interpreted(self):
        return True

    @property
    def raw(self):
        raise NotImplementedError
