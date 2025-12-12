import os
import pytest
import shutil
import signal
import tempfile
import torch.distributed.elastic.rendezvous.registry as rdzv_registry
from argparse import ArgumentParser
from hyperpod_elastic_agent import HyperPodRendezvousBackend
from hyperpod_elastic_agent.run import (
    add_additional_hyperpod_args,
    additional_hyperpod_config_from_args,
    main,
    register_hyperpod_rendezvous,
    start_api_server,
)
from torch.distributed.elastic.agent.server import RunResult
from torch.distributed.elastic.agent.server.api import WorkerState
from torch.distributed.elastic.multiprocessing import ProcessFailure, SignalException
from torch.distributed.elastic.multiprocessing.errors import ChildFailedError
from torch.distributed.elastic.rendezvous import RendezvousParameters
from unittest.mock import Mock, patch


class TestRun:

    @classmethod
    def setup_class(cls):
        register_hyperpod_rendezvous()
        cls.custom_args = [
            "--pre-train-script",
            "pre_train.sh",
            "--pre-train-args",
            "'pre_1 pre_2 pre_3'",
            "--post-train-script",
            "post_train.sh",
            "--post-train-args",
            "'post_1 post_2 post_3'",
            "--server-port",
            "9090",
            "--server-log-level",
            "debug",
            "--server-shutdown-timeout",
            "60",
            "--shutdown-signal",
            "SIGTERM",
            "--shutdown-timeout",
            "15",
        ]
        cls.resource_config_dir = tempfile.mkdtemp()
        cls.training_args = [
            "--rdzv-backend",
            "static",
            "--rdzv-conf",
            f"resource_config_dir='{cls.resource_config_dir}'",
            "unit_test_training.sh",
            "Training!!",
        ]

    @classmethod
    def teardown_class(cls):
        shutil.rmtree(cls.resource_config_dir)

    @pytest.fixture
    def mock_agent(self):
        with patch('hyperpod_elastic_agent.run.PLRHyperPodElasticAgent'
                   ) as mock_agent:
            yield mock_agent

    @pytest.fixture
    def ipr_mock_agent(self):
        with patch('hyperpod_elastic_agent.run.IPRHyperPodElasticAgent'
                   ) as ipr_mock_agent:
            yield ipr_mock_agent

    @pytest.fixture
    def mock_agent_api_server(self):
        with patch(
                'hyperpod_elastic_agent.run.HyperPodElasticAgentServer'
        ) as mock_api_server:
            yield mock_api_server

    def test_additional_hyperpod_config_from_args(self):
        parser = ArgumentParser()
        add_additional_hyperpod_args(parser)
        args = parser.parse_args(self.custom_args)
        pre_post_train_config, server_specs, shutdown_config = additional_hyperpod_config_from_args(
            args)
        assert pre_post_train_config.pre_train_script == "pre_train.sh"
        assert pre_post_train_config.pre_train_args == "'pre_1 pre_2 pre_3'"
        assert pre_post_train_config.post_train_script == "post_train.sh"
        assert pre_post_train_config.post_train_args == "'post_1 post_2 post_3'"
        assert shutdown_config.shutdown_timeout == 15
        assert shutdown_config.shutdown_signal == signal.SIGTERM
        assert server_specs["port"] == 9090
        assert server_specs["log_level"] == "debug"
        assert server_specs["timeout_graceful_shutdown"] == 60
        assert server_specs["timeout_keep_alive"] == 5

    @patch.dict(os.environ, {"NNODES": "2"})
    def test_register_hyperpod_rendezvous(self):
        rdzv_parameters = RendezvousParameters(
            backend="hyperpod",
            endpoint="dummy",
            min_nodes=1,
            max_nodes=1,
            run_id="TEST_ID",
            **dict(
                local_world_size=5,
                resource_config_dir=self.resource_config_dir,
            ),
        )
        handler = rdzv_registry.get_rendezvous_handler(rdzv_parameters)
        assert isinstance(handler, HyperPodRendezvousBackend)
        assert handler.get_backend() == "hyperpod"
        assert handler.get_run_id() == "TEST_ID"
        assert handler.local_world_size == 5

    @patch.dict(os.environ, {"NNODES": "2"})
    def test_run_success(
        self,
        mock_agent,
        mock_agent_api_server,
    ):
        mock_agent_instance = mock_agent.return_value
        mock_agent_instance.run = Mock(return_value=RunResult(
            state=WorkerState.SUCCEEDED))
        main(self.custom_args + self.training_args)
        mock_agent.assert_called_once()
        mock_agent_instance.run.assert_called_once()
        mock_agent_api_server.assert_called_once()

    @patch.dict(os.environ, {"NNODES": "2"})
    def test_run_failure(
        self,
        mock_agent,
        mock_agent_api_server,
    ):
        mock_agent_instance = mock_agent.return_value
        run_result = RunResult(state=WorkerState.FAILED,
                               failures={
                                   0:
                                   ProcessFailure(local_rank=0,
                                                  pid=111,
                                                  exitcode=1,
                                                  error_file="dummy")
                               })
        mock_agent_instance.run = Mock(return_value=run_result)
        with pytest.raises(ChildFailedError) as cm:
            main(self.custom_args + self.training_args)
        mock_agent_api_server.assert_called_once()
        assert cm.value.failures == run_result.failures

    def test_run_signal_exception(
        self,
        mock_agent,
    ):
        mock_agent_instance = mock_agent.return_value
        mock_agent_instance.run = Mock(side_effect=SignalException(
            msg="Dummy Exception",
            sigval=signal.SIGINT,
        ))
        with pytest.raises(Exception):
            main(self.custom_args + self.training_args)

    def test_unsupported_elasticity(
        self,
        mock_agent,
    ):
        with pytest.raises(AssertionError) as err:
            main(self.custom_args + ["--nnodes=1:4"] + self.training_args)
        assert str(
            err.value) == "Elastic cluster size is currently not supported"

    @patch.dict(os.environ, {"NNODES": "2"})
    def test_inprocess_restart_flag(self, mock_agent, ipr_mock_agent):
        mock_agent_instance = mock_agent.return_value
        ipr_mock_agent_instance = ipr_mock_agent.return_value

        # Test with --inprocess-restart flag
        ipr_mock_agent_instance.run = Mock(return_value=RunResult(
            state=WorkerState.SUCCEEDED))
        main(self.custom_args + ["--inprocess-restart"] + self.training_args)

        ipr_mock_agent.assert_called_once()
        mock_agent.assert_not_called()

        # Reset mocks
        ipr_mock_agent.reset_mock()
        mock_agent.reset_mock()

        # Test without --inprocess-restart flag
        mock_agent_instance.run = Mock(return_value=RunResult(
            state=WorkerState.SUCCEEDED))
        main(self.custom_args + self.training_args)

        mock_agent.assert_called_once()
        ipr_mock_agent.assert_not_called()

    @patch.dict(os.environ, {"HYPERPOD_ELASTICAGENT_SERVER_MAX_RETRY": "3"})
    def test_start_api_server_launch_failure(
        self,
        mock_agent_api_server,
    ):
        mock_agent = Mock()
        mock_server = Mock()

        mock_agent_api_server.return_value = mock_server
        mock_server.is_alive.return_value = False
        mock_server.started = False

        # Test when server is not alive
        with pytest.raises(
                ValueError,
                match="Exception in launching HyperPodElasticAgentServer"):
            start_api_server(mock_agent, {})

    @patch.dict(os.environ, {"HYPERPOD_ELASTICAGENT_SERVER_MAX_RETRY": "3"})
    @patch('hyperpod_elastic_agent.run.time')
    def test_start_api_server_start_timeout(
        self,
        mock_time,
        mock_agent_api_server,
    ):
        mock_agent = Mock()
        mock_server = Mock()

        mock_agent_api_server.return_value = mock_server
        mock_server.is_alive.return_value = True
        mock_server.started = False
        mock_time.time.side_effect = [0, 10] * 5
        mock_time.sleep = Mock()

        with pytest.raises(
                ValueError,
                match="Failed to launch HyperPodElasticAgentServer within"):
            start_api_server(mock_agent, {})

        mock_server.start.assert_called()
        mock_server.shutdown.assert_called()
