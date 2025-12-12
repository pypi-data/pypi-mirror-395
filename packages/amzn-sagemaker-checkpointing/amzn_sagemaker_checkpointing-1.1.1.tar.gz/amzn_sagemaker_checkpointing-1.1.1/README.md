# Amazon SageMaker Checkpointing Library

A high-performance, tiered storage library for distributed checkpointing that enables efficient checkpoint management across multiple storage tiers including in-memory, and Amazon S3.

## Overview

The `amzn-sagemaker-checkpointing` library provides seamless integrations with different checkpointing solutions of distributed training frameworks:

- **Tiered Storage Architecture**: Automatic management across in-memory, and S3 storage tiers
- **Frameworks supported**: Pytorch DCP
- **High Performance**: Optimized for large-scale distributed training workloads
- **Fault Tolerance**: Automatic fallback mechanisms and consistency guarantees
- **Flexible Configuration**: Customizable storage policies
- **Logging**: Structured logging with rank, step, and operation details

## Key Features

### **Tiered Storage Strategy**
- **In-Memory Tier**: Ultra-fast checkpoint storage for immediate access
- **S3 Tier**: Durable cloud storage for long-term checkpoint retention

### **Intelligent Fallback**
- Automatic fallback from in-memory to S3 when memory reads fail
- Consistency guarantees across storage tiers
- Graceful degradation under failure conditions

## Infrastructure Prerequisites

### HyperPod Cluster Settings
AWS HyperPod Cluster with TieredStorage enabled

### S3 Tier Configuration
In order to use S3 Tier, the IAM role asssociated with the training pods should have the following access
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "s3:DeleteObject",
                "s3:GetBucketLocation",
                "s3:GetObject",
                "s3:ListBucket",
                "s3:PutObject"
            ],
            "Resource": [
                "arn:aws:s3:::<bucket_name>",
                "arn:aws:s3:::<bucket_name>/*"
            ],
            "Effect": "Allow"
        }
    ]
}
```

If you are using a S3 bucket in an account different than your training infrastructure. Please add the
following to your S3 bucket policy
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "CheckPointCrossAccountAccess",
            "Effect": "Allow",
            "Principal": {
                "AWS": <AWS principal>
            },
            "Action": [
                "s3:DeleteObject",
                "s3:GetBucketLocation",
                "s3:GetObject",
                "s3:ListBucket",
                "s3:PutObject"
            ],
            "Resource": [
                "arn:aws:s3:::<bucket_name>",
                "arn:aws:s3:::<bucket_name>/*"
            ]
        }
    ]
}
```

## Installation
### Prerequisites
```bash
pip install s3torchconnector tenacity torch boto3 botocore
```

### SageMaker Checkpointing Library
```bash
pip install amzn-sagemaker-checkpointing
```

## Quick Start

### Basic Usage with PyTorch DCP Async Save

```python
import torch
import torch.distributed as dist
from torch.distributed.checkpoint import async_save, load
from amzn_sagemaker_checkpointing.config.sagemaker_checkpoint_config import SageMakerCheckpointConfig
from amzn_sagemaker_checkpointing.checkpointing.filesystem.filesystem import (
    SageMakerTieredStorageWriter,
    SageMakerTieredStorageReader
)

# Initialize distributed training
dist.init_process_group(backend="nccl")

# Configure checkpointing
checkpoint_config = SageMakerCheckpointConfig(
    # Unique ID for your training job 
    # Allowed characters in ID include: alphanumeric, hyphens, and underscores
    namespace=os.environ.get('TRAINING_JOB_NAME', f'job-{int(time.time())}'), 
    
    # Number of distributed processes/available GPUs
    world_size=dist.get_world_size(), 
    
    # S3 storage location, required for SageMakerTieredStorageReader for read fallbacks
    # Required for SageMakerTieredStorageWriter when save_to_s3 is True
    s3_tier_base_path="s3://my-bucket/checkpoints"

)

# Your model and optimizer
model = MyModel()
optimizer = torch.optim.AdamW(model.parameters())

# Training loop
future = None
in_memory_ckpt_freq = 10
s3_ckpt_freq = 50

for training_step in range(1000):
    # ... training code ...
    
    # Save checkpoint
    if (training_step % in_memory_ckpt_freq == 0 or 
        training_step % s3_ckpt_freq == 0):
        # Create state dictionary
        state_dict = {
            "model": model.state_dict(),
            "optimizer": optimizer.state_dict(),
            "step": training_step,
            "epoch": epoch
        }
        
        # Create storage writer for current step
        checkpoint_config.save_to_s3 = training_step % s3_ckpt_freq == 0
        storage_writer = SageMakerTieredStorageWriter(
            checkpoint_config=checkpoint_config,
            step=training_step
        )

        # wait for previous checkpoint to get completed
        if future is not None:
            exc = future.exception()
            if exc:
                print(f"Failure in saving previous checkpoint:{str(exc)}")
                #Handle failures as required
            else:
                result = future.result()
                #Process results from save, if required
        
        # Async save checkpoint using PyTorch DCP
        future = async_save(state_dict=state_dict, storage_writer=storage_writer)
        
        # Continue training while checkpoint saves in background
```

### Loading Checkpoints

```python
# Create state dictionary template
state_dict = {
    "model": model.state_dict(),
    "optimizer": optimizer.state_dict(),
    "step": 0,
    "epoch": 0
}

# Load latest checkpoint
storage_reader = SageMakerTieredStorageReader(checkpoint_config=checkpoint_config)
load(state_dict, storage_reader=storage_reader)

# Load specific checkpoint step
storage_reader = SageMakerTieredStorageReader(
    checkpoint_config=checkpoint_config, 
    step=500 # Or don't pass step if you have to load the latest available step.
)
try:
    load(state_dict, storage_reader=storage_reader)
except BaseException as e:
    print(f"Checkpoint load failed: {str(e)}")
    # Add additional exception handling
```

## Configuration

### SageMakerCheckpointConfig

```python
from amzn_sagemaker_checkpointing.config.sagemaker_checkpoint_config import SageMakerCheckpointConfig

config = SageMakerCheckpointConfig(
    # Required parameters
    
    # Unique ID for your training job 
    # Allowed characters in ID include: alphanumeric, hyphens, and underscores
    namespace=os.environ.get('TRAINING_JOB_NAME', f'job-{int(time.time())}'), 
    
    # Number of distributed processes/available GPUs
    world_size=<num_of_distributed_processes>,
    
    #Optional parameters
    
    # Example: "s3://bucket/path"
    s3_tier_base_path=[s3_uri], 
    
    # Flag indicating if the checkpoint needs to be saved in S3
    save_to_s3=[True|False],
    
    # Custom logger instance
    logger=[application logger instance] 
)
```

### Configuration Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `namespace` | str | Yes | Unique ID for your training job. Allowed characters are: alphanumeric, hyphens, and underscores |
| `world_size` | int | Yes | Total number of distributed processes/available GPUs |
| `s3_tier_base_path` | str | No | S3 bucket and path prefix (must start with `s3://`) |
| `save_to_s3` | bool | No | Flag indicating if the checkpoint needs to be saved in S3 |
| `logger` | Logger | No | Custom logger instance |

## Advanced Usage

### Complete Distributed Training Example

```python
import os
import torch
import torch.distributed as dist
import torch.nn as nn
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.distributed.checkpoint import async_save, load
from amzn_sagemaker_checkpointing.config.sagemaker_checkpoint_config import SageMakerCheckpointConfig
from amzn_sagemaker_checkpointing.checkpointing.filesystem.filesystem import (
    SageMakerTieredStorageWriter,
    SageMakerTieredStorageReader
)

def setup_distributed():
    """Initialize distributed training"""
    dist.init_process_group(backend="nccl")
    torch.cuda.set_device(dist.get_rank())

def create_model():
    """Create and wrap model with DDP"""
    model = nn.Linear(1000, 10).cuda()
    return DDP(model, device_ids=[dist.get_rank()])

def main():
    setup_distributed()
    
    # Model and optimizer setup
    model = create_model()
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
    lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=100, gamma=0.9)
    
    # Checkpoint configuration
    checkpoint_config = SageMakerCheckpointConfig(
        namespace=os.environ.get('TRAINING_JOB_NAME', f'job-{int(time.time())}'),
        world_size=dist.get_world_size(),
        s3_tier_base_path="s3://my-training-bucket/checkpoints",
    )
    
    # Resume from checkpoint if available
    start_step = 0
    try:
        state_dict = {
            "model": model.state_dict(),
            "optimizer": optimizer.state_dict(),
            "lr_scheduler": lr_scheduler.state_dict(),
            "step": 0
        }
        
        storage_reader = SageMakerTieredStorageReader(checkpoint_config=checkpoint_config)
        load(state_dict, storage_reader=storage_reader)
        
        model.load_state_dict(state_dict["model"])
        optimizer.load_state_dict(state_dict["optimizer"])
        lr_scheduler.load_state_dict(state_dict["lr_scheduler"])
        start_step = state_dict["step"] + 1
        
        print(f"Resumed training from step {start_step}")
    except BaseException as e:
        print(f"No checkpoint found, starting from scratch: {str(e)}")
    
    # Training loop
    in_memory_ckpt_freq = 10
    s3_ckpt_freq = 50
    future = None
    for step in range(start_step, 1000):
        # Training step
        optimizer.zero_grad()
        
        # Dummy forward pass (replace with your actual training logic)
        inputs = torch.randn(32, 1000).cuda()
        targets = torch.randint(0, 10, (32,)).cuda()
        outputs = model(inputs)
        loss = nn.CrossEntropyLoss()(outputs, targets)
        
        loss.backward()
        optimizer.step()
        lr_scheduler.step()
        
        # Save checkpoint
        if (step % in_memory_ckpt_freq == 0 or
            step % s3_ckpt_freq == 0):
            state_dict = {
                "model": model.state_dict(),
                "optimizer": optimizer.state_dict(),
                "lr_scheduler": lr_scheduler.state_dict(),
                "step": step
            }
            
            # Configure is S3 save is required for the step
            checkpoint_config.save_to_s3 = step % s3_ckpt_freq == 0

            # Create storage writer for current step
            storage_writer = SageMakerTieredStorageWriter(
                checkpoint_config=checkpoint_config,
                step=step
            )
            
            # Optional: wait for previous checkpoint
            if future is not None:
                exc = future.exception()
                if exc:
                    print(f"Failure in saving previous checkpoint: {str(exc)}")
                    # Handle failures as required
                else:
                    result = future.result()
                    # Process results from save, if required
            
            # Async save (non-blocking)
            future = async_save(state_dict=state_dict, storage_writer=storage_writer)
            
    # Cleanup
    dist.destroy_process_group()

if __name__ == "__main__":
    main()
```

### Using Path-based Step Detection

The library can automatically detect the training step from the checkpoint path:

```python
# Step will be automatically extracted from path
storage_writer = SageMakerTieredStorageWriter(
    checkpoint_config=checkpoint_config,
    path=f"step_{training_step}/checkpoint"  # Step extracted from path
)

# Or specify step explicitly (overrides path-based detection)
storage_writer = SageMakerTieredStorageWriter(
    checkpoint_config=checkpoint_config,
    path="any/path/here",
    step=training_step  # Explicit step takes precedence
)
```

## Storage Tier Behavior

### In-Memory Tier
- **Always attempted first** for maximum performance
- Provides ultra-low latency checkpoint access
- Falls back to S3 if read fails
- Automatically managed with configurable retention policies

### S3 Tier
- Durable cloud storage for long-term retention
- Automatic fallback destination when in-memory reads fail
- Chunked uploads for large checkpoints (32MB chunks)

### Consistency Guarantees

The library ensures checkpoint consistency through:
1. **Automatic fallback**: Seamless transition between storage tiers
2. **Metadata consistency**: Checkpoint metadata is stored alongside data in each tier
3. **Atomic operations**: Each checkpoint operation is atomic across all items

## Logging

Logs are written to both console and namespace-specific files:

- Console logs for immediate feedback during development
- File logs at `/var/log/sagemaker_checkpointing/{namespace}_checkpointing.log`
- Structured logging with rank, step, and operation details
- Separate log filtering for checkpointing-specific events

### Log Format
```
[timestamp] [namespace] [logger_name] [INFO] [filename:451] [Rank 0] Step 240: Starting checkpoint write ([SavePlan Items Count] items)
[timestamp] [namespace] [logger_name] [INFO] [filename:498] [Rank 0] Step 240: In-memory write completed in [Latency]s ([Throughput] MB/s)
[timestamp] [namespace] [logger_name] [INFO] [filename:530] [Rank 0] Step 240: S3 batch write completed in [Latency]s ([Size] total, [Throughput] MB/s average)
```

## Error Handling and Recovery

### Automatic Fallback Scenarios

The library handles various failure scenarios automatically:

1. **In-memory service unavailable**: Falls back to S3 storage
2. **Partial write failures**: Ensures all-or-nothing consistency
3. **Network interruptions**: Retries with exponential backoff
4. **S3 throttling**: Automatic retry with jitter

## Best Practices

### 1. Namespace Management
```python
import time
import os

# Use unique namespaces per training job
config = SageMakerCheckpointConfig(
    namespace=os.environ.get('TRAINING_JOB_NAME', f'job-{int(time.time())}'),
    world_size=dist.get_world_size()
)
```

### 2. Save Frequency Optimization
```python
# Balance performance vs. durability based on model size
model_size_gb = sum(p.numel() * p.element_size() for p in model.parameters()) / (1024**3)

if model_size_gb > 10:  # Large models
    s3_save_freq = 200  # Less frequent S3 saves
elif model_size_gb > 1:  # Medium models
    s3_save_freq = 100
else:  # Small models
    s3_save_freq = 50

config = SageMakerCheckpointConfig(
    namespace=os.environ.get('TRAINING_JOB_NAME', f'job-{int(time.time())}'),
    world_size=world_size,
    save_to_s3=True,
    s3_tier_base_path="s3://bucket/checkpoints"
)
```

### 3. Memory Management
```python
# For very large models, consider checkpointing less frequently
# or using gradient checkpointing to reduce memory usage

if torch.cuda.memory_allocated() > 0.8 * torch.cuda.max_memory_allocated():
    print("High memory usage detected, reducing checkpoint frequency")
    # Adjust checkpoint frequency dynamically
```

### 4. Error handling
Add required exception handling for failures in save and load checkpoint
operations to prevent interruptions to the training jobs.
```python
    # Exception handling on the future corresponding to the async_save
    if future is not None:
        exc = future.exception()
        if exc:
            print(f"Failure in saving previous checkpoint: {str(exc)}")
            # Handle failures as required
        else:
            result = future.result()
            # Process results from save, if required
```

```python
    # Exception handling for load
    try:
        state_dict = {
            "model": model.state_dict(),
            "optimizer": optimizer.state_dict(),
            "lr_scheduler": lr_scheduler.state_dict(),
            "step": 0
        }

        storage_reader = SageMakerTieredStorageReader(checkpoint_config=checkpoint_config)
        load(state_dict, storage_reader=storage_reader)

        model.load_state_dict(state_dict["model"])
        optimizer.load_state_dict(state_dict["optimizer"])
        lr_scheduler.load_state_dict(state_dict["lr_scheduler"])
        start_step = state_dict["step"] + 1

        print(f"Resumed training from step {start_step}")
    except BaseException as e:
        print(f"No checkpoint found, starting from scratch: {str(e)}")
```

## Troubleshooting

### Common Issues

1. **"Namespace cannot be empty"**
   - Ensure `namespace` is provided in `SageMakerCheckpointConfig`
   - Use descriptive, unique namespaces for each training job

2. **"Invalid S3 tier base path"**
   - S3 paths must start with `s3://`
   - Example: `s3://my-bucket/checkpoints`
   - Ensure bucket exists and is accessible

3. **"Unable to fetch region for S3 bucket"**
   - Ensure AWS credentials are properly configured
   - Verify S3 bucket exists and is accessible
   - Check IAM permissions for S3 access

4. **"Invalid step value"**
   - Provide explicit step number or ensure path contains `step_N` pattern
   - Example valid paths: `/path/step_100/checkpoint`, `step_42`

### Performance Optimization

1. **Adjust save frequencies** based on model size and training speed
3. **Use appropriate S3 bucket regions** to minimize latency
4. **Configure retention policies** to manage storage costs
5. **Consider checkpoint compression** for very large models

## Requirements

- Python >= 3.10
- PyTorch with distributed checkpoint support
- AWS credentials configured (for S3 tier)
- Network access to in-memory checkpoint service (if using in-memory tier)

## Dependencies

- `torch`: PyTorch framework
- `boto3`: AWS SDK for Python
- `s3torchconnector`: S3 integration for PyTorch
- `tenacity`: Retry mechanisms
- `xxhash`: Fast hashing for checksums

## License

This project is licensed under the Apache License 2.0. See the LICENSE.txt file in the package for details.
