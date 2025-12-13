#!/bin/bash
set -e

mkdir -p .hatch

cat > .hatch/hatch_plugin.py << 'EOF'
from hatch.env.collectors.plugin.interface import EnvironmentCollectorInterface

class CustomEnvironmentCollector(EnvironmentCollectorInterface):
    PLUGIN_NAME = 'custom'
    
    def get_initial_config(self):
        return {}
    
    def finalize_config(self, config):
        return config
EOF

echo "Hatch plugin created"
