import os, sys
from time import sleep
import threading
import main
from exception_handler import ExceptionHandler
from event_message import EventMessage

messaging = {}
proxies = {}

class App(object):

    event = None
    results = None

    @ExceptionHandler.test_for_exception
    def __init__(self):
        self.result_store_proxy = proxies.get('result_store_proxy', None)
        if self.result_store_proxy is None:
            raise ValueError("Result Store Proxy Not Set")
        self.producer = producer = messaging.get('producer', None)
        if self.producer is None:
            raise ValueError("Producer Not Set")
        self.consumer = producer = messaging.get('consumer', None)
        if self.consumer is None:
            raise ValueError("Consumer Not Set")
        self.event = EventMessage()

        self.coarse_step_size_db = 10
        self.medium_step_size_db = 5
        self.fine_step_size = 1
        self.interferer_to_sut_rx_attenuator_value = 120
        self.interferer_to_sut_rx_attenuator_minimum_value = 40
        self.test_repeat_max_count = 10
        
        self.results = {}
        self.results['aggregate_test_id'] = self.result_store_proxy.get_next_index()
        self.results['aggregate_test_name'] = 'sit'
        self.results['sub_tests'] = {}

        self.main_routine_complete = False

        # self.main_routine()

    # def _test_for_trigger_enabled(self, routing_key: str, event: EventMessage) -> bool:
    #     return routing_key.endswith('test.update') and event.name=='trigger_enabled'
    
    # def _test_for_trigger_disabled(self, routing_key: str, event: EventMessage) -> bool:
    #     return routing_key.endswith('test.update') and event.name=='trigger_disabled'
    
    # def _test_for_sut_tx_transmission_start(self, routing_key: str, event: EventMessage) -> bool:
    #     return routing_key.endswith('sut_tx.test.update') and event.name=='transmission_start'
    
    # def _test_for_sut_tx_transmission_end(self, routing_key: str, event: EventMessage) -> bool:
    #     return routing_key.endswith('sut_tx.test.update') and event.name=='transmission_end'
    
    def _test_for_sut_rx_transmission_received(self, routing_key: str, event: EventMessage) -> bool:
        return routing_key.endswith('sut_rx.test.update') and event.name=='transmission_received'
    
    def _test_for_sut_rx_timeout(self, routing_key: str, event: EventMessage) -> bool:
        return routing_key.endswith('sut_rx.test.update') and event.name=='timeout'
    
    def _publish_test_start_event(self, test_id, attenuation_db):
        event_to_publish = EventMessage()
        event_to_publish.test_id = self.results['aggregate_test_id']
        event_to_publish.name = 'no_instruments'
        event_to_publish.payload = dict(test_id=test_id, ir_rf_attenuator=attenuation_db)
        self.producer.send_data_to_topic(['scenario.scenario.start'], event_to_publish.create_message_to_send())    
        
    def _consumer_running_in_thread(self, cb):
        self.consumer(os.environ.get('RABBITMQ_HOST'), os.environ.get('RABBITMQ_EXCHANGE'), os.environ.get('ROUTING_KEY'), cb)

    def _get_sub_test_name(self) -> str:
        return f'attenuation_{self.interferer_to_sut_rx_attenuator_value}'
    
    def _initialise_sub_test_entry_if_needed(self, sub_test_name: str):
        if not self.results['sub_tests'].get(sub_test_name, False):
            self.results['sub_tests'][sub_test_name] = []
    
    def _has_sub_test_reached_maximum_test_count(self, sub_test_name):
        return len(self.results['sub_tests'][sub_test_name]) == self.test_repeat_max_count

    def _has_last_three_sub_tests_resulted_in_all_failed_transmissions(self) -> bool:
        list_of_sub_test_results = []
        for idx, this_sub_test_name in enumerate(self.results['sub_tests']):
            list_of_sub_test_results.append(self.results['sub_tests'][this_sub_test_name])
        if idx < 2:
            return False
        if [sum(x) for x in list_of_sub_test_results[-3:]] == [0,0,0]:
            return True
        return False

    def _record_sub_test_result(self, sub_test_name, result):
        self.results['sub_tests'][sub_test_name].append(result)

    def _has_test_routine_finished(self, sub_test_name) -> bool:
        routine_has_finished = False
        has_minimum_attenuation_been_reached = self.interferer_to_sut_rx_attenuator_value == self.interferer_to_sut_rx_attenuator_minimum_value
        if has_minimum_attenuation_been_reached and self._has_sub_test_reached_maximum_test_count(sub_test_name):
            routine_has_finished = True
        elif self._has_last_three_sub_tests_resulted_in_all_failed_transmissions():
            routine_has_finished = True
        return routine_has_finished

    def _determine_and_set_next_attenuation_value(self) -> int:
        return_value_db = 0
        # Map db changes
        db_changes = []
        for idx, this_sub_test_name in enumerate(self.results['sub_tests']):
            db_changes.append(int(this_sub_test_name.replace('attenuation_','')))
        # And capture results in list
        list_of_sub_test_result_transmission_count = []
        for idx, this_sub_test_name in enumerate(self.results['sub_tests']):
            list_of_sub_test_result_transmission_count.append(sum((self.results['sub_tests'][this_sub_test_name])))
        if not idx:
            return self.interferer_to_sut_rx_attenuator_value - self.coarse_step_size_db
        last_step_size = db_changes[-2]-db_changes[-1]
        last_sub_test_transmission_count = list_of_sub_test_result_transmission_count[-1]
        if last_sub_test_transmission_count and last_step_size==self.coarse_step_size_db:
            return_value_db = self.interferer_to_sut_rx_attenuator_value - self.coarse_step_size_db
        elif not last_sub_test_transmission_count and last_step_size==self.coarse_step_size_db:
            return_value_db = self.interferer_to_sut_rx_attenuator_value + self.medium_step_size_db
        elif last_step_size!=self.coarse_step_size_db:
            return_value_db = self.interferer_to_sut_rx_attenuator_value + self.fine_step_size
        if self.results['sub_tests'].get(f'attenuation_{return_value_db}', None) is not None:
            # Delete previous measurement results if they exist
            del self.results['sub_tests'][f'attenuation_{return_value_db}']
        return return_value_db

    def process_result_and_set_next_test_conditions(self, transmission_received: bool):
        this_sub_test_name = self._get_sub_test_name()
        self._initialise_sub_test_entry_if_needed(this_sub_test_name)
        self._record_sub_test_result(this_sub_test_name, transmission_received)
        if self._has_test_routine_finished(this_sub_test_name):
            self.main_routine_complete = True
        else:
            if self._has_sub_test_reached_maximum_test_count():
                self.interferer_to_sut_rx_attenuator_value = self._determine_and_set_next_attenuation_value()

    @ExceptionHandler.test_for_exception
    def main_routine(self):
        self._publish_test_start_event(self.interferer_to_sut_rx_attenuator_value)
        def consumer_callback(ch, method, properties, body):
            this_event = EventMessage().extract_consumed_message_information(body)
            routing_key = method.routing_key
            if self._test_for_sut_rx_transmission_received(routing_key, this_event):
                self.process_result_and_set_next_test_conditions(True)
                self._publish_test_start_event(self.interferer_to_sut_rx_attenuator_value)
            if self._test_for_sut_rx_timeout(routing_key, this_event):
                self.process_result_and_set_next_test_conditions(False)
                self._publish_test_start_event(self.interferer_to_sut_rx_attenuator_value)
            ch.basic_ack(delivery_tag = method.delivery_tag)

        consumer_background_thread = threading.Thread(target=self._consumer_running_in_thread, args=(consumer_callback,), daemon=True)
        consumer_background_thread.start()
        sleep(1)
        cycle_pause_duration_secs = 0.1
        while not self.main_routine_complete:
            sleep(cycle_pause_duration_secs)


if __name__ == '__main__':
    try:
        App()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
