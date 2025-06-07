#!/usr/bin/env bash

set -e

if [ -f .env ]; then
    set -a
    source .env
    set +a
else
    echo ".env file not found"
    exit 1
fi

/opt/homebrew/opt/meilisearch/bin/meilisearch
