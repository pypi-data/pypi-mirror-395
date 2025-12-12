# -*- coding: utf-8 -*-

from builtins import str
from builtins import range
from adsputils import ADSCelery, ADSTask
import unittest


class TestUpdateRecords(unittest.TestCase):

    def test_config(self):
        app = ADSCelery('test',local_config={
            'FOO': ['bar', {}]
            })
        self.assertEqual(app._config['FOO'], ['bar', {}])
        self.assertEqual(app.conf['FOO'], ['bar', {}])
        
        self.assertEqual(app.conf['CELERY_RESULT_SERIALIZER'], 'adsmsg')
        self.assertFalse(app._config.get('CELERY_RESULT_SERIALIZER', None))
    
    def test_app_task(self):
        
        class NewCelery(ADSCelery):
            def attempt_recovery(self, task, args=None, kwargs=None, einfo=None, retval=None):
                if 'Failing!' in str(retval):
                    # half the number of processed objects
                    first_half, second_half = args[0][0:int(len(args[0])/2)], args[0][int(len(args[0])/2):]
                    # resubmit
                    args = list(args)
                    args[0] = first_half
                    task.apply(args=args, kwargs=kwargs)
                    args[0] = second_half
                    task.apply(args=args, kwargs=kwargs)
                    
        app = NewCelery('test',local_config={
            'FOO': ['bar', {}]
            })
        
        
        processed = []
        @app.task
        def test(batch):
            if len(batch) == 10:
                processed.append('Failure')
                raise Exception('Failing!')
            processed.append(batch)
        
        self.assertRaises(Exception, lambda: test.apply(args=(list(range(10)),)))
        self.assertEqual(processed, ['Failure', 'Failure', [0,1,2,3,4], [5,6,7,8,9]])
        
        processed = []
        test.max_retries = 3
        self.assertRaises(Exception, lambda: test.apply(args=(list(range(10)),)))
        self.assertEqual(processed, ['Failure', 'Failure', 'Failure', 'Failure', [0,1,2,3,4], [5,6,7,8,9]])
        
if __name__ == '__main__':
    unittest.main()
