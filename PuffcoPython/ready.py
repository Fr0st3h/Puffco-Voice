import threading
import asyncio

readyMode = False
startPreheat = False

async def readyCallback(Device):
    print("Ready mode started a preheat cycle")
    preheatBytes = bytearray([0, 0, 224, 64])
    await Device.sendCommand(preheatBytes)

async def readyLoop(Device):
    global readyMode
    global startPreheat
    while readyMode:
        if not startPreheat:
            state = await Device.getChargeState()
            #print("Waiting for puffco to be plugged in..")
            if(state == 0):
                startPreheat = True
            await asyncio.sleep(1)
        if startPreheat:
            state = await Device.getChargeState()
            #print("Waiting for device to be unplugged..")
            if(state == 4):
                startPreheat = False
                await readyCallback(Device)
            await asyncio.sleep(1)
        
def runLoop(Device):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(readyLoop(Device))
    loop.close()