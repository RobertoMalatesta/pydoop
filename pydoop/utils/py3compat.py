# BEGIN_COPYRIGHT
#
# Copyright 2009-2016 CRS4.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# END_COPYRIGHT


# flake8: noqa

import sys

_is_py3 = sys.version_info[0] == 3


def __identity(x):
    return x


def __chr(x):
    return chr(x)


def __iteritems_2(x):
    return x.iteritems()


def __iteritems_3(x):
    return x.items()

def __parser_read_2(parser, f):
    parser.readfp(f)
    
def __parser_read_3(parser, f):
    parser.read_file(f)

if _is_py3:
    from io import BytesIO as StringIO
    import configparser
    import pickle
    clong = int
    #  something that should be interpreted as a string
    basestring = str
    unicode = str
    parser_read = __parser_read_3
    xchr = __identity
    czip = zip
    cmap = map
    cfilter = filter
    iteritems = __iteritems_3
else:
    from itertools import izip as czip
    from itertools import imap as cmap
    from itertools import ifilter as cfilter
    from cStringIO import StringIO
    import cPickle as pickle
    import ConfigParser as configparser
    parser_read = __parser_read_2    
    #  something that should be interpreted as a string
    basestring = unicode
    unicode = unicode
    clong = long
    xchr = __chr
    iteritems = __iteritems_2

