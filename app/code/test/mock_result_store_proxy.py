class MockResultStoreProxy(object):

    def __init__(self) -> None:
        pass

    def get_next_index(self)->int:
        return 1

    def save_results(self, result_id, result_name, results):
        return dict(result_location="path/to/file")
    
    def download_file(self, result_id, station_url, filename):
        return dict(file_location="path/to/file")
