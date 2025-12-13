class SageMakerTieredStorageError(Exception):
    """Base exception class for all SageMaker checkpointing errors."""

    pass


class SageMakerInMemoryTierError(SageMakerTieredStorageError):
    """Errors related to InMemory Tier."""

    pass


class SageMakerS3TierError(SageMakerTieredStorageError):
    """Errors related to S3 Tier."""

    pass


class SageMakerTieredStorageConfigError(SageMakerTieredStorageError):
    """Errors related to checkpoint configuration."""

    pass
