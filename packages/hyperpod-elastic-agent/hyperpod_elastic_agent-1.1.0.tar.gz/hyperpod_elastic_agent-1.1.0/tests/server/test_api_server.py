import json
import pytest
import logging

from hyperpod_elastic_agent.logagent import LogState
from hyperpod_elastic_agent.ipc import InProcessRestartSocketServer
from hyperpod_elastic_agent.server import AgentInfo, AgentState, HyperPodElasticAgentServer
from fastapi.testclient import TestClient
from http import HTTPStatus
from unittest.mock import Mock, patch

AGENT_STATE_TRANSITIONS = {
    AgentState.READY: '2024-11-20T23:37:17.855065+00:00',
    AgentState.RUNNING: '2024-11-20T23:37:37.594312+00:00',
    AgentState.COMPLETED: '2024-11-20T23:38:08.703561+00:00',
}


class TestHyperPodElasticAgentServer:

    @classmethod
    def setup_class(cls):
        cls.server_specs = {
            "host": "127.0.0.1",
            "port": 8000,
            "log_level": "info",
        }

    @pytest.fixture
    def mock_thread(self):
        patched_thread = patch('threading.Thread')
        patched_thread.start = Mock()
        return patched_thread

    @pytest.fixture
    def mock_agent(self):
        mock_agent = Mock()
        mock_agent.set_agent_state = Mock()
        mock_agent.set_agent_state_running = Mock()
        mock_agent.get_agent_state_info = Mock(return_value=AgentInfo(
            state=AgentState.READY,
            transitions=AGENT_STATE_TRANSITIONS,
            ip_version="2025-01-10T12:00:00Z",
        ))
        mock_agent.version = "1.1.0"
        mock_agent.get_agent_progress = Mock(return_value={})
        mock_agent._ipc_server = Mock(
            return_value=InProcessRestartSocketServer(local_world_size=4))
        mock_agent.assigned_rank = 0
        mock_agent.get_assigned_rank = Mock(return_value=0)
        mock_agent.spare = False
        mock_agent.priority = False
        mock_agent.get_restart_mode = Mock(return_value="in_process_restart")
        return mock_agent

    @pytest.fixture
    def mock_app(self, mock_thread, mock_agent):
        with patch('threading.Thread', return_value=mock_thread):
            server = HyperPodElasticAgentServer(mock_agent, self.server_specs)
            return server._app

    @pytest.fixture
    def mock_server(self, mock_agent):
        server = HyperPodElasticAgentServer(mock_agent, self.server_specs)
        server._server.run = Mock()
        yield server

    @pytest.fixture
    def client(self, mock_app):
        return TestClient(mock_app)

    def test_register_routes(self, mock_app):
        assert mock_app.routes

    def test_api_start_empty_master(self, client, mock_agent):
        response = client.post("/start",
                               content=json.dumps({
                                   "rank": 0,
                                   "nnodes": 1,
                                   "faultCount": 33,
                                   "master_addr": "",
                                   "master_port": "",
                                   "ipVersion": "2025-01-10T12:00:00Z",
                                   "rankIps": [],
                                   "spare": False,
                               }))
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        # Check that the error is about the master_addr field
        error_detail = response.json()
        assert "detail" in error_detail
        assert len(error_detail["detail"]) > 0
        # Check that at least one error mentions "master_addr"
        assert any("master_addr" in str(error.get("loc", []))
                   for error in error_detail["detail"])
        # Check that the error message contains our custom validation message
        assert any(
            "Empty master_addr received from operator" in error.get("msg", "")
            for error in error_detail["detail"])

    def test_api_start(self, client, mock_agent):
        rank_ips = [
            {
                'ip': '192.168.111.1',
                'rank': 0,
            },
            {
                'ip': '192.168.111.2',
                'rank': 1,
            },
        ]
        worker_data = [{
            "rank": 0,
            "group_rank": 0,
            "local_rank": 1,
            "data": {
                "foo": "bar",
            },
        }]
        response = client.post("/start",
                               content=json.dumps({
                                   "rank": 0,
                                   "nnodes": 1,
                                   "faultCount": 33,
                                   "master_addr": "192.168.111.1",
                                   "master_port": "23456",
                                   "ipVersion": "2025-01-10T12:00:00Z",
                                   "rankIps": rank_ips,
                                   "worker_data": worker_data,
                                   "spare": 0,
                               }))
        assert response.status_code == HTTPStatus.OK
        mock_agent.set_agent_state_running.assert_called_once()
        mock_agent.update_rendezvous_info.assert_called_once_with(
            0,
            1,
            33,
            "192.168.111.1",
            23456,
            "2025-01-10T12:00:00Z",
            rank_ips,
            worker_data,
        )
        mock_agent.set_assigned_rank.assert_called_once_with(0)

    def test_api_start_incorrect_data(self, client, mock_agent):
        response = client.post("/start",
                               content=json.dumps({
                                   "rank": "invalid_rank",
                                   "nnodes": 1,
                               }))
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        # FastAPI validation errors has this format
        # {'detail': [{'input': 'invalid_rank', 'loc': ['body', 'rank'], 'msg': 'Input should be a valid integer, unable to parse'}]
        error_detail = response.json()
        assert "detail" in error_detail
        assert len(error_detail["detail"]) > 0
        # Check that the error is about the rank field
        assert any("rank" in str(error.get("loc", []))
                   for error in error_detail["detail"])
        # Neither set_agent_state_running nor set_agent_state should be called
        # because the request fails validation before reaching our handler
        mock_agent.set_agent_state_running.assert_not_called()
        mock_agent.set_agent_state.assert_not_called()

    def test_api_start_with_list_log_monitoring(self, client, mock_agent):
        """Test that the API accepts a list of dictionaries for log_monitoring_configuration."""
        log_monitoring_config = [{
            "name": "TrainingStart",
            "logPattern": ".*Training script started.*",
            "expectedStartCutOffInSeconds": 300
        }, {
            "name": "TFLOPs",
            "logPattern": ".* (.+)TFLOPs.*",
            "expectedRecurringFrequencyInSeconds": 60,
            "metricThreshold": 100,
            "operator": "lt"
        }]
        response = client.post("/start",
                               content=json.dumps({
                                   "rank":
                                   0,
                                   "nnodes":
                                   1,
                                   "faultCount":
                                   33,
                                   "master_addr":
                                   "192.168.111.1",
                                   "master_port":
                                   "23456",
                                   "log_monitoring_configuration":
                                   log_monitoring_config
                               }))
        assert response.status_code == HTTPStatus.OK
        mock_agent.set_log_monitoring_configuration.assert_called_once_with(
            log_monitoring_config)

    def test_api_stop(self, client, mock_agent):
        response = client.post("/stop")
        assert response.status_code == HTTPStatus.OK
        mock_agent.set_agent_state.assert_called_once_with(AgentState.STOPPING)
        mock_agent.set_restart_mode.assert_called_once_with("ipr")

    def test_api_stop_global_plr(self, client, mock_agent):
        response = client.post(
            "/stop",
            content=json.dumps({
                "restart_mode": "global_plr",
            }),
        )
        assert response.status_code == HTTPStatus.OK
        mock_agent.set_agent_state.assert_called_once_with(AgentState.STOPPING)
        mock_agent.set_restart_mode.assert_called_once_with("global_plr")

    def test_api_stop_with_timeout_and_signal(self, client, mock_agent):
        """Test /stop API with custom timeout and signal"""
        response = client.post(
            "/stop",
            content=json.dumps({
                "restart_mode": "ipr",
                "is_graceful": True,  # Use graceful shutdown
                "timeout": 600,
            }),
        )
        assert response.status_code == HTTPStatus.OK
        mock_agent.set_agent_state.assert_called_once_with(AgentState.STOPPING)
        mock_agent.set_restart_mode.assert_called_once_with("ipr")
        # Verify timeout and graceful flag were stored
        mock_agent.set_graceful_shutdown_params.assert_called_once_with(
            True, 600)

    def test_api_status(self, client, mock_agent):
        response = client.get("/status")
        assert response.status_code == HTTPStatus.OK
        assert json.loads(response.content) == {
            'status': 'ready',
            'transitions': AGENT_STATE_TRANSITIONS,
            'ipversion': '2025-01-10T12:00:00Z',
            'agent_version': '1.1.0',
            'assigned_rank': '0',
            'spare': 'False',
            'restartMode': 'in_process_restart',
        }
        mock_agent.get_agent_state_info.assert_called_once()

    def test_api_status_no_rank(self, client, mock_agent):
        # Simulate no rank being assigned yet
        mock_agent.get_assigned_rank.return_value = -1
        mock_agent.priority = True
        response = client.get("/status")
        assert response.status_code == HTTPStatus.OK
        assert json.loads(response.content) == {
            'status': 'ready',
            'transitions': AGENT_STATE_TRANSITIONS,
            'ipversion': '2025-01-10T12:00:00Z',
            'agent_version': '1.1.0',
            "spare": 'False',
            "priority": 'True',
            'restartMode': 'in_process_restart',
        }
        mock_agent.get_agent_state_info.assert_called_once()

    def test_api_update(self, client, mock_agent):
        rank_ips = [
            {
                'ip': '192.168.111.1',
                'rank': 0,
            },
            {
                'ip': '192.168.111.2',
                'rank': 1,
            },
        ]
        fault_data = {
            "plr_failed_ranks": rank_ips,
            "ipr_fault_data": [],
        }
        mock_agent.fault_data = fault_data
        response = client.post("/update",
                               content=json.dumps({
                                   "rank": 0,
                                   "nnodes": 1,
                                   "faultCount": 33,
                                   "master_addr": "192.168.111.1",
                                   "master_port": "23456",
                                   "ipVersion": "2025-01-10T12:00:00Z",
                                   "rankIps": rank_ips,
                                   "spare": False,
                               }))
        mock_agent.update_rendezvous_info.assert_called_once_with(
            0,
            1,
            33,
            "192.168.111.1",
            23456,
            "2025-01-10T12:00:00Z",
            rank_ips,
            None,
        )

        assert response.status_code == HTTPStatus.OK
        assert json.loads(response.content) == {
            'status': 'ready',
            'transitions': AGENT_STATE_TRANSITIONS,
            'ipversion': '2025-01-10T12:00:00Z',
            'agent_version': '1.1.0',
            'assigned_rank': '0',
            "spare": 'False',
            'restartMode': 'in_process_restart',
        }
        mock_agent.get_agent_state_info.assert_called_once()
        mock_agent.send_rank_info.assert_called_once_with(0)

    def test_api_update_empty_master(self, client, mock_agent):
        response = client.post("/update",
                               content=json.dumps({
                                   "rank": 0,
                                   "nnodes": 1,
                                   "faultCount": 33,
                                   "master_addr": "",
                                   "master_port": "",
                                   "ipVersion": "2025-01-10T12:00:00Z",
                                   "rankIps": [],
                                   "spare": False,
                               }))
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        # Check that the error is about the master_addr field
        error_detail = response.json()
        assert "detail" in error_detail
        assert len(error_detail["detail"]) > 0
        # Check that at least one error mentions "master_addr"
        assert any("master_addr" in str(error.get("loc", []))
                   for error in error_detail["detail"])
        # Check that the error message contains our custom validation message
        assert any(
            "Empty master_addr received from operator" in error.get("msg", "")
            for error in error_detail["detail"])

    def test_api_update_incorrect_data(self, client, mock_agent):
        response = client.post("/update",
                               content=json.dumps({
                                   "rank": "invalid_rank",
                                   "nnodes": 1,
                               }))
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        # Check that the error is about the rank field
        error_detail = response.json()
        assert "detail" in error_detail
        assert len(error_detail["detail"]) > 0
        # Check that at least one error mentions "rank"
        assert any("rank" in str(error.get("loc", []))
                   for error in error_detail["detail"])

    def test_api_update_with_list_log_monitoring(self, client, mock_agent):
        """Test that the API accepts a list of dictionaries for log_monitoring_configuration."""
        log_monitoring_config = [{
            "name": "TrainingStart",
            "logPattern": ".*Training script started.*",
            "expectedStartCutOffInSeconds": 300
        }, {
            "name": "TFLOPs",
            "logPattern": ".* (.+)TFLOPs.*",
            "expectedRecurringFrequencyInSeconds": 60,
            "metricThreshold": 100,
            "operator": "lt"
        }]
        response = client.post("/update",
                               content=json.dumps({
                                   "rank":
                                   0,
                                   "nnodes":
                                   1,
                                   "faultCount":
                                   33,
                                   "master_addr":
                                   "192.168.111.1",
                                   "master_port":
                                   "23456",
                                   "log_monitoring_configuration":
                                   log_monitoring_config
                               }))
        assert response.status_code == HTTPStatus.OK
        mock_agent.set_log_monitoring_configuration.assert_called_once_with(
            log_monitoring_config)

    def test_validation_exception_handler(self, client, mock_agent):
        """Test that validation errors are properly logged with details."""
        # Test data with validation errors
        test_data = {
            "rank": "invalid_rank",
            "nnodes": "invalid_nnodes",
            "faultCount": "invalid_faultCount",
            "master_addr": 123,  # Should be a string
            "master_port": {},  # Should be int or string
        }

        # Send the request
        response = client.post("/update", content=json.dumps(test_data))

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

        # Check the response contains detailed error information
        error_detail = response.json()
        assert "detail" in error_detail
        assert len(error_detail["detail"]) >= 4  # At least 4 validation errors

        # Check that the error details contain the expected fields
        error_fields = set()
        for error in error_detail["detail"]:
            if "loc" in error and len(error["loc"]) >= 2:
                error_fields.add(error["loc"][1])

        assert "rank" in error_fields
        assert "nnodes" in error_fields
        assert "faultCount" in error_fields
        assert "master_addr" in error_fields

    def test_api_shutdown(self, client, mock_agent):
        response = client.post("/shutdown")
        assert response.status_code == HTTPStatus.OK
        mock_agent.set_agent_state.assert_called_once_with(AgentState.SHUTDOWN)

    def test_server_run(self, mock_server):
        mock_server.start()
        mock_server._server.run.assert_called_once()

    def test_server_shutdown(self, mock_server):
        mock_server.shutdown()
        assert mock_server._server.should_exit
        assert mock_server._server.force_exit
