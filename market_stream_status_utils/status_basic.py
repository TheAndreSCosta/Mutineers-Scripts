import requests

# ANSI escape codes for colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# Start a session to maintain cookies and handle redirects
session = requests.Session()

# Get user input
user_input = input("Enter a state or a comma-separated list of states (e.g. ny or ny,ca,tx): ")

# Split the input string into a list of data centers
dcs = [dc.strip() for dc in user_input.split(',')]

#TODO: Delete this print
print(dcs)  # This will print the list of data centers

indexes = ['a', 'b']
node_numbers = ['01', '02', '03']

# Define the payload (login credentials)
payload = {
    "username": "jmxadmin",  # Replace with your actual username
    "password": "password03"   # Replace with your actual password
}

for dc in dcs:
    for node_number in node_numbers:
        for index in indexes:
            print("Querying state: ", dc)
            
            login_url = f"http://{dc}0-fbofd{node_number}{index}-prd{dc}.prd.fndlsb.net:8443/login"
            status_url = f"http://{dc}0-fbofd{node_number}{index}-prd{dc}.prd.fndlsb.net:8443/management/market-stream/status"
            try:    
                login_response = session.post(login_url, data=payload, allow_redirects=False, timeout=1.2)

                if login_response.status_code == 302:
                    CYAN = "\033[96m"
                    MAGENTA = "\033[95m"
                    print(f"Login successful on host {dc}0-fbofd{YELLOW}{node_number}{RESET}{MAGENTA}{index}{RESET}-prd{dc}, redirecting...")

                    status_response = session.get(status_url)

                    # Check if we successfully accessed the status page
                    if status_response.status_code == 200:
                        # Print the content of the response (Market Stream Status)p
                        # print(status_response.text)
                        
                        cache_running = status_response.text.split()[3]
                        cache_healthy = status_response.text.split()[4]
                        if cache_running == "cacheIsRunning=true":
                            print(f"{GREEN}{cache_running} {cache_healthy}{RESET}")
                        else:
                            print(f"{RED}{cache_running} {cache_healthy}{RESET}")
                        # Check if the first string matches the required conditions
                        if cache_running == "cacheIsRunning=true" or cache_running == "cacheIsRunning=false":
                            break
                    else:
                        print(f"Failed to access status page: {status_response.status_code}")

                else:
                    print(f"Login failed: {login_response.status_code}")
                    print(login_response.text) 
                   
            except requests.exceptions.Timeout:
                print("Request timed out. Continuing to next iteration.")
