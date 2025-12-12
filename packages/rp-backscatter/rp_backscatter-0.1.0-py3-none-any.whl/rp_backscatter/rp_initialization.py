import rp
import backscatter_packaged
from backscatter_packaged import *
import argparse


def initializeAndSetVariablesOnRP(channel, bufferSize, decimation, trig_lvl, source):
    initializeInterface()
    g_adc_axi_start, g_adc_axi_size = getMemoryRegion()
    print(f"Reserved memory Start: {g_adc_axi_start:x} Size: {g_adc_axi_size:x}\n")
    setDecimationFactor(decimation)
    setTriggerDelay(channel, int(bufferSize))
    acq1_start_address = g_adc_axi_start
    setBufferSamples(channel, acq1_start_address, bufferSize)
    enableDMA(channel, True)
    acqSetTriggerLevel(channel, trig_lvl)
    acqSetTriggerSrc(source)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--channel", type=str)
    parser.add_argument("--buffer_size", type=int)
    parser.add_argument("--decimation", type=int)
    parser.add_argument("--trig_level", type=float)
    parser.add_argument("--source", type=int)
    args = parser.parse_args()

    initializeAndSetVariablesOnRP(
        channel=args.channel,
        bufferSize=args.buffer_size,
        decimation=args.decimation,
        trig_lvl=args.trig_level,
        source=args.source
    )

    