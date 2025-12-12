"""Fetch pod logs for HPJob in parallel."""

# Standard Library
import argparse
import concurrent.futures
import os
import threading
from typing import List

# Third Party
from kubernetes import client, config


def print_pod_data(pods: List[client.models.v1_pod.V1Pod]):
    for pod in pods:
        print(f"Pod name: {pod.metadata.name}")
        print(f"    Pod status: {pod.status.phase}")
        print(f"    Pod IP: {pod.status.pod_ip}")
        hpjob = pod.metadata.labels["HPJob"]
        print(f"    Pod HPJob: {hpjob}")


class Counter:
    """Thread-safe counter"""

    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.value += 1


def main():
    parser = argparse.ArgumentParser(
        description="Save logs in parallel for all pods for a given HPJob"
    )
    parser.add_argument(
        "--job_name",
        type=str,
        default="hppt-mnist-lightning-cd",
        help="HPJob name to fetch logs for",
    )
    parser.add_argument(
        "--log_dir",
        type=str,
        default="logs/cpu_scaling",
        help="Log directory prefix to save logs to",
    )
    parser.add_argument(
        "--max_parallel_workers",
        type=int,
        default=100,
        help="Max number of parallel worker threads",
    )
    parser.add_argument(
        "--fetch_pod_version",
        type=int,
        default=1,
        choices=[1, 2],
        help="Fetch pod version",
    )
    args = parser.parse_args()

    config.load_kube_config()
    # https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/CoreV1Api.md
    v1 = client.CoreV1Api()

    # Fetch pods for the job
    # TODO(viczhu): time which one is faster
    if args.fetch_pod_version == 1:
        pods = v1.list_namespaced_pod(namespace="default", watch=False).items
        pods = [pod for pod in pods if pod.metadata.name.startswith(args.job_name)]
    elif args.fetch_pod_version == 2:
        pods = v1.list_pod_for_all_namespaces(label_selector=f"HPJob={args.job_name}").items

    print_pod_data(pods)

    def fetch_log(fetch_args):
        pod: client.models.v1_pod.V1Pod
        successful_pods_counter: Counter
        pod, successful_pods_counter = fetch_args

        try:
            log = v1.read_namespaced_pod_log(
                name=pod.metadata.name, namespace=pod.metadata.namespace
            )
            file_path = f"{args.log_dir}/{pod.metadata.name}.log"
            with open(file_path, "w", encoding="utf8") as f:
                f.write(log)
            successful_pods_counter.increment()

            print(f"Successfully fetched logs for {pod.metadata.name} and saved to {file_path}")
        except Exception as e:
            print(f"Failed to fetch logs for {pod.metadata.name}: {e}")

    # Create log dir if it doesnt exist
    os.makedirs(args.log_dir, exist_ok=True)

    # Thread-safe counter
    successful_pods_counter = Counter()

    # Map only accepts 1 arg, so we need to pass a list of tuples
    fetch_args = [(pod, successful_pods_counter) for pod in pods]

    # Fetch logs in parallel
    # Use ThreadPoolExecutor for I/O bound operations over ProcessPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.max_parallel_workers) as executor:
        executor.map(fetch_log, fetch_args)

    total_pods = len(pods)
    print(
        f"\n\nWe have successfully fetched logs for "
        f"{successful_pods_counter.value}/{total_pods} pods!"
    )


if __name__ == "__main__":
    main()
