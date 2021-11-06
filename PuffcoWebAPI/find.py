import asyncio
from bleak import BleakScanner

SERVICE_UUID = "06caf9c0-74d3-454f-9be9-e30cd999c17a"
attempted_devices = list()

async def main():
    scanning = True
    while scanning:
        print("Scanning")
        devices = await BleakScanner.discover()
        for d in devices:
            service_uuids = d.metadata.get('uuids')
        
            if SERVICE_UUID in service_uuids:
                print(f'Found Peak Pro "{d.name}" ({d.address})')
                scanning = False
asyncio.run(main())