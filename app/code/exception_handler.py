import sys, logging, traceback, os
from datetime import datetime

config = {}

logging.basicConfig(filename=os.path.join(os.environ.get('LOG_DESTINATION'), 'app.log'), filemode='w',
                    format='%(asctime)s: %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
if os.environ.get('ENVIRONMENT_TYPE') == 'production':
    # Only log errors in the production environment
    logging.basicConfig(filename=os.path.join(os.environ.get('LOG_DESTINATION'), 'app.log'), filemode='w',
                        format='%(asctime)s: %(name)s - %(levelname)s - %(message)s', level=logging.ERROR)


class ExceptionHandler(object):
    @staticmethod
    def test_for_exception(func):
        def inner_function(*args, **kwargs):
            try:
                fn_result = func(*args, **kwargs)
            except Exception as err:
                # Different exception types can be added and even custom exceptions created
                tb = sys.exc_info()[-1]
                stk = traceback.extract_tb(tb, 1)
                fname = stk[0][2]
                str_error = "({}) {} - [caused_by: {}]".format(datetime.now().strftime("%Y/%m/%d %H:%M:%S"), err, stk)
                print(str_error)
                logging.error(str_error)
                producer = config.get('producer', None)
                if producer is not None:
                    producer.send_data_to_topic(['responding.error'], str_error)
                raise err
            return fn_result
        return inner_function
