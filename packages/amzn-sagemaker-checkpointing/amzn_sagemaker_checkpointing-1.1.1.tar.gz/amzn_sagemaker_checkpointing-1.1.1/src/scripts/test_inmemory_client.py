from amzn_sagemaker_checkpointing.storage.clients.inmemory.inmemory_client import (
    InMemoryCheckpointClient,
    InMemoryClientConfig,
)

config = InMemoryClientConfig(
    base_url="http://localhost:9201",
    request_timeout=5.0,
    request_retries=3,
    retry_backoff=0.2,
)

client = InMemoryCheckpointClient(
    namespace="test-ns",
    rank="0",
    world_size="1",
    config=config,
    metadata_file_count=0,
    steps_retained=3,
)

try:
    print("Creating namespace...")
    ns_config = client.get_or_create_namespace()
    assert isinstance(ns_config, dict), "Expected a dictionary namespace config"
    print(ns_config)
    assert "num_ranks" in ns_config and ns_config["num_ranks"] == 1, "Incorrect num_ranks"
    assert (
        "steps_to_retain_per_rank" in ns_config and ns_config["steps_to_retain_per_rank"] == 3
    ), "Incorrect steps_retained"
    print("Namespace created and validated.")

    print("Uploading checkpoint...")
    step = 1001
    data = b"hello checkpoint"
    client.put_checkpoint(step=step, data=data)
    print("Checkpoint uploaded.")

    print("Reading back checkpoint...")
    content = client.get_checkpoint(step=step)
    assert content == data, "Checkpoint content mismatch!"
    print("Checkpoint content verified.")

    print("Fetching latest checkpoints...")
    latest = client.get_latest_checkpoints(limit=5)
    assert step in latest, f"Expected step {step} in latest checkpoints"
    print(f"Latest checkpoints: {latest}")

    print("Deleting checkpoint...")
    client.delete_checkpoint(step=step)
    post_delete = client.get_checkpoint(step=step)
    assert post_delete is None, "Checkpoint was not deleted!"
    print("Checkpoint deletion verified.")

    print("Deleting namespace...")
    client.delete_namespace()
    post_ns = client.get_namespace_config()
    print(post_ns)
    assert post_ns == {}, "Namespace was not deleted or recreated with default values"
    print("Namespace deletion verified.")

    print("All tests passed!")

except Exception as e:
    print("Test failed:", e)

finally:
    client.close()
