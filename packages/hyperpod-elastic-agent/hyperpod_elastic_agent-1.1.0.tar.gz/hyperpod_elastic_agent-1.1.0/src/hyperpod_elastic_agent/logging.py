import os
import logging
import torch

from typing import Optional


class HyperPodElasticAgentAdapter(logging.LoggerAdapter):
    rank: int = 0
    restart_count: int = 0

    def __init__(self, name="HyperPodElasticAgent"):
        formatter = logging.Formatter(
            fmt="[HyperPodElasticAgent] %(asctime)s [%(levelname)s] "
            "[rank%(rank)s-restart%(restart_count)s] %(pathname)s:%(lineno)s: %(message)s",
        )
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger = logging.getLogger(name)
        logger.setLevel(os.environ.get("LOGLEVEL", logging.INFO))
        logger.handlers.clear()
        logger.propagate = False
        logger.addHandler(handler)
        super().__init__(logger)

    @staticmethod
    def update_run_info(rank: int, restart_count: int):
        HyperPodElasticAgentAdapter.rank = rank
        HyperPodElasticAgentAdapter.restart_count = restart_count

    def process(self, msg, kwargs):
        extra = kwargs.get('extra', {})
        extra['rank'] = self.rank
        extra['restart_count'] = self.restart_count
        kwargs['extra'] = extra
        return msg, kwargs


def get_logger(name: Optional[str] = None):
    """
    Util function to override torch.distributed.elastic.utils.logging.get_logger
    with custom logging configuration.

    Args:
        name: Name of the logger. If no name provided, the name will
              be derived from the call stack.
    """
    return HyperPodElasticAgentAdapter(name)


torch.distributed.elastic.utils.logging.get_logger = get_logger
