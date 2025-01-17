"""Class for fetching data from the Archiver Appliance using JSON."""
from aa import data, fetcher


class JsonFetcher(fetcher.AaFetcher):
    """Class to fetch data from the Archiver Appliance using JSON."""

    def __init__(self, hostname, port):
        """

        Args:
            hostname: hostname of Archiver Appliance
            port: port to connect to
        """
        super(JsonFetcher, self).__init__(hostname, port)
        self._url = '{}/retrieval/data/getData.json'.format(self._endpoint)

    def _parse_raw_data(self, response, pv, start, end, count):
        json_data = response.json()
        archive_data = data.ArchiveData.empty(pv)

        if json_data:
            events = []
            json_events = json_data[0]['data']
            for json_event in json_events:
                timestamp = json_event['secs'] + 1e-9 * json_event['nanos']
                events.append(data.ArchiveEvent(pv,
                                                json_event['val'],
                                                timestamp,
                                                json_event['severity']))

            archive_data = data.data_from_events(pv, events)

        return archive_data
