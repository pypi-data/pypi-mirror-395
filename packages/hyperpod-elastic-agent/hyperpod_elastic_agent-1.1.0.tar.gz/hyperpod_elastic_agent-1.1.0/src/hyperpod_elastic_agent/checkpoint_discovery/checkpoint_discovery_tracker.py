from collections import defaultdict
from collections.abc import KeysView
from enum import Enum
from typing import Optional

from ..logging import get_logger

logger = get_logger(__name__)


class CheckpointType(str, Enum):
    """
    Checkpoint types
    """
    MODEL_CHECKPOINT = "model_checkpoint"
    DATA_CHECKPOINT = "data_checkpoint"


class CheckpointData:
    def __init__(
        self,
        step: int,
        path: Optional[str],
        prefix: str,
        checkpoint_type_keys: KeysView[CheckpointType],
    ):
        self._path = path
        self._step = step
        self._prefix = prefix
        self.checkpoint_type_data: dict[CheckpointType, set] = {}
        for k in checkpoint_type_keys :
            self.checkpoint_type_data[k] = set()

    @property
    def prefix(self) -> str:
        return self._prefix

    @property
    def path(self) -> Optional[str]:
        return self._path

    @property
    def step(self) -> int:
        return self._step

    def update(self, rank: int, path: Optional[str], checkpoint_type: CheckpointType):
        if rank in self.checkpoint_type_data[checkpoint_type]:
            logger.warning(f"Rank {rank} already reported for step {self._step}")
        if self.path and path and self.path != path:
            logger.warning(f"Path mismatch for step {self.step}: {path} != {self.path}. Overwriting with {path}")
        if path is not None:
            self._path = path
        self.checkpoint_type_data[checkpoint_type].add(rank)

    def is_complete(self, expected_ranks: dict[CheckpointType, Optional[int]]) -> bool:
        """
        Checks whether checkpoint data is complete
        """
        for k, v in expected_ranks.items():
            # v being None implies we expected some ranks to do checkpointing with
            # checkpoint_type "k" but no clients have been registered with it
            if v is None or (len(self.checkpoint_type_data[k]) != v):
                return False
        return True


class CheckpointPathMetadata:

    def __init__(self, prefix: str, checkpoint_types: dict[CheckpointType,
                                                           Optional[int]]):
        self.prefix = prefix
        self.checkpoint_types = checkpoint_types


class CheckpointTracker:
    """
    Checkpoint Discovery Tracker that will run on Agent. Contains aggragation logic to
    determine latest local (per pod) valid checkpoint
    """

    def __init__(self):
        self.checkpoint_path_metadata: Optional[CheckpointPathMetadata] = None
        self.checkpoint_datas: defaultdict[str, dict[int, CheckpointData]] = defaultdict(dict)
        self.max_valid_checkpoint: Optional[CheckpointData] = None
        self.latest_valid_checkpoints: defaultdict[str, set[CheckpointData]] = defaultdict(set)
        self.progress: dict[dict] = {}

    def _reset(self,):
        self.checkpoint_path_metadata = None
        self.checkpoint_datas = {}
        self.max_valid_checkpoint = None
        self.latest_valid_checkpoints = defaultdict(set)

    @property
    def prefix(self) -> str:
        if not self.checkpoint_path_metadata:
            return ""
        return self.checkpoint_path_metadata.prefix

    def update_checkpoint_info(
            self, prefix: str, checkpoint_types: dict[CheckpointType, Optional[int]]) -> None:
        if not self.progress or prefix not in self.progress:
            self.max_valid_checkpoint = None
        elif self.progress:
            self.max_valid_checkpoint = CheckpointData(
                step=int(self.progress[prefix]["progressCount"]),
                path=self.progress[prefix]["progressData"],
                prefix=prefix,
                checkpoint_type_keys=checkpoint_types.keys()
            )
        if not self.checkpoint_path_metadata or self.checkpoint_path_metadata.prefix != prefix:
            self.checkpoint_path_metadata = CheckpointPathMetadata(prefix, checkpoint_types)
        else:
            for k, v in checkpoint_types.items():
                if v is not None:
                    self.checkpoint_path_metadata.checkpoint_types[k] = v
                    
            
        # Prune all prefixes apart from current one in checkpoint datas
        if prefix not in self.checkpoint_datas:
            self.checkpoint_datas = defaultdict(dict) 
        else:
            defaultdict(dict, {prefix: self.checkpoint_datas[prefix]})

    def update_checkpoint_data(self, rank: int, step: int, path: Optional[str],
                               checkpoint_type: CheckpointType) -> None:

        assert self.checkpoint_path_metadata is not None, (
            "checkpoint_path_metadata must be set before updating checkpoint data"
        )
        if step not in self.checkpoint_datas[self.prefix]:
            self.checkpoint_datas[self.prefix][step] = CheckpointData(
                step, path, self.checkpoint_path_metadata.prefix, self.checkpoint_path_metadata.checkpoint_types.keys())

        checkpoint_data = self.checkpoint_datas[self.prefix][step]
        checkpoint_data.update(rank, path, checkpoint_type)

        if not checkpoint_data.is_complete(self.checkpoint_path_metadata.checkpoint_types):
            return

        self.latest_valid_checkpoints[self.prefix].add(checkpoint_data)
        if self.max_valid_checkpoint is None or step > self.max_valid_checkpoint.step:
            self.max_valid_checkpoint = checkpoint_data

    def get_checkpoint_data(self, step: int) -> Optional[CheckpointData]:
        return self.checkpoint_datas[self.prefix].get(step)
    
    def get_latest_checkpoint_path(self, reset_invalid_ckpts: bool = True) -> Optional[str]:
        if self.max_valid_checkpoint is None:
            if reset_invalid_ckpts:
                self.checkpoint_datas.clear()
            return None
        # Clear all checkpoint data for steps greater than max valid checkpoint
        if reset_invalid_ckpts:
            for step in list(self.checkpoint_datas[self.prefix].keys()):
                if step > self.max_valid_checkpoint.step:
                    del self.checkpoint_datas[self.prefix][step]
        return self.max_valid_checkpoint.path

    def get_latest_valid_checkpoints(self) -> set[CheckpointData]:
        """Get all valid checkpoints"""
        return self.latest_valid_checkpoints[self.prefix]

    def get_completed_ranks(self, step: int,
                            checkpoint_type: CheckpointType) -> set:
        if step in self.checkpoint_datas[self.prefix]:
            return self.checkpoint_datas[self.prefix][step].checkpoint_type_data[
                checkpoint_type]
        return set()
