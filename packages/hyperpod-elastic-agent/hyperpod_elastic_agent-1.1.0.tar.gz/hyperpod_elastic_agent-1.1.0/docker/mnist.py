# Modified from https://github.com/kubeflow/training-operator/tree/master/examples/pytorch/mnist
from __future__ import print_function

import argparse
import os
import logging
import torch
import torch.distributed as dist
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from torch.distributed.elastic.multiprocessing.errors import record
from torch.utils.tensorboard import SummaryWriter
from torch.utils.data import DistributedSampler
from torchvision import datasets, transforms

logging.basicConfig(format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 20, 5, 1)
        self.conv2 = nn.Conv2d(20, 50, 5, 1)
        self.fc1 = nn.Linear(4 * 4 * 50, 500)
        self.fc2 = nn.Linear(500, 10)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x, 2, 2)
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, 2, 2)
        x = x.view(-1, 4 * 4 * 50)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)


def train(args, model, device, train_loader, epoch, writer):
    model.train()
    optimizer = optim.SGD(model.parameters(),
                          lr=args.lr,
                          momentum=args.momentum)

    for batch_idx, (data, target) in enumerate(train_loader):
        # Attach tensors to the device.
        data, target = data.to(device), target.to(device)

        optimizer.zero_grad()
        output = model(data)
        loss = F.nll_loss(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % args.log_interval == 0:
            logger.info(
                "Train Epoch: {} [{}/{} ({:.0f}%)]\tloss={:.4f}".format(
                    epoch,
                    batch_idx * len(data),
                    len(train_loader.dataset),
                    100.0 * batch_idx / len(train_loader),
                    loss.item(),
                ))
            niter = epoch * len(train_loader) + batch_idx
            writer.add_scalar("loss", loss.item(), niter)


def test(model, device, test_loader, writer, epoch):
    model.eval()

    correct = 0
    with torch.inference_mode():
        for data, target in test_loader:
            # Attach tensors to the device.
            data, target = data.to(device), target.to(device)

            output = model(data)
            # Get the index of the max log-probability.
            pred = output.max(1, keepdim=True)[1]
            correct += pred.eq(target.view_as(pred)).sum().item()

    logger.info("\naccuracy={:.4f}\n".format(
        float(correct) / len(test_loader.dataset)))
    writer.add_scalar("accuracy",
                      float(correct) / len(test_loader.dataset), epoch)


@record
def main():
    logger.info(
        f"World Size: {os.environ['WORLD_SIZE']}. Rank: {os.environ['RANK']}")

    rank = int(os.environ["RANK"])
    local_rank = int(os.environ["LOCAL_RANK"])
    logger.info(
        f"[Rank={rank} LocalRank={local_rank}] Training script started")
    failure_count = int(os.environ.get("FAILURE_COUNT", "1"))
    current_retry_count = int(os.environ.get("TORCHELASTIC_RESTART_COUNT",
                                             "1"))
    fail_ranks = get_ranks_to_fail()
    test_case = os.environ.get("TEST_CASE", "sad")
    fail_after_epoch = int(os.environ.get("TEST_FAIL_AFTER_EPOCH", "1"))

    # Training settings
    parser = argparse.ArgumentParser(
        description="PyTorch FashionMNIST Example")
    parser.add_argument(
        "--batch-size",
        type=int,
        default=64,
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
        "--momentum",
        type=float,
        default=0.5,
        metavar="M",
        help="SGD momentum (default: 0.5)",
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
        "--backend",
        type=str,
        help="Distributed backend",
        choices=[dist.Backend.GLOO, dist.Backend.NCCL, dist.Backend.MPI],
        default=dist.Backend.NCCL,
    )

    args = parser.parse_args()
    use_cuda = not args.no_cuda and torch.cuda.is_available()
    if use_cuda:
        logger.info("Using CUDA")
        if args.backend != dist.Backend.NCCL:
            logger.warning(
                "Warning. Please use `nccl` distributed backend for the best performance using GPUs"
            )

    writer = SummaryWriter(args.dir)

    torch.manual_seed(args.seed)

    logger.info("Using distributed PyTorch with {} backend".format(
        args.backend))
    device = torch.device(f"cuda:{local_rank}" if use_cuda else "cpu")

    # Attach model to the device.
    model = Net().to(device)

    dist.init_process_group(backend=args.backend)
    model = nn.parallel.DistributedDataParallel(model)

    # Get FashionMNIST train and test dataset.
    train_ds = datasets.FashionMNIST(
        "./data",
        train=True,
        download=True,
        transform=transforms.Compose([transforms.ToTensor()]),
    )
    test_ds = datasets.FashionMNIST(
        "./data",
        train=False,
        download=True,
        transform=transforms.Compose([transforms.ToTensor()]),
    )
    # Add train and test loaders.
    train_loader = torch.utils.data.DataLoader(
        train_ds,
        batch_size=args.batch_size,
        sampler=DistributedSampler(train_ds),
    )
    test_loader = torch.utils.data.DataLoader(
        test_ds,
        batch_size=args.test_batch_size,
        sampler=DistributedSampler(test_ds),
    )
    for epoch in range(1, args.epochs + 1):
        train(args, model, device, train_loader, epoch, writer)
        test(model, device, test_loader, writer, epoch)
        if rank in fail_ranks and test_case != "happy" and \
           current_retry_count < failure_count and epoch == fail_after_epoch:
            logger.info(
                f"[Rank={rank}] Current Retry count {current_retry_count}/{failure_count}"
            )
            logger.error(f"[Rank={rank}] Failing dummy training script")
            raise ValueError(
                f"Failing training script for {rank=} after {epoch=}")

    if args.save_model:
        torch.save(model.state_dict(), "mnist_cnn.pt")
    logger.info(f"[Rank={rank}] Training script successful")


def get_ranks_to_fail():
    # Fail for rank 2 by default
    fail_ranks_str = os.environ.get("FAIL_RANKS", "2,")
    fail_ranks = [int(rank) for rank in fail_ranks_str.split(',') if rank]
    return fail_ranks


if __name__ == "__main__":
    main()
