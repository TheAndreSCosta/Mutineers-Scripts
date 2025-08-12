from properties import load_config
from prompt import prompt_environment, prompt_data_centers, prompt_dev_flavors
from gen_hosts import generate_hostnames
from jmx_operations import jmx_operations
from ssh_operatrions import ssh_connect, restart_routine


config = load_config()

NODE_COUNT = config["NODE_COUNT"]
INDEXES = config["INDEXES"]
DEFAULT_ENV = config["DEFAULT_ENV"]
ENVIRONMENTS = config["ENVIRONMENTS"]

if __name__ == "__main__":
    env = prompt_environment()
    env_dcs = ENVIRONMENTS.get(env, [])
    selected_dcs = prompt_data_centers(env, env_dcs)

    if env == "dev":
        dev_flavors = prompt_dev_flavors()
    else:
        dev_flavors = None


    hostnames = generate_hostnames(
        dcs=selected_dcs,
        env=env,
        node_count=NODE_COUNT,
        indexes=INDEXES,
        dev_flavors=dev_flavors
    )

    #DEBUG - start -
    print("\n Generated Hostnames:")
    for hostname in hostnames:
        print(f" - {hostname}")
    #DEBUG - end -

    jmx_operations(hostnames)