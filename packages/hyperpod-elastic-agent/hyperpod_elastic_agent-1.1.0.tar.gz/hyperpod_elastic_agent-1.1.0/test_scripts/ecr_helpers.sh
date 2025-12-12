REGION=us-west-2

function ecr_docker_auth {
  aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $1
}

function dlc_ecr_docker_auth {
  ecr_docker_auth 763104351884.dkr.ecr.$REGION.amazonaws.com
}