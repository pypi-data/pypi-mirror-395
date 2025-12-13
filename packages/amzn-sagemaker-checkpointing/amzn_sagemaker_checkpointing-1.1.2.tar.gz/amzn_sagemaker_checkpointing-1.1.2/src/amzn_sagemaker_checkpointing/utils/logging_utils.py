import logging


class SageMakerCheckpointingLoggerAdapter(logging.LoggerAdapter):
    """Adapter that adds checkpointing marker to all log records"""

    def process(self, msg, kwargs):
        # Add custom attribute to identify checkpointing logs
        if "extra" not in kwargs:
            kwargs["extra"] = {}
        kwargs["extra"]["_sagemaker_checkpointing"] = True
        return msg, kwargs


class CheckpointFilter(logging.Filter):
    """Filter that only allows checkpointing logs"""

    def filter(self, record):
        # Only allow records with our custom attribute
        return hasattr(record, "_sagemaker_checkpointing")
