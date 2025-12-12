#!/usr/bin/env python
# -*- coding: utf-8 -*-


from builtins import str
import sys
import os

import unittest
import json
import inspect
from mock import patch
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa
import adsputils

class TestAdsOrcidCelery(unittest.TestCase):
    """
    Tests the appliction's methods
    """
    def setUp(self):
        unittest.TestCase.setUp(self)


    def tearDown(self):
        unittest.TestCase.tearDown(self)


    def test_load_config(self):
        with patch('adsputils.load_module') as load_module:
            c = adsputils.load_config()
            f = os.path.abspath(os.path.join(os.path.dirname(inspect.getsourcefile(adsputils)), '..'))
            self.assertEqual((f + '/config.py',),
                              load_module.call_args_list[0][0])
            self.assertEqual((f + '/local_config.py',),
                              load_module.call_args_list[1][0])
            self.assertEqual(c['PROJ_HOME'], f)

        with patch('adsputils.load_module') as load_module:
            adsputils.load_config('/tmp')
            self.assertEqual(('/tmp/config.py',),
                              load_module.call_args_list[0][0])
            self.assertEqual(('/tmp/local_config.py',),
                              load_module.call_args_list[1][0])


    def test_load_module(self):
        f = os.path.abspath(os.path.join(os.path.dirname(inspect.getsourcefile(adsputils)), './tests/config_sample.py'))
        x = adsputils.load_module(f)
        self.assertEqual(x, {'FOO': {'bar': ['baz', 1]}})


    def test_setup_logging(self):
        with patch('adsputils.ConcurrentRotatingFileHandler') as cloghandler:
            adsputils.setup_logging('app')
            f = os.path.abspath(os.path.join(os.path.abspath(__file__), '../../..'))
            if sys.version_info > (3,):
                test_data = "call(backupCount=10, encoding='UTF-8', filename='{filename}/logs/app.log', maxBytes=10485760, mode='a')".format(filename=f)
            else:
                test_data = "call(backupCount=10, encoding=u'UTF-8', filename=u'{filename}/logs/app.log', maxBytes=10485760, mode=u'a')".format(filename=f)
            self.assertEqual(test_data,
                             str(cloghandler.call_args))


    def test_get_date(self):
        """Check we always work with UTC dates"""

        d = adsputils.get_date()
        self.assertTrue(d.tzname() == 'UTC')

        d1 = adsputils.get_date('2009-09-04T01:56:35.450686Z')
        self.assertTrue(d1.tzname() == 'UTC')
        self.assertEqual(d1.isoformat(), '2009-09-04T01:56:35.450686+00:00')
        self.assertEqual(adsputils.date2solrstamp(d1), '2009-09-04T01:56:35.450686Z')

        d2 = adsputils.get_date('2009-09-03T20:56:35.450686-05:00')
        self.assertTrue(d2.tzname() == 'UTC')
        self.assertEqual(d2.isoformat(), '2009-09-04T01:56:35.450686+00:00')
        self.assertEqual(adsputils.date2solrstamp(d2), '2009-09-04T01:56:35.450686Z')

        d3 = adsputils.get_date('2009-09-03T20:56:35.450686')
        self.assertTrue(d3.tzname() == 'UTC')
        self.assertEqual(d3.isoformat(), '2009-09-03T20:56:35.450686+00:00')
        self.assertEqual(adsputils.date2solrstamp(d3), '2009-09-03T20:56:35.450686Z')

    def test_update_from_env(self):
        os.environ["FOO"] = "2"
        os.environ["BAR"] = "False"
        os.environ["ORCID_PIPELINE_BAR"] = "True"
        conf = {'FOO': 1, 'BAR': False}
        adsputils.conf_update_from_env("ORCID_PIPELINE", conf)
        self.assertEqual(conf, {'FOO': 2, 'BAR': True})


class TestDbType(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.app = adsputils.ADSCelery('test', local_config=\
            {
            'SQLALCHEMY_URL': 'sqlite:///',
            'SQLALCHEMY_ECHO': False
            })


    def tearDown(self):
        unittest.TestCase.tearDown(self)
        self.app.close_app()

    def test_utcdatetime_type(self):

        base = declarative_base()
        class Test(base):
            __tablename__ = 'testdate'
            id = sa.Column(sa.Integer, primary_key=True)
            created = sa.Column(adsputils.UTCDateTime, default=adsputils.get_date)
            updated = sa.Column(adsputils.UTCDateTime)
        base.metadata.bind = self.app._engine
        base.metadata.create_all()

        with self.app.session_scope() as session:
            session.add(Test())
            m = session.query(Test).first()
            assert m.created
            assert m.created.tzname() == 'UTC'
            assert '+00:00' in str(m.created)

            current = adsputils.get_date('2018-09-07T20:22:02.249389+00:00')
            m.updated = current
            session.commit()

            m = session.query(Test).first()
            assert str(m.updated) == str(current)

            t = adsputils.get_date()
            m.created = t
            session.commit()
            m = session.query(Test).first()
            assert m.created == t

        # not ideal, but db exists in memory anyways...
        base.metadata.drop_all()


if __name__ == '__main__':
    unittest.main()
