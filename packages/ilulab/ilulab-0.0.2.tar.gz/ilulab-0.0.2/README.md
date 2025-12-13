# IluLab Python Client

Lightweight Python client for tracking ML experiments with IluLab.

## Installation

```bash
pip install ilulab
```

## Quick Start

Set your API token as an environment variable:

```bash
export ILULAB_TOKEN="your_api_token_here"
```

then use the client in your code:

```python
from ilulab import IlulabClient

# Initialize client
client = IlulabClient()

# Create a project
project = client.create_project(
    name="my-ml-project",
    description="Testing ilulab"
)

# Create a run
run = client.create_run(
    project_id=project["id"],
    name="experiment-1",
    tags=["baseline", "resnet"]
)

# Log parameters
run.log_params({
    "batch_size": 32,
    "optimizer": "adam",
    "model": "resnet50"
})

# Log metrics during training
for epoch in range(10):
    # ... training code ...
    loss = 0.5 - epoch * 0.03  # example
    accuracy = 0.6 + epoch * 0.04  # example

    run.log_metrics({
        "train_loss": loss,
        "train_accuracy": accuracy
    }, step=epoch)

# Mark run as completed
run.finish()

# Clean up
client.close()
```

## Using Context Managers

```python
from ilulab import IlulabClient

with IlulabClient() as client:
    project = client.create_project(name="my-project")

    with client.create_run(project["id"], name="experiment-1") as run:
        run.log_param("learning_rate", 0.001)

        for step in range(100):
            run.log_metric("loss", 1.0 / (step + 1), step=step)

        # Automatically marked as completed on exit
        # (or failed if an exception occurs)
```
