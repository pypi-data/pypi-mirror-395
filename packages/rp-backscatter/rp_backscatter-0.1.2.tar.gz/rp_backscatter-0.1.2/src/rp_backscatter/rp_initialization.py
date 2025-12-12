import rp
import backscatter_packaged
from backscatter_packaged import *
import argparse


def initializeAndSetVariablesOnRP(bufferSize, decimation, trig_lvl):
    initializeInterface()
    g_adc_axi_start, g_adc_axi_size = getMemoryRegion()
    print(f"Reserved memory Start: {g_adc_axi_start:x} Size: {g_adc_axi_size:x}\n")
    setDecimationFactor(decimation)
    setTriggerDelay(rp.RP_CH_1, int(bufferSize))
    acq1_start_address = g_adc_axi_start
    setBufferSamples(rp.RP_CH_1, acq1_start_address, bufferSize)
    enableDMA(rp.RP_CH_1, True)
    acqSetTriggerLevel(rp.RP_T_CH_1, trig_lvl)
    acqSetTriggerSrc(rp.RP_TRIG_SRC_CHA_PE)
    print("Finished initializing and setting variables on RP.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--buffer_size", type=int)
    parser.add_argument("--decimation", type=int)
    parser.add_argument("--trig_level", type=float)
    args = parser.parse_args()

    initializeAndSetVariablesOnRP(
        bufferSize=args.buffer_size,
        decimation=args.decimation,
        trig_lvl=args.trig_level,
    )

    