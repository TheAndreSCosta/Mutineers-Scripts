import paramiko
import subprocess
import time

def ssh_connect(host, username, password, command, use_sudo=False):
    try:
        # Remove old host key to avoid host key verification errors
        try:
            subprocess.run(["ssh-keygen", "-R", host], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as e:
            print(f"Warning: Could not remove old host key for {host}: {e}")

        ssh = paramiko.SSHClient()
        # Automatically add the host key if not already known
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(hostname=host, username=username, password=password)

        if use_sudo:
            command = f"echo {password} | sudo -S {command}"

        stdin, stdout, stderr = ssh.exec_command(command)

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

        # if output:
        #     print("Output:")
        #     print(output)
        if error:
            print("Error:")
            print(error)

        # Wait for the stop command to complete before proceeding
        if "stop" in command.lower():
            print("Waiting for the stop command to complete...")
            time.sleep(5)  
        # Wait for the start command to allow service initialization
        if "start" in command.lower():
            print("Waiting for the start command to complete...")
            time.sleep(5)