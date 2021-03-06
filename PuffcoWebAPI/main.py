from Puffco import Puffco
from aioflask import Flask, render_template
from flask import request
import asyncio
from matplotlib import colors
import ready as Ready
import threading

mac = "PUFFCO MAC HERE"

loop = asyncio.get_event_loop()
app = Flask(__name__)
Device = Puffco(mac)

modes = list(["lantern", "party", "stealth", "ready"])
statusList = list(["on", "enable", "off", "disable"])

@app.route('/mode', methods=['GET'])
async def handle_mode():
    mode = request.args.get('type','')
    status = request.args.get('status','')
    color = request.args.get('color','')
    statusInList = False
    modeInList = False
    if(status in statusList):
        statusInList = True
    if(mode in modes):
        modeInList = True
    if(mode == "lantern"):
        if(status == "on" or status == "enable"):
            await Device.sendLanternStatus(1)
            return "Lantern was turned on for {}".format(await Device.getName())
        elif(status == "off" or status == "disable"):
            await Device.sendLanternStatus(0)
            return "Lantern was turned off for {}".format(await Device.getName())
        elif(color):
            try:
                colour = colors.hex2color(colors.cnames[color])
                red = colour[0]*255
                green = colour[1]*255
                blue = colour[2]*255
                colourBytes = bytearray([int(red), int(green), int(blue), 0, 1, 0, 0, 0])
                await Device.sendLanternColour(colourBytes)
            except:
                if(color == "rainbow"):
                    colourBytes = bytearray([255, 255, 0, 1, 1, 0, 0, 0])
                    await Device.sendLanternColour(colourBytes)
                else:
                    return "The colour " + color + " was not found", 400
            return "Lantern colour was set to " + color, 200
    elif(mode == "party"):
        if(status == "on"):
            colour = bytearray([255,255,0,1,1,0,0,0])
            await Device.sendLanternStatus(1)
            await Device.sendLanternColour(colour)
            return "Party mode was turned on for {}".format(await Device.getName())
        elif(status == "off"):
            colour = bytearray([255,0,0,0,1,0,0,0])
            await Device.sendLanternStatus(0)
            await Device.sendLanternColour(colour)
            return "Party mode was turned off for {}".format(await Device.getName())
    elif(mode == "stealth"):
        if(status == "on"):
            await Device.sendStealthStatus(1)
            return "Stealth was turned on for {}".format(await Device.getName())
        elif(status == "off"):
            await Device.sendStealthStatus(0)
            return "Stealth was turned off for {}".format(await Device.getName())
    elif(mode == "ready"):
        if(status == "on"):
            Ready.readyMode = True
            _thread = threading.Thread(target=Ready.runLoop, args=(Device,))
            _thread.start()
            return f"Ready mode was turned on for {await Device.getName()}", 200
        elif(status == "off"):
            Ready.readyMode = False
            return f"Ready mode was turned off for {await Device.getName()}", 200
        return "Something went wrong with ready mode.", 400
    if(not modeInList):
        return "The Mode " + mode + " was not found.", 400
    if(not statusInList):
        return "The status " + status + " was not found.", 400

@app.route('/cmd', methods=['GET'])
async def handle_cmd():
    command = request.args.get('command','')
    profile = request.args.get('profile','')
    if(command == "preheat"):
        if(profile != ""):
            if(profile == "?"):
                return "The profile wasn't specified", 400
            profile = int(profile) - 1
            await Device.changeProfile(profile, True)
            preheatBytes = bytearray([0, 0, 224, 64])
            await Device.sendCommand(preheatBytes)
            return "Starting preheat for profile {}. Heating to {} celsius for {} seconds".format(await Device.getProfileName(), await Device.getProfileTemp(), await Device.getProfileTime()), 200
        await Device.changeProfile(await Device.getProfile())
        preheatBytes = bytearray([0, 0, 224, 64])
        await Device.sendCommand(preheatBytes)
        return "Starting preheat for profile {}. Heating to {} celsius for {} seconds".format(await Device.getProfileName(), await Device.getProfileTemp(), await Device.getProfileTime()), 200
    elif(command== "boost"):
        state = await Device.getState()
        if(state == 8):
            stopCycle = bytearray([0, 0, 16, 65])
            await Device.sendCommand(stopCycle)
            return f"Boosted puffco {await Device.getBoostTemp()} degrees and {await Device.getBoostTime()} seconds", 200
        else:
            return "Your puffco hasn't finished preheating", 400
    elif(command== "stop"):
        state = await Device.getState()
        if(state == 7 or state == 8):
            stopCycle = bytearray([0, 0, 0, 65])
            await Device.sendCommand(stopCycle)
            return "Stopped preheat cycle", 200
        else:
            return "You are not in a preheat cycle", 400
    return "Command not found", 200

@app.route('/info', methods=['GET'])
async def handle_info():
    length = request.args.get('length','')
    infoType = request.args.get('type','')
    if(infoType == "dabs" or infoType == "dogs"):
        if(length == "total"):
            return f"Your total amount of dabs taken since {await Device.getBirthday()} is {await Device.getTotalDabsTaken()}", 200
        elif(length == "daily" or length == "day"):
            return f"Your daily dab amount is {await Device.getDailyDabsTaken()}", 200
        elif(length == "left" or length == "remaining"):
            return f"The approximate amount of dabs left before the battery dies is {await Device.getDabsLeft()}", 200
        else:
            return f"The length {length} was not found.", 400
    elif(infoType == "battery"):
        preheatBytes = bytearray([0, 0, 160, 64])
        await Device.sendCommand(preheatBytes)
        return f"Your puffco is at {await Device.getBatteryLevel()} percent", 200
    else:
        return f"The type {infoType} was not found.", 400

@app.route('/preheat', methods=['GET'])
async def handle_preheat():
    temp = request.args.get('temperature','')
    secs = request.args.get('seconds','')
    if(temp):
        await Device.changeProfile(await Device.getProfile())
        await Device.setProfileTemp(temp)
        await Device.setProfileTime(secs)
        preheatBytes = bytearray([0, 0, 224, 64])
        await Device.sendCommand(preheatBytes)
        return "Preheating puffco to " + temp + "celcius for " + secs + " seconds", 200
    else:
        return "Error while preheating", 400

@app.route('/')
async def index():
    try:
        await asyncio.wait_for(Device.connect(), timeout=7.5)
        clickButton = bytearray([0, 0, 64, 64])
        await Device.sendCommand(clickButton)
        return f"Connected to {await Device.getName()}", 200
    except asyncio.TimeoutError:
        return f"Failed to connect to puffco", 400

app.run(address="127.0.0.1", port="8080")
