from influxdb.client import InfluxDBClient
from requests.adapters import HTTPAdapter


class InfluxAuthAdapter(HTTPAdapter):
    def __init__(self, org_id, token):
        super().__init__()
        self.org_id = org_id
        self.token = token

    def send(self, request, stream=False, timeout=None, verify=True, cert=None, proxies=None):
        request.url += "&u=%s&p=" % self.org_id
        request.headers["Authorization"] = "Token %s" % self.token
        return super().send(request, stream, timeout, verify, cert, proxies)


def create_influxdb_client(**kwargs):
    if "token" in kwargs:
        parameters = kwargs.copy()
        del parameters["token"]
        del parameters["org_id"]
        client = InfluxDBClient(**parameters)
        client._session.mount("%s://" % client._scheme, InfluxAuthAdapter(kwargs["org_id"], kwargs["token"]))
    else:
        client = InfluxDBClient(**kwargs)

    return client
