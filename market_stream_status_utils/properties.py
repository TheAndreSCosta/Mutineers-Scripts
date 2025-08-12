import yaml

def load_config(path="resources/properties.yml"):
    """Loads config from YAML and returns key components."""
    with open(path, "r") as f:
        config = yaml.safe_load(f)

    settings = config.get("settings", {})
    
    node_count = settings.get("node_count", 3)
    indexes = settings.get("indexes", ["a", "b"])
    default_env = settings.get("default_env", "dev")
    environments = settings.get("environments", {})

    return {
        "NODE_COUNT": node_count,
        "INDEXES": indexes,
        "DEFAULT_ENV": default_env,
        "ENVIRONMENTS": environments
    }
