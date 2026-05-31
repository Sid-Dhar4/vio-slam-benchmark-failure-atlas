# Environment

Host Python tooling will handle automation, plotting, tests, and evo. Backend builds will be pinned separately.

## Running tests

Use the project test wrapper:

```bash
./scripts/run_tests.sh
```

Reason: ROS 2 environments can expose external pytest plugins into the shell. The wrapper disables third-party pytest plugin autoloading so tests run with project dependencies only.
