from enum import Enum
from bleak import BleakClient
from Utils import Utils
import datetime

class Puffco():
    DEVICE_NAME = "F9A98C15-C651-4F34-B656-D100BF58004D"
    COMMAND = "F9A98C15-C651-4F34-B656-D100BF580040"

    DEVICE_NAME = "F9A98C15-C651-4F34-B656-D100BF58004D"
    DEVICE_CHARGE_STATE = "F9A98C15-C651-4F34-B656-D100BF580031"
    DEVICE_STATE = "F9A98C15-C651-4F34-B656-D100BF580022"
    DEVICE_BIRTHDAY = "F9A98C15-C651-4F34-B656-D100BF58004E"
    DEVICE_BATTERY_CURRENT = "F9A98C15-C651-4F34-B656-D100BF580020"

    LANTERN_STATUS = "F9A98C15-C651-4F34-B656-D100BF58004A"
    LANTERN_COLOUR = "F9A98C15-C651-4F34-B656-D100BF580048"

    STEALTH_STATUS = "F9A98C15-C651-4F34-B656-D100BF580042"

    BOOST_TEMP = "F9A98C15-C651-4F34-B656-D100BF580067"
    BOOST_TIME = "F9A98C15-C651-4F34-B656-D100BF580068"

    TOTAL_DABS = "F9A98C15-C651-4F34-B656-D100BF58002F"
    DAILY_DABS = "F9A98C15-C651-4F34-B656-D100BF58003B"
    DABS_LEFT = "F9A98C15-C651-4F34-B656-D100BF58003A"

    PROFILE_CURRENT = "F9A98C15-C651-4F34-B656-D100BF580041"
    PROFILE = "F9A98C15-C651-4F34-B656-D100BF580061"
    PROFILE_NAME = "F9A98C15-C651-4F34-B656-D100BF580062"
    PROFILE_PREHEAT_TEMP = "F9A98C15-C651-4F34-B656-D100BF580063"
    PROFILE_PREHEAT_TIME = "F9A98C15-C651-4F34-B656-D100BF580064"

    def __init__(self, mac : str):
        self.mac = mac
        self.client = BleakClient(mac)

    async def connect(self):
        await self.client.connect()
        if(self.client.is_connected):
            return True
        else:
            return False

    async def readString(self, UUID):
        return await self.client.read_gatt_char(UUID)

    async def isConnected(self):
        return self.client.is_connected

    async def getName(self):
        deviceName = await self.readString(self.DEVICE_NAME)
        return deviceName.decode()

    async def getProfile(self):
        currentProfile = await self.client.read_gatt_char(self.PROFILE_CURRENT)
        data = Utils.parseFloat(currentProfile)
        return int(round(data, 1))

    async def changeProfile(self, prof, realProfileBytes = False):
        if(prof == 0):
            profile = bytearray([0, 0, 0, 0])
        elif(prof == 1):
            profile = bytearray([1, 0, 0, 0])
        elif(prof == 2):
            profile = bytearray([2, 0, 0, 0])
        elif(prof == 3):
            profile = bytearray([3, 0, 0, 0])
        await self.client.write_gatt_char(self.PROFILE, profile, response=True)
        if(realProfileBytes):
            if(prof == 0):
                profile = bytearray([0, 0, 0, 0])
            elif(prof == 1):
                profile = bytearray([0, 0, 128, 63])
            elif(prof == 2):
                profile = bytearray([0, 0, 0, 64])
            elif(prof == 3):
                profile = bytearray([0, 0, 64, 64])
            await self.client.write_gatt_char(self.PROFILE_CURRENT, profile, response=True)

    async def setProfileTime(self, seconds):
        time = Utils.packFloat(int(seconds))
        print(time)
        await self.client.write_gatt_char(self.PROFILE_PREHEAT_TIME, time, response=True)

    async def setProfileTemp(self, temp):
        temperature = Utils.packFloat(int(temp))
        print(temperature)
        await self.client.write_gatt_char(self.PROFILE_PREHEAT_TEMP, temperature, response=True)

    async def sendCommand(self, commandArray):
        await self.client.write_gatt_char(self.COMMAND, commandArray, response=True)

    async def getBirthday(self):
        birthday = await self.client.read_gatt_char(self.DEVICE_BIRTHDAY)
        datetime_time = datetime.datetime.fromtimestamp(int(Utils.parseInt(birthday)))
        datetime_time = str(datetime_time).split(" ")[0]
        return datetime_time

    async def sendStealthStatus(self, status):
        if(status == 0):
            commandArray = bytearray([0, 0, 0, 0])
        elif(status == 1):
            commandArray = bytearray([1, 0, 0, 0])
        await self.client.write_gatt_char(self.STEALTH_STATUS, commandArray, response=True)

    async def getTotalDabsTaken(self):
        totalDabs = await self.client.read_gatt_char(self.TOTAL_DABS)
        return int(Utils.parseFloat(totalDabs))

    async def getDabsLeft(self):
        dabsLeft = await self.client.read_gatt_char(self.DABS_LEFT)
        return int(Utils.parseFloat(dabsLeft))

    async def getDailyDabsTaken(self):
        dailyDabs = await self.client.read_gatt_char(self.DAILY_DABS)
        return round(Utils.parseFloat(dailyDabs), 1)

    async def getProfileName(self):
        profileName = await self.client.read_gatt_char(self.PROFILE_NAME)
        return profileName.decode()

    async def getProfileTemp(self):
        test = await self.client.read_gatt_char(self.PROFILE_PREHEAT_TEMP)
        data = Utils.parseFloat(test)
        return int(round(data, 1))

    async def getProfileTime(self):
        test = await self.client.read_gatt_char(self.PROFILE_PREHEAT_TIME)
        data = Utils.parseFloat(test)
        return int(round(data, 1))

    async def sendLanternStatus(self, status):
        if(status == 0):
            commandArray = bytearray([0, 0, 0, 0])
        elif(status == 1):
            commandArray = bytearray([1, 0, 0, 0])
        await self.client.write_gatt_char(self.LANTERN_STATUS, commandArray, response=True)

    async def sendLanternColour(self, colour):
        await self.client.write_gatt_char(self.LANTERN_COLOUR, colour, response=True)

    async def getBatteryLevel(self):
        battery = await self.client.read_gatt_char(self.DEVICE_BATTERY_CURRENT)
        data = Utils.parseFloat(battery)
        return str(round(data, 1))

    async def getBoostTemp(self):
        temp = await self.client.read_gatt_char(self.BOOST_TEMP)
        data = Utils.parseFloat(temp)
        return int(data)

    async def getBoostTime(self):
        time = await self.client.read_gatt_char(self.BOOST_TIME)
        data = Utils.parseFloat(time)
        return int(data)

    async def getState(self):
        time = await self.client.read_gatt_char(self.DEVICE_STATE)
        data = Utils.parseFloat(time)
        return int(data)

    async def getChargeState(self):
        time = await self.client.read_gatt_char(self.DEVICE_CHARGE_STATE)
        data = Utils.parseFloat(time)
        return int(data)