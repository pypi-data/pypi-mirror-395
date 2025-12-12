"""VirtualDojo CLI - Command-line interface for VirtualDojo CRM."""

__version__ = "0.3.0"
__app_name__ = "virtualdojo-cli"

# Default server URL - change this for your deployment
DEFAULT_SERVER_URL = "https://app01.virtualdojo.com"

# Common development URLs (for reference)
DEV_URLS = {
    "local": "http://localhost:8000",
    "docker": "http://localhost:8000",
    "staging": "https://staging.virtualdojo.com",
    "production": "https://app01.virtualdojo.com",
}
