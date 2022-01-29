#!/usr/bin/env bash
docker run --name apigen --rm -v $(pwd):/data genapi $1