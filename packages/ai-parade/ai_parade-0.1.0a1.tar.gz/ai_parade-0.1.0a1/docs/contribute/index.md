# Contribution guides

Install dev dependencies:

```sh
uv sync --group dev
```

This will install dependencies for:

- tests
- generating docs

## Build Documentation

Generate the docs:

```sh
mkdocs serve
```

## Architecture

```mermaid
sequenceDiagram
    box User environment
    actor User
    participant toolkit
    end
    box Model environment
    participant toolkit puppet
    participant model code
    end
    User->>toolkit: Install
    Note over toolkit puppet, model code: Environment is created
    
    User->>toolkit: create runner
    toolkit->>toolkit puppet: spawns and connects to a new process
    toolkit puppet->>+model code: creates model
    toolkit puppet->>toolkit: OK
    User->>toolkit: run conversion
    toolkit->>toolkit puppet: sends conversion command
    Note over toolkit puppet, model code: The model is used for the converison
    toolkit puppet->>toolkit: OK
    User->>toolkit: dispose runner
    toolkit->>toolkit puppet: dispose or disconnect
    toolkit puppet->>model code: dispose of the model
    deactivate model code
    toolkit puppet->>toolkit: OK
```
