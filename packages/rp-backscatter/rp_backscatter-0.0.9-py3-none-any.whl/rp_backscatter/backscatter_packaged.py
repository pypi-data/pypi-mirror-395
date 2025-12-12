import numpy as np
import rp
import time
import argparse

def createBuffer(bufferSize):
    return np.zeros(int(bufferSize), dtype=np.int16)

def getMemoryRegion():
    memoryRegion = rp.rp_AcqAxiGetMemoryRegion()
    g_adc_axi_start = memoryRegion[1]
    g_adc_axi_size = memoryRegion[2] 
    return g_adc_axi_start, g_adc_axi_size 

def initializeInterface():
    rp.rp_Init()
    rp.rp_AcqReset()
    print("Acquisition Reset\n")

def setDecimationFactor(dec):
    rp.rp_AcqAxiSetDecimationFactor(dec)

def setTriggerDelay(channel, size):
    rp.rp_AcqAxiSetTriggerDelay(channel,int(size))   #rp.RP_CH_1

def setBufferSamples(channel, start_address, bufferSize):
    rp.rp_AcqAxiSetBufferSamples(channel, start_address, int(bufferSize))  #rp.RP_CH_1

def enableDMA(channel, enable):
    rp.rp_AcqAxiEnable(channel, enable)

def rp_AcqSetTriggerLevel(trigger_channel, level):
    rp.rp_AcqSetTriggerLevel(trigger_channel, level)

def startAcquisition():
    rp.rp_AcqStart()
    print("ACQ Started\n")

def acqSetTriggerLevel(trigger_channel, level):
    rp.rp_AcqSetTriggerLevel(trigger_channel, level)

def acqSetTriggerSrc(source):
    rp.rp_AcqSetTriggerSrc(source)

def stopAcquisition():
    rp.rp_AcqStop()
    print("Stop DMA acq\n")

def startDataAcquisition(acquisition_time):
    startAcquisition()
    print("ACQ Started\n")
    rp.rp_AcqSetTriggerSrc(rp.RP_TRIG_SRC_CHA_PE)
    state = rp.RP_TRIG_STATE_TRIGGERED

    while 1:
        state = rp.rp_AcqGetTriggerState()[1]
        if state == rp.RP_TRIG_STATE_TRIGGERED:
            print("Triggered")
            time.sleep(acquisition_time)
            break

def checkFillState():
    fillState = False
    while not fillState:
        fillState = rp.rp_AcqAxiGetBufferFillState(rp.RP_CH_1)[1]
    print("DMA buffer full")
    return fillState

def getWritePointerAtTrig(channel):
    posChA = rp.rp_AcqAxiGetWritePointerAtTrig(channel)[1]
    return posChA

def transferCapturedData(bufferSize, posChA, file_name, CHUNK):
    start_time = time.perf_counter()
    with open(file_name, "wb") as f:
        for offset in range(0, int(bufferSize), CHUNK):
            this_chunk = min(CHUNK, int(bufferSize) - offset)
            buf = np.zeros(this_chunk, dtype=np.int16)
            # ---- Start timing DMA read ----
            t0 = time.perf_counter()
            rp.rp_AcqAxiGetDataRawNP(rp.RP_CH_1, posChA + offset, buf)
            t1 = time.perf_counter()
            dma_read_time = t1 - t0
            # ---- End timing DMA read ----
            f.write(buf.tobytes())
            print("Sent data to PC")
            print(f"Chunk {offset//CHUNK + 1} | {this_chunk} samples | DMA read time: {dma_read_time:.6f} s")

    end_time = time.perf_counter()
    elapsed = end_time - start_time
    print(f"DMA save complete.")
    print(f"Total time: {elapsed:.2f} seconds")
    print(f"File size: ~{bufferSize*2/1024/1024:.1f} MB")
    print(f"Speed: {(bufferSize*2/1e6)/elapsed:.1f} MB/s")


def disableAxiChannel(channel):
    rp.rp_AcqAxiEnable(channel, False)

def releaseResources():
    print("\nReleasing resources\n")
    rp.rp_Release()

# def runRedPitayaBackscatterPipeline(channel, bufferSize, decimation, trig_lvl, acquisition_time, file_name, chunk_size, source):
#     initializeInterface()
#     g_adc_axi_start, g_adc_axi_size = getMemoryRegion()
#     print(f"Reserved memory Start: {g_adc_axi_start:x} Size: {g_adc_axi_size:x}\n")
#     setDecimationFactor(decimation)
#     setTriggerDelay(channel, int(bufferSize))
#     acq1_start_address = g_adc_axi_start
#     setBufferSamples(channel, acq1_start_address, bufferSize)
#     enableDMA(channel, True)
#     acqSetTriggerLevel(channel, trig_lvl)
#     acqSetTriggerSrc(source)
#     startDataAcquisition(acquisition_time)
#     checkFillState()
#     stopAcquisition()
#     posCha = getWritePointerAtTrig(channel)
#     transferCapturedData(bufferSize, posCha, file_name, chunk_size)
#     disableAxiChannel(channel)
#     releaseResources()
#     print("Finished execution of Red Pitaya backscatter pipeline.")

def runRedPitayaBackscatterPipeline(channel, bufferSize, acquisition_time, file_name, chunk_size):
    startDataAcquisition(acquisition_time)
    checkFillState()
    stopAcquisition()
    posCha = getWritePointerAtTrig(channel)
    transferCapturedData(bufferSize, posCha, file_name, chunk_size)
    disableAxiChannel(channel)
    releaseResources()
    print("Finished execution of Red Pitaya backscatter pipeline.")

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
    print("Finished initializing and setting variables on RP.")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--channel", type=str)
    parser.add_argument("--buffer_size", type=int)
    parser.add_argument("--acquisition_time", type=float)
    parser.add_argument("--file_name", type=str)
    parser.add_argument("--chunk_size", type=int)
    args = parser.parse_args()

    print("\n--- Received Parameters in backscatter_packaged.py ---")
    for k, v in vars(args).items():
        print(f"{k}: {v}")
    print("--------------------------------------------------------\n")

    runRedPitayaBackscatterPipeline(
            channel=args.channel,
            bufferSize=args.buffer_size,
            acquisition_time=args.acquisition_time,
            file_name=args.file_name,
            chunk_size=args.chunk_size,
        )

