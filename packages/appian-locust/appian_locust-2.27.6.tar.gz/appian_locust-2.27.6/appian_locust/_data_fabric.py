from typing import Optional, Dict, Any

from ._interactor import _Interactor

DATA_FABRIC_URI_PATH = "/suite/rest/a/applications/latest/app/process-hq"


class _DataFabric:
    def __init__(self, interactor: _Interactor):
        self.interactor = interactor

    def fetch_data_fabric_json(self, locust_request_label: Optional[str] = None,
                               additional_url_path: str = "") -> Dict[str, Any]:
        headers = self.interactor.setup_sail_headers()
        headers['X-Client-Mode'] = 'DESIGN'
        label = locust_request_label or "DataFabric.Ui"
        additional_url_path = f"/{additional_url_path}" \
            if additional_url_path and additional_url_path[0] != "/" \
            else additional_url_path
        response = self.interactor.get_page(
            f"{DATA_FABRIC_URI_PATH}{additional_url_path}", headers=headers, label=label)
        response.raise_for_status()
        return response.json()
