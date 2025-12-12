# -*- coding: utf-8 -*-
"""
TinyTuya - Asynchronous Example

This demonstrates how to use the `tinytuya_async.DeviceAsync` class to control and
monitor a Tuya device asynchronously. The example shows how to run
concurrent tasks for a device's routine and main control flow, ensuring
non-blocking I/O operations.

Setup:
    Replace 'DEVICEID', 'DEVICEADDRESS', 'DEVICEKEY', and 'DEVICEVERSION'
    with your specific device details. The script will create a background
    task to listen for device status updates and a main task to send
    commands to the device.

Author: 3735943886
"""
import asyncio
import tinytuya
import tinytuya_async

#tinytuya.set_debug(True)
device = None

async def device_routine(id, ip, key, ver):
    global device
    # The device object can also be created without async with.
    # device = tinytuya_async.DeviceAsync(id, ip, key, version=ver, persist=True)
    async with tinytuya_async.DeviceAsync(id, ip, key, version=ver, persist=True) as device:
        # Asynchronous methods such as 'status', 'receive', and 'heartbeat' must all be called with 'await' to function correctly.
        await device.status()
        while(True):
            data = await device.receive()
            print('Received Payload: %r' % data)
            await device.heartbeat()

async def main():
    # Example creating an asynchronous task to run the device_routine concurrently.
    # The device_routine will run in the background while the main() function executes its sleep and control commands.
    task = asyncio.create_task(device_routine('DEVICEID', 'DEVICEADDRESS', 'DEVICEKEY', 'DEVICEVERSION'))

    # Sending a control command (payload) while another task (device_routine) is waiting for a packet via 'receive()'.
    await asyncio.sleep(5)
    await device.turn_off(1)
    await asyncio.sleep(5)
    await device.turn_on(1)
    await asyncio.sleep(5)

    # If the 'async with' statement was not used, 'device.close()' would need to be called explicitly to properly close the connection.
    # await device.close()

if __name__ == "__main__":
    asyncio.run(main())
