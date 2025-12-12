#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import os

import unittest
import json
import inspect
from mock import patch
from kombu import serialization
from adsputils import serializer
from adsmsg import BibRecord
from adsmsg.msg import Msg

class TestAdsOrcidCelery(unittest.TestCase):
    """
    Tests the JSON serializer of adsmsg protobufs
    """
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        serialization.register('adsmsg', *serializer.register_args)
    
    
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        serialization.unregister('adsmsg')
        
    
    def test_serializer(self):
        b = BibRecord(bibcode='bibcode')
        cls, data = b.dump()
        
        self.assertEqual('adsmsg.bibrecord.BibRecord', cls)
        if sys.version_info > (3,):
            test_data = b'\n\x07bibcode'
        else:
            test_data = '\n\x07bibcode'
        self.assertEqual(data, test_data) # let's hope the upstream adsmsg doesn't change impl...
        
        
        # dump using default 'json' serializer
        content_type, encoding, data = serialization.dumps(b)
        self.assertEqual('{"__adsmsg__": ["adsmsg.bibrecord.BibRecord", "CgdiaWJjb2Rl"]}',
                         data)
        
        # load using our deserializer
        o = serialization.loads(data, 'application/x-adsmsg', encoding)
        self.assertTrue(isinstance(o, BibRecord))
        self.assertEqual(o.bibcode, 'bibcode')

        
        # and arbitrarily nested objects should pose no difficulties
        test = [{'foo': b}, b, [[b]]]
        content_type, encoding, data = serialization.dumps(test)
        o = serialization.loads(data, 'application/x-adsmsg', encoding)
        
        for x in (o[0]['foo'], o[1], o[2][0][0]):
            self.assertTrue(isinstance(x, BibRecord))
            self.assertEqual(x.bibcode, "bibcode")


    def test_utf8(self):
        b = BibRecord(bibcode=u'\u01b5')
        ctype, enc, data = serialization.dumps(b)
        o = serialization.loads(data, 'application/x-adsmsg', 'utf-8')
        self.assertTrue(isinstance(o, BibRecord))
        self.assertEqual(o.bibcode, u'\u01b5')
        

if __name__ == '__main__':
    unittest.main()
