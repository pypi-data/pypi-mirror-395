"""Simple example showing how to use ilulab client."""

from ilulab import IlulabClient


def main():
    # Initialize client
    client = IlulabClient()

    # Create a project
    project = client.create_project(name="example-project", description="A simple example project")
    print(f"Created project: {project['name']} ({project['id']})")

    # Create a run with tags
    run = client.create_run(
        project_id=project["id"],
        name="example-run-1",
        description="Testing the ilulab client",
        tags=["example", "test"],
    )
    print(f"Created run: {run.run_id}")

    # Log parameters (hyperparameters, config)
    run.log_params(
        {
            "batch_size": 32,
            "optimizer": "adam",
            "model_architecture": "resnet50",
        }
    )
    print("Logged parameters")

    # Simulate a training loop
    print("\nSimulating training loop...")
    for epoch in range(10):
        # Simulate metrics
        train_loss = 1.0 / (epoch + 1)
        val_loss = 1.2 / (epoch + 1)
        val_acc = 0.5 + epoch * 0.05

        # Log metrics for this step
        run.log_metrics(
            {"train_loss": train_loss, "val_loss": val_loss, "val_accuracy": val_acc},
            step=epoch,
        )

        print(
            f"{epoch + 1}/10: train_loss={train_loss:.4f}, "
            "val_loss={val_loss:.4f}, val_accuracy={val_acc:.4f}"
        )

    # Mark run as completed
    run.finish()
    print("\nRun completed!")

    # Retrieve run data
    run_data = client.get_run(run.run_id)
    print(
        f"\nRun has {len(run_data['parameters'])} parameters and {len(run_data['metrics'])} metrics"
    )

    # List all runs in the project
    runs = client.list_runs(project_id=project["id"])
    print(f"\nTotal runs in project: {len(runs)}")

    # Clean up
    client.close()


if __name__ == "__main__":
    main()
