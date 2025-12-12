import json
import pytest
import re

from hyperpod_elastic_agent.server.server import AgentState
from hyperpod_elastic_agent.server.util import (
    StatusResponse,
    StatusResponseJSONEncoder,
)
from hyperpod_elastic_agent.ipc.util import IPCWorkerGroup
from hyperpod_elastic_agent.ipc.common import RestartMode
from torch.distributed.elastic.multiprocessing import ProcessFailure
from unittest.mock import Mock, mock_open, patch

TORCHELASTIC_ERROR_FILE = '''{
          "message": {
            "message": "RuntimeError: [../third_party/gloo/gloo/transport/tcp/pair.cc:534] Connection closed by peer",
            "extraInfo": {
              "py_callstack": "Traceback Connection closed by peer [192.168.65.3]:35304",
              "timestamp": "1730223202"
            }
          }
        }'''


class TestUtil:

    @classmethod
    def setup_class(cls):
        with patch("builtins.open",
                   new_callable=mock_open,
                   read_data=TORCHELASTIC_ERROR_FILE), patch(
                       "os.path.isfile", return_value=True):
            cls.proc_failure_0 = ProcessFailure(
                local_rank=0,
                pid=111,
                exitcode=1,
                error_file="/tmp/hyperpod/none_2o6jvae_/attempt_0/0/error.json",
            )

    def test_success(self):
        status_resp = StatusResponse(
            status=AgentState.COMPLETED,
            transitions={
                AgentState.READY: '2024-11-20T23:37:17.855065+00:00',
                AgentState.RUNNING: '2024-11-20T23:37:37.594312+00:00',
                AgentState.COMPLETED: '2024-11-20T23:38:08.703561+00:00',
            },
            agent_version="1.1.0",
            ip_version="2025-01-10T12:00:00Z",
            restart_mode="in_process_restart",
        )
        resp_txt = json.dumps(status_resp, cls=StatusResponseJSONEncoder)
        expected = (
            r'\{"status": "completed", "transitions": \{'
            r'"READY": "\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}\+\d{2}:\d{2}", '
            r'"RUNNING": "\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}\+\d{2}:\d{2}", '
            r'"COMPLETED": "\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}\+\d{2}:\d{2}"\}, '
            r'"restartMode": "in_process_restart", '
            r'"ipversion": "2025-01-10T12:00:00Z", '
            r'"agent_version": "1.1.0"\}')
        assert re.fullmatch(expected, resp_txt) is not None

    def test_log_state_failure(self):
        status_resp = StatusResponse(
            status=AgentState.FAULTED,
            reason="LogStateHanging_dummy_rule_1",
            message="{x}",
            transitions={
                AgentState.READY: '2024-11-20T23:37:17.855065+00:00',
                AgentState.RUNNING: '2024-11-20T23:37:37.594312+00:00',
                AgentState.FAULTED: '2024-11-20T23:38:08.703561+00:00',
            },
            agent_version="1.1.0",
            spare="False",
            restart_mode="in_process_restart",
        )
        resp_txt = str(json.dumps(status_resp, cls=StatusResponseJSONEncoder))
        expected = (
            r'\{"status": "faulted", "transitions": \{'
            r'"READY": "\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}\+\d{2}:\d{2}", '
            r'"RUNNING": "\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}\+\d{2}:\d{2}", '
            r'"FAULTED": "\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}\+\d{2}:\d{2}"\}, '
            r'"reason": "LogStateHanging_dummy_rule_1", "message": "\{.*\}", '
            r'"restartMode": "in_process_restart", '
            r'"agent_version": "1.1.0", "spare": "False"\}')
        assert re.fullmatch(expected, resp_txt) is not None

    def test_log_state_faulted(self):
        status_resp = StatusResponse(
            status=AgentState.FAULTED,
            reason="LogStateFaulted_OutOfMemoryError",
            message="{x}",
            transitions={
                AgentState.READY: '2024-11-20T23:37:17.855065+00:00',
                AgentState.RUNNING: '2024-11-20T23:37:37.594312+00:00',
                AgentState.FAULTED: '2024-11-20T23:38:08.703561+00:00',
            },
            agent_version="1.1.0",
        )
        resp_txt = str(json.dumps(status_resp, cls=StatusResponseJSONEncoder))
        expected = (
            r'\{"status": "faulted", "transitions": \{'
            r'"READY": "\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}\+\d{2}:\d{2}", '
            r'"RUNNING": "\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}\+\d{2}:\d{2}", '
            r'"FAULTED": "\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}\+\d{2}:\d{2}"\}, '
            r'"reason": "LogStateFaulted_OutOfMemoryError", "message": "\{.*\}", '
            r'"agent_version": "1.1.0"\}')
        assert re.fullmatch(expected, resp_txt) is not None

    def test_worker_state_failure(self):
        status_resp = StatusResponse(
            status=AgentState.FAULTED,
            reason="WorkerStateFailed",
            message="{x}",
            transitions={
                AgentState.READY: '2024-11-20T23:37:17.855065+00:00',
                AgentState.RUNNING: '2024-11-20T23:37:37.594312+00:00',
                AgentState.FAULTED: '2024-11-20T23:38:08.703561+00:00',
            },
            agent_version="1.1.0",
            ip_version="2025-01-10T12:00:00Z",
            assigned_rank="4",
            restart_mode="in_process_restart",
        )
        resp_txt = str(json.dumps(status_resp, cls=StatusResponseJSONEncoder))
        expected = (
            r'\{"status": "faulted", "transitions": \{'
            r'"READY": "\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}\+\d{2}:\d{2}", '
            r'"RUNNING": "\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}\+\d{2}:\d{2}", '
            r'"FAULTED": "\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}\+\d{2}:\d{2}"\}, '
            r'"reason": "WorkerStateFailed", "message": "\{.*\}", '
            r'"restartMode": "in_process_restart", '
            r'"ipversion": "2025-01-10T12:00:00Z", '
            r'"agent_version": "1.1.0", "assigned_rank": "4"\}')
        assert re.fullmatch(expected, resp_txt) is not None

    def test_incorrect_encoder(self):
        with pytest.raises(
                TypeError,
                match="Object of type Mock is not JSON serializable"):
            json.dumps(Mock(), cls=StatusResponseJSONEncoder)

    def test_ipr_failure(self):
        ipc_worker_group = IPCWorkerGroup(local_world_size=1)
        ipc_worker_group.set_data(
            global_rank=0,
            group_rank=0,
            local_rank=0,
            data="error trace",
        )
        ipc_worker_group.fail_rank(
            global_rank=0,
            group_rank=0,
            local_rank=0,
            restart_mode=RestartMode.PROCESS_LEVEL_RESTART,
        )
        status_resp = StatusResponse(
            status=AgentState.FAULTED,
            reason="ProcessStateFailure_Ranks0",
            transitions={
                AgentState.READY: '2024-11-20T23:37:17.855065+00:00',
                AgentState.RUNNING: '2024-11-20T23:37:37.594312+00:00',
            },
            agent_version="1.1.0",
            restart_mode=RestartMode.IN_PROCESS_RESTART,
            ip_version="2025-01-10T12:00:00Z",
            ipc_worker_group=ipc_worker_group,
            progress={
                "checkpointProgress": {
                    "progressData": "test_path_4",
                    "progressCount": 4
                }
            },
        )
        resp_txt = str(json.dumps(status_resp, cls=StatusResponseJSONEncoder))
        print(resp_txt)
        assert re.search(r'"status": "faulted"', resp_txt) is not None
        transition_regex = (
            r'"transitions": \{'
            r'"READY": "\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}\+\d{2}:\d{2}", '
            r'"RUNNING": "\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}\+\d{2}:\d{2}"\}, '
        )
        assert re.search(transition_regex, resp_txt) is not None
        assert re.search(r'"reason": "ProcessStateFailure_Ranks0"',
                         resp_txt) is not None
        assert re.search(r'"rank_labels": {}', resp_txt) is not None
        assert re.search(
            r'"worker_data": \[\{"rank": 0, "group_rank": 0, "local_rank": 0, "failed": true, "data": "error trace"}]',
            resp_txt) is not None
        assert re.search(r'"restartMode": "process_level_restart"',
                         resp_txt) is not None
        assert re.search(r'"ipversion": "2025-01-10T12:00:00Z"',
                         resp_txt) is not None
        assert re.search(
            r'"progress": {"checkpointProgress": {"progressData": "test_path_4", "progressCount": 4}}',
            resp_txt) is not None
        assert re.search(r'"agent_version": "1.1.0"', resp_txt) is not None
        assert re.search(r'"restartMode": "process_level_restart"',
                         resp_txt) is not None

    def test_ipr_running(self):
        ipc_worker_group = IPCWorkerGroup(local_world_size=4)
        ipc_worker_group.set_data(
            global_rank=1,
            group_rank=1,
            local_rank=1,
            data="global_step=0",
        )
        status_resp = StatusResponse(
            status=AgentState.RUNNING,
            transitions={
                AgentState.READY: '2024-11-20T23:37:17.855065+00:00',
                AgentState.RUNNING: '2024-11-20T23:37:37.594312+00:00',
            },
            reason="RunningStarted",
            agent_version="1.1.0",
            ip_version="2025-01-10T12:00:00Z",
            ipc_worker_group=ipc_worker_group,
            progress={
                "checkpointProgress": {
                    "progressData": "test_path_4",
                    "progressCount": 4
                }
            },
        )
        resp_txt = str(json.dumps(status_resp, cls=StatusResponseJSONEncoder))
        expected = (
            r'\{"status": "running", "transitions": \{'
            r'"READY": "\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}\+\d{2}:\d{2}", '
            r'"RUNNING": "\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}\+\d{2}:\d{2}"\}, "reason": "RunningStarted", '
            r'"worker_data": \[\{"rank": 1, "group_rank": 1, "local_rank": 1, "failed": false, "data": "global_step=0"\}\], '
            r'"rank_labels": {}, "ipversion": "2025-01-10T12:00:00Z", '
            r'"progress": {"checkpointProgress": {"progressData": "test_path_4", "progressCount": 4}}, '
            r'"agent_version": "1.1.0"\}')
        assert re.fullmatch(expected, resp_txt) is not None
