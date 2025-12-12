import signal
import unittest
from unittest.mock import MagicMock, patch

from hyperpod_elastic_agent.config import ShutdownConfig
from hyperpod_elastic_agent.elastic_agent.plr_hyperpod_elastic_agent import PLRHyperPodElasticAgent
from torch.distributed.elastic.agent.server.api import WorkerGroup, WorkerSpec, WorkerState
from torch.distributed.elastic.multiprocessing import LogsSpecs


class TestTimeoutFunctionality(unittest.TestCase):

    def setUp(self):
        self.spec = MagicMock(spec=WorkerSpec)
        self.spec.role = "test_role"
        self.spec.local_world_size = 1
        self.spec.max_restarts = 3
        self.spec.rdzv_handler = MagicMock()
        self.spec.rdzv_handler.get_run_id.return_value = "test_run"
        
        self.logs_specs = MagicMock(spec=LogsSpecs)
        self.logs_specs.root_log_dir = "/tmp"
        
        self.shutdown_config = ShutdownConfig(
            shutdown_timeout=15,
            shutdown_signal=signal.SIGTERM
        )

    @patch('tempfile.mkdtemp')
    @patch('hyperpod_elastic_agent.elastic_agent.hyperpod_elastic_agent.CheckpointDiscoverySocketServer')
    def test_stop_workers_with_custom_timeout(self, mock_server, mock_mkdtemp):
        """Test _stop_workers stores custom timeout"""
        mock_mkdtemp.return_value = "/tmp/test"
        
        agent = PLRHyperPodElasticAgent(
            spec=self.spec,
            logs_specs=self.logs_specs,
            pre_post_train_config=MagicMock(),
            shutdown_config=self.shutdown_config,
            version="1.0.0"
        )
        
        # Mock the _shutdown method to avoid actual shutdown
        agent._shutdown = MagicMock()
        agent.stop_log_monitoring = MagicMock()
        agent._training_stages_generator = MagicMock(return_value=iter([]))
        
        worker_group = MagicMock(spec=WorkerGroup)
        
        # Set custom timeout using helper method
        agent.set_graceful_shutdown_params(None, 600)
        
        # Test with custom timeout
        agent._stop_workers(worker_group)
        
        # Verify _shutdown was called with timeout parameter
        agent._shutdown.assert_called_once_with(death_sig=signal.SIGTERM, is_restart=False, timeout=600)

    @patch('tempfile.mkdtemp')
    @patch('hyperpod_elastic_agent.elastic_agent.hyperpod_elastic_agent.CheckpointDiscoverySocketServer')
    def test_stop_workers_with_custom_signal(self, mock_server, mock_mkdtemp):
        """Test _stop_workers with custom signal"""
        mock_mkdtemp.return_value = "/tmp/test"
        
        agent = PLRHyperPodElasticAgent(
            spec=self.spec,
            logs_specs=self.logs_specs,
            pre_post_train_config=MagicMock(),
            shutdown_config=self.shutdown_config,
            version="1.0.0"
        )
        
        agent._shutdown = MagicMock()
        agent.stop_log_monitoring = MagicMock()
        agent._training_stages_generator = MagicMock(return_value=iter([]))
        
        worker_group = MagicMock(spec=WorkerGroup)
        
        # Set graceful shutdown using helper method
        agent.set_graceful_shutdown_params(True, None)
        
        # Test with graceful shutdown
        agent._stop_workers(worker_group)
        
        agent._shutdown.assert_called_once_with(death_sig=signal.SIGUSR1, is_restart=False, timeout=None)

    @patch('tempfile.mkdtemp')
    @patch('hyperpod_elastic_agent.elastic_agent.hyperpod_elastic_agent.CheckpointDiscoverySocketServer')
    def test_shutdown_uses_stored_timeout(self, mock_server, mock_mkdtemp):
        """Test _shutdown uses stored timeout from API"""
        mock_mkdtemp.return_value = "/tmp/test"
        
        agent = PLRHyperPodElasticAgent(
            spec=self.spec,
            logs_specs=self.logs_specs,
            pre_post_train_config=MagicMock(),
            shutdown_config=self.shutdown_config,
            version="1.0.0"
        )
        
        # Mock pcontext
        mock_pcontext = MagicMock()
        agent._pcontext = mock_pcontext
        agent._worker_watchdog = None
        agent._health_check_server = None
        agent._rdzv_handler = None
        
        # Test _shutdown with explicit timeout parameter
        agent._shutdown(death_sig=signal.SIGUSR1, timeout=600)
        
        # Verify pcontext.close was called with passed timeout
        mock_pcontext.close.assert_called_once_with(
            death_sig=signal.SIGUSR1,
            timeout=600
        )

    @patch('tempfile.mkdtemp')
    @patch('hyperpod_elastic_agent.elastic_agent.hyperpod_elastic_agent.CheckpointDiscoverySocketServer')
    def test_shutdown_uses_config_timeout_when_no_stored_timeout(self, mock_server, mock_mkdtemp):
        """Test _shutdown uses config timeout when no stored timeout"""
        mock_mkdtemp.return_value = "/tmp/test"
        
        agent = PLRHyperPodElasticAgent(
            spec=self.spec,
            logs_specs=self.logs_specs,
            pre_post_train_config=MagicMock(),
            shutdown_config=self.shutdown_config,
            version="1.0.0"
        )
        
        mock_pcontext = MagicMock()
        agent._pcontext = mock_pcontext
        agent._worker_watchdog = None
        agent._health_check_server = None
        agent._rdzv_handler = None
        
        # No timeout parameter passed
        agent._shutdown(death_sig=signal.SIGTERM)
        
        # Verify pcontext.close was called with config timeout
        mock_pcontext.close.assert_called_once_with(
            death_sig=signal.SIGTERM,
            timeout=15  # from shutdown_config
        )


if __name__ == '__main__':
    unittest.main()