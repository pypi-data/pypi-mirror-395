# Docker container
To build a docker container first build a wheel from the root directory. This will build a wheel and copy it to `docker/dist` folder.
```
brazil-build
```
```
## Build local test images with latest changes
./test_scripts/update_local_test_image.sh
```

Run the minimal docker test build
```
## Success
docker run --rm -it --network=host \
           -e TEST_SLEEP_TIME=15 \
           ptjob:latest

## Failure
docker run --rm -it --network=host \
           -e TEST_CASE=sad \
           -e TEST_SLEEP_TIME=5 \
           ptjob:latest
```


Run the mnist docker test build
```
### Distributed testing
### 1. Launch 2 docker containers on 2 ports (add/remove --gpus=all based on host)
### 2. Issue start on both 
docker run --rm -it --network=host \
           -e NNODES=2 -e NPROC_PER_NODE=2 -e AGENT_PORT=8000 \
           --gpus=all --shm-size=2gb \
           ptjob:mnist

docker run --rm -it --network=host \
           -e NNODES=2 -e NPROC_PER_NODE=2 -e AGENT_PORT=8080 \
           --gpus=all --shm-size=2gb \
           ptjob:mnist

curl -X POST \
     -d '{"rank": 0, "nnodes": 2, "faultCount": 0, "master_addr": "127.0.0.1", "master_port": "23456"}' \
     http://127.0.0.1:8000/start
curl -X POST \
     -d '{"rank": 1, "nnodes": 2, "faultCount": 0, "master_addr": "127.0.0.1", "master_port": "23456"}' \
     http://127.0.0.1:8080/start
```

--- 
## Run with Log Agent

Similar to the step above:
```
brazil-build
cp build/*.whl docker/
```

Then build the docker and test locally:

```
cd docker/
docker build -t log-agent-test -f Dockerfile.logagent .

docker run -it --rm -p 8080:8080 log-agent-test
# On other terminal, run `curl -X POST -d '{"rank": 0, "nnodes": 2, "faultCount": 0, "master_addr": "127.0.0.1", "master_port": "23456"}' http://127.0.0.1:8080/start`
# should see status HEALTHY

docker run -it --rm -p 8080:8080 -e LOG_INTERVAL=120 log-agent-test
# On other terminal, run `curl -X POST -d '{"rank": 0, "nnodes": 2, "faultCount": 0, "master_addr": "127.0.0.1", "master_port": "23456"}' http://127.0.0.1:8080/start`
# wait for 30 seconds, should see status HANGING


docker run -it --rm -p 8080:8080 -v `pwd`/podinfo:/etc/podinfo/ -e LOG_TFLOPS=90 log-agent-test
# On other terminal, run `curl -X POST -d '{"rank": 0, "nnodes": 2, "faultCount": 0, "master_addr": "127.0.0.1", "master_port": "23456"}' http://127.0.0.1:8080/start`
# should see status SLOW

```

