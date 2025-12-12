#!/bin/bash
set -exu

source test_scripts/ecr_helpers.sh
rm -rf build/hyperpod_elastic_agent-* docker/hyperpod_elastic_agent-* && brazil-build build

PUBLISH=false
while getopts "p" option; do
   case $option in
      p)
         PUBLISH=true ;;
     \?) # Invalid option
         echo "Error: Invalid option"
         exit;;
   esac
done

DEV_IMAGE_TAG="-$USER"
if $PUBLISH; then
  DEV_IMAGE_TAG=""
fi

DUMMY_TRAINING_IMG_TAG="latest$DEV_IMAGE_TAG"
MNIST_TRAINING_IMG_TAG="mnist$DEV_IMAGE_TAG"
IPR_TRAINING_IMG_TAG="ipr$DEV_IMAGE_TAG"

cp -r docker/* build/ # Put Dockerfile required files under build with whl file
cd build

ACCOUNT_ID=448049793756 # Use compass-goodput-benchmark@amazon.com by default for now

PT_JOB_REPO=$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/ptjob

ada credentials update --profile goodput-benchmark --role=Admin --account $ACCOUNT_ID --once
export AWS_PROFILE=goodput-benchmark
aws sts get-caller-identity # Verify identity is as expected

# Dummy training
# Need ecr auth to use DLC as base image
dlc_ecr_docker_auth
docker build -t ptjob:$DUMMY_TRAINING_IMG_TAG .
docker tag ptjob:$DUMMY_TRAINING_IMG_TAG $PT_JOB_REPO:$DUMMY_TRAINING_IMG_TAG
ecr_docker_auth $PT_JOB_REPO
docker push $PT_JOB_REPO:$DUMMY_TRAINING_IMG_TAG

# Mnist training
# Need ecr auth to use DLC as base image
dlc_ecr_docker_auth
docker build -t ptjob:$MNIST_TRAINING_IMG_TAG -f mnist.Dockerfile .
docker tag ptjob:$MNIST_TRAINING_IMG_TAG $PT_JOB_REPO:$MNIST_TRAINING_IMG_TAG
ecr_docker_auth $PT_JOB_REPO
docker push $PT_JOB_REPO:$MNIST_TRAINING_IMG_TAG

# IPR training
# Need ecr auth to use DLC as base image
dlc_ecr_docker_auth
docker build -t ptjob:$IPR_TRAINING_IMG_TAG -f ipr.Dockerfile .
docker tag ptjob:$IPR_TRAINING_IMG_TAG $PT_JOB_REPO:$IPR_TRAINING_IMG_TAG
ecr_docker_auth $PT_JOB_REPO
docker push $PT_JOB_REPO:$IPR_TRAINING_IMG_TAG
