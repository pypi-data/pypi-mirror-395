from kombu.utils import json as kombu_json
from adsmsg.msg import Msg
import base64

"""Custom de/serializer for adsmsg objects. We piggyback on the JSON
protocol (default for Celery). 'dumps' method is not changed at all,
and for the 'loads' we take advantage of the 'object_hook' method of
the JSON protocol. That allow us to turn serialized adsmsg's into 
Protobufs. 


This serializer must be registered with the celery (workers). This
happens automatically when 'adsputils' is installed. Manually it can
be done as so:

from kombu.serialization import register
register('adsmsg', dumps, loads,  content_type='application/x-adsmsg',
    content_encoding='utf-8') 

There are multiple ways to tell Celery to use the de/serializer:

    1. set the default config
        CELERY_ACCEPT_CONTENT = ['adsmsg']
        CELERY_TASK_SERIALIZER = 'adsmsg'
        CELERY_RESULT_SERIALIZER = 'adsmsg'
    2. set serizalizer in task
        @app.task(...., serializer='adsmsg')
    3. set serializer for a message: 
        task.task_xxxx.apply_sync(...., serializer='adsmsg')
    4. override the default json serializer:
        register('json', loads, dumps, 'application/json', 'utf-8')
"""        

def adsmsg_converter(dct):
    if '__adsmsg__' in dct:
        cls, data = dct['__adsmsg__']
        return Msg.loads(cls, base64.b64decode(data)) # ('class.name', 'binary data.....')
    return dct

json_loads = kombu_json.json.loads

def my_loads(s):
    return json_loads(s, object_hook=adsmsg_converter)

dumps = kombu_json.dumps

def loads(s):
    return kombu_json.loads(s, _loads=my_loads)


register_args = (kombu_json.dumps, loads, 'application/x-adsmsg', 'utf-8')
