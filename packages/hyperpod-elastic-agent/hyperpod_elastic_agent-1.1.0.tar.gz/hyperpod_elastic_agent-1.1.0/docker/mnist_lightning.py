import argparse
import logging
import multiprocessing as mp
import os
import psutil
import pytorch_lightning as pl
import torch.nn as nn
import torch.nn.functional as F
import signal
import time
import torch
from torch.distributed.elastic.multiprocessing.errors import record
from torch.utils.data import DataLoader, random_split
from torchvision.datasets import MNIST
from torchvision import transforms

logging.basicConfig(format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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
        self.log('train_loss', loss)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = self.loss_fn(y_hat, y)
        preds = torch.argmax(y_hat, dim=1)
        accuracy = (preds == y).float().mean()
        self.log('val_loss', loss)
        self.log('val_accuracy', accuracy)


HUNG_JOB_SIGTERM_TIMEOUT_SECONDS = 10


class HungJobDetectionMonitor:

    def __init__(self):
        self.monitor_process = mp.Process(target=self.monitor_loop,
                                          args=(10, ),
                                          daemon=True)
        logger.info("Creating HungJobDetectionMonitor")

    def start(self):
        logger.info("Creating signal handlers for the trainer process")
        signal.signal(signal.SIGTERM, self.signal_handler)
        logger.info("SIGTERM handlers has been hooked / modified")

        logger.info("Forking monitoring daemon process")
        self.monitor_process.start()
        logger.info("Forking monitoring daemon process / Done")

    def monitor_loop(self, sleep_time):
        logger.info("Configure signal handlers for the monitor process")
        signal.signal(signal.SIGTERM, self.signal_handler)
        logger.info(
            f"Monitor process pid {os.getpid()}, main process pid {os.getppid()}"
        )
        time.sleep(sleep_time)
        self.terminate_parent()

    def stop(self):
        logger.info(f"Stopping monitoring daemon process")
        if self.monitor_process:
            self.monitor_process.kill()
        else:
            logger.info(f"Monitoring daemon process is not running")

    def signal_handler(self, signum, frame):
        exit(0)

    @staticmethod
    def terminate_parent():
        parent = psutil.Process(os.getppid())
        logger.info(f"Sending SIGTERM to {parent=}")
        parent.terminate()  # Send SIGTERM
        try:
            parent.wait(timeout=HUNG_JOB_SIGTERM_TIMEOUT_SECONDS)
        except psutil.TimeoutExpired:
            logger.info(
                f"Monitoring daemon failed to gracefully terminate parent. Sending SIGKILL to {parent=}"
            )
            parent.kill()


class HungJobCallback(pl.Callback):

    def __init__(self):
        super().__init__()
        self.monitor = HungJobDetectionMonitor()
        self._start_monitor()

    def _start_monitor(self):
        logger.info(
            "Initialize HungJobDetectionCallback / Done, starting HungJobDetectionMonitor"
        )
        self.monitor.start()

    def on_train_start(self, trainer, pl_module):
        logger.info("Training is starting")

    def on_train_end(self, trainer, pl_module):
        self.monitor.stop()
        logger.info("Training is ending")


class CustomCallback(pl.Callback):

    def __init__(self):
        super().__init__()

    def on_train_start(self, trainer, pl_module):
        logger.info("Training is starting")

    def on_train_end(self, trainer, pl_module):
        logger.info("Training is ending")

    def on_train_batch_start(self, trainer, pl_module, batch, batch_idx):
        logger.debug("Batch is starting")

    def on_train_batch_end(self, trainer, pl_module, outputs, batch,
                           batch_idx):
        logger.debug("Batch is ending")


@record
def main():
    logger.info(
        f"World Size: {os.environ['WORLD_SIZE']}. Rank: {os.environ['RANK']}")

    rank = int(os.environ["RANK"])
    local_rank = int(os.environ["LOCAL_RANK"])
    logger.info(
        f"[Rank={rank} LocalRank={local_rank}] Training script started")

    # Training settings
    parser = argparse.ArgumentParser(
        description="PyTorchLightning MNIST Example")
    parser.add_argument(
        "--batch-size",
        type=int,
        default=32,
        metavar="N",
        help="input batch size for training (default: 64)",
    )
    parser.add_argument(
        "--test-batch-size",
        type=int,
        default=1000,
        metavar="N",
        help="input batch size for testing (default: 1000)",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=1,
        metavar="N",
        help="number of epochs to train (default: 10)",
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
        "--save-model",
        action="store_true",
        default=False,
        help="For Saving the current Model",
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
        help="how many devices to train on",
    )

    args = parser.parse_args()
    use_cuda = not args.no_cuda and torch.cuda.is_available()
    if use_cuda:
        logger.info("Using CUDA")
        if args.accelerator not in ["gpu", "auto"]:
            logger.error("Set accelerator to `gpu` or `auto`")

    torch.manual_seed(args.seed)

    logger.info(f"Using accelerator {args.accelerator}")
    device = torch.device(f"cuda:{local_rank}" if use_cuda else "cpu")

    # Attach model to the device.
    model = LitMNIST(lr=args.lr).to(device)

    transform = transforms.Compose(
        [transforms.ToTensor(),
         transforms.Normalize((0.1307, ), (0.3081, ))])
    dataset = MNIST('./data', train=True, download=True, transform=transform)
    train_dataset, val_dataset = random_split(dataset, [55000, 5000])
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size)
    val_loader = DataLoader(val_dataset, batch_size=args.test_batch_size)

    trainer = pl.Trainer(
        max_epochs=args.epochs,
        callbacks=[CustomCallback()],
        accelerator=args.accelerator,
        devices=args.devices,
        log_every_n_steps=args.log_interval,
    )
    trainer.fit(model, train_loader, val_loader)

    if args.save_model:
        torch.save(model.state_dict(), "mnist_lightning.pt")
    logger.info(f"[Rank={rank}] Training script successful")


if __name__ == "__main__":
    main()
