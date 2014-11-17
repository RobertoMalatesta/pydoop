# BEGIN_COPYRIGHT
#
# Copyright 2009-2014 CRS4.
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

import unittest
import itertools as it
import os
import tempfile
import shutil

from pydoop.mapreduce.streams import ProtocolError
from pydoop.mapreduce.binary_streams import BinaryDownStreamFilter
from pydoop.mapreduce.binary_streams import BinaryWriter
from pydoop.mapreduce.binary_streams import BinaryUpStreamFilter
from pydoop.mapreduce.binary_streams import BinaryUpStreamDecoder

from pydoop.test_utils import WDTestCase


STREAM_1 = [
    ('start', 0),
    ('setJobConf', ('key1', 'value1', 'key2', 'value2')),
    ('setInputTypes', 'key_type', 'value_type'),
    ('runMap', 'input_split', 3, False),
    ('mapItem', 'key1', 'val1'),
    ('mapItem', 'key1', 'val2'),
    ('mapItem', 'key2', 'val3'),
    ('runReduce', 0, False),
    ('reduceKey', 'key1'),
    ('reduceValue', 'val1'),
    ('reduceValue', 'val2'),
    ('reduceKey', 'key2'),
    ('reduceValue', 'val3'),
    ('close',),
    ]

STREAM_2 = [
    ('status',  'I am ok'),
    ('registerCounter', 1 , 'group', 'name'),
    ('incrementCounter', 1 , 289189289),
    ('progress', 0.5),
    ('output', 'key1', 'value1'),
    ('output', 'key2', 'value2'),
    ('output', 'key3', 'value3'),
    ('output', 'key4', 'value4'),
    ('status',  'I am still ok'),    
    ('done',),
    ]


current_dir = os.path.dirname(__file__)

MAP_JAVA_DOWNLINK_DATA=os.path.join(current_dir, 'data/mapper_downlink.data')
RED_JAVA_DOWNLINK_DATA=os.path.join(current_dir, 'data/reducer_downlink.data')


def stream_writer(fname, data):
    with open(fname, 'w') as f:
        bw = BinaryWriter(f)
        for vals in data:
            cmd, args = vals[0], vals[1:]
            bw.send(vals[0], *args)

class TestBinaryStream(WDTestCase):

    def test_downlink(self):
        fname = self._mkfn('foo.bin')
        stream_writer(fname, STREAM_1)
        with open(fname, 'r') as f:
            stream = BinaryDownStreamFilter(f)
            try:
                for (cmd, args), vals in it.izip(stream, STREAM_1):
                    self.assertEqual(cmd, vals[0])
                    self.assertTrue((len(vals) == 1 and not args)
                                    or (vals[1:] == args))
            except ProtocolError as e:
                print 'error -- %s' % e

    def test_on_java_downlink_data(self):
        wd = tempfile.mkdtemp(prefix='pydoop_')
        map_cmd_out = os.path.join(wd, 'mapper_cmd.txt')
        red_cmd_out = os.path.join(wd, 'reducer_cmd.txt')
        def decode(istream, ostream):
            cmd_stream = BinaryDownStreamFilter(istream)
            for (cmd, args) in cmd_stream:
                ostream.write('cmd: {}, args: {}\n'.format(cmd, args))
        try:
            for i, o in ((MAP_JAVA_DOWNLINK_DATA, map_cmd_out),
                         (RED_JAVA_DOWNLINK_DATA, red_cmd_out)):
                with open(i, 'r') as f:
                    with open(o, 'w') as w:
                        decode(f, w)
        finally:
            shutil.rmtree(wd)

    def test_uplink(self):
        fname = self._mkfn('foo.bin')
        with open(fname, 'w') as f:
            w = BinaryUpStreamFilter(f)
            for vals in STREAM_2:
                cmd, args = vals[0], vals[1:]
                print cmd, args
                w.send(cmd, *args)
        with open(fname, 'r') as f:
            cmd_stream = BinaryUpStreamDecoder(f)
            for (cmd, args), vals in it.izip(cmd_stream, STREAM_2):
                self.assertEqual(cmd, vals[0])
                self.assertTrue((len(vals) == 1 and not args)
                                    or (vals[1:] == args))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestBinaryStream('test_downlink'))
    suite.addTest(TestBinaryStream('test_on_java_downlink_data'))
    suite.addTest(TestBinaryStream('test_uplink'))    
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run((suite()))