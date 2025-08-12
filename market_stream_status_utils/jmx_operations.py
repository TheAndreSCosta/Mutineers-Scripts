import requests

from credentials import load_credentials

# ANSI escape codes for colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

credentials = load_credentials()

SBV2_USERNAME = credentials["SBV2_USERNAME"]
SBV2_PASSWORD = credentials["SBV2_PASSWORD"]
JMX_USERNAME = credentials["JMX_USERNAME"]
JMX_PASSWORD = credentials["JMX_PASSWORD"]

session = requests.Session()

payload = {
    "username": "jmxadmin",  # Replace with your actual username
    "password": "password03"   # Replace with your actual password
}

def jmx_operations(hostnames):
    for hostname in hostnames:
        login_url = f"http://{hostname}:8443/login"
        status_url = f"http://{hostname}:8443/management/market-stream/status"
        try:    
            login_response = session.post(login_url, data=payload, allow_redirects=False, timeout=1.2)

            if login_response.status_code == 302:
                CYAN = "\033[96m"
                MAGENTA = "\033[95m"
                print(f"Login successful on host {hostname}, redirecting...")

                status_response = session.get(status_url)

                # Check if we successfully accessed the status page
                if status_response.status_code == 200:
                    # Print the content of the response (Market Stream Status)
                    # print(status_response.text)
                    
                    cache_running = status_response.text.split()[3]
                    cache_health = status_response.text.split()[4]
                    if cache_running == "cacheIsRunning=true":
                        print(f"{GREEN}{cache_running} {cache_health}{RESET}")
                    else:
                        print(f"{RED}{cache_running} {cache_health}{RESET}")
                    # # Check if the first string matches the required conditions
                    # if cache_running == "cacheIsRunning=true" or cache_running == "cacheIsRunning=false":
                    #     break
                else:
                    print(f"Failed to access status page: {status_response.status_code}")

            else:
                print(f"Login failed: {login_response.status_code}")
                print(login_response.text) 
                
        except requests.exceptions.Timeout:
            print(f"Request timed out for {YELLOW}{hostname}. Continuing to next iteration.")
