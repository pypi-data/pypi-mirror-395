import os
import signal
import unittest
from unittest.mock import patch, MagicMock

from hyperpod_elastic_agent.elastic_event_handler import (
    _signal_handler,
    elastic_event_detected,
    _signal_received,
)


class TestElasticEventHandler(unittest.TestCase):

    def setUp(self):
        # Reset signal state before each test
        import hyperpod_elastic_agent.elastic_event_handler as eh
        eh._signal_received.clear()
        eh._signal_received[signal.SIGUSR1] = False
        eh._signal_received[signal.SIGTERM] = False

    def test_event_handler_sigusr1(self):
        """Test SIGUSR1 event handler"""
        from hyperpod_elastic_agent.elastic_event_handler import _signal_received
        _signal_handler(signal.SIGUSR1, None)
        self.assertTrue(_signal_received[signal.SIGUSR1])

    def test_event_handler_sigterm(self):
        """Test SIGTERM event handler"""
        from hyperpod_elastic_agent.elastic_event_handler import _signal_received
        _signal_handler(signal.SIGTERM, None)
        self.assertTrue(_signal_received[signal.SIGTERM])

    def test_elastic_event_detected_sigterm(self):
        """Test elastic_event_detected for SIGTERM - should return False (not handled)"""
        from hyperpod_elastic_agent.elastic_event_handler import _signal_received
        _signal_received[signal.SIGTERM] = True
        # SIGTERM is not handled by elastic_event_detected, only SIGUSR1
        self.assertFalse(elastic_event_detected(signal.SIGTERM))

    @patch.dict(os.environ, {'HYPERPOD_SIGNAL_COORDINATION': 'disabled'})
    def test_elastic_event_detected_disabled_mode(self):
        """Test elastic_event_detected in disabled mode"""
        _signal_received[signal.SIGUSR1] = True
        self.assertFalse(elastic_event_detected(signal.SIGUSR1))

    @patch.dict(os.environ, {'HYPERPOD_SIGNAL_COORDINATION': 'invalid'})
    def test_elastic_event_detected_invalid_mode(self):
        """Test elastic_event_detected with invalid coordination mode"""
        # Need to reload module to pick up new env var
        import importlib
        import hyperpod_elastic_agent.elastic_event_handler
        importlib.reload(hyperpod_elastic_agent.elastic_event_handler)
        from hyperpod_elastic_agent.elastic_event_handler import elastic_event_detected, _signal_received
        
        _signal_received[signal.SIGUSR1] = True
        # Invalid coordination mode should return False
        self.assertFalse(elastic_event_detected(signal.SIGUSR1))

    @patch.dict(os.environ, {'HYPERPOD_SIGNAL_COORDINATION': 'distributed'})
    @patch('torch.distributed.is_initialized', return_value=False)
    def test_elastic_event_detected_distributed_not_initialized(self, mock_dist):
        """Test elastic_event_detected in distributed mode when not initialized"""
        import importlib
        import hyperpod_elastic_agent.elastic_event_handler
        importlib.reload(hyperpod_elastic_agent.elastic_event_handler)
        from hyperpod_elastic_agent.elastic_event_handler import elastic_event_detected, _signal_received
        
        _signal_received[signal.SIGUSR1] = True
        self.assertTrue(elastic_event_detected(signal.SIGUSR1))

    @patch.dict(os.environ, {'HYPERPOD_SIGNAL_COORDINATION': 'distributed'})
    @patch('torch.distributed.is_initialized', return_value=True)
    @patch('torch.cuda.is_available', return_value=True)
    @patch('torch.cuda.current_device', return_value=0)
    @patch('torch.tensor')
    @patch('torch.distributed.all_reduce')
    def test_elastic_event_detected_distributed_with_cuda(self, mock_all_reduce, mock_tensor, mock_device, mock_cuda, mock_dist):
        """Test elastic_event_detected in distributed mode with CUDA"""
        import importlib
        import hyperpod_elastic_agent.elastic_event_handler
        importlib.reload(hyperpod_elastic_agent.elastic_event_handler)
        from hyperpod_elastic_agent.elastic_event_handler import elastic_event_detected, _signal_received
        
        mock_signal_tensor = MagicMock()
        mock_signal_tensor.item.return_value = 1.0
        mock_tensor.return_value = mock_signal_tensor
        
        _signal_received[signal.SIGUSR1] = True
        result = elastic_event_detected(signal.SIGUSR1)
        
        self.assertTrue(result)
        mock_all_reduce.assert_called_once()

    @patch.dict(os.environ, {'HYPERPOD_SIGNAL_COORDINATION': 'distributed'})
    @patch('torch.distributed.is_initialized', side_effect=ImportError())
    def test_elastic_event_detected_distributed_import_error(self, mock_dist):
        """Test elastic_event_detected in distributed mode with import error"""
        import importlib
        import hyperpod_elastic_agent.elastic_event_handler
        importlib.reload(hyperpod_elastic_agent.elastic_event_handler)
        from hyperpod_elastic_agent.elastic_event_handler import elastic_event_detected, _signal_received
        
        _signal_received[signal.SIGUSR1] = True
        self.assertTrue(elastic_event_detected(signal.SIGUSR1))

    def test_elastic_event_detected_invalid_coordination_mode_direct(self):
        """Test elastic_event_detected with invalid coordination mode set directly"""
        import hyperpod_elastic_agent.elastic_event_handler as eh
        
        # Temporarily set invalid coordination mode
        original_mode = eh._SIGNAL_COORDINATION_MODE
        eh._SIGNAL_COORDINATION_MODE = 'invalid_mode'
        
        try:
            _signal_received[signal.SIGUSR1] = True
            result = elastic_event_detected(signal.SIGUSR1)
            self.assertFalse(result)
        finally:
            # Restore original mode
            eh._SIGNAL_COORDINATION_MODE = original_mode


if __name__ == '__main__':
    unittest.main()