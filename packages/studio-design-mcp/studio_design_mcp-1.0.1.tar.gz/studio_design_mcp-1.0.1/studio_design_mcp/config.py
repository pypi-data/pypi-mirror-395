import os
import sys

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

"""
Configuration for Designer Studio MCP server.
Focused on mobile UI inspiration: Mobbin only.
"""

class Config:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._initialized = True
            self._initialize_config()

    def _initialize_config(self):
        # Working directory configuration
        self.WORKING_PATH = os.environ.get('WORKING_PATH', os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../temp'))
        os.makedirs(self.WORKING_PATH, exist_ok=True)

        # Mobbin configuration
        self.MOBBIN_USERNAME = os.environ.get('MOBBIN_USERNAME')
        self.MOBBIN_PASSWORD = os.environ.get('MOBBIN_PASSWORD')
        
        # Figma configuration
        self.FIGMA_TOKEN = os.environ.get('FIGMA_TOKEN')

    def _get_config_value(self, env_var: str, default_value: str) -> str:
        value = os.environ.get(env_var)
        if value:
            print(f"Using {env_var} from environment")
            return value
        print(f"Using default value for {env_var}")
        return default_value

# Create global config instance
config = Config()
