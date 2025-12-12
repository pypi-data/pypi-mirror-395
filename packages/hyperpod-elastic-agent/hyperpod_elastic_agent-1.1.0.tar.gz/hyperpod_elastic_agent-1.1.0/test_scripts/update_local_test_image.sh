set -exu

source test_scripts/ecr_helpers.sh

dlc_ecr_docker_auth

cp -r docker/* build/ # Put Dockerfile required files under build with whl file
cd build

docker build -t ptjob:latest .
docker build -t ptjob:mnist -f mnist.Dockerfile .
docker build -t ptjob:ipr -f ipr.Dockerfile .