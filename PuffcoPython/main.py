import asyncio
from aioflask import Flask, render_template
from bleak import BleakClient
from flask import request
import struct

address = "AA:BB:CC:DD:EE:FF"#Change this to your puffco bluetooth address
COMMAND = "F9A98C15-C651-4F34-B656-D100BF580040"

DEVICE_NAME = "F9A98C15-C651-4F34-B656-D100BF58004D"

PROFILE_CURRENT = "F9A98C15-C651-4F34-B656-D100BF580041"
PROFILE = "F9A98C15-C651-4F34-B656-D100BF580061"
PROFILE_NAME = "F9A98C15-C651-4F34-B656-D100BF580062"
PROFILE_PREHEAT_TEMP = "F9A98C15-C651-4F34-B656-D100BF580063"
PROFILE_PREHEAT_TIME = "F9A98C15-C651-4F34-B656-D100BF580064"

def parse(data):
    stuct = struct.unpack('f', data)
    remove = ['(', ',', ')']
    for chars in remove:
        stuct = str(stuct).replace(chars, "")
    return stuct

loop = asyncio.get_event_loop()
client = BleakClient(address, loop=loop)
app = Flask(__name__)

async def changeProfile(prof, realProfileBytes = False):
    if(prof == 0):
        profile = bytearray([0, 0, 0, 0])
    elif(prof == 1):
        profile = bytearray([1, 0, 0, 0])
    elif(prof == 2):
        profile = bytearray([2, 0, 0, 0])
    elif(prof == 3):
        profile = bytearray([3, 0, 0, 0])
    print("Changed profile to {}".format(prof))
    await client.write_gatt_char(PROFILE, profile)
    if(realProfileBytes):
        if(prof == 0):
            profile = bytearray([0, 0, 0, 0])
        elif(prof == 1):
            profile = bytearray([0, 0, 128, 63])
        elif(prof == 2):
            profile = bytearray([0, 0, 0, 64])
        elif(prof == 3):
            profile = bytearray([0, 0, 64, 64])
        await client.write_gatt_char(PROFILE_CURRENT, profile)


async def getProfileTemp():
    test = await client.read_gatt_char(PROFILE_PREHEAT_TEMP)
    data = parse(test)
    return int(round(float(data), 1))

async def getProfileTime():
    test = await client.read_gatt_char(PROFILE_PREHEAT_TIME)
    data = parse(test)
    return int(round(float(data), 1))

async def setProfileTime(seconds):
    time = struct.pack("<f", seconds)
    print(time)
    await client.write_gatt_char(PROFILE_PREHEAT_TIME, time)

async def setProfileTemp(temp):
    temperature = struct.pack("<f", temp)
    print(temperature)
    await client.write_gatt_char(PROFILE_PREHEAT_TEMP, temperature)

async def getProfile():
    test = await client.read_gatt_char(PROFILE_CURRENT)
    data = parse(test)
    return int(round(float(data), 1))

async def getProfileName():
    test = await client.read_gatt_char(PROFILE_NAME)
    return test.decode()

async def getDeviceName():
    name = await client.read_gatt_char(DEVICE_NAME)
    return name.decode()

async def sendCommand(client, commandArray):
    await client.write_gatt_char(COMMAND, commandArray)

@app.route('/preheat', methods=['GET'])
async def handle_preheat():
    temp = request.args.get('temperature','')
    secs = request.args.get('seconds','')
    if(temp):
        await changeProfile(await getProfile())
        await setProfileTemp(float(temp))
        await setProfileTime(float(secs))
        preheatBytes = bytearray([0, 0, 224, 64])
        await sendCommand(client, preheatBytes)
        return "Preheating puffco to " + temp + "celcius for " + secs + " seconds", 200
    else:
        return "lol", 200

@app.route('/cmd', methods=['GET'])
async def handle_cmd():
    command = request.args.get('command','')
    profile = request.args.get('profile','')
    if(command == "preheat"):
        if(profile != ""):
            if(profile == "1"):
                profile = 0
            elif(profile == "2"):
                profile = 1
            elif(profile == "3"):
                profile = 2
            elif(profile == "4"):
                profile = 3
            await changeProfile(profile, True)
            preheatBytes = bytearray([0, 0, 224, 64])
            await sendCommand(client, preheatBytes)
            return "Starting preheat for profile {}. ".format(await getProfileName()), 200
        await changeProfile(await getProfile())
        preheatBytes = bytearray([0, 0, 224, 64])
        await sendCommand(client, preheatBytes)
        return "Starting preheat for profile {}. Heating to {} celsius for {} seconds".format(await getProfileName(), await getProfileTemp(), await getProfileTime()), 200
    return "Command not found", 200

@app.route('/')
async def index():
    try:
        await asyncio.wait_for(client.connect(), timeout=7.5)
        print(f"Connected: {client.is_connected}\n")
        return f"Connected to {await getDeviceName()}", 200
    except asyncio.TimeoutError:
        return f"Failed to connect to puffco", 400
    
app.run(address="127.0.0.1", port="8080")
