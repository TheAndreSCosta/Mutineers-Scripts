import threading
import time

from credentials import load_credentials
from properties import load_config
from prompt import prompt_environment, prompt_data_centers, prompt_dev_flavors
from gen_hosts import generate_hostnames
from jmx_operations import jmx_operations
from ssh_operatrions import restart_routine
from collections import defaultdict

credentials = load_credentials()

SBV2_USERNAME = credentials["SBV2_USERNAME"]
SBV2_PASSWORD = credentials["SBV2_PASSWORD"]

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


    failed_hosts = jmx_operations(hostnames)
    
    def get_az(hostname):
        # Example: extract AZ from hostname, adjust regex as needed
        # If AZ is always the first 3 chars, e.g., "wv0-fbofd01a-prd..."
        return hostname.split('-')[0]
    
    #DEBUG - start -
    print("\n Failed Hostnames AZ:")
    for failed_host in failed_hosts:
        print(f" - {get_az(failed_host)}")
    #DEBUG - end -
    
    def restart_and_check(host, max_retries=6):  # 6 retries = 1 hour max with 10min interval
        print(f"\n[THREAD] Starting restart routine for {host}")
        try:
            restart_routine(host, SBV2_USERNAME, SBV2_PASSWORD)
        except Exception as e:
            print(f"[THREAD] Error restarting {host}: {e}")
            return

        retries = 0
        while retries < max_retries:
            print(f"[THREAD] Waiting 10 minutes before checking status for {host} (retry {retries+1}/{max_retries})")
            time.sleep(600)  # 10 minutes
            try:
                status = jmx_operations([host])
            except Exception as e:
                print(f"[THREAD] Error checking status for {host}: {e}")
                status = True  # Assume still failing to retry

            if not status:
                print(f"[THREAD] {host} is now cacheIsRunning=true. Stopping thread.")
                break
            else:
                print(f"[THREAD] {host} still cacheIsRunning=false. Retrying...")
                retries += 1

        if retries == max_retries:
            print(f"[THREAD] Max retries reached for {host}. Giving up.")


    if failed_hosts:
        print("\nHosts with cacheIsRunning=false:")
        for host in failed_hosts:
            print(f" - {host}")

        threads = []
        for host in failed_hosts:
            t = threading.Thread(target=restart_and_check, args=(host,))
            t.start()
            threads.append(t)

        # Wait for all threads to finish
        for t in threads:
            t.join()
    else:
        print("\nAll hosts returned cacheIsRunning=true.")