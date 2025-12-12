#!/usr/bin/env bash
set -euo pipefail

black src/
isort --profile black src/
