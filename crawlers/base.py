from abc import ABC, abstractmethod


class BaseCrawler(ABC):
    def __init__(self, data_source, event_type):
        self.data = []
        self.data_source = data_source
        self.data_type = event_type

    @abstractmethod
    def crawl(self):
        pass


class SeismicCrawler(BaseCrawler):
    def __init__(self, data_source):
        super().__init__(data_source, "seismic")

    @abstractmethod
    def pandify_data(self):
        pass
