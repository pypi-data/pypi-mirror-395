# Developing SageMakerCheckpointing

This package uses the [hatch](https://hatch.pypa.io/latest/) build system.

### Building

A number of scripts and commands exist in `pyproject.toml` under the `scripts` configurations with more
documentation in the comments of `pyproject.toml`. Running a script for a specific environment is simply running
`hatch run <env_name>:<script>`. You can omit the `<env_name>` for those under the `default` environment.

You need to set up hatch pluging first:
```
./setup-hatch.sh
```

### Available Hatch Commands

- **`hatch run release`** - Runs typing checks (mypy), tests, and coverage.
- **`hatch test --cover`** - Runs tests and coverage.
- **`hatch typing`** - Runs mypy type checking.
- **`hatch fmt`** - Formats code using ruff.
- **`hatch build`** - builds both source and wheel distributions in ./build directory.
