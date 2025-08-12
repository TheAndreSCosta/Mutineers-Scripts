# credentials.py
import os
import yaml

def load_credentials(path="resources/credentials.yml"):
    """
    Load credentials from a YAML file.

    :param credentials_file: Path to the credentials YAML file.
    :return: A dictionary containing the loaded credentials.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Credentials file '{path}' not found. Please ensure it exists.")

    try:
        with open(path, "r") as file:
            config = yaml.safe_load(file)

        return {
            "SBV2_USERNAME": config["credentials"]["sbv2"]["username"],
            "SBV2_PASSWORD": config["credentials"]["sbv2"]["password"],
            "JMX_USERNAME": config["credentials"]["jmx"]["username"],
            "JMX_PASSWORD": config["credentials"]["jmx"]["password"],
        }
    except KeyError as e:
        raise KeyError(f"Missing key in credentials file: {e}")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML file: {e}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred while loading credentials: {e}")