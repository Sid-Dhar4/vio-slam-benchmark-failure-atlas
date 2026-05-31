#!/usr/bin/env bash
set -euo pipefail

# ROS 2 can expose pytest plugins from /opt/ros into the shell.
# Disable third-party pytest plugin autoloading so project tests run only with project dependencies.
export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1

cd "$(dirname "$0")/.."
pytest -q "$@"
