#!/bin/bash

# install act
# curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

REPO_ABSOLUTE_PATH=$(dirname "$(readlink -f "$0")")
SECRETS_PATH="../.secrets"

act --local-repository "dev/github-pages-overwriter@v0=${REPO_ABSOLUTE_PATH}" --secret-file "${SECRETS_PATH}"
