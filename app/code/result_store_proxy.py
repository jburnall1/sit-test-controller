from os import environ
import requests
import json
from exception_handler import ExceptionHandler
# from station_proxy import StationProxy

class ResultStoreProxy(object):

    def __init__(self) -> None:
        self._result_store_url = environ.get('RESULT_STORE_URL', None)
        if self._result_store_url is None:
            raise ValueError("Environment Variable Not Set")

    @ExceptionHandler.test_for_exception
    def get_next_index(self)->int:
        response = requests.get("{}/next-index".format(self._result_store_url))
        if response.status_code == 400:
            raise ValueError("URL Not Found. Docker may not be running")
        response_dict = response.json()
        return response_dict['test_id']
    
    @ExceptionHandler.test_for_exception
    def save_results(self, result_id, result_name, results):
        url = "{}/{}".format(self._result_store_url, result_id)
        response = requests.post(url, json={result_name: results})
        return response

    # @ExceptionHandler.test_for_exception
    # def download_file(self, result_id, filename):
    #     url = "{}/download/{}".format(self._result_store_url, result_id)
    #     response = requests.post(url, json=dict(station_url=StationProxy()._station_url, filename=filename))
    #     return response

    # @ExceptionHandler.test_for_exception
    # def download_file_as(self, result_id, filename, new_filename):
    #     url = "{}/download-as/{}/{}".format(self._result_store_url, result_id, new_filename)
    #     response = requests.post(url, json=dict(station_url=StationProxy()._station_url, filename=filename))
    #     return response

    # @ExceptionHandler.test_for_exception
    # def delete_test(self, result_id):
    #     url = "{}/{}".format(self._result_store_url, result_id)
    #     response = requests.delete(url)
    #     return response

