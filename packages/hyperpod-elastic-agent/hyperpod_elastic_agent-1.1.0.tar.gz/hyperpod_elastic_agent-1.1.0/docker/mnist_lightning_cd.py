"""Integration test for Checkpoint Discovery."""

# Standard Library
import argparse
import logging
import os
import time
from collections import defaultdict
from functools import wraps

# Third Party
# pylint: disable=import-error,no-name-in-module
import pytorch_lightning as pl
import torch.nn.functional as F
import torch
import torch.multiprocessing as mp
from torch.distributed.elastic.multiprocessing.errors import record
from torch.utils.data import Dataset, DataLoader
from torch.multiprocessing import set_start_method
from torch import nn

# First party
from hyperpod_elastic_agent import CheckpointDiscoverySocketClient
from hyperpod_elastic_agent.checkpoint_discovery import CheckpointType

# pylint: enable=import-error,no-name-in-module

logging.basicConfig(format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# We need to set the MP start method here so that the benchmark instances
# will use the correct mp context when creating their mp.Queue
set_start_method("fork", force=True)


def benchmarkMP_helper(func):
    @wraps(func)
    def wrapper(*args, _queue, **kwargs):
        start_time = time.perf_counter()
        ret_value = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        _queue.put((func.__qualname__, execution_time))
        return ret_value

    return wrapper


class Benchmark:
    def __init__(self, rank):
        self.call_data = defaultdict(list)
        self.rank = rank
        logger.info(f"Benchmark class initialized for rank {self.rank}")

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            logger.debug(
                f"[benchmark][{self.rank}] {func.__qualname__} executed in {execution_time:.4f} seconds"
            )
            # __name__ only resolves function name
            # __qualname__ resolves class name + function name
            # __module__ + '.' + __qual_name resolves module name + qualname
            # use qualname for now
            self.call_data[func.__qualname__].append(execution_time)
            return result

        return wrapper

    def get_stats(self, func):
        if func is None:
            return None

        func_name = func.__qualname__
        logger.debug(f"[benchmark][{self.rank}][get_stats()] func_name: {func_name}")
        if func_name not in self.call_data:
            return {
                "func_name": func_name,
                "rank": self.rank,
                "STATS": "N/A",
            }

        data = self.call_data[func_name]
        return {
            "func_name": func_name,
            "rank": self.rank,
            "call_count": len(data),
            "average_time": sum(data) / len(data),
            "total_time": sum(data),
            "min_time": min(data),
            "max_time": max(data),
        }


class BenchmarkMP(Benchmark):
    # class that supports benchmarking processes launched with MP
    # note: decorated functions need to also be decorated with benchmarkMP_helper
    # which will update the queue in the parent by wrapping the function
    # with a function that takes in an additional keyword arg `_queue`
    # this also requires in the mp.Process to pass in the keyword arg `_queue`
    # pointing to the benchmark classes queue
    def __init__(self, rank):
        super().__init__(rank)
        self.queue = mp.Queue()

    def get_stats(self, func):
        # Process queue when get_stats is called
        while not self.queue.empty():
            func_name, execution_time = self.queue.get()
            logger.debug(
                f"[benchmarkMP][{self.rank}][get_stats()] got from queue: {func_name} with execution time: {execution_time}!"
            )
            self.call_data[func_name].append(execution_time)
        return super().get_stats(func)


def get_test_type_and_case():
    test_type = os.environ.get("TEST_TYPE", "standard")  # [standard, manual_rollback]
    test_case = os.environ.get("TYPE_CASE", "sad")  # [happy, sad]
    return test_type, test_case


def get_test_checkpoint_failure():
    # used for sad path only
    return os.environ.get("TEST_CKPT_FAIL", "data")  # [both, model, data]


def get_test_update_failure():
    # cases for ranks to fail updating CD client
    # 1. all ranks fail to update CD client
    # 2. 1/2 nodes stop reporting
    # 3. 1/2 ranks within each node stop reporting
    # 4. set global ranks overall stop reporting (default to 1 rank)
    #   - uses FAIL_RANKS to determine which ranks to stop reporting
    # used for sad path only
    return os.environ.get(
        "TEST_UPDATE_FAIL", "set"
    )  # [all, half_across_nodes, half_within_nodes, set]


def get_world_size():
    return int(os.environ.get("WORLD_SIZE", -1))


def get_local_world_size():
    return int(os.environ.get("LOCAL_WORLD_SIZE", -1))


def get_rank():
    return int(os.environ.get("RANK", -1))


def get_local_rank():
    return int(os.environ.get("LOCAL_RANK", -1))


def get_ranks_to_fail():
    # Fail for rank 1 by default
    fail_ranks_str = os.environ.get("FAIL_RANKS", "1,")
    fail_ranks = [int(rank) for rank in fail_ranks_str.split(",") if rank]
    return fail_ranks


def get_last_succ_ckpt():
    # get last successful checkpoint before expected failure for sad case
    return int(os.environ.get("LAST_SUCC_CKPT", 300))


def get_current_retry_count():
    # get last successful checkpoint before expected failure for sad case
    return int(os.environ.get("TORCHELASTIC_RESTART_COUNT", "1"))


def log_benchmark_stats():
    logger.info(benchmarkMP.get_stats(_cd_update_model_checkpoint_async))
    logger.info(benchmarkMP.get_stats(_cd_update_data_checkpoint_async))
    logger.info(benchmark.get_stats(cd_get_latest_checkpoint_path))
    logger.info(benchmark.get_stats(get_cd_client))
    logger.info(benchmark.get_stats(MockCDSaveAsync.on_train_batch_end))


benchmark = Benchmark(rank=get_rank())
benchmarkMP = BenchmarkMP(rank=get_rank())


all_processes = defaultdict(list)


class LitMNIST(pl.LightningModule):
    """
    https://swan-gallery.web.cern.ch/notebooks/GPU_and_data/DeepLearning-GPU/PyTorch_Lightning_MNIST.html
    """

    def __init__(self, lr):
        super().__init__()
        self.lr = lr
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.5)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)
        self.loss_fn = nn.CrossEntropyLoss()

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        output = F.log_softmax(x, dim=1)
        return output

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.lr)

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = self.loss_fn(y_hat, y)
        self.log("train_loss", loss)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = self.loss_fn(y_hat, y)
        preds = torch.argmax(y_hat, dim=1)
        accuracy = (preds == y).float().mean()
        self.log("val_loss", loss)
        self.log("val_accuracy", accuracy)


@benchmarkMP
@benchmarkMP_helper
def _cd_update_model_checkpoint_async(cd=None, rank=None, step=None, path=None) -> None:
    # pass in instantiated CD client from main process
    logger.debug(
        f"[MockCDSaveAsync][{rank}] _cd_update_model_checkpoint_async start for rank={rank}, path={path}_{step}, step={step}"
    )
    if cd:
        cd.update(checkpoint_type=CheckpointType.MODEL_CHECKPOINT, step=step, path=f"{path}_{step}")
    logger.debug(
        f"[MockCDSaveAsync][{rank}] _cd_update_model_checkpoint_async complete for rank={rank}, path={path}_{step}, step={step}"
    )


@benchmarkMP
@benchmarkMP_helper
def _cd_update_data_checkpoint_async(cd=None, rank=None, step=None, path=None) -> None:
    # pass in instantiated CD client from main process
    logger.debug(
        f"[MockCDSaveAsync][{rank}] _cd_update_data_checkpoint_async start for rank={rank}, path={path}_{step}, step={step}"
    )
    if cd:
        cd.update(checkpoint_type=CheckpointType.DATA_CHECKPOINT, step=step, path=f"{path}_{step}")
    logger.debug(
        f"[MockCDSaveAsync][{rank}] _cd_update_data_checkpoint_async complete for rank={rank}, path={path}_{step}, step={step}"
    )


@benchmark
def cd_get_latest_checkpoint_path(cd_client) -> None:
    return cd_client.get_latest_checkpoint_path()


def _mock_async(cd=None, rank=None, step=None, path=None) -> None:
    time.sleep(10)


@benchmark
def get_cd_client(prefix, num_model_checkpoints, num_data_checkpoints):
    logger.debug(
        f"Creating checkpoint discovery client with {prefix=}, {num_model_checkpoints=}, {num_data_checkpoints=}"
    )
    return CheckpointDiscoverySocketClient(
        prefix=prefix,
        num_model_checkpoints=num_model_checkpoints,
        num_data_checkpoints=num_data_checkpoints,
    )


class MockCDSaveAsync(pl.Callback):
    def __init__(
        self,
        checkpoint_dir_path,
        num_model_checkpoints,
        num_data_checkpoints,
        checkpoint_interval=10,
    ):
        super().__init__()
        self.checkpoint_dir_path = checkpoint_dir_path
        self.checkpoint_interval = checkpoint_interval
        self.prefix = checkpoint_dir_path
        self.num_model_checkpoints = num_model_checkpoints
        self.num_data_checkpoints = num_data_checkpoints
        self.cd = get_cd_client(
            prefix=checkpoint_dir_path,
            num_model_checkpoints=num_model_checkpoints,
            num_data_checkpoints=num_data_checkpoints,
        )
        self.rank = get_rank()
        self.local_rank = get_local_rank()
        self.last_succ_ckpt = get_last_succ_ckpt()
        self.current_retry_count = get_current_retry_count()
        self.test_ckpt_fail = get_test_checkpoint_failure()
        self.test_update_fail = get_test_update_failure()
        self.ranks_to_fail = get_ranks_to_fail()
        logger.info(f"[MockCDSaveAsync][{self.rank}] Init for rank {self.rank}")

    def start_process(self, process, batch_idx):
        all_processes[batch_idx].append(process)
        process.start()

    def on_train_batch_start(self, trainer, pl_module, batch, batch_idx):
        if self.current_retry_count == 0 and batch_idx == (
            self.last_succ_ckpt + 2 * self.checkpoint_interval
        ):
            # wait for last successful ckpt async processes to complete then fail training script
            join_batch_step = self.last_succ_ckpt
            if join_batch_step != -1:
                for p in all_processes[join_batch_step]:
                    # wait for all processes to complete
                    p.join()
            log_benchmark_stats()
            # synchronize here so all ranks have successfully pushed their CD updates
            # and logged their current benchmark stats
            torch.distributed.barrier()
            fail_ranks = get_ranks_to_fail()
            _, test_case = get_test_type_and_case()
            if self.rank in fail_ranks and test_case != "happy":
                time.sleep(10)
                logger.error(f"[Rank={self.rank}] Failing dummy training script")
                raise ValueError(
                    f"Failing training script for rank={self.rank} on step={batch_idx} after {self.last_succ_ckpt}"
                )

    @benchmark
    def on_train_batch_end(self, trainer, pl_module, outputs, batch, batch_idx):
        if batch_idx % self.checkpoint_interval == 0 and batch_idx != 0:
            logger.info(
                f"[MockCDSaveAsync][{self.rank}] Batch {batch_idx} is ending, process submitted"
            )
            path = self.checkpoint_dir_path
            step = batch_idx

            # Model checkpoint
            if self.local_rank + 1 <= self.num_model_checkpoints:
                if (
                    (self.test_ckpt_fail != "data")
                    and (step > get_last_succ_ckpt() and self.current_retry_count == 0)
                    and (
                        (self.test_update_fail == "all")
                        or (
                            self.test_update_fail == "half_across_nodes"
                            and self.rank < get_world_size() // 2
                        )
                        or (
                            self.test_update_fail == "half_within_nodes"
                            and self.local_rank % 2 == 0
                        )
                        or (self.test_update_fail == "set" and self.rank in self.ranks_to_fail)
                    )
                ):
                    # Mock CD client update
                    logger.debug(
                        f"[MockCDSaveAsync][{self.rank}][{self.local_rank}] model checkpoint mock update for {batch_idx} for {self.test_update_fail=} and {self.test_ckpt_fail=}"
                    )
                    # instantiate process that does not call cd.update(), simulating a slow/hanging process
                    process = mp.Process(
                        target=_mock_async,
                        args=(self.cd, self.rank, step, path),
                        kwargs={"_queue": benchmarkMP.queue},
                    )
                    self.start_process(process, batch_idx)
                else:
                    # Actual CD client update
                    # pass CDClient instantiated in main process to forked process
                    process = mp.Process(
                        target=_cd_update_model_checkpoint_async,
                        args=(self.cd, self.rank, step, path),
                        kwargs={"_queue": benchmarkMP.queue},
                    )
                    self.start_process(process, batch_idx)

            # Data checkpoint
            if self.local_rank + 1 <= self.num_data_checkpoints:
                if (
                    (self.test_ckpt_fail != "model")
                    and (step > get_last_succ_ckpt() and self.current_retry_count == 0)
                    and (
                        (self.test_update_fail == "all")
                        or (
                            self.test_update_fail == "half_across_nodes"
                            and self.rank < get_world_size() // 2
                        )
                        or (
                            self.test_update_fail == "half_within_nodes"
                            and self.local_rank % 2 == 0
                        )
                        or (self.test_update_fail == "set" and self.rank in self.ranks_to_fail)
                    )
                ):
                    # Mock CD client update
                    logger.debug(
                        f"[MockCDSaveAsync][{self.rank}][{self.local_rank}] data checkpoint mock update for {batch_idx} for {self.test_update_fail=} and {self.test_ckpt_fail=}"
                    )
                    # instantiate process that does not call cd.update(), simulating a slow/hanging process
                    process = mp.Process(
                        target=_mock_async,
                        args=(self.cd, self.rank, step, path),
                        kwargs={"_queue": benchmarkMP.queue},
                    )
                    self.start_process(process, batch_idx)
                else:
                    # Actual CD client update
                    # pass CDClient instantiated in main process to forked process
                    process = mp.Process(
                        target=_cd_update_data_checkpoint_async,
                        args=(self.cd, self.rank, step, path),
                        kwargs={"_queue": benchmarkMP.queue},
                    )
                    self.start_process(process, batch_idx)


class MockCDResume(pl.Callback):
    def __init__(self, checkpoint_dir_path, num_model_checkpoints, num_data_checkpoints):
        super().__init__()
        self.rank = get_rank()
        logger.info(f"[MockCDResume][{self.rank}] Init before cd client initialization")
        self.cd = get_cd_client(
            prefix=checkpoint_dir_path,
            num_model_checkpoints=num_model_checkpoints,
            num_data_checkpoints=num_data_checkpoints,
        )
        self.resume_from_path = cd_get_latest_checkpoint_path(self.cd)
        current_retry_count = get_current_retry_count()
        last_succ_ckpt = get_last_succ_ckpt()
        logger.info(
            f"[MockCDResume][{self.rank}] Init returned checkpoint discovery path is: {self.resume_from_path}, type:{type(self.resume_from_path)}"
        )
        test_type, _ = get_test_type_and_case()

        if test_type == "standard":
            if current_retry_count == 0:
                assert self.resume_from_path is None
            elif current_retry_count == 1:
                assert (
                    self.resume_from_path == f"{checkpoint_dir_path}_{last_succ_ckpt}"
                ), f"Mismatch! Returned {self.resume_from_path}, expected {checkpoint_dir_path}_{last_succ_ckpt}"
        elif test_type == "manual_rollback":
            # TODO(viczhu): should return None on both first run and new run
            # temporarily also check "" until placeholder ckpt is fixed
            assert (
                self.resume_from_path is None or self.resume_from_path == ""
            ), f"Mismatch! Returned {self.resume_from_path}, expected None"

    def on_train_start(self, trainer, pl_module):
        if self.resume_from_path is not None:
            # TODO(viczhu): update so that mock resume sets correct current step on restart
            # needs to modify lightning trainer internals which is fragile
            cur_step = self.resume_from_path.split("_")[-1]
            logger.info(
                f"[MockCDResume][{self.rank}] Training is starting from {self.resume_from_path}, found step={cur_step}"
            )
            trainer._global_step = cur_step
            trainer.batch_idx = cur_step
        else:
            logger.info(f"[MockCDResume][{self.rank}] Training is starting from scratch")


class MockDataset(Dataset):
    def __getitem__(self, _):
        # image, class
        return (torch.randn(1, 28, 28), torch.randint(0, 10, (1,)).item())

    def __len__(self):
        # fake large dataset
        return 2147483647  # 2**31 - 1


def get_mock_dataloader(batch_size=1):
    return DataLoader(
        MockDataset(),
        batch_size=batch_size,
    )


@record
def main():
    world_size = get_world_size()
    local_world_size = get_local_world_size()
    rank = get_rank()
    local_rank = get_local_rank()
    current_retry_count = get_current_retry_count()
    test_type, test_case = get_test_type_and_case()
    fail_ranks = get_ranks_to_fail()
    last_succ_ckpt = get_last_succ_ckpt()
    ckpt_failure_type = get_test_checkpoint_failure()
    update_failure_type = get_test_update_failure()

    logger.info(f"World Size: {world_size}. Local World Size: {local_world_size}. Rank: {rank}")
    logger.info(f"[Rank={rank} LocalRank={local_rank}] Training script started")
    logger.info(f"[Rank={rank} LocalRank={local_rank}] {current_retry_count=}")
    logger.info(f"Test type: {test_type}. Test case: {test_case}")
    logger.info(f"Fail ranks: {fail_ranks}. Set last successful ckpt: {last_succ_ckpt}")
    logger.info(
        f"Checkpoint failure type: {ckpt_failure_type}. Update failure type: {update_failure_type}"
    )

    # Training settings
    parser = argparse.ArgumentParser(
        description="Checkpoint Discovery Integration test with PyTorchLightning MNIST"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=32,
        metavar="N",
        help="input batch size for training (default: 64)",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=400,
        help="max number of steps",
    )
    parser.add_argument(
        "--test-batch-size",
        type=int,
        default=1000,
        metavar="N",
        help="input batch size for testing (default: 1000)",
    )
    parser.add_argument(
        "--lr",
        type=float,
        default=0.01,
        metavar="LR",
        help="learning rate (default: 0.01)",
    )
    parser.add_argument(
        "--no-cuda",
        action="store_true",
        default=False,
        help="disables CUDA training",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=1,
        metavar="S",
        help="random seed (default: 1)",
    )
    parser.add_argument(
        "--log-interval",
        type=int,
        default=10,
        metavar="N",
        help="how many batches to wait before logging training status",
    )
    parser.add_argument(
        "--dir",
        default="logs",
        metavar="L",
        help="directory where summary logs are stored",
    )
    parser.add_argument(
        "--accelerator",
        type=str,
        help="Device accelerator",
        choices=["gpu", "cpu", "auto"],
        default="auto",
    )
    parser.add_argument(
        "--devices",
        type=int,
        default=1,
        help="how many devices to train on, and also how many model checkpoints",
    )
    parser.add_argument(
        "--num_data_checkpoints",
        type=int,
        default=1,
        help="how many data checkpoints, must be <= local world size",
    )
    parser.add_argument(
        "--checkpoint-interval",
        type=int,
        default=10,
        help="checkpoint interval",
    )
    parser.add_argument(
        "--checkpoint-dir-path",
        type=str,
        default="base-checkpoint-dir-path/",
        help="checkpoint dir path",
    )
    parser.add_argument(
        "--num_nodes",
        type=int,
        default=1,
        help="number of nodes",
    )

    args = parser.parse_args()

    use_cuda = not args.no_cuda and torch.cuda.is_available()
    if use_cuda:
        logger.info("Using CUDA")
        if args.accelerator not in ["gpu", "auto"]:
            logger.error("Set accelerator to `gpu` or `auto`")
            raise ValueError(
                f"Accelerator `{args.accelerator}` is not supported. Please set accelerator to `gpu` or `auto`"
            )

    torch.manual_seed(args.seed)

    logger.info(f"Number of nodes: {args.num_nodes}. Number of devices: {args.devices}")
    logger.info(f"Using accelerator {args.accelerator}")
    device = torch.device(f"cuda:{local_rank}" if use_cuda else "cpu")

    # Attach model to the device.
    model = LitMNIST(lr=args.lr).to(device)

    train_loader = get_mock_dataloader(batch_size=args.batch_size)
    val_loader = get_mock_dataloader(batch_size=args.test_batch_size)

    if test_type == "manual_rollback" and current_retry_count == 1:
        # simulate manual rollback and make sure new cd client clear latest checkpoint
        new_checkpoint_dir_path = "new-" + args.checkpoint_dir_path
        logger.info(
            f"Manual rollback test on restart, changing checkpoint_dir_path to {new_checkpoint_dir_path}"
        )
        args.checkpoint_dir_path = new_checkpoint_dir_path

    trainer = pl.Trainer(
        num_nodes=args.num_nodes,
        max_epochs=1,
        max_steps=args.max_steps,
        use_distributed_sampler=False,  # required as otherwise mem error thrown with large fake dataset
        callbacks=[
            MockCDResume(
                checkpoint_dir_path=args.checkpoint_dir_path,
                num_model_checkpoints=args.devices,
                num_data_checkpoints=args.num_data_checkpoints,
            ),
            MockCDSaveAsync(
                checkpoint_dir_path=args.checkpoint_dir_path,
                num_model_checkpoints=args.devices,
                num_data_checkpoints=args.num_data_checkpoints,
                checkpoint_interval=args.checkpoint_interval,
            ),
        ],
        accelerator=args.accelerator,
        devices=args.devices,
        log_every_n_steps=args.log_interval,
        strategy="ddp",
    )
    trainer.fit(model, train_loader, val_loader)

    logger.info(f"[Rank={rank}] Training script successful")
    # Note that if get_stats() is called before all the async processes complete,
    # those unfinished async processes will not be included in the reported stats.
    log_benchmark_stats()


if __name__ == "__main__":
    main()
