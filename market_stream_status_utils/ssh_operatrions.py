import paramiko
import time

def ssh_connect(host, username, password, command, use_sudo=False):
    try:
        # Create an SSH client
        ssh = paramiko.SSHClient()
        
        # Automatically add the host key if not already known
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect to the host
        ssh.connect(hostname=host, username=username, password=password)
        
        # If sudo is required, prepend 'sudo -S' to the command and pass the password
        if use_sudo:
            command = f"echo {password} | sudo -S {command}"

        # Execute the command
        stdin, stdout, stderr = ssh.exec_command(command)
        
        # Read the output and error streams
        output = stdout.read().decode()
        error = stderr.read().decode()
        
        # Close the connection
        ssh.close()
        
        return output, error
    except Exception as e:
        return None, str(e)
    
def restart_routine(host, username, password):
    """
    Executes a restart routine on the given host.
    The routine includes checking the service status, stopping the service, waiting for completion, and restarting it.

    :param host: The target host to execute the routine on.
    :param username: SSH username.
    :param password: SSH password.
    """
    commands = [
        "systemctl status ppb-fbo-service",
        "systemctl stop ppb-fbo-service",
        "systemctl status ppb-fbo-service",
        "systemctl start ppb-fbo-service",
        "systemctl status ppb-fbo-service"
    ]

    for i, command in enumerate(commands):
        print(f"Executing command {i + 1}/{len(commands)}: {command} on {host}...")
        output, error = ssh_connect(host, username, password, command, use_sudo=True)

        if output:
            print("Output:")
            print(output)
        if error:
            print("Error:")
            print(error)

        # Wait for the stop command to complete before proceeding
        if "stop" in command.lower():
            print("Waiting for the stop command to complete...")
            time.sleep(5)  # Waiting for the stop command to complete)