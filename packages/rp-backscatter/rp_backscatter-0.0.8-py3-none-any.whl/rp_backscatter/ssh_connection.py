import numpy as np
import matplotlib.pyplot as plt
from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient
import pickle
import time

def setup_ssh_connection(RP_IP, USERNAME, PASSWORD, pkl_file_path):
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    ssh_str_time = "created_at_" + time.strftime("%Y%m%d-%H%M%S")
    with pkl_file_path.open("wb") as f:
        pickle.dump(ssh_str_time, f)
    print("[PC] Connecting to Red Pitaya...")
    ssh.connect(RP_IP, username=USERNAME, password=PASSWORD)
    print("[PC] Connected.\n")
    return ssh

def execute_remote_command_backscatter(ssh, pd_acquisition, detected_python="/usr/bin/python"):
    cmd = (
        f"bash -lc '{detected_python} -u /root/backscatter_packaged.py "
        f"--acquisition_time {pd_acquisition['acquisition_time']} "
        f"--file_name {pd_acquisition['file_name']} "
        f"--chunk_size {pd_acquisition['chunk_size']} "
        f"--channel {pd_acquisition['channel']} "
        f"--buffer_size {pd_acquisition['buffer_size']}'"
    )
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print("[PC] Running DMA acquisition on RP...")
    for line in stdout:
        print("[RP]", line.strip())
        err = stderr.read().decode()
    if err:
        print("[RP STDERR]", err)
    exit_code = stdout.channel.recv_exit_status()
    print(f"[PC] Acquisition script exited with code {exit_code}\n")
    return exit_code

def execute_remote_command_initialization(ssh, pd_initialization, detected_python="/usr/bin/python"):
    cmd = (
    f"bash -lc '{detected_python} -u /root/rp_initialization.py "
    f"--channel {pd_initialization['channel']} "
    f"--buffer_size {pd_initialization['buffer_size']} "
    f"--decimation {pd_initialization['decimation']} "
    f"--trig_level {pd_initialization['trig_level']} "
    f"--source {pd_initialization['source']}'"
        )
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print("[PC] Running initialization on RP...")
    for line in stdout:
        print("[RP]", line.strip())
        # Capture STDERR
    err = stderr.read().decode()
    if err:
        print("[RP STDERR]", err)
    exit_code = stdout.channel.recv_exit_status()
    print(f"[PC] Initialization script exited with code {exit_code}\n")
    return exit_code

def transfer_from_ssh_to_local(ssh, remote_dma_path, local_dma_path):
    print("[PC] Transferring dma.bin from RP...")
    with SCPClient(ssh.get_transport()) as scp:
        scp.get(remote_dma_path, local_dma_path)
    print("[PC] File transferred.\n")

def load_samples(local_dma_path):
    samples = np.fromfile(local_dma_path, dtype=np.int16)
    return samples

def close_ssh_connection(ssh):
    ssh.close()
    print("[PC] SSH connection closed.")

def plot_first_n_samples(samples, n, ADC_bit_to_voltage_factor, channel_name):
    plt.figure(figsize=(10,5))
    plt.plot(samples[:n] / ADC_bit_to_voltage_factor, label=channel_name)
    plt.grid(True)
    plt.title(f"Red Pitaya DMA Sample Data - First {n} Samples")
    plt.legend()
    plt.show()

def run_SSH_rp_backscatter_pipeline(pd, remote_dma_path, local_dma_path, 
                                    ADC_bit_to_voltage_factor, ssh):
    print("Running remote backscatter command")
    execute_remote_command_backscatter(ssh, pd)
    print("Finished running remote backscatter command")
    print("Starting file transfer from ssh to local")
    transfer_from_ssh_to_local(ssh, remote_dma_path, local_dma_path)
    print("Finished file transfer")
    print("Loading samples")
    samples = load_samples(local_dma_path) / ADC_bit_to_voltage_factor
    print("Finished loading samples")
    return samples


    