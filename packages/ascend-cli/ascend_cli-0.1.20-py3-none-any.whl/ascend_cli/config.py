import configparser
from pathlib import Path
import shutil
import os

APP_NAME = "ascend"
APP_DIR = Path(os.path.expanduser("~")) / f".{APP_NAME}"
CONFIG_FILE_NAME = "config.conf"
DEFAULT_CONFIG_PATH = APP_DIR / CONFIG_FILE_NAME
DATA_DIR = APP_DIR / "data"
LOGS_DIR = APP_DIR / "logs"

class ConfigError(Exception):
    """Custom exception for configuration-related errors."""
    pass

def _ensure_app_dir_exists():
    """
    Ensures that the application directory and its subdirectories exist,
    and copies the default config if it's not there.
    """
    if DEFAULT_CONFIG_PATH.exists():
        return

    # Create all necessary directories
    APP_DIR.mkdir(exist_ok=True)
    DATA_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)

    # Copy the template config file from the package
    try:
        # This locates the template file inside the installed package
        package_dir = Path(__file__).parent.resolve()
        template_path = package_dir / CONFIG_FILE_NAME
        if template_path.exists():
            shutil.copy(template_path, DEFAULT_CONFIG_PATH)
            print(f"✅ A new configuration file has been created for you at: {DEFAULT_CONFIG_PATH}")
            print("   Please review and edit it for your needs.")
        else:
            # This case should not happen in a normal installation
            raise ConfigError(f"Could not find the config template inside the package at {template_path}.")
    except Exception as e:
        raise ConfigError(f"Failed to create the default configuration file. Reason: {e}")

class ConfigManager:
    def __init__(self, config_file_path: Path, section: str):
        self.config_file = config_file_path
        self.section = section
        self.parser = configparser.ConfigParser()
        self.settings = {}

        if self.config_file and self.config_file.is_file():
            self.parser.read(self.config_file)
        elif self.config_file:
            raise ConfigError(f"Configuration file specified but not found: {self.config_file}")
        else:
            # This can happen if get_config_path returns None, which it shouldn't
            # after the new logic, but as a safeguard.
            raise ConfigError("No valid configuration file could be found or created.")

    def load(self, **kwargs):
        """
        Loads settings from the config file and merges them with command-line arguments.
        Command-line arguments (kwargs) override config file settings.
        """
        config_from_file = {}
        if self.parser.has_section(self.section):
            config_from_file = dict(self.parser.items(self.section))

        self.settings = config_from_file.copy()
        
        cli_args = {k: v for k, v in kwargs.items() if v is not None}
        self.settings.update(cli_args)

    def get(self, key: str, required: bool = True, default=None):
        """
        Retrieves a setting by key. Raises ConfigError if a required setting is missing.
        """
        value = self.settings.get(key)
        if value is None or value == '':
            if required:
                raise ConfigError(f"Missing required setting: '{key}'. "
                                  f"Provide it in '{self.config_file}' under section '[{self.section}]' "
                                  "or as a command-line option.")
            return default
        return value

    def get_app_data_dir(self) -> Path:
        """
        Returns the application's data directory path.
        This is a centralized place for the class to provide this path.
        """
        return DATA_DIR

def get_config_path(cli_config_path: Path | None) -> Path:
    """
    Determines the configuration file path with the following priority:
    1. Path provided via --config CLI flag.
    2. Default path at ~/.ascend/config.conf.
    
    Ensures the default directory structure and config file exist if needed.
    """
    if cli_config_path:
        return cli_config_path
    
    # If no CLI path is given, ensure the default app directory is set up.
    _ensure_app_dir_exists()
    
    return DEFAULT_CONFIG_PATH 