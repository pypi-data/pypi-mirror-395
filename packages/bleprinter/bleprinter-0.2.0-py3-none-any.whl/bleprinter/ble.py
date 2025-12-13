import asyncio

from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

# For some reason, bleak reports the 0xaf30 service on my macOS, while it reports
# 0xae30 (which I believe is correct) on my Raspberry Pi. This hacky workaround
# should cover both cases.
POSSIBLE_SERVICE_UUIDS = [
    "0000ae30-0000-1000-8000-00805f9b34fb",
    "0000af30-0000-1000-8000-00805f9b34fb",
]

TX_CHARACTERISTIC_UUID = "0000ae01-0000-1000-8000-00805f9b34fb"
RX_CHARACTERISTIC_UUID = "0000ae02-0000-1000-8000-00805f9b34fb"
PRINTER_READY_NOTIFICATION = bytearray(b"\x51\x78\xae\x01\x01\x00\x00\x00\xff")

SCAN_TIMEOUT_S = 10
WAIT_AFTER_EACH_CHUNK_S = 0.02
WAIT_FOR_PRINTER_DONE_TIMEOUT = 30


async def scan(timeout: int):
    def filter_fn(_: BLEDevice, adv_data: AdvertisementData):
        return any(uuid in adv_data.service_uuids for uuid in POSSIBLE_SERVICE_UUIDS)

    device = await BleakScanner.find_device_by_filter(filter_fn, timeout=timeout)
    if device is None:
        raise RuntimeError(
            "Unable to find printer, make sure it is turned on and in range"
        )

    return device


def chunkify(data: bytearray, chunk_size: int):
    return (data[i : i + chunk_size] for i in range(0, len(data), chunk_size))


def notification_receiver_factory(event: asyncio.Event):
    def notification_receiver(_: BleakGATTCharacteristic, data: bytearray):
        if data == PRINTER_READY_NOTIFICATION:
            event.set()

    return notification_receiver


# Finished printing, waiting for printer to confirm before disconnecting.
async def wait_for_printer_ready(event: asyncio.Event):
    _ = await event.wait()


async def run_ble(data: bytearray):
    address = await scan(SCAN_TIMEOUT_S)
    async with BleakClient(address) as client:
        chunk_size = client.mtu_size - 3
        event = asyncio.Event()

        receive_notification = notification_receiver_factory(event)

        await client.start_notify(RX_CHARACTERISTIC_UUID, receive_notification)

        for chunk in chunkify(data, chunk_size):
            await client.write_gatt_char(TX_CHARACTERISTIC_UUID, chunk)
            await asyncio.sleep(WAIT_AFTER_EACH_CHUNK_S)

        await asyncio.wait_for(
            wait_for_printer_ready(event), timeout=WAIT_FOR_PRINTER_DONE_TIMEOUT
        )
