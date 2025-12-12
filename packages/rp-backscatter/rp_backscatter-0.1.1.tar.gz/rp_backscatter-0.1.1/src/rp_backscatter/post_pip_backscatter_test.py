import rp_backscatter
import numpy as np
import matplotlib.pyplot as plt
from rp_backscatter import ssh_connection
from pathlib import Path
import rp
import backscatter_packaged
from backscatter_packaged import *
import rp_initialization
from rp_initialization import *

RP_IP = "169.254.188.142"
USERNAME = "root"
PASSWORD = "root"
REMOTE_DMA_PATH = "/root/dma.bin"
LOCAL_DMA_PATH  = "C:/Users/kings/OneDrive/Desktop/red_pitaya_backscatter/dma.bin"
pd_initialization = {'buffer_size': 114294784, 'decimation': 1, 'trig_level': 0.1, 
        'acquisition_time': 1, 'file_name': 'dma.bin', 'chunk_size': 20000000, 'source': 'rp.RP_TRIG_SRC_CHA_PE'}

n = 5000
ADC_bit_to_voltage_factor = 8192
channel_name = 'Channel 1'
PKL_FILE_DIRECTORY_PATH = Path(r"C:\Users\kings\OneDrive\Desktop\Research\INSITE2_gui\ssh_log.pkl")
ssh_key = rp_backscatter.ssh_connection.setup_ssh_connection(RP_IP, USERNAME, PASSWORD, PKL_FILE_DIRECTORY_PATH)
print(ssh_key)
pd_acq = {'channel': 'rp.RP_T_CH_1', 'buffer_size': 114294784, 'decimation': 1, 'trig_level': 0.1, 
        'acquisition_time': 1.0, 'file_name': 'dma.bin', 'chunk_size': 20000000}
#rp_backscatter.ssh_connection.execute_remote_command_initialization(ssh_key, pd_initialization)
rp_backscatter.ssh_connection.run_SSH_rp_backscatter_pipeline(pd_acq, REMOTE_DMA_PATH, LOCAL_DMA_PATH,
                                 ADC_bit_to_voltage_factor, ssh_key)

