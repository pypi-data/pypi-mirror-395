import unittest
from unittest import TestCase

from amzn_sagemaker_checkpointing.checkpointing.filesystem.exceptions import SageMakerTieredStorageConfigError
from amzn_sagemaker_checkpointing.checkpointing.filesystem.filesystem import SageMakerTieredStorageWriter
from amzn_sagemaker_checkpointing.config.sagemaker_checkpoint_config import SageMakerCheckpointConfig


class TestConfiguration(TestCase):
    def test_valid_configuration_variations(self):
        """Test various valid configuration combinations."""
        valid_configs = [
            # Minimal valid config
            {
                "namespace": "test",
                "world_size": 1,
            },
            # Config with all optional parameters
            {
                "namespace": "full-test",
                "world_size": 8,
                "disk_tier_base_path": "/tmp/checkpoints",
                "s3_tier_base_path": "s3://my-bucket/checkpoints",
                "save_to_s3": True,
                "save_to_disk": True,
            },
            # Config with special characters in namespace
            {
                "namespace": "test-with-dashes_and_underscores",
                "world_size": 4,
            },
            # Config with large world size
            {
                "namespace": "large-scale",
                "world_size": 1000,
            },
        ]

        for config_dict in valid_configs:
            with self.subTest(config=config_dict):
                config = SageMakerCheckpointConfig(**config_dict)
                self.assertEqual(config.namespace, config_dict["namespace"])
                self.assertEqual(config.world_size, config_dict["world_size"])

    def test_invalid_configuration_variations(self):
        """Test various invalid configuration combinations."""
        invalid_configs = [
            # Empty namespace
            {"namespace": "", "world_size": 1},
            # None namespace
            {"namespace": None, "world_size": 1},
            # Zero world size
            {"namespace": "test", "world_size": 0},
            # Negative world size
            {"namespace": "test", "world_size": -1},
            # Very large negative world size
            {"namespace": "test", "world_size": -999999},
            # pass save_to_s3 flag without s3_tier_base_path
            {"namespace": "test", "world_size": 1, "save_to_s3": True},
            # pass save_to_s3 flag with  empty s3_tier_base_path
            {
                "namespace": "test",
                "world_size": 1,
                "save_to_s3": True,
                "s3_tier_base_path": "",
            },
        ]

        for config_dict in invalid_configs:
            with self.subTest(config=config_dict):
                config = SageMakerCheckpointConfig(**config_dict)
                with self.assertRaises(SageMakerTieredStorageConfigError):
                    # Try to create a writer to trigger validation
                    SageMakerTieredStorageWriter(config, path="step_1", step=-1)


class TestConfigurationProperties(TestCase):
    def test_configuration_property_defaults(self):
        """Test that configuration properties have correct defaults."""
        config = SageMakerCheckpointConfig(namespace="test-defaults", world_size=2)

        # Test that required properties are set
        self.assertEqual(config.namespace, "test-defaults")
        self.assertEqual(config.world_size, 2)

        # Test that optional properties have reasonable defaults or None
        # (The actual defaults depend on the implementation)
        self.assertIsNotNone(config.save_to_disk)
        self.assertIsNotNone(config.save_to_s3)

    def test_configuration_property_assignment(self):
        """Test that configuration properties are correctly assigned."""
        config = SageMakerCheckpointConfig(
            namespace="test-assignment",
            world_size=8,
            disk_tier_base_path="/custom/local/path",
            s3_tier_base_path="s3://custom-bucket/path",
            save_to_disk=True,
            save_to_s3=True,
        )

        self.assertEqual(config.namespace, "test-assignment")
        self.assertEqual(config.world_size, 8)
        self.assertEqual(config.disk_tier_base_path, "/custom/local/path")
        self.assertEqual(config.s3_tier_base_path, "s3://custom-bucket/path")
        self.assertEqual(config.save_to_disk, True)
        self.assertEqual(config.save_to_s3, True)


if __name__ == "__main__":
    unittest.main()
