import os
import pytest
import re
import tempfile
import time
import torch.distributed.elastic.rendezvous.registry as rdzv_registry

from hyperpod_elastic_agent.config import PrePostTrainConfig, ShutdownConfig
from hyperpod_elastic_agent.elastic_agent.plr_hyperpod_elastic_agent import PLRHyperPodElasticAgent
from hyperpod_elastic_agent.elastic_agent.ipr_hyperpod_elastic_agent import IPRHyperPodElasticAgent
from hyperpod_elastic_agent.ipc import HyperPodIPCException
from hyperpod_elastic_agent.ipc.util import IPCWorkerGroup, RestartMode
from hyperpod_elastic_agent.logagent.log_agent import LogState, LogEvalResult
from hyperpod_elastic_agent.run import register_hyperpod_rendezvous
from hyperpod_elastic_agent.server.server import AgentState
from dataclasses import dataclass
from torch.distributed.elastic.agent.server.api import RunResult, Worker, WorkerSpec, WorkerState, WorkerGroup
from torch.distributed.elastic.rendezvous import RendezvousParameters
from torch.distributed.elastic.multiprocessing import LogsSpecs, ProcessFailure, Std
from unittest.mock import Mock, patch, create_autospec
from typing import Tuple, Callable


def _echo(msg):
    return msg


@dataclass
class Conf:
    entrypoint: Callable
    local_world_size: int
    args: Tuple = ()
    role: str = "default"
    redirects: Std = Std.NONE
    tee: Std = Std.NONE


RESOURCE_CONFIG_DIR = tempfile.TemporaryDirectory()


class TestHyperPodElasticAgent:

    @pytest.fixture
    def mock_logs_specs(self):
        mock = Mock(spec=LogsSpecs)
        mock._local_ranks_filter = None
        return mock

    @pytest.fixture
    def mock_log_agent(self):
        with patch(
                'hyperpod_elastic_agent.elastic_agent.hyperpod_elastic_agent.LogAgent'
        ) as mock:
            yield mock

    @pytest.fixture
    def mock_start_processes(self):
        with patch(
                'hyperpod_elastic_agent.elastic_agent.hyperpod_elastic_agent.start_processes'
        ) as mock:
            yield mock

    @patch("tempfile.mkdtemp", return_value=RESOURCE_CONFIG_DIR.name)
    @patch.dict(os.environ, {"NNODES": "2"})
    def _create_agent(self, agent_class, mock_logs_specs, mkdtemp):
        node_config = Conf(
            entrypoint=_echo,
            args=("foo", ),
            local_world_size=2,
        )
        additional_conf = {
            "local_world_size": 2,
            "resource_config_dir": RESOURCE_CONFIG_DIR.name,
        }
        rdzv_params = RendezvousParameters(
            backend="hyperpod",
            endpoint="",
            run_id="test_run",
            min_nodes=2,
            max_nodes=2,
            **additional_conf,
        )
        register_hyperpod_rendezvous()
        rdzv_handler = rdzv_registry.get_rendezvous_handler(rdzv_params)
        self.worker_spec = WorkerSpec(
            role=node_config.role,
            local_world_size=node_config.local_world_size,
            entrypoint=node_config.entrypoint,
            args=node_config.args,
            rdzv_handler=rdzv_handler,
            max_restarts=0,
            monitor_interval=0.01,
            master_addr=None,
            master_port=None,
        )
        pre_post_train_config = PrePostTrainConfig(
            pre_train_script="pre-train-script.sh",
            post_train_script="post-train-script.sh",
        )
        shutdown_config = ShutdownConfig(
            shutdown_timeout=15,
            shutdown_signal="SIGKILL",
        )
        version = "1.1.0"
        ipr_args = {"inprocess_timeout": 120}
        return agent_class(
            self.worker_spec,
            mock_logs_specs,
            pre_post_train_config,
            shutdown_config,
            version,
            **ipr_args,
        )

    @pytest.fixture
    def plr_agent(self, mock_logs_specs, mock_log_agent):
        agent = self._create_agent(
            PLRHyperPodElasticAgent,
            mock_logs_specs,
        )
        assert agent.version == "1.1.0"
        assert agent.get_restart_mode() == RestartMode.PROCESS_LEVEL_RESTART.value
        return agent

    @pytest.fixture
    def ipr_agent(self, mock_logs_specs, mock_log_agent):
        agent = self._create_agent(
            IPRHyperPodElasticAgent,
            mock_logs_specs,
        )
        assert agent.version == "1.1.0"
        assert agent.get_restart_mode() == RestartMode.IN_PROCESS_RESTART.value
        return agent

    @pytest.fixture(params=[
        pytest.param(PLRHyperPodElasticAgent, id="PLR"),
        pytest.param(IPRHyperPodElasticAgent, id="IPR")
    ])
    def agent(self, request, mock_logs_specs, mock_log_agent):
        return self._create_agent(
            request.param,
            mock_logs_specs,
        )

    def test_init(self, agent, mock_log_agent):
        if isinstance(agent, PLRHyperPodElasticAgent):
            assert agent._agent_state == AgentState.READY
        elif isinstance(agent, IPRHyperPodElasticAgent):
            assert agent._agent_state == AgentState.INIT

    def test_get_restart_mode(self, agent):
        """Test that each agent type returns the correct restart mode."""
        if isinstance(agent, PLRHyperPodElasticAgent):
            assert agent.get_restart_mode() == "process_level_restart"
        elif isinstance(agent, IPRHyperPodElasticAgent):
            assert agent.get_restart_mode() == "in_process_restart"

    def test_repr(self, agent):
        if isinstance(agent, PLRHyperPodElasticAgent):
            assert repr(agent).startswith("PLRHyperPodElasticAgent(")
        elif isinstance(agent, IPRHyperPodElasticAgent):
            assert repr(agent).startswith("IPRHyperPodElasticAgent(")

    def test_stop_workers(self, agent):
        worker_group = WorkerGroup(spec=self.worker_spec)
        agent._stop_workers(worker_group)
        assert worker_group.state == WorkerState.INIT
        if isinstance(agent, PLRHyperPodElasticAgent):
            assert agent._agent_state == AgentState.READY
        elif isinstance(agent, IPRHyperPodElasticAgent):
            assert agent._agent_state == AgentState.INIT
        assert agent.priority == False

    def test_initialize_workers(self, mock_start_processes, agent,
                                mock_log_agent):
        worker_group = agent.get_worker_group()
        agent._initialize_workers(worker_group)
        time.sleep(self.worker_spec.monitor_interval)
        mock_start_processes.assert_called_once()
        assert worker_group.state == WorkerState.HEALTHY
        mock_log_agent.assert_called_once()

    def test_ipr_pause_workers(self, ipr_agent, mock_start_processes):
        mock_ipc_server = Mock()
        mock_ipc_server.send_fault.return_value = True
        mock_ipc_server.get_ranks_at_barrier.return_value = True
        ipr_agent._ipc_server = mock_ipc_server

        ipr_agent.set_agent_state(AgentState.READY)
        ipr_agent.set_agent_state(AgentState.RUNNING)
        assert ipr_agent._agent_state == AgentState.RUNNING
        worker_group = ipr_agent.get_worker_group()
        ipr_agent._initialize_workers(worker_group)
        time.sleep(self.worker_spec.monitor_interval)
        assert worker_group.state == WorkerState.HEALTHY

        # Simulate failure on another node - infra sends /stop signal
        ipr_agent.set_agent_state(AgentState.STOPPING)
        ipr_agent._pause_workers(worker_group)
        # Make sure agent state goes back to READY
        assert ipr_agent._agent_state == AgentState.READY
        assert ipr_agent.priority == True
        mock_ipc_server.send_fault.assert_called_once()
        mock_ipc_server.get_ranks_at_barrier.assert_called_once()

    @patch.object(IPRHyperPodElasticAgent, '_pause_workers')
    @patch.object(IPRHyperPodElasticAgent, '_stop_workers')
    def test_ipr_pause_or_stop_workers(
        self,
        mock_stop_workers,
        mock_pause_workers,
        ipr_agent,
        mock_start_processes,
    ):
        # Begin pre-train script
        next(ipr_agent._training_stages_gen)
        ipr_agent._pause_or_stop_workers(ipr_agent._worker_group)
        # Should not stop or pause for pretrain
        mock_pause_workers.assert_not_called()
        mock_stop_workers.assert_not_called()

        # Begin training script
        next(ipr_agent._training_stages_gen)
        ipr_agent._pause_or_stop_workers(ipr_agent._worker_group)
        # Should pause workers during training
        mock_pause_workers.assert_called_once()

        # Begin post-train script
        next(ipr_agent._training_stages_gen)
        ipr_agent._pause_or_stop_workers(ipr_agent._worker_group)
        # Should stop workers during post-training
        mock_stop_workers.assert_called_once()

    @patch(
        'hyperpod_elastic_agent.elastic_agent.hyperpod_elastic_agent.LocalElasticAgent.run'
    )
    def test_run(self, mock_super_run, agent):
        agent.run()
        mock_super_run.assert_called_once()

    def test_set_agent_state(self, agent, mock_log_agent):
        if isinstance(agent, IPRHyperPodElasticAgent):
            agent.set_agent_state(AgentState.READY)
        agent.set_agent_state(AgentState.RUNNING)
        assert agent._agent_state == AgentState.RUNNING

    @pytest.mark.parametrize("log_state, reason",
                             [(LogState.HANGING, "LogHang"),
                              (LogState.SLOW, "LogSlow"),
                              (LogState.FAULTED, "LogFault")])
    def test_set_agent_state_fault_log(self, agent, log_state, reason):
        if isinstance(agent, IPRHyperPodElasticAgent):
            agent.set_agent_state(AgentState.READY)
        agent.set_agent_state(AgentState.RUNNING)
        agent._log_agent.log_eval_results = [
            LogEvalResult(log_state=log_state, rule_name_log_line={"logrule": "test log line"})
        ]
        agent.set_agent_state_fault()
        assert agent._agent_reason.startswith(reason)
        assert re.search(r'logrule', agent._agent_message) is not None
        assert agent._agent_state == AgentState.FAULTED

    @pytest.mark.parametrize("worker_state, reason",
                             [(WorkerState.FAILED, "WorkerCrash"),
                              (WorkerState.UNHEALTHY, "WorkerUnhealthy")])
    def test_set_agent_state_fault_worker(self, agent, worker_state, reason):
        if isinstance(agent, IPRHyperPodElasticAgent):
            agent.set_agent_state(AgentState.READY)
        agent.set_agent_state(AgentState.RUNNING)
        proc_failure_0 = ProcessFailure(
            local_rank=0,
            pid=111,
            exitcode=1,
            error_file="/tmp/hyperpod/none_2o6jvae_/attempt_0/0/error.json",
        )
        proc_failure_1 = ProcessFailure(
            local_rank=1,
            pid=123,
            exitcode=1,
            error_file="<N/A>",
        )
        agent._run_result = RunResult(state=worker_state,
                                      failures={
                                          0: proc_failure_0,
                                          1: proc_failure_1
                                      },
                                      return_values={})

        agent.set_agent_state_fault()
        assert agent._agent_reason == reason
        assert re.search(r'exited with code', agent._agent_message) is not None
        assert agent._agent_state == AgentState.FAULTED

    def test_set_agent_state_fault_unknown(self, agent):
        if isinstance(agent, IPRHyperPodElasticAgent):
            agent.set_agent_state(AgentState.READY)
        agent.set_agent_state(AgentState.RUNNING)
        agent.set_agent_state_fault()
        assert agent._agent_reason == "WorkerFault"
        assert agent._agent_state == AgentState.FAULTED

    def test_set_agent_state_fault_ipc(self, ipr_agent):
        ipr_agent.set_agent_state(AgentState.READY)
        ipr_agent.set_agent_state(AgentState.RUNNING)
        mock_ipc_server = Mock()
        ipr_agent._ipc_server = mock_ipc_server
        ipc_wg = IPCWorkerGroup(local_world_size=1)
        ipc_wg.set_data(
            group_rank=0,
            global_rank=0,
            local_rank=0,
            data='"0": "faultData"',
        )
        ipc_wg.fail_rank(
            group_rank=0,
            global_rank=0,
            local_rank=0,
            restart_mode=RestartMode.LOCAL_PRL,
            reason="test_reason",
            message="test_message",
        )
        mock_ipc_server.ipc_wg = ipc_wg
        ipr_agent.set_agent_state_fault()
        assert ipr_agent._agent_reason == "test_reason"
        assert ipr_agent._agent_message == "test_message"
        assert ipr_agent._agent_state == AgentState.FAULTED

    def test_set_agent_state_fault_ipc_default(self, ipr_agent):
        ipr_agent.set_agent_state(AgentState.READY)
        ipr_agent.set_agent_state(AgentState.RUNNING)
        mock_ipc_server = Mock()
        ipr_agent._ipc_server = mock_ipc_server
        ipc_wg = IPCWorkerGroup(local_world_size=1)
        ipc_wg.fail_rank(
            group_rank=0,
            global_rank=0,
            local_rank=0,
            restart_mode=RestartMode.LOCAL_PRL,
        )
        mock_ipc_server.ipc_wg = ipc_wg
        ipr_agent.set_agent_state_fault()
        assert ipr_agent._agent_reason == "WorkerReportedFault"
        assert ipr_agent._agent_state == AgentState.FAULTED

    def test_get_agent_state_info(self, agent):
        if isinstance(agent, IPRHyperPodElasticAgent):
            agent.set_agent_state(AgentState.READY)
        agent.set_agent_state(AgentState.RUNNING)
        agent_info = agent.get_agent_state_info()
        assert agent_info.state == AgentState.RUNNING
        assert all(state in agent_info.transitions
                   for state in (AgentState.READY, AgentState.RUNNING))

    def test_get_run_result(self, agent):
        assert agent.get_run_result() == agent._run_result

    def test_shutdown(self, agent):
        agent._shutdown()
        assert agent._pcontext is None
        if isinstance(agent, PLRHyperPodElasticAgent):
            assert agent._agent_state == AgentState.READY
        elif isinstance(agent, IPRHyperPodElasticAgent):
            assert agent._agent_state == AgentState.INIT

    def test_training_stages_generator(self, mock_start_processes,
                                       mock_log_agent, agent):
        stages = agent._training_stages_generator()
        agent.update_rendezvous_info(
            rank=0,
            nnodes=2,
            fault_count=23,
            master_addr="192.168.111.1",
            master_port=23456,
            ip_version="2025-01-10T12:00:00Z",
            rank_ips=[
                {
                    "ip": "192.168.111.1",
                    "rank": 0,
                },
            ],
        )

        # Pre-train stage
        next(stages)
        agent_info = agent.get_agent_state_info()
        assert agent._worker_group.state == WorkerState.HEALTHY
        assert agent_info.ip_version == "2025-01-10T12:00:00Z"
        assert mock_start_processes.call_args.kwargs["name"] == "default"
        assert mock_start_processes.call_args.kwargs[
            "entrypoint"] == "pre-train-script.sh"
        mock_start_processes.reset_mock()

        # Training stage
        next(stages)
        assert agent._worker_group.state == WorkerState.HEALTHY
        assert mock_start_processes.call_args.kwargs["name"] == "default"
        assert mock_start_processes.call_args.kwargs["args"] == {
            0: ('foo', ),
            1: ('foo', )
        }
        assert mock_start_processes.call_args.kwargs["envs"][0][
            "TORCHELASTIC_RESTART_COUNT"] == "23"
        assert mock_start_processes.call_args.kwargs["envs"][0][
            "JOB_RESTART_COUNT"] == "23"
        assert mock_start_processes.call_args.kwargs["envs"][0][
            "MASTER_ADDR"] == "192.168.111.1"
        assert mock_start_processes.call_args.kwargs["envs"][0][
            "MASTER_PORT"] == "23456"
        assert mock_start_processes.call_args.kwargs["entrypoint"] == _echo

        # Post-train stage
        mock_start_processes.reset_mock()
        next(stages)
        assert agent._worker_group.state == WorkerState.HEALTHY
        assert mock_start_processes.call_args.kwargs["name"] == "default"
        assert mock_start_processes.call_args.kwargs[
            "entrypoint"] == "post-train-script.sh"

        # Generator should be exhausted
        with pytest.raises(StopIteration):
            next(stages)

    @patch(
        'hyperpod_elastic_agent.elastic_agent.plr_hyperpod_elastic_agent.time.sleep'
    )
    def test_invoke_run(self, mock_sleep, mock_start_processes, agent):
        agent._monitor_workers = Mock()
        agent._monitor_workers.side_effect = [
            RunResult(state=WorkerState.INIT),
            # Pre-train
            RunResult(state=WorkerState.SUCCEEDED),
            # Train
            RunResult(state=WorkerState.SUCCEEDED),
            # Post-train
            RunResult(state=WorkerState.SUCCEEDED),
        ]
        # Forcing out of _invoke_run loop through an exception
        mock_sleep.side_effect = [None, None, None, None, Exception("Forced")]

        if isinstance(agent, IPRHyperPodElasticAgent):
            agent.set_agent_state(AgentState.READY)
        agent.set_agent_state(AgentState.RUNNING)
        agent.can_start = True
        with pytest.raises(Exception, match="Forced"):
            agent._invoke_run()
        agent_info = agent.get_agent_state_info()
        assert agent_info.state == AgentState.COMPLETED
        assert mock_start_processes.call_count == 3

    @patch(
        'hyperpod_elastic_agent.elastic_agent.plr_hyperpod_elastic_agent.time.sleep'
    )
    def test_invoke_run_stage_failure_plr(
        self,
        mock_sleep,
        mock_start_processes,
        plr_agent,
    ):
        mock_ipc_server = Mock()
        mock_ipc_server.is_failed = False
        plr_agent._ipc_server = mock_ipc_server

        plr_agent._monitor_workers = Mock()
        plr_agent._monitor_workers.side_effect = [
            RunResult(state=WorkerState.INIT),
            # Pre-train
            RunResult(state=WorkerState.HEALTHY),
            RunResult(state=WorkerState.SUCCEEDED),
            # Train
            RunResult(state=WorkerState.UNKNOWN),
            RunResult(state=WorkerState.FAILED),
        ]
        # Forcing out of _invoke_run loop through an exception
        mock_sleep.side_effect = [
            None, None, None, None, None,
            Exception("Forced")
        ]
        plr_agent.update_rendezvous_info(
            rank=0,
            nnodes=2,
            fault_count=23,
            master_addr="192.168.111.1",
            master_port=23456,
            ip_version="2025-01-10T12:00:00Z",
            rank_ips=[{
                "ip": "192.168.111.1",
                "rank": 0,
            }, {
                "ip": "192.168.111.1",
                "rank": 1,
            }],
        )
        plr_agent.set_agent_state(AgentState.RUNNING)
        plr_agent.can_start = True
        with pytest.raises(Exception, match="Forced"):
            plr_agent._invoke_run()
        agent_info = plr_agent.get_agent_state_info()
        assert agent_info.state == AgentState.FAULTED
        assert mock_start_processes.call_count == 2

    @patch(
        'hyperpod_elastic_agent.elastic_agent.plr_hyperpod_elastic_agent.time.sleep'
    )
    def test_invoke_run_stage_failure_ipr(
        self,
        mock_sleep,
        mock_start_processes,
        ipr_agent,
    ):
        mock_ipc_server = Mock()
        mock_ipc_server.is_failed = False
        ipr_agent._ipc_server = mock_ipc_server

        ipr_agent._monitor_workers = Mock()
        ipr_agent._monitor_workers.side_effect = [
            RunResult(state=WorkerState.INIT),
            # Pre-train
            RunResult(state=WorkerState.HEALTHY),
        ]
        # Forcing out of _invoke_run loop through an exception
        mock_sleep.side_effect = [None, None, Exception("Forced")]
        ipr_agent.set_agent_state(AgentState.READY)
        ipr_agent.set_agent_state(AgentState.RUNNING)
        ipr_agent.can_start = True
        with pytest.raises(Exception, match="Forced"):
            ipr_agent._invoke_run()
        agent_info = ipr_agent.get_agent_state_info()
        assert agent_info.state == AgentState.FAULTED
        assert mock_start_processes.call_count == 1

    @patch(
        'hyperpod_elastic_agent.elastic_agent.ipr_hyperpod_elastic_agent.time.sleep'
    )
    def test_invoke_run_ipr(self, mock_sleep, mock_start_processes, ipr_agent):
        mock_ipc_server = Mock()
        mock_ipc_server.send_start.return_value = True
        mock_ipc_server.get_ranks_at_barrier.return_value = True
        mock_ipc_server.passed_barrier.return_value = False
        ipr_agent._ipc_server = mock_ipc_server

        # This test validates that IPR agent reaches READY state without signal from operator
        ipr_agent._monitor_workers = Mock()
        ipr_agent._monitor_workers.side_effect = [
            RunResult(state=WorkerState.INIT),
            # Pre-train
            RunResult(state=WorkerState.SUCCEEDED),
            # Train
            RunResult(state=WorkerState.HEALTHY),
            RunResult(state=WorkerState.HEALTHY),
        ]
        # Forcing out of _invoke_run loop through an exception
        mock_sleep.side_effect = [None, None, None, None, Exception("Forced")]

        with pytest.raises(Exception, match="Forced"):
            ipr_agent._invoke_run()
        # After pre-training succeeds and training script is started, Agent should be in READY state
        agent_info = ipr_agent.get_agent_state_info()
        assert agent_info.state == AgentState.READY
        assert mock_start_processes.call_count == 2
        mock_ipc_server.get_ranks_at_barrier.assert_called_once()

    @patch(
        'hyperpod_elastic_agent.elastic_agent.ipr_hyperpod_elastic_agent.time.sleep'
    )
    @pytest.mark.skip(
        reason=
        "Test passes locally but fails during remote build. Disabling for now")
    def test_invoke_run_ipr_stop(self, mock_sleep, mock_start_processes,
                                 ipr_agent):
        # This test validates receiving a /stop signal while processes are healthy
        # resets AgentState back to READY

        original_pause_workers = ipr_agent._pause_workers
        pause_workers_spy = create_autospec(
            original_pause_workers,
            wraps=original_pause_workers,
        )
        ipr_agent._pause_workers = pause_workers_spy

        ipr_agent._monitor_workers = Mock()
        ipr_agent._monitor_workers.side_effect = [
            # Train
            RunResult(state=WorkerState.HEALTHY),
            RunResult(state=WorkerState.HEALTHY),
        ]
        # Forcing out of _invoke_run loop through an exception
        mock_sleep.side_effect = [None, Exception("Forced")]

        # Simulate receiving a /stop signal while in RUNNING state
        next(ipr_agent._training_stages_gen)
        next(ipr_agent._training_stages_gen)
        ipr_agent.set_agent_state(AgentState.READY)
        ipr_agent.set_agent_state(AgentState.RUNNING)
        ipr_agent._passed_barrier = True
        ipr_agent.set_agent_state(AgentState.STOPPING)
        assert ipr_agent._agent_state == AgentState.STOPPING
        assert ipr_agent._passed_barrier == True

        with pytest.raises(Exception, match="Forced"):
            ipr_agent._invoke_run()
        # Agent should go back to READY state
        agent_info = ipr_agent.get_agent_state_info()
        assert agent_info.state == AgentState.READY
        assert ipr_agent._passed_barrier == False
        assert mock_start_processes.call_count == 2
        # _pause_workers should be called
        pause_workers_spy.assert_called_once()

    @patch(
        'hyperpod_elastic_agent.elastic_agent.ipr_hyperpod_elastic_agent.time.sleep'
    )
    def test_invoke_run_plr_in_ipr_mode(
        self,
        mock_sleep,
        mock_start_processes,
        ipr_agent,
    ):
        mock_ipc_server = Mock()
        ipr_agent._ipc_server = mock_ipc_server
        ipr_agent._monitor_workers = Mock()
        ipr_agent._process_level_start = True
        ipr_agent._monitor_workers.side_effect = [
            # Train
            RunResult(state=WorkerState.HEALTHY),
            RunResult(state=WorkerState.HEALTHY),
        ]
        ipr_agent._agent_state = AgentState.READY
        # Forcing out of _invoke_run loop through an exception
        mock_sleep.side_effect = [None, Exception("Forced")]
        with pytest.raises(Exception, match="Forced"):
            ipr_agent._invoke_run()
        mock_ipc_server.clear_clients.assert_called_once()

    def test_send_rank_info_failure(
        self,
        mock_start_processes,
        ipr_agent,
    ):
        mock_ipc_server = Mock()
        mock_ipc_server.send_rank_info.side_effect = [
            HyperPodIPCException("Fail")
        ]
        ipr_agent._ipc_server = mock_ipc_server

        ipr_agent.update_rendezvous_info(
            rank=0,
            nnodes=2,
            fault_count=23,
            master_addr="192.168.111.1",
            master_port=23456,
            ip_version="2025-01-10T12:12:00Z",
            rank_ips=[{
                "ip": "192.168.111.1",
                "rank": 0,
            }, {
                "ip": "192.168.111.1",
                "rank": 1,
            }],
        )
        assert ipr_agent._rdzv_handler.ip_version == "2025-01-10T12:12:00Z"
        ipr_agent.send_rank_info(rank=4)
        agent_info = ipr_agent.get_agent_state_info()
        assert agent_info.ip_version is None

    @patch(
        "hyperpod_elastic_agent.elastic_agent.ipr_hyperpod_elastic_agent.logger"
    )
    def test_send_rank_info_workers_not_started(
        self,
        mock_logger,
        mock_start_processes,
        ipr_agent,
    ):
        mock_ipc_server = Mock()
        ipr_agent._ipc_server = mock_ipc_server
        ipr_agent._worker_group.workers = [
            Worker(
                local_rank=local_rank,
                global_rank=local_rank,
                role_rank=0,
                world_size=4,
                role_world_size=4,
            ) for local_rank in range(4)
        ]
        ipr_agent.send_rank_info(rank=2)
        mock_logger.debug.assert_called_once_with(
            "Failed to send rank info to clients: Workers not initialized yet, cannot apply updates from operator."
        )
        agent_info = ipr_agent.get_agent_state_info()
        assert agent_info.ip_version is None

    def test_handle_spare_update(self, ipr_agent):
        # Test spare transition behavior
        assert ipr_agent.spare
        ipr_agent.handle_spare_update(False, 1)
        assert not ipr_agent._process_level_start
        ipr_agent.handle_spare_update(True, 1)
        assert ipr_agent._process_level_start

        # Test startup priority behavior
        ipr_agent._agent_state = AgentState.READY
        ipr_agent.handle_spare_update(False, 0)
        assert not ipr_agent.priority
        ipr_agent._agent_state = AgentState.INIT
        ipr_agent.handle_spare_update(True, 0)
        assert not ipr_agent.priority
        ipr_agent.handle_spare_update(False, 0)
        assert ipr_agent.priority

    def test_handle_healthy_state(self, ipr_agent):
        for idx, worker in enumerate(ipr_agent._worker_group.workers):
            worker.id = idx
        wg = ipr_agent._worker_group
        mock_ipc_server = Mock()
        ipr_agent._ipc_server = mock_ipc_server
        assert ipr_agent._agent_state == AgentState.INIT
        ipr_agent.set_agent_state(AgentState.READY)
        ipr_agent.set_agent_state(AgentState.RUNNING)
        # Simulate start conditions
        mock_ipc_server.at_barrier.return_value, ipr_agent.can_start = True, True
        ipr_agent._handle_healthy_state(wg.spec.role, wg)
        assert ipr_agent._agent_state == AgentState.RUNNING
        mock_ipc_server.reset_mock()
        # Simulate local PLR conditions
        mock_ipc_server.at_barrier.return_value = False
        ipr_agent._process_level_start = False
        assert not ipr_agent._process_level_start
        ipc_wg = IPCWorkerGroup(local_world_size=1)
        ipc_wg.set_data(
            group_rank=0,
            global_rank=0,
            local_rank=0,
            data='"0": "faultData"',
        )
        ipc_wg.fail_rank(
            group_rank=0,
            global_rank=0,
            local_rank=0,
            restart_mode=RestartMode.LOCAL_PRL,
        )
        mock_ipc_server.ipc_wg = ipc_wg
        ipr_agent._handle_healthy_state(wg.spec.role, wg)
        assert ipr_agent._agent_state == AgentState.FAULTED
        assert ipr_agent._process_level_start
        # Simulate global PLR conditions
        ipc_wg.reset()
        assert not ipc_wg.is_failed
        ipr_agent._process_level_start = False
        ipr_agent.set_restart_mode("process_level_restart")
        assert ipr_agent._process_level_start

    def test_get_log_agent_state(self, agent, mock_log_agent):
        from hyperpod_elastic_agent.logagent.log_agent import LogState, LogEvalResult

        # Test with FAULTED state - should be prioritized over other states
        mock_log_agent_instance = mock_log_agent.return_value
        mock_log_agent_instance.log_eval_results = [
            LogEvalResult(log_state=LogState.FAULTED,
                          rule_name_log_line={"OutOfMemoryError": "test log line"}),
            LogEvalResult(log_state=LogState.HANGING, rule_name_log_line={"SlowRule": "test log line"}),
            LogEvalResult(log_state=LogState.SLOW, rule_name_log_line={"AnotherRule": "test log line"})
        ]
        mock_log_agent_instance.log_state = [
            LogState.FAULTED, LogState.HANGING, LogState.SLOW
        ]

        log_state, rule_name_log_line = agent.get_log_agent_state()
        assert log_state == LogState.FAULTED
        assert list(rule_name_log_line.keys()) == ["OutOfMemoryError"]

        # Test with HANGING state - should be prioritized over SLOW
        mock_log_agent_instance.log_eval_results = [
            LogEvalResult(log_state=LogState.HANGING, rule_name_log_line={"SlowRule": "test log line"}),
            LogEvalResult(log_state=LogState.SLOW, rule_name_log_line={"AnotherRule": "test log line"}),
            LogEvalResult(log_state=LogState.HEALTHY, rule_name_log_line=None)
        ]
        mock_log_agent_instance.log_state = [
            LogState.HANGING, LogState.SLOW, LogState.HEALTHY
        ]

        log_state, rule_name_log_line = agent.get_log_agent_state()
        assert log_state == LogState.HANGING
        assert list(rule_name_log_line.keys()) == ["SlowRule"]

        # Test with SLOW state
        mock_log_agent_instance.log_eval_results = [
            LogEvalResult(log_state=LogState.SLOW, rule_name_log_line={"AnotherRule": "test log line"}),
            LogEvalResult(log_state=LogState.HEALTHY, rule_name_log_line=None),
            LogEvalResult(log_state=LogState.HEALTHY, rule_name_log_line=None)
        ]
        mock_log_agent_instance.log_state = [
            LogState.SLOW, LogState.HEALTHY, LogState.HEALTHY
        ]

        log_state, rule_name_log_line = agent.get_log_agent_state()
        assert log_state == LogState.SLOW
        assert list(rule_name_log_line.keys()) == ["AnotherRule"]

        # Test with WAITING state
        mock_log_agent_instance.log_eval_results = [
            LogEvalResult(log_state=LogState.WAITING, rule_name_log_line=None),
            LogEvalResult(log_state=LogState.HEALTHY, rule_name_log_line=None),
            LogEvalResult(log_state=LogState.HEALTHY, rule_name_log_line=None)
        ]
        mock_log_agent_instance.log_state = [
            LogState.WAITING, LogState.HEALTHY, LogState.HEALTHY
        ]

        log_state, rule_name_log_line = agent.get_log_agent_state()
        assert log_state == LogState.WAITING
        assert rule_name_log_line is None

        # Test with all HEALTHY state
        mock_log_agent_instance.log_eval_results = [
            LogEvalResult(log_state=LogState.HEALTHY, rule_name_log_line=None),
            LogEvalResult(log_state=LogState.HEALTHY, rule_name_log_line=None),
            LogEvalResult(log_state=LogState.HEALTHY, rule_name_log_line=None)
        ]
        mock_log_agent_instance.log_state = [
            LogState.HEALTHY, LogState.HEALTHY, LogState.HEALTHY
        ]

        log_state, rule_name_log_line = agent.get_log_agent_state()
        assert log_state == LogState.HEALTHY
        assert rule_name_log_line is None

    def test_monitor_workers_with_faulted_state(self, agent, mock_log_agent):
        from hyperpod_elastic_agent.logagent.log_agent import LogState, LogEvalResult
        from torch.distributed.elastic.agent.server.api import WorkerState

        # Setup worker group
        worker_group = agent.get_worker_group()
        worker_group.state = WorkerState.HEALTHY

        # Setup mock for LocalElasticAgent._monitor_workers
        with patch(
                'torch.distributed.elastic.agent.server.local_elastic_agent.LocalElasticAgent._monitor_workers'
        ) as mock_super_monitor:
            mock_super_monitor.return_value = RunResult(
                state=WorkerState.HEALTHY)

            # Test with FAULTED log state
            mock_log_agent_instance = mock_log_agent.return_value
            mock_log_agent_instance.log_eval_results = [
                LogEvalResult(log_state=LogState.FAULTED,
                              rule_name_log_line={"OutOfMemoryError": "test log line"})
            ]

            # Set the log_eval_results directly on the agent's _log_agent instance
            agent._log_agent = mock_log_agent_instance

            # Mock self._pcontext to be not None to avoid early return in _monitor_workers
            agent._pcontext = Mock()

            # Reset the mock for super()._monitor_workers to ensure it returns HEALTHY
            mock_super_monitor.reset_mock()
            mock_super_monitor.return_value = RunResult(
                state=WorkerState.HEALTHY)

            result = agent._monitor_workers(worker_group)
            # Verify the result
            assert result.state == WorkerState.UNHEALTHY

            # Test with HANGING log state
            mock_log_agent_instance.log_eval_results = [
                LogEvalResult(log_state=LogState.HANGING,
                              rule_name_log_line={"SlowRule": "test log line"}),
                LogEvalResult(log_state=LogState.HEALTHY, rule_name_log_line=None)
            ]

            # Reset the mock for super()._monitor_workers to ensure it returns HEALTHY
            mock_super_monitor.reset_mock()
            mock_super_monitor.return_value = RunResult(
                state=WorkerState.HEALTHY)

            result = agent._monitor_workers(worker_group)
            # Verify the result
            assert result.state == WorkerState.UNHEALTHY

            # Reset the mock for super()._monitor_workers to ensure it returns HEALTHY
            mock_super_monitor.reset_mock()
            mock_super_monitor.return_value = RunResult(
                state=WorkerState.HEALTHY)

            # Test with SLOW log state
            mock_log_agent_instance.log_eval_results = [
                LogEvalResult(log_state=LogState.SLOW,
                              rule_name_log_line={"AnotherRule": "test log line"}),
                LogEvalResult(log_state=LogState.HEALTHY, rule_name_log_line=None)
            ]

            # Reset the mock for super()._monitor_workers to ensure it returns HEALTHY
            mock_super_monitor.reset_mock()
            mock_super_monitor.return_value = RunResult(
                state=WorkerState.HEALTHY)

            result = agent._monitor_workers(worker_group)
            assert result.state == WorkerState.UNHEALTHY

            # Test with all HEALTHY log state
            mock_log_agent_instance.log_eval_results = [
                LogEvalResult(log_state=LogState.HEALTHY, rule_name_log_line=None)
            ]

            # Reset the mock for super()._monitor_workers to ensure it returns HEALTHY
            mock_super_monitor.reset_mock()
            mock_super_monitor.return_value = RunResult(
                state=WorkerState.HEALTHY)

            result = agent._monitor_workers(worker_group)
            # Verify the result
            assert result.state == WorkerState.HEALTHY

    def test_set_restart_mode(self, ipr_agent):
        ipr_agent.set_restart_mode("in_process_restart")
        assert not ipr_agent._process_level_start
        ipr_agent.set_restart_mode("process_level_restart")
        assert ipr_agent._process_level_start
        ipr_agent._process_level_start = False
        ipr_agent.set_restart_mode("local_process_level_restart")
        assert not ipr_agent._process_level_start
        ipr_agent.set_restart_mode("foo_bar")
        assert not ipr_agent._process_level_start

    def test_stop_workers_resets_ipversion(self, ipr_agent):
        ipr_agent.update_rendezvous_info(
            rank=0,
            nnodes=2,
            fault_count=23,
            master_addr="192.168.111.1",
            master_port=23456,
            ip_version="2025-01-10T12:12:00Z",
            rank_ips=[{
                "ip": "192.168.111.1",
                "rank": 0,
            }, {
                "ip": "192.168.111.1",
                "rank": 1,
            }],
        )
        assert ipr_agent._rdzv_handler.ip_version == "2025-01-10T12:12:00Z"
        ipr_agent._stop_workers(ipr_agent._worker_group)
        assert ipr_agent._rdzv_handler.ip_version is None

    @pytest.mark.parametrize("worker_state", [
        WorkerState.INIT,
        WorkerState.HEALTHY
    ])
    def test_start_log_monitoring_valid_worker_states(self, agent, mock_log_agent, worker_state):
        """Test that start_log_monitoring proceeds when worker state is INIT or HEALTHY"""
        # Setup
        agent._worker_group.state = worker_state
        agent._remaining_restarts = 2
        agent._worker_group.spec.max_restarts = 3

        # Mock the log agent instance
        mock_log_agent_instance = mock_log_agent.return_value
        agent._log_agent = mock_log_agent_instance

        # Mock LogAgent.compute_attempt_dir at the module level where it's imported
        with patch('hyperpod_elastic_agent.elastic_agent.hyperpod_elastic_agent.LogAgent.compute_attempt_dir', return_value="/tmp/attempt_1") as mock_compute_dir:
            # Call start_log_monitoring
            agent.start_log_monitoring()

            # Verify LogAgent.start was called with the correct parameters
            mock_log_agent_instance.start.assert_called_once_with(
                "/tmp/attempt_1",
                {0},
                agent._log_monitoring_configuration
            )

            # Verify compute_attempt_dir was called with correct parameters
            mock_compute_dir.assert_called_once_with(
                run_log_dir=getattr(agent._logs_specs, "_run_log_dir", ""),
                attempt_num=1
            )

    @pytest.mark.parametrize("worker_state", [
        WorkerState.SUCCEEDED,
        WorkerState.FAILED,
        WorkerState.UNHEALTHY,
        WorkerState.UNKNOWN
    ])
    def test_start_log_monitoring_invalid_worker_states_skips_monitoring(self, agent, mock_log_agent, worker_state):
        """Test that start_log_monitoring skips when worker state is not INIT or HEALTHY"""
        # Setup
        agent._worker_group.state = worker_state

        # Mock the log agent instance
        mock_log_agent_instance = mock_log_agent.return_value
        agent._log_agent = mock_log_agent_instance

        # Mock logger to capture debug message
        with patch('hyperpod_elastic_agent.elastic_agent.hyperpod_elastic_agent.logger') as mock_logger:
            # Call start_log_monitoring
            agent.start_log_monitoring()

            # Verify debug message was logged
            mock_logger.debug.assert_called_once_with(
                f"Skip starting log monitoring since worker state is {worker_state}"
            )

            # Verify LogAgent.start was NOT called
            mock_log_agent_instance.start.assert_not_called()
