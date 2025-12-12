from typing import Optional, Dict, Any
import json

from ._interactor import _Interactor

CP_WORKSPACE_URI_PATH = "/suite/rest/a/applications/latest/app/control-panel"


class _ControlPanelWorkspace:
    """Handles interactions with Appian Control Panel workspace."""

    def __init__(self, interactor: _Interactor):
        self.interactor = interactor

    def fetch_cp_workspace_json(self, locust_request_label: Optional[str] = None) -> Dict[str, Any]:
        """Fetches control panel workspace JSON data.

        Args:
            locust_request_label: Optional label for locust request tracking

        Returns:
            Dict containing control panel workspace data
        """
        headers = self.interactor.setup_sail_headers()
        headers['X-Client-Mode'] = 'DESIGN'
        label = locust_request_label or "ControlPanel.Ui"
        response = self.interactor.get_page(CP_WORKSPACE_URI_PATH, headers=headers, label=label)
        response.raise_for_status()
        return response.json()
