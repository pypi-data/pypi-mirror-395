from locust import TaskSet, Locust
from .mock_client import CustomLocust
from .mock_reader import read_mock_file
from requests.exceptions import HTTPError
from appian_locust import AppianTaskSet
from appian_locust._interactor import _Interactor
from appian_locust._control_panel_workspace import _ControlPanelWorkspace
import json
import unittest


class TestControlPanel(unittest.TestCase):

    def setUp(self) -> None:
        self.custom_locust = CustomLocust(Locust())
        setattr(self.custom_locust.client, "feature_flag", "")
        setattr(self.custom_locust.client, "feature_flag_extended", "")
        parent_task_set = TaskSet(self.custom_locust)

        setattr(parent_task_set, "host", "")
        setattr(parent_task_set, "auth", ["", ""])
        self.task_set = AppianTaskSet(parent_task_set)
        self.task_set.host = ""

        self.custom_locust.set_response("auth?appian_environment=tempo", 200, '{}')
        self.interactor = _Interactor(self.custom_locust.client, "")
        self.interactor.login(["", ""])
        self.task_set.on_start()

    def tearDown(self) -> None:
        self.task_set.on_stop()

    def test_control_panel_workspace(self) -> None:
        cp_response = read_mock_file("control_panel_site.json")
        self.custom_locust.set_response("/suite/rest/a/applications/latest/app/control-panel",
                                        200,
                                        cp_response)

        cp_workspace = _ControlPanelWorkspace(self.interactor)
        result = cp_workspace.fetch_cp_workspace_json()

        self.assertEqual(json.loads(cp_response), result)

    def test_control_panel_workspace_error(self) -> None:
        self.custom_locust.set_response("/suite/rest/a/applications/latest/app/control-panel", 404, "not found")

        cp_workspace = _ControlPanelWorkspace(self.interactor)
        with self.assertRaises(HTTPError):
            cp_workspace.fetch_cp_workspace_json()


if __name__ == '__main__':
    unittest.main()
