import json
from datetime import datetime
from pytest_httpserver import HTTPServer
from werkzeug.wrappers import Response, Request

UID = "aezakmi-aezakmi-2137-l33t5p34k"
RESULTS = ['0', '1'] * 50


class TotallyRealQC:
    def __init__(self, processing_time_seconds) -> None:
        self.processing_seconds = processing_time_seconds
        self.start = datetime.now()
        self.num_reqs = 0
        self.last_success = False

    def get_result(self, r: Request) -> Response:
        if self.last_success:
            self.num_reqs = 0
            self.last_success = False
        self.num_reqs += 1
        if (datetime.now() - self.start).total_seconds() < self.processing_seconds:
            return Response(json.dumps(dict()), status=200, content_type='application/json')

        self.last_success = True
        return Response(json.dumps(RESULTS), status=200, content_type='application/json')


REAL_QC = TotallyRealQC(0.5)


def setup_server_orca_endpoints(httpserver: HTTPServer) -> HTTPServer:

    # functional
    httpserver.expect_request('/health').respond_with_json({'status': 'ok'})

    httpserver.expect_request('/tasks', method='POST').respond_with_json(
        {
            "uid": UID,
            "machine": "ORCA1",
            "status": "COMPLETED",
            "created": "never",
            "job_ids": {
                "ids": ["laksjdlfyqwuoiefusdfhjlashdfaksjdhf"]
            }
        })

    httpserver.expect_request(f'/tasks/{UID}/status').respond_with_json({"status": "Completed"})
    httpserver.expect_request(f'/tasks/{UID}/results').respond_with_handler(REAL_QC.get_result)

    httpserver.expect_request('/machines').respond_with_json({'names': ['ORCA-PT-1-A', 'ORCA-PT-1-B']})
    httpserver.expect_request('/machines/queue-count').respond_with_json({'ORCA-PT-1-A': 2, 'ORCA-PT-1-B': 1})
    return httpserver
