import pytest

from hyperpod_elastic_agent.checkpoint_discovery import CheckpointTracker, CheckpointType

TEST_PATH_PREFIX = "TESTPATH"
NUM_MODEL_CHECKPOINT_RANKS = 8
NUM_DATA_CHECKPOINT_RANKS = 2


class TestCheckpointTracker:

    @pytest.fixture
    def tracker(self):
        checkpoint_tracker = CheckpointTracker()
        checkpoint_types = {
            CheckpointType.MODEL_CHECKPOINT: NUM_MODEL_CHECKPOINT_RANKS,
            CheckpointType.DATA_CHECKPOINT: NUM_DATA_CHECKPOINT_RANKS
        }
        checkpoint_tracker.update_checkpoint_info("TESTPREFIX",
                                                  checkpoint_types)
        return checkpoint_tracker

    def test_single_valid_update(self, tracker: CheckpointTracker):
        tracker.update_checkpoint_data(
            rank=1,
            step=0,
            path=TEST_PATH_PREFIX + "0",
            checkpoint_type=CheckpointType.MODEL_CHECKPOINT)
        assert 0 not in [
            x.step for x in tracker.get_latest_valid_checkpoints()
        ]
        assert tracker.get_completed_ranks(
            0, CheckpointType.MODEL_CHECKPOINT) == {
                1,
            }

    def test_complete_checkpoint(self, tracker: CheckpointTracker):
        # Submit updates for all 8 ranks for model checkpoint
        step = 1000
        for checkpoint_type, N in zip(
            [CheckpointType.MODEL_CHECKPOINT, CheckpointType.DATA_CHECKPOINT],
            [NUM_MODEL_CHECKPOINT_RANKS, NUM_DATA_CHECKPOINT_RANKS]):
            for rank in range(N):
                tracker.update_checkpoint_data(rank=rank,
                                               step=step,
                                               path=TEST_PATH_PREFIX +
                                               f"{step}",
                                               checkpoint_type=checkpoint_type)

        assert step in [x.step for x in tracker.get_latest_valid_checkpoints()]
        assert tracker.get_completed_ranks(
            step, CheckpointType.MODEL_CHECKPOINT) == set(
                range(NUM_MODEL_CHECKPOINT_RANKS))
        assert tracker.get_completed_ranks(
            step, CheckpointType.DATA_CHECKPOINT) == set(
                range(NUM_DATA_CHECKPOINT_RANKS))
        assert tracker.get_latest_checkpoint_path(
        ) == TEST_PATH_PREFIX + f"{step}"

    def test_multiple_steps(self, tracker: CheckpointTracker):
        # Complete step 1000
        for checkpoint_type, N in zip(
            [CheckpointType.MODEL_CHECKPOINT, CheckpointType.DATA_CHECKPOINT],
            [NUM_MODEL_CHECKPOINT_RANKS, NUM_DATA_CHECKPOINT_RANKS]):
            for rank in range(N):
                tracker.update_checkpoint_data(rank=rank,
                                               step=1000,
                                               path=TEST_PATH_PREFIX + "1000",
                                               checkpoint_type=checkpoint_type)

        # Partially complete step 2000
        for rank in range(
                NUM_MODEL_CHECKPOINT_RANKS):  # Only complete model checkpoint
            tracker.update_checkpoint_data(
                rank=rank,
                step=2000,
                path=TEST_PATH_PREFIX + "2000",
                checkpoint_type=CheckpointType.MODEL_CHECKPOINT)

        # Complete step 3000
        for checkpoint_type, N in zip(
            [CheckpointType.MODEL_CHECKPOINT, CheckpointType.DATA_CHECKPOINT],
            [NUM_MODEL_CHECKPOINT_RANKS, NUM_DATA_CHECKPOINT_RANKS]):
            for rank in range(N):
                tracker.update_checkpoint_data(rank=rank,
                                               step=3000,
                                               path=TEST_PATH_PREFIX + "3000",
                                               checkpoint_type=checkpoint_type)

        assert sorted([x.step for x in tracker.get_latest_valid_checkpoints()
                       ]) == [1000, 3000]
        assert tracker.get_completed_ranks(
            2000, CheckpointType.MODEL_CHECKPOINT) == set(range(8))
        assert tracker.get_latest_checkpoint_path(
        ) == TEST_PATH_PREFIX + "3000"

    @pytest.mark.parametrize(
        "step, ranks, checkpoint_type",
        [
            (1000, range(7),
             CheckpointType.MODEL_CHECKPOINT),  # Missing last rank
            (2000, [0, 2, 4, 6
                    ], CheckpointType.MODEL_CHECKPOINT),  # Missing odd ranks
            (3000, [7], CheckpointType.DATA_CHECKPOINT),  # Only last rank
        ])
    def test_incomplete_checkpoints(self, tracker: CheckpointTracker, step,
                                    ranks, checkpoint_type):
        for rank in ranks:
            tracker.update_checkpoint_data(rank=rank,
                                           step=step,
                                           path=TEST_PATH_PREFIX + f"{step}",
                                           checkpoint_type=checkpoint_type)

        assert len(tracker.get_latest_valid_checkpoints()) == 0
        assert len(tracker.get_completed_ranks(step,
                                               checkpoint_type)) == len(ranks)
        assert tracker.get_latest_checkpoint_path() is None

    def test_out_of_order_updates(self, tracker: CheckpointTracker):
        # Complete checkpoint 2000 before 1000
        for step in [2000, 1000]:
            for checkpoint_type, N in zip([
                    CheckpointType.MODEL_CHECKPOINT,
                    CheckpointType.DATA_CHECKPOINT
            ], [NUM_MODEL_CHECKPOINT_RANKS, NUM_DATA_CHECKPOINT_RANKS]):
                for rank in range(N):
                    tracker.update_checkpoint_data(
                        rank=rank,
                        step=step,
                        path=TEST_PATH_PREFIX + f"{step}",
                        checkpoint_type=checkpoint_type)

        assert tracker.max_valid_checkpoint == tracker.get_checkpoint_data(
            2000)
        assert tracker.get_checkpoint_data(1000) is not None
        assert tracker.get_checkpoint_data(2000) is not None
        assert tracker.get_latest_checkpoint_path(
        ) == TEST_PATH_PREFIX + "2000"

    @pytest.mark.parametrize("complete_steps, expected_path",
                             (([], None), ([1000], TEST_PATH_PREFIX + "1000")))
    def test_reset_invalid_ckpts_on_restart(self, tracker: CheckpointTracker,
                                            complete_steps: list,
                                            expected_path: str):
        # Fully complete steps
        for step in complete_steps:
            for checkpoint_type, N in zip([
                    CheckpointType.MODEL_CHECKPOINT,
                    CheckpointType.DATA_CHECKPOINT
            ], [NUM_MODEL_CHECKPOINT_RANKS, NUM_DATA_CHECKPOINT_RANKS]):
                for rank in range(N):
                    tracker.update_checkpoint_data(
                        rank=rank,
                        step=step,
                        path=TEST_PATH_PREFIX + f"{step}",
                        checkpoint_type=checkpoint_type)

        # Partially complete Model checkpoint
        step = 2000
        for checkpoint_type, N in zip(
            [CheckpointType.MODEL_CHECKPOINT, CheckpointType.DATA_CHECKPOINT],
            [NUM_MODEL_CHECKPOINT_RANKS - 1, NUM_DATA_CHECKPOINT_RANKS]):
            for rank in range(N):
                tracker.update_checkpoint_data(rank=rank,
                                               step=step,
                                               path=TEST_PATH_PREFIX +
                                               f"{step}",
                                               checkpoint_type=checkpoint_type)

        path = tracker.get_latest_checkpoint_path()
        assert path == expected_path

        # Partially complete remaining checkpoint
        tracker.update_checkpoint_data(
            rank=NUM_MODEL_CHECKPOINT_RANKS - 1,
            step=step,
            path=TEST_PATH_PREFIX + f"{step}",
            checkpoint_type=CheckpointType.MODEL_CHECKPOINT)
        path = tracker.get_latest_checkpoint_path()
        assert path == expected_path

    def test_none_path_for_data_checkpoint_type(self,
                                                tracker: CheckpointTracker):
        step = 1000
        expected_path = TEST_PATH_PREFIX + f"{step}"
        for rank in range(NUM_MODEL_CHECKPOINT_RANKS):
            tracker.update_checkpoint_data(
                rank=rank,
                step=1000,
                path=expected_path,
                checkpoint_type=CheckpointType.MODEL_CHECKPOINT,
            )
        for rank in range(NUM_DATA_CHECKPOINT_RANKS):
            tracker.update_checkpoint_data(
                rank=rank,
                step=1000,
                path=None,
                checkpoint_type=CheckpointType.DATA_CHECKPOINT,
            )
        path = tracker.get_latest_checkpoint_path()
        assert path == expected_path

    def test_incomplete_num_expected_ranks_info(self, ):
        checkpoint_tracker = CheckpointTracker()

        # Update checkpoint info with Model checkpoint
        checkpoint_tracker.update_checkpoint_info(
            "TESTPREFIX", {
                CheckpointType.MODEL_CHECKPOINT: NUM_MODEL_CHECKPOINT_RANKS,
                CheckpointType.DATA_CHECKPOINT: None,
            })
        # Make updates for model checkpoints
        step = 1000
        expected_path = TEST_PATH_PREFIX + f"{step}"
        for rank in range(NUM_MODEL_CHECKPOINT_RANKS):
            checkpoint_tracker.update_checkpoint_data(
                rank=rank,
                step=step,
                path=expected_path,
                checkpoint_type=CheckpointType.MODEL_CHECKPOINT,
            )
        # Ensure valid checkpoint is not complete without data checkpoint
        path = checkpoint_tracker.get_latest_checkpoint_path(
            reset_invalid_ckpts=False)
        assert path is None

        # Update data checkpoint
        checkpoint_tracker.update_checkpoint_info(
            "TESTPREFIX", {
                CheckpointType.MODEL_CHECKPOINT: None,
                CheckpointType.DATA_CHECKPOINT: NUM_DATA_CHECKPOINT_RANKS,
            })
        for rank in range(NUM_DATA_CHECKPOINT_RANKS):
            checkpoint_tracker.update_checkpoint_data(
                rank=rank,
                step=step,
                path=expected_path,
                checkpoint_type=CheckpointType.DATA_CHECKPOINT,
            )

        path = checkpoint_tracker.get_latest_checkpoint_path()
        assert path == expected_path
