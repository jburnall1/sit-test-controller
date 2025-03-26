import os
import context
from rspmessaginglib.rabbit_mq_producer import RabbitMQProducer
from rspmessaginglib.rabbit_mq_consumer import RabbitMQConsumer

dir_path = os.path.dirname(os.path.realpath(__file__))
os.environ['ENVIRONMENT_TYPE'] = 'test'
os.environ['LOG_DESTINATION'] = os.path.join(dir_path)
os.environ['TEST_BASE_PATH'] = os.path.join(dir_path, 'tests')
os.environ['RABBITMQ_HOST'] = 'localhost'
os.environ['RABBITMQ_USER'] = 'guest'
os.environ['RABBITMQ_PASS'] = 'guest'
os.environ['RABBITMQTT_EXCHANGE'] = 'amq.topic'
os.environ['RABBITMQ_EXCHANGE'] = 'responding'
os.environ['ROUTING_KEY'] = '#'

ip = '192.168.1.42'
# ip = '192.168.10.2'
os.environ['RESULT_STORE_URL'] = f'http://{ip}:5111/result-store'

# from result_store_proxy import ResultStoreProxy
from mock_result_store_proxy import MockResultStoreProxy as ResultStoreProxy   #.mock_result_store_proxy import MockResultStoreProxy as ResultStoreProxy

import app
app.proxies['result_store_proxy'] = ResultStoreProxy()
app.messaging['producer'] = RabbitMQProducer(os.environ.get('RABBITMQ_HOST'), os.environ.get('RABBITMQ_USER'), os.environ.get('RABBITMQ_PASS'))
app.messaging['consumer'] = RabbitMQConsumer
